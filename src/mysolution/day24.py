#!/usr/bin/env python3
"""Solution to Day n: _
https://adventofcode.com/2023/day/n
"""

from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
import numpy as np
import itertools
from sympy import Symbol, solve_poly_system


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        puzzle = read_input(fobj)

    p1 = p1_solve(puzzle)
    print("Part 1:", p1)

    p2 = p2_solve(puzzle)
    print("Part 2:", p2)

   
def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return Puzzle.from_str(fobj.read())


@dataclasses.dataclass
class Puzzle:
    A: list[np.array]
    B: list[int]
    C: list[tuple[int, int]]

    @classmethod
    def from_str(cls, s: str) -> Self:
        A, B, C = [], [], []
        for line in s.strip().splitlines():
            position, velocity = line.strip().split('@')
            x, y, z = map(int, position.strip().split(','))
            u, v, w = map(int, velocity.strip().split(','))
            A.append(np.array([v,  -u]))
            B.append(v*x - u*y)
            C.append(((u, x), (v, y), (w, z)))
        return cls(A=A, B=B, C=C)


def p1_solve(puzzle):
    n = len(puzzle.A)
    A = puzzle.A 
    B = puzzle.B
    C = puzzle.C

    # at_least = 7
    # at_most = 27
    at_least = 200000000000000
    at_most = 400000000000000

    ans = 0
    for i, j in itertools.combinations(range(n), 2):
        try:
            Z = np.linalg.solve(np.array([A[i], A[j]]), np.array([B[i], B[j]]))
            if (all(at_least <= k <= at_most for k in Z) and
                (Z[0] - C[i][0][1])*C[i][0][0] >= 0 and
                (Z[1] - C[i][1][1])*C[i][1][0] >= 0 and
                (Z[0] - C[j][0][1])*C[j][0][0] >= 0 and
                (Z[1] - C[j][1][1])*C[j][1][0] >= 0):
                ans += 1

        except np.linalg.LinAlgError:
            continue
    return ans


# Copy pasterino
def p2_solve(puzzle):
    C = puzzle.C
    n = len(C)

    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    u = Symbol('u')
    v = Symbol('v')
    w = Symbol('w')

    equations, t_syms = [], []
    for idx, ((u0, x0), (v0, y0), (w0, z0)) in enumerate(C[:3]):
        t = Symbol(f't{idx}')
        equations.append(x + u*t - x0 - u0*t)
        equations.append(y + v*t - y0 - v0*t)
        equations.append(z + w*t - z0 - w0*t)
        t_syms.append(t)

    ans = solve_poly_system(equations, *([x, y, z, u, v, w] + t_syms))[0][:3]
    return sum(ans)
                

if __name__ == '__main__':
    program()

