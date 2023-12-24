#!/usr/bin/env python3
"""Solution to Day n: _
https://adventofcode.com/2023/day/n
"""

from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses

        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        _ = read_input(fobj)


    p1 = 0
    print("Part 1:", p1)

    p2 = 0
    print("Part 2:", p2)

   
def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    # return [Puzzle.from_str(line.strip()) for line in fobj.readlines()]
    return Puzzle.from_str(fobj.read())


@dataclasses.dataclass
class Puzzle:

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls()


if __name__ == '__main__':
    program()

