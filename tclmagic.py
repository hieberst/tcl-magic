"""
IPython Tcl magics.
"""

import ast
import os
import sys
import tkinter

from contextlib import contextmanager

from IPython.core import display
from IPython.core.error import UsageError
from IPython.core.magic import (Magics, magics_class, line_cell_magic)
from IPython.core.magic_arguments import (argument, magic_arguments, parse_argstring)


@contextmanager
def capture_fd(fd, captured):
    """Capture a file descriptor fd and write to the file object captured."""
    fd_in, fd_out = os.pipe()
    saved = os.dup(fd)
    os.dup2(fd_out, fd)
    try:
        yield
    finally:
        os.dup2(saved, fd)
        os.close(fd_out)
        with os.fdopen(fd_in, 'r') as f:
            captured.write(f.read())


@magics_class  # pylint: disable=too-few-public-methods
class TclMagics(Magics):
    """Magic class that creates the Tcl magics."""

    def __init__(self, shell):
        super(TclMagics, self).__init__(shell)
        self._tcl = tkinter.Tcl()
        self._add_tcl_syntax()

    @magic_arguments()
    @argument('--out', type=str, help='The variable in which to store the result.')
    @argument('--err', type=str, help='The variable in which to store the Tcl error.')
    @argument('argv', nargs='*', metavar='ARG')
    @line_cell_magic
    def tcl(self, line, cell=None):
        """The custom magics %tcl and %%tcl."""
        args = parse_argstring(self.tcl, line)
        result = None
        tclerr = None
        if cell is None:  # line magic
            cell = self._load(args.argv)
        if cell is not None:
            self._tcl.setvar("argc", len(args.argv))
            self._tcl.setvar("argv", ' '.join(args.argv))
            try:
                # we cannot use sys.stdout.fileno() in a Jupyter notebook
                with capture_fd(1, sys.stdout), capture_fd(2, sys.stderr):
                    result = self._tcl.eval(cell)
                try:
                    result = ast.literal_eval(result)
                except (SyntaxError, ValueError):
                    pass
            except tkinter.TclError as e:
                tclerr = str(e)
        result = result if result != "" else None
        if args.out:
            self.shell.user_ns[args.out] = result
            result = None
        if args.err:
            self.shell.user_ns[args.err] = tclerr
        elif tclerr:
            sys.stderr.write("TclError: " + tclerr)
        return result

    @staticmethod
    def _add_tcl_syntax():
        """Add Tcl syntax highlighting."""
        # we need to use cdn.rawgit.com instead of raw.github.com since
        # raw.github.com always returns text/plain for the content type
        # and that violates "X-Content-Type-Options: nosniff"
        data = """
            requirejs.config({
                paths: {
                    codemirror: "https://cdn.rawgit.com/marijnh/CodeMirror/master"
                }
            });
            requirejs(["codemirror/mode/tcl/tcl"], function(codemirror) {
                IPython.CodeCell.options_default.highlight_modes['magic_text/x-tcl'] = {'reg':[/^%%tcl/]};
                IPython.notebook.events.one('kernel_ready.Kernel', function() {
                    IPython.notebook.get_cells().map(function(cell) {
                        if (cell.cell_type == 'code') {
                            cell.auto_highlight();
                        }
                    });
                });
            });
        """
        # noinspection PyTypeChecker
        # due to https://github.com/ipython/ipython/issues/12182
        display.display_javascript(data, raw=True)

    @staticmethod
    def _load(argv):
        """Load an external Tcl script, modifies argv."""
        content = None
        if not argv:
            raise UsageError('%tcl FILENAME [ARGS...]')
        try:
            with open(argv[0], "r") as file:
                content = file.read()
        except EnvironmentError as e:
            sys.stderr.write(str(e))
        del argv[0]
        return content


def load_ipython_extension(ipython):
    """Callback function called when loading the extension."""
    ipython.register_magics(TclMagics)


def unload_ipython_extension(ipython):
    """Callback function called when unloading the extension."""
    del ipython.magics_manager.magics['line']['tcl']
    del ipython.magics_manager.magics['cell']['tcl']
