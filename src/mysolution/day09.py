#!/usr/bin/env python3
"""Solution to Day 9: 
https://adventofcode.com/2023/day/9
"""
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
        report = read_input(fobj)

    p1 = sum(history.fst_value for history in report)
    print("Part 1:", p1)

    p2 = sum(history.snd_value for history in report)
    print("Part 2:", p2)


def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return [History.from_str(line) for line in fobj]


@dataclasses.dataclass(frozen=True)
class History:
    sequence: list[int]

    @classmethod
    def from_str(cls, s: str) -> Self:
        sequence = list(map(int, s.strip().split()))
        return cls(sequence=sequence)
    
    @cached_property
    def fst_value(self) -> int:
        differences = self.sequence[:]
        value = differences[-1]
        while any(val for val in differences):
            differences = [cur - prev for prev, cur in more_itertools.pairwise(differences)]
            value += differences[-1]
        return value
        
    @cached_property
    def snd_value(self) -> int:
        differences = self.sequence[:]
        value, factor = differences[0], -1
        while any(val for val in differences):
            differences = [cur - prev for prev, cur in more_itertools.pairwise(differences)]
            value += differences[0] * factor
            factor *= -1
        return value
     

if __name__ == '__main__':
    program()

