#!/usr/bin/env python

import lazy_table as lt
import numpy as np


def f(y):
    return np.array([y[1], (1. - y[0]**2) * y[1] - y[0]])


def solve(n_steps, t1=16., y0=(2., 0.)):
    h = t1 / n_steps
    y = np.array(y0)
    for _ in range(n_steps):
        y = y + h * f(y)
    return y


def convergence_table(init_n_steps=200):
    prev_value = np.nan
    prev_delta = np.nan
    for n_steps in init_n_steps * 2**np.arange(0, 12):
        y = solve(n_steps)
        value = y[0]
        delta = value - prev_value
        ratio = prev_delta / delta
        order = np.log2(ratio)
        prev_value = value
        prev_delta = delta
        yield [n_steps, value, delta, order]


lt.stream(
    convergence_table(),
    tablefmt='simple',
    headers=['Steps', 'Value', 'Delta', 'Order'],
)
