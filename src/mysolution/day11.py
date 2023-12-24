#!/usr/bin/env python3
from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from enum import IntEnum, StrEnum, unique 
import itertools
import more_itertools
from functools import cached_property
from bisect import bisect_left

        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        universe = read_input(fobj)

    p1 = shortest_path(universe, expansion_factor=2)
    print("Part 1:", p1)

    p2 = shortest_path(universe, expansion_factor=1000000)
    print("Part 2:", p2)


def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return Universe.from_str(fobj.read())


@dataclasses.dataclass(frozen=True)
class Universe:
    galaxies: list[tuple[int, int]]
    row_spaces: list[int]
    col_spaces: list[int]

    @classmethod
    def from_str(cls, s: str) -> Self:
        grid = []
        galaxies = []
        for r, line in enumerate(s.strip().splitlines()):
            row = []
            for c, galaxy in enumerate(line):
                if galaxy == '#':
                    galaxies.append((r, c))
                row.append(galaxy)
            grid.append(row)
 
        row_spaces = [i for i, row in enumerate(grid) if all(c == '.' for c in row)]
        col_spaces = [j for j, col in enumerate(zip(*grid)) if all(c == '.' for c in col)]

        return cls(
            galaxies=galaxies,
            row_spaces=row_spaces,
            col_spaces=col_spaces
        )


def shortest_path(universe: Unverse, expansion_factor: int) -> int:
    ans = 0
    for idx, (x1, y1) in enumerate(universe.galaxies[:-1]):
        for x2, y2 in universe.galaxies[idx+1:]:
            dx = abs(bisect_left(universe.row_spaces, x2) - bisect_left(universe.row_spaces, x1))
            dy = abs(bisect_left(universe.col_spaces, y2) - bisect_left(universe.col_spaces, y1))
            ans += abs(y1 - y2) + abs(x1 - x2) + (dx + dy)*(expansion_factor-1)
    return ans


if __name__ == '__main__':
    program()

