"""
IPython Tcl magics.
"""

import ast
import os
import sys
import tkinter

from contextlib import contextmanager

from IPython.core import display
from IPython.core.magic import (Magics, magics_class, line_cell_magic, UsageError)


@contextmanager
def capture_fd(fd, captured):
    """Capture a file descriptor fd and write to the file object captured."""
    fdin, fdout = os.pipe()
    saved = os.dup(fd)
    os.dup2(fdout, fd)
    try:
        yield
    finally:
        os.dup2(saved, fd)
        os.close(fdout)
        with os.fdopen(fdin, 'r') as f:
            captured.write(f.read())


@magics_class  # pylint: disable=too-few-public-methods
class TclMagics(Magics):
    """Magic class that creates the Tcl magics."""

    def __init__(self, shell):
        super(TclMagics, self).__init__(shell)
        self._tcl = tkinter.Tcl()
        self._add_tcl_syntax()

    @line_cell_magic
    def tcl(self, line, cell=None):
        """The custom magics %tcl and %%tcl."""
        result = None
        if cell is None:  # line magic
            line, cell = self._load(line)
        if cell is not None:
            self._tcl.setvar("argc", len(line.split()))
            self._tcl.setvar("argv", line)
            try:
                # we can not use sys.stdout.fileno() in a Jupyter notebook
                with capture_fd(1, sys.stdout), capture_fd(2, sys.stderr):
                    result = self._tcl.eval(cell)
            except tkinter.TclError as e:
                sys.stderr.write("TclError: " + str(e))
        try:
            result = ast.literal_eval(result)
        except (SyntaxError, ValueError):
            pass
        return result if result else None

    @staticmethod
    def _add_tcl_syntax():
        """Add Tcl syntax highlightning."""
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
        display.display_javascript(data, raw=True)

    @staticmethod
    def _load(line):
        """Load an external Tcl script."""
        cell = None
        argv = line.split(None, 1)
        if not argv:
            raise UsageError('%tcl FILENAME [ARGS...]')
        else:
            name = argv[0]
            line = argv[1] if len(argv) == 2 else ""
            try:
                with open(name, "r") as file:
                    cell = file.read()
            except FileNotFoundError as e:
                sys.stderr.write(str(e))
        return line, cell


def load_ipython_extension(ipython):
    """Callback function called when loading the extension."""
    ipython.register_magics(TclMagics)


def unload_ipython_extension(ipython):
    """Callback function called when unloading the extension."""
    del ipython.magics_manager.magics['line']['tcl']
    del ipython.magics_manager.magics['cell']['tcl']
