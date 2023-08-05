"""Terminal management for exposing terminals to a web interface using Tornado.
"""
# Copyright (c) Jupyter Development Team
# Copyright (c) 2014, Ramalingam Saravanan <sarava@sarava.net>
# Distributed under the terms of the Simplified BSD License.


import asyncio
import codecs
import itertools
import logging
import os
import select
import signal
import warnings
from collections import deque

try:
    from ptyprocess import PtyProcessUnicode

    def preexec_fn():
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

except ImportError:
    try:
        from winpty import PtyProcess as PtyProcessUnicode
    except ImportError:
        PtyProcessUnicode = object
    preexec_fn = None  # type:ignore[assignment]

from tornado.ioloop import IOLoop

ENV_PREFIX = "PYXTERM_"  # Environment variable prefix

# TERM is set according to xterm.js capabilities
DEFAULT_TERM_TYPE = "xterm-256color"


class PtyWithClients:
    def __init__(self, argv, env=None, cwd=None):
        self.clients = []
        # Use read_buffer to store historical messages for reconnection
        self.read_buffer: deque[list] = deque([], maxlen=1000)
        kwargs = dict(argv=argv, env=env or [], cwd=cwd)
        if preexec_fn is not None:
            kwargs["preexec_fn"] = preexec_fn
        self.ptyproc = PtyProcessUnicode.spawn(**kwargs)
        # The output might not be strictly UTF-8 encoded, so
        # we replace the inner decoder of PtyProcessUnicode
        # to allow non-strict decode.
        self.ptyproc.decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")

    def resize_to_smallest(self):
        """Set the terminal size to that of the smallest client dimensions.

        A terminal not using the full space available is much nicer than a
        terminal trying to use more than the available space, so we keep it
        sized to the smallest client.
        """
        minrows = mincols = 10001
        for client in self.clients:
            rows, cols = client.size
            if rows is not None and rows < minrows:
                minrows = rows
            if cols is not None and cols < mincols:
                mincols = cols

        if minrows == 10001 or mincols == 10001:
            return

        rows, cols = self.ptyproc.getwinsize()
        if (rows, cols) != (minrows, mincols):
            self.ptyproc.setwinsize(minrows, mincols)

    def kill(self, sig=signal.SIGTERM):
        """Send a signal to the process in the pty"""
        self.ptyproc.kill(sig)

    def killpg(self, sig=signal.SIGTERM):
        """Send a signal to the process group of the process in the pty"""
        if os.name == "nt":
            return self.ptyproc.kill(sig)
        pgid = os.getpgid(self.ptyproc.pid)
        os.killpg(pgid, sig)

    async def terminate(self, force=False):
        """This forces a child process to terminate. It starts nicely with
        SIGHUP and SIGINT. If "force" is True then moves onto SIGKILL. This
        returns True if the child was terminated. This returns False if the
        child could not be terminated."""
        if os.name == "nt":
            signals = [signal.SIGINT, signal.SIGTERM]
        else:
            signals = [signal.SIGHUP, signal.SIGCONT, signal.SIGINT, signal.SIGTERM]

        _ = IOLoop.current()

        def sleep():
            return asyncio.sleep(self.ptyproc.delayafterterminate)

        if not self.ptyproc.isalive():
            return True
        try:
            for sig in signals:
                self.kill(sig)
                await sleep()
                if not self.ptyproc.isalive():
                    return True
            if force:
                self.kill(signal.SIGKILL)
                await sleep()
                if not self.ptyproc.isalive():
                    return True
                else:
                    return False
            return False
        except OSError:
            # I think there are kernel timing issues that sometimes cause
            # this to happen. I think isalive() reports True, but the
            # process is dead to the kernel.
            # Make one last attempt to see if the kernel is up to date.
            await sleep()
            if not self.ptyproc.isalive():
                return True
            else:
                return False


def _update_removing(target, changes):
    """Like dict.update(), but remove keys where the value is None."""
    for k, v in changes.items():
        if v is None:
            target.pop(k, None)
        else:
            target[k] = v


