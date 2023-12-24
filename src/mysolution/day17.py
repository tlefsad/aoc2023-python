#!/usr/bin/env python3
from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from enum import IntEnum, StrEnum, unique 
import itertools
import more_itertools
from functools import cached_property
from heapq import heappop, heappush
from collections import defaultdict
from dataclasses import field

        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        crucible = read_input(fobj)

    p1 = shortest_path(crucible.grid, 1, 3)
    print("Part 1:", p1)

    p2 = shortest_path(crucible.grid, 4, 10)
    print("Part 2:", p2)

   
def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return Crucible.from_str(fobj.read())


@dataclasses.dataclass(frozen=True)
class Crucible:
    grid: dict[complex, int]

    @classmethod
    def from_str(cls, s: str) -> Self:
        grid = {
            complex(i, -j): int(num) 
            for j, line in enumerate(s.strip().splitlines()) 
            for i, num in enumerate(line.strip())
        }
        end = max(grid.keys(), key=lambda x: id(x))
        return cls(grid=grid)


@dataclasses.dataclass(frozen=True, order=True)
class Block:
    heat: int
    moves: int
    pos: complex = field(compare=False)
    dir: complex = field(compare=False)


def shortest_path(grid, min_moves, max_moves):
    end = max(grid.keys(), key=lambda x: id(x))
    q = []
    for i in (1, -1j):
        heappush(q, Block(grid[i], 1, i, i))
    min_heat = defaultdict(lambda : float('inf'))
    while q:
        block = heappop(q)

        if block.pos == end and block.moves >= min_moves:
            return block.heat 
        
        for moves, dir, min_moves in [(block.moves+1, block.dir, 1), 
                                      (1, block.dir * 1j, min_moves),
                                      (1, block.dir * -1j, min_moves)]:
            if ((min_moves <= block.moves) and 
                (moves <= max_moves) and 
                (pos := block.pos + dir) in grid and
                (heat := block.heat + grid[pos]) < min_heat[pos, dir, moves]):

                heappush(q, Block(heat, moves, pos, dir))
                min_heat[pos, dir, moves] = heat


if __name__ == '__main__':
    program()

