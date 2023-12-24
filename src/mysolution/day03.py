#!/usr/bin/env python3
from __future__ import annotations

from typing import TextIO, Iterable
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from itertools import product
import re
import math


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        engine_schematic = read_input(fobj)

    # Part 1: find the sum of 
    p1 = sum(sum(parts)for parts in engine_schematic.gears)
    print("Part 1:", p1)

    p2 = sum(math.prod(parts) for parts in engine_schematic.gears if len(parts) == 2)
    print("Part 2:", p2)


def read_input(fobj: TextIO) -> EngineSchematic:
    """Reads and parses input file according to problem statement.
    """
    return EngineSchematic.from_str(fobj.read())


@dataclasses.dataclass
class EngineSchematic:
    gears: Iterable[list[int]]

    @classmethod
    def from_str(cls, s: str) -> Self: 
        schematic = [line.strip() for line in s.strip().splitlines()]

        gears = {
            (row, col): []
            for row, text in enumerate(schematic)
            for col, char in enumerate(text)
            if char not in '.0123456789'
        }

        for row, text in enumerate(schematic):
            for col in re.finditer(r'\d+', text):
                rows = range(row-1, row+2)
                cols = range(col.start()-1, col.end()+1)
                for pos in product(rows, cols):
                    if pos in gears.keys():
                        gears[pos].append(int(col.group()))

        return cls(gears=gears.values())


if __name__ == '__main__':
    program()