def _poll(fd: int, timeout: float = 0.1) -> list:
    """Poll using poll() on posix systems and select() elsewhere (e.g., Windows)"""
    if os.name == "posix":
        poller = select.poll()  # noqa: ignore missing method on Windows
        poller.register(
            fd, select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
        )  # read-only
        return poller.poll(timeout * 1000)  # milliseconds
    else:
        # poll() not supported on Windows
        r, _, _ = select.select([fd], [], [], timeout)
        return r


class TermManagerBase:
    """Base class for a terminal manager."""

    def __init__(
        self, shell_command, server_url="", term_settings=None, extra_env=None, ioloop=None
    ):
        self.shell_command = shell_command
        self.server_url = server_url
        self.term_settings = term_settings or {}
        self.extra_env = extra_env
        self.log = logging.getLogger(__name__)

        self.ptys_by_fd = {}

        if ioloop is not None:
            warnings.warn(
                f"Setting {self.__class__.__name__}.ioloop is deprecated and ignored",
                DeprecationWarning,
                stacklevel=2,
            )

    def make_term_env(self, height=25, width=80, winheight=0, winwidth=0, **kwargs):
        """Build the environment variables for the process in the terminal."""
        env = os.environ.copy()
        # ignore any previously set TERM
        # TERM is set according to xterm.js capabilities
        env["TERM"] = self.term_settings.get("type", DEFAULT_TERM_TYPE)
        dimensions = "%dx%d" % (width, height)
        if winwidth and winheight:
            dimensions += ";%dx%d" % (winwidth, winheight)
        env[ENV_PREFIX + "DIMENSIONS"] = dimensions
        env["COLUMNS"] = str(width)
        env["LINES"] = str(height)

        if self.server_url:
            env[ENV_PREFIX + "URL"] = self.server_url

        if self.extra_env:
            _update_removing(env, self.extra_env)

        term_env = kwargs.get("extra_env", {})
        if term_env and isinstance(term_env, dict):
            _update_removing(env, term_env)

        return env

    def new_terminal(self, **kwargs):
        """Make a new terminal, return a :class:`PtyWithClients` instance."""
        options = self.term_settings.copy()
        options["shell_command"] = self.shell_command
        options.update(kwargs)
        argv = options["shell_command"]
        env = self.make_term_env(**options)
        cwd = options.get("cwd", None)
        return PtyWithClients(argv, env, cwd)

    def start_reading(self, ptywclients):
        """Connect a terminal to the tornado event loop to read data from it."""
        fd = ptywclients.ptyproc.fd
        self.ptys_by_fd[fd] = ptywclients
        loop = IOLoop.current()
        loop.add_handler(fd, self.pty_read, loop.READ)

    def on_eof(self, ptywclients):
        """Called when the pty has closed."""
        # Stop trying to read from that terminal
        fd = ptywclients.ptyproc.fd
        self.log.info("EOF on FD %d; stopping reading", fd)
        del self.ptys_by_fd[fd]
        IOLoop.current().remove_handler(fd)

        # This closes the fd, and should result in the process being reaped.
        ptywclients.ptyproc.close()

    def pty_read(self, fd, events=None):
        """Called by the event loop when there is pty data ready to read."""
        # prevent blocking on fd
        if not _poll(fd, timeout=0.1):  # 100ms
            self.log.debug(f"Spurious pty_read() on fd {fd}")
            return
        ptywclients = self.ptys_by_fd[fd]
        try:
            self.pre_pty_read_hook(ptywclients)
            s = ptywclients.ptyproc.read(65536)
            ptywclients.read_buffer.append(s)
            for client in ptywclients.clients:
                client.on_pty_read(s)
        except EOFError:
            self.on_eof(ptywclients)
            for client in ptywclients.clients:
                client.on_pty_died()

    def pre_pty_read_hook(self, ptywclients):
        """Hook before pty read, subclass can patch something into ptywclients when pty_read"""

    def get_terminal(self, url_component=None):
        """Override in a subclass to give a terminal to a new websocket connection

        The :class:`TermSocket` handler works with zero or one URL components
        (capturing groups in the URL spec regex). If it receives one, it is
        passed as the ``url_component`` parameter; otherwise, this is None.
        """
        raise NotImplementedError

    def client_disconnected(self, websocket):
        """Override this to e.g. kill terminals on client disconnection."""
        pass

    async def shutdown(self):
        await self.kill_all()

    async def kill_all(self):
        futures = []
        for term in self.ptys_by_fd.values():
            futures.append(term.terminate(force=True))
        # wait for futures to finish
        if futures:
            await asyncio.gather(*futures)


