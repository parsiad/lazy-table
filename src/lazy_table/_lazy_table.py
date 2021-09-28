from tabulate import tabulate

from .artists import Console


def stream(table, artist=None, n_rows=None, **kwargs):
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
        A callable that takes as input a string table which determines how to render it. If unspecified,
        ``lazy_table.artists.Console`` is used.
    n_rows : int, optional
        Number of rows in table.
    """
    if artist is None:
        artist = Console()
    rows = []
    t = tabulate(rows, **kwargs)
    artist(t, n_rows)
    for row in table:
        rows.append(row)
        t = tabulate(rows, **kwargs)
        artist(t, n_rows)
