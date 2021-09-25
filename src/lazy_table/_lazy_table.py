import sys

from tabulate import tabulate


class ConsoleArtist:
    """Renders a table to the console.

    Parameters
    ----------
    clear : bool
        Clears the screen every time the table is updated.
    out : TextIOBase
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


def stream(table, artist=None, **kwargs):
    """Streams a table.

    kwargs are forwarded to tabulate.

    Examples
    --------
    >>> import time
    >>> import lazy_table as lt
    >>>
    >>> def fib_table(n):
    ...     x0, x1 = 0, 1
    ...     yield [0, x0]
    ...     yield [1, x1]
    ...     for i in range(2, n + 1):
    ...         x0, x1 = x1, x0 + x1
    ...         yield [i, x1]
    ...         time.sleep(1)  # Simulate work
    >>>
    >>> lt.stream(fib_table(10), headers=['N', 'F_N'])

    Parameters
    ----------
    table : Generator[List[T], None, None]
        A generator which yields rows of the table.
    artist : callable, optional
        A callable of the form ``draw(string)`` which determines how to render the table. If unspecified,
        ``lazy_table.Console`` is used.
    """
    if artist is None:
        artist = ConsoleArtist()
    rows = []
    for row in table:
        rows.append(row)
        t = tabulate(rows, **kwargs)
        artist(t)
