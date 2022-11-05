"""_lazy_table.py"""

from typing import Generator, List, Optional, Sequence, TypeVar

from tabulate import tabulate

from .artists import Artist, Console

T = TypeVar("T")


def stream(
    table: Generator[Sequence[T], None, None],
    artist: Artist = None,
    n_rows: Optional[int] = None,
    **kwargs,
):
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
    table
        A generator which yields rows of the table.
    artist
        A callable which determines how to render a table. If unspecified, ``lazy_table.artists.Console()`` is used.
    n_rows
        Number of rows in table.
    """
    if artist is None:
        artist = Console()
    rows: List[Sequence[T]] = []
    result = tabulate(rows, **kwargs)
    artist.init(n_rows)
    artist.render(result)
    for row in table:
        rows.append(row)
        result = tabulate(rows, **kwargs)
        artist.render(result)