class SingleTermManager(TermManagerBase):
    """All connections to the websocket share a common terminal."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.terminal = None

    def get_terminal(self, url_component=None):
        if self.terminal is None:
            self.terminal = self.new_terminal()
            self.start_reading(self.terminal)
        return self.terminal

    async def kill_all(self):
        await super().kill_all()
        self.terminal = None


class MaxTerminalsReached(Exception):
    def __init__(self, max_terminals):
        self.max_terminals = max_terminals

    def __str__(self):
        return "Cannot create more than %d terminals" % self.max_terminals


class UniqueTermManager(TermManagerBase):
    """Give each websocket a unique terminal to use."""

    def __init__(self, max_terminals=None, **kwargs):
        super().__init__(**kwargs)
        self.max_terminals = max_terminals

    def get_terminal(self, url_component=None):
        if self.max_terminals and len(self.ptys_by_fd) >= self.max_terminals:
            raise MaxTerminalsReached(self.max_terminals)

        term = self.new_terminal()
        self.start_reading(term)
        return term

    def client_disconnected(self, websocket):
        """Send terminal SIGHUP when client disconnects."""
        self.log.info("Websocket closed, sending SIGHUP to terminal.")
        if websocket.terminal:
            if os.name == "nt":
                websocket.terminal.kill()
                # Immediately call the pty reader to process
                # the eof and free up space
                self.pty_read(websocket.terminal.ptyproc.fd)
                return
            websocket.terminal.killpg(signal.SIGHUP)


class NamedTermManager(TermManagerBase):
    """Share terminals between websockets connected to the same endpoint."""

    def __init__(self, max_terminals=None, **kwargs):
        super().__init__(**kwargs)
        self.max_terminals = max_terminals
        self.terminals = {}

    def get_terminal(self, term_name):
        assert term_name is not None

        if term_name in self.terminals:
            return self.terminals[term_name]

        if self.max_terminals and len(self.terminals) >= self.max_terminals:
            raise MaxTerminalsReached(self.max_terminals)

        # Create new terminal
        self.log.info("New terminal with specified name: %s", term_name)
        term = self.new_terminal()
        term.term_name = term_name
        self.terminals[term_name] = term
        self.start_reading(term)
        return term

    name_template = "%d"

    def _next_available_name(self):
        for n in itertools.count(start=1):
            name = self.name_template % n
            if name not in self.terminals:
                return name

    def new_named_terminal(self, **kwargs):
        if "name" in kwargs:
            name = kwargs["name"]
        else:
            name = self._next_available_name()
        term = self.new_terminal(**kwargs)
        self.log.info("New terminal with automatic name: %s", name)
        term.term_name = name
        self.terminals[name] = term
        self.start_reading(term)
        return name, term

    def kill(self, name, sig=signal.SIGTERM):
        term = self.terminals[name]
        term.kill(sig)  # This should lead to an EOF

    async def terminate(self, name, force=False):
        term = self.terminals[name]
        await term.terminate(force=force)

    def on_eof(self, ptywclients):
        super().on_eof(ptywclients)
        name = ptywclients.term_name
        self.log.info("Terminal %s closed", name)
        self.terminals.pop(name, None)

    async def kill_all(self):
        await super().kill_all()
        self.terminals = {}
