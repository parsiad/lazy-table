import sys


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

    def __call__(self, result):
        if self._clear:
            self._out.write('\x1b[2J')
        else:
            self._out.write('\033[F\033[K' * self._n_lines)
        self._n_lines = result.count('\n') + 1
        self._out.write(result)
        self._out.write('\n')
        self._out.flush()
