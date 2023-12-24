#!/usr/bin/env python3
from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from enum import IntEnum, StrEnum, unique 
import itertools
import more_itertools
from functools import cached_property, cache, partial

        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        contraption = read_input(fobj)


    p1 = bfs((-1, 1), grid=contraption.grid)
    print("Part 1:", p1)

    p2 = max(map(partial(bfs, grid=contraption.grid), ((pos-dir, dir) for dir in (1, 1j, -1, -1j)
                 for pos in contraption.grid if (pos - dir) not in contraption.grid)))
    print("Part 2:", p2)

   
def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return Contraption.from_str(fobj.read())



@dataclasses.dataclass
class Contraption:
    grid: dict[complex, str]

    @classmethod
    def from_str(cls, s: str) -> Self:
        grid = {}
        for j, line in enumerate(s.strip().splitlines()):
            for i, char in enumerate(line.strip()):
                grid[complex(i, j)] = char

        return cls(grid=grid)


def bfs(start, grid=None):
    visited = set()
    q = [start]
    while q:
        pos, dir = q.pop()
        while (pos, dir) not in visited:
            visited.add((pos, dir))
            pos += dir
            match grid.get(pos):
                case '|':
                    dir = 1j
                    q.append((pos, -dir))
                case '-':
                    dir = -1
                    q.append((pos, -dir))
                case '/':
                    dir = (dir * 1j).conjugate() # rotate 90 degree
                case '\\':
                    dir = (dir * -1j).conjugate() # rotate 270 degree
                case None:
                    break

    return len(set(pos for pos, _ in visited)) - 1
            

if __name__ == '__main__':
    program()

