#!/usr/bin/env python3
from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from enum import IntEnum, StrEnum, unique 
import itertools
import more_itertools
from functools import cached_property

        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        platform = read_input(fobj)
    
    p1 = p1_solve(platform)
    print("Part 1:", p1)

    p2 = p2_solve(platform) 
    print("Part 2:", p2)


def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return Platform.from_str(fobj.read())


@dataclasses.dataclass(frozen=True)
class Platform:
    grid: tuple[tuple[str]]

    def __repr__(self):
        return '\n'.join("".join(i) for i in self.grid)
    
    @classmethod
    def from_str(cls, s: str) -> Self:
        grid = tuple(tuple(line) for line in s.strip().splitlines())
        return cls(
            grid=grid,
        )


def tilt(grid, direction):
    match direction:
        case "left":
            split, reverse = more_itertools.split_after, True
        case "right":
            split, reverse = more_itertools.split_before, False
        case _:
            raise ValueError("Direction must be either left or right.")
        
    cols = []
    for col in grid:
        partitions = split(col, lambda s: s == '#')
        cols.append(
            tuple(itertools.chain(
                *(sorted(p, reverse=reverse) for p in partitions)
            ))
        )
    return tuple(cols)


def roll(grid): # normal
    north = zip(*tilt(zip(*grid), "left")) # North: transpose -> tilt left -> transpose
    west = tilt(north, "left") # West: tilt left
    south = zip(*tilt(zip(*west), "right")) # South: transpose -> tilt right -> transpose
    east = tilt(south, "right") # East: tilt right
    return east


def p1_solve(platform: Platform):
    grid = tuple(zip(*tilt(zip(*platform.grid), "left")))
    return sum(col.count('O')*i for i, col in zip(range(len(grid), 0, -1), grid))


def p2_solve(platform: Platform):
    cycles = 10**9
    grid = platform.grid
    seen = {grid: 0}
    while (grid := roll(grid)) not in seen:
        seen[grid] = len(seen)
        
    cycle_begin = cycles - seen[grid]
    cycle_length = len(seen) - seen[grid]
    for _ in range(cycle_begin % cycle_length):
        grid = roll(grid)

    return sum(col.count('O')*i for i, col in zip(range(len(grid), 0, -1), grid))

if __name__ == '__main__':
    program()

