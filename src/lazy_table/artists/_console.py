"""_console.py"""

# pylint: disable=too-few-public-methods

from time import perf_counter
import sys


def _clear(clear, n_lines, out):
    if clear:
        out.write("\x1b[2J")
    else:
        out.write("\x1b[1K\033[F\033[K" * n_lines)


class Console:
    """Renders a table to the console.

    Parameters
    ----------
    clear : bool, optional
        Clears the screen every time the table is updated.
    out : TextIOBase, optional
        Text stream to write to. If unspecified, ``sys.stdout`` is used.
    """
    def __init__(self, clear=False, out=sys.stdout):
        self._clear = clear
        self._out = out

    def render(self, result):
        _clear(self._clear, self._n_lines, self._out)
        self._n_lines = result.count("\n") + 1
        self._out.write(result)
        self._out.write("\n")
        self._out.flush()

    def init(self, _):
        self._n_lines = 0


class ConsoleWithProgress:
    """Renders a table to the console along with a progress bar.

    See docstring of ``Console`` for a list of parameters.
    """
    def __init__(self, clear=False, out=sys.stdout, width=32):
        self._clear = clear
        self._out = out
        self._width = width

    def _progress(self):
        frac = self._n_calls / self._n_rows
        n_complete_symbols = int(self._width * frac)
        n_incomplete_symbols = self._width - n_complete_symbols
        complete_symbols = "█" * n_complete_symbols
        incomplete_symbols = " " * n_incomplete_symbols
        elapsed = perf_counter() - self._start
        n_iters_per_sec = self._n_calls / elapsed
        self._out.write(f"|{complete_symbols}{incomplete_symbols}| {self._n_calls}/{self._n_rows}")
        self._out.write(f" [{elapsed:.2f}s, {n_iters_per_sec:.2f}it/s]\n")

    def render(self, result):
        _clear(self._clear, self._n_lines, self._out)
        self._n_lines = result.count("\n") + 3
        self._out.write(result)
        self._out.write("\n")
        self._out.write("\n")
        self._progress()
        self._n_calls += 1

    def init(self, n_rows):
        self._n_calls = 0
        self._n_lines = 0
        self._n_rows = n_rows
        self._start = perf_counter()
