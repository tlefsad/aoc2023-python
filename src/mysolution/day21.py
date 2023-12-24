#!/usr/bin/env python3
"""Solution to Day n: _
https://adventofcode.com/2023/day/n
"""

from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from collections import deque, OrderedDict, defaultdict
import numpy as np

        
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


@dataclasses.dataclass(frozen=True)
class Puzzle:
    grid: list[list[int]]
    entry: tuple[int, int]

    @classmethod
    def from_str(cls, s: str) -> Self:
        grid = []
        for r, line in enumerate(s.strip().splitlines()):
            row = []
            for c, char in enumerate(line.strip()):
                if char == 'S':
                    entry = (r, c)
                    char = '.'
                row.append(char)
            grid.append(row)
        
        return cls(grid=grid, entry=entry)


def bfs(puzzle, steps):
    default_grid, entry = puzzle.grid, puzzle.entry
    m, n = len(default_grid), len(default_grid[0])
    grid = dict()
    queue = deque([entry])
    for step in range(steps):
        for _ in range(len(queue)):
            row, col = queue.popleft()
            grid[row, col] = '.'
            for r, c in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                pos = row + r, col + c
                default_pos = default_grid[pos[0]%m][pos[1]%n]
                if grid.setdefault(pos, default_pos) == '.':
                    grid[pos] = 'O'
                    queue.append(pos)
    return len(queue)
    

def p1_solve(puzzle):
    return bfs(puzzle, 64)


def p2_solve(puzzle):
    # polynomial extrapolation
    a0 = bfs(puzzle, 0*131 + 65)
    a1 = bfs(puzzle, 1*131 + 65)
    a2 = bfs(puzzle, 2*131 + 65)

    vandermonde = np.matrix([[0, 0, 1], [1, 1, 1], [4, 2, 1]])
    b = np.array([a0, a1, a2])
    x = np.linalg.solve(vandermonde, b).astype(np.int64)

    # 26501365 = 202300 * 131 + 65
    n = 202300
    return x[0] * n * n + x[1] * n + x[2]


if __name__ == '__main__':
    program()

