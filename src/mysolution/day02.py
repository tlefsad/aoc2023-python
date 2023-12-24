#!/usr/bin/env python3
"""Solution to Day 2: Cube Conundrum 
https://adventofcode.com/2023/day/2
"""
from __future__ import annotations

from typing import TextIO
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from functools import cached_property
import math


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        games = read_input(fobj)

    # Part 1: find the sum of ids of possible game. 
    p1 = sum(game.id for game in games if game.is_possible)
    print("Part 1:", p1)

    # Part 2: find the sum of the power of game sets
    p2 = sum(game.power for game in games)
    print("Part 2:", p2)


def read_input(fobj: TextIO) -> list[Game]:
    """Reads and parses input file according to problem statement.
    """
    return [Game.from_str(record) for record in fobj]


@dataclasses.dataclass(frozen=True)
class Game:
    id: int
    bag: list[Cubes]

    @classmethod
    def from_str(cls, s: str) -> Self:
        game, bag = s.strip().split(':')
        _, game_id = game.strip().split()
        subsets = bag.strip().split(';')
        return cls(
            id=int(game_id), 
            bag=[Cubes.from_str(subset) for subset in subsets]
        )

    @cached_property
    def is_possible(self) -> bool:
        return all(self.bag)

    @cached_property
    def power(self) -> int:
        return math.prod(map(max, zip(*self.bag)))
   

@dataclasses.dataclass(frozen=True, order=True)
class Cubes:
    red: int = 0
    green: int = 0
    blue: int = 0

    @classmethod
    def from_str(cls, s: str) -> Self:
        cubes = {}
        for info in s.strip().split(','):
            value, color = info.strip().split()
            cubes[color] = int(value)
        return cls(**cubes)

    def __bool__(self):
        return self.red <= 12 and self.green <= 13 and self.blue <= 14

    def __iter__(self):
        yield from (self.red, self.green, self.blue) 


if __name__ == '__main__':
    program()

