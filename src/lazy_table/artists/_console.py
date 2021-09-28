import sys

from tqdm import tqdm


def _clear(clear, n_lines, out):
    if clear:
        out.write('\x1b[2J')
    else:
        out.write('\033[F\033[K' * n_lines)


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
        self._n_lines = 0
        self._out = out

    def __call__(self, result, _):
        _clear(self._clear, self._n_lines, self._out)
        self._n_lines = result.count('\n') + 1
        self._out.write(result)
        self._out.write('\n')
        self._out.flush()


class ConsoleWithProgress:
    """Renders a table to the console along with a progress bar.

    See docstring of ``Console`` for a list of parameters.
    """
    def __init__(self, clear=False, out=sys.stdout):
        self._clear = clear
        self._n_lines = 0
        self._n_calls = -1
        self._out = out

    def __call__(self, result, n_rows):
        _clear(self._clear, self._n_lines, self._out)
        self._n_calls += 1
        self._n_lines = result.count('\n') + 4
        with tqdm(file=self._out, total=n_rows) as progress_bar:
            progress_bar.update(self._n_calls)
            progress_bar.write(result)
            progress_bar.write('\n')
