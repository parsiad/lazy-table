[![](https://static.pepy.tech/personalized-badge/lazy-table?period=total&units=international_system&left_color=grey&right_color=blue&left_text=pypi%20downloads)](https://pepy.tech/project/lazy-table)
[![](https://badge.fury.io/py/lazy-table.svg)](https://badge.fury.io/py/lazy-table)
![](https://img.shields.io/pypi/pyversions/lazy-table.svg)

<p align="center">
  <img alt="lazy_table" src="https://raw.githubusercontent.com/parsiad/lazy-table/master/logo.png">
</p>

A [python-tabulate](https://github.com/astanin/python-tabulate) wrapper for producing tables from generators.

## Motivation

lazy_table is useful when (*i*) each row of your table is generated by a possibly expensive computation and (*ii*) you want to print rows to the screen as soon as they are available.

For example, the rows in the table below correspond to [numerically solving an ordinary differential equation](https://en.wikipedia.org/wiki/Numerical_methods_for_ordinary_differential_equations) with progressively more steps. See [examples/euler_vdp.py](https://raw.githubusercontent.com/parsiad/lazy-table/master/examples/euler_vdp.py) for the code to generate this table.

![](https://github.com/parsiad/lazy-table/blob/main/examples/euler_vdp.gif?raw=true)

Here is the same example with a progress bar.

![](https://github.com/parsiad/lazy-table/blob/main/examples/euler_vdp_with_progress.gif?raw=true)

## Installation and usage

Install lazy_table via pip:

```console
$ pip install lazy_table
```

In your Python code, add

```python
import lazy_table as lt
```

Now, generating your own lazy table is as simple as calling `lt.stream` on a generator that yields one or more lists, where each list is a row of your table (see the example below).

## Example

As a toy example, consider printing the first 10 [Fibonacci numbers](https://en.wikipedia.org/wiki/Fibonacci_number) in a table.
Since this is a relatively cheap operation, we will pretend it is expensive by adding an artificial `sleep(1)` call beteween Fibonacci numbers.

```python
import time
import lazy_table as lt

def fib_table(n):
     x0, x1 = 0, 1
     yield [0, x0]
     yield [1, x1]
     for i in range(2, n + 1):
         time.sleep(1)  # Simulate work
         x0, x1 = x1, x0 + x1
         yield [i, x1]

lt.stream(fib_table(10), headers=['N', 'F_N'])
```

Your final table should look like this:

```
  N    F_N
---  -----
  0      0
  1      1
  2      1
  3      2
  4      3
  5      5
  6      8
  7     13
  8     21
  9     34
 10     55
```

You can also specify an "artist" that determines how the table is rendered.
For example, the `ConsoleWithProgress` artist displays a progress bar alongside the table indicating the percentage of rows completed:

```python
n_rows = 10
artist = lt.artists.ConsoleWithProgress()
lt.stream(fib_table(n_rows), headers=['N', 'F_N'], n_rows=n_rows, artist=artist)
```
