#!/usr/bin/env python
"""Produce a convergence table for Euler\'s method applied to the Van der Pol oscillator."""

# pylint: disable=R0913

import argparse
import numpy as np
import lazy_table as lt


def dynamics(state, damping_strength):
    """Dynamics of the Van der Pol oscillator."""
    return np.array([
        state[1],
        damping_strength * (1. - state[0]**2) * state[1] - state[0],
    ])


def solve(init_pos, init_vel, final_time, damping_strength, n_steps):
    """Solve the Van der Pol oscillator up to a given time using Euler's method."""
    h = final_time / n_steps
    state = np.array([init_pos, init_vel])
    for _ in range(n_steps):
        state = state + h * dynamics(state=state, damping_strength=damping_strength)
    return state.tolist()


def convergence_table(init_pos, init_vel, final_time, damping_strength, init_n_steps, n_rows):
    """Generate a convergence table for Euler's method applied to the Van der Pol oscillator."""
    prev_value = np.nan
    prev_delta = np.nan
    for n_steps in init_n_steps * 2**np.arange(0, n_rows):
        value, _ = solve(
            init_pos=init_pos,
            init_vel=init_vel,
            final_time=final_time,
            damping_strength=damping_strength,
            n_steps=n_steps,
        )
        delta = value - prev_value
        ratio = prev_delta / delta
        order = np.log2(ratio)
        prev_value = value
        prev_delta = delta
        yield [n_steps, value, delta, order]


parser = argparse.ArgumentParser(
    description='produce a convergence table for Euler\'s method applied to the Van der Pol oscillator',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--init_pos', default=2., help='initial position', metavar='', type=float)
parser.add_argument('--init_vel', default=0., help='initial velocity', metavar='', type=float)
parser.add_argument('--final_time', default=16., help='final time', metavar='', type=float)
parser.add_argument('--damping_strength', default=1., help='damping strength', metavar='', type=float)
parser.add_argument('--init_n_steps', default=200, help='initial number of steps', metavar='', type=int)
parser.add_argument('--n_rows', default=12, help='number of rows in convergence table', metavar='', type=int)
parser.add_argument('--tablefmt',
                    default='simple',
                    help='see https://github.com/astanin/python-tabulate',
                    metavar='',
                    type=str)
parser.add_argument('--show_progress', help='enables a progress bar', action='store_true')
args = parser.parse_args()

table = convergence_table(
    init_pos=args.init_pos,
    init_vel=args.init_vel,
    final_time=args.final_time,
    damping_strength=args.damping_strength,
    init_n_steps=args.init_n_steps,
    n_rows=args.n_rows,
)
artist = lt.artists.ConsoleWithProgress() if args.show_progress else lt.artists.Console()
headers = ['Steps', 'Value', 'Delta', 'Order']
lt.stream(table, artist=artist, headers=headers, tablefmt=args.tablefmt, n_rows=args.n_rows)
