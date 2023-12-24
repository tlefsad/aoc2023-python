#!/usr/bin/env python3
from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from enum import IntEnum, StrEnum, unique 
import itertools
import more_itertools
from functools import cached_property, cache
import re
import math
from collections import Counter, deque

        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        springs = read_input(fobj)


    p1 = 0
    for spring in springs:
        p1 += possible_ways(spring.records, spring.groups)
    print("Part 1:", p1)

    p2 = 0
    for spring in springs:
        records = "?".join([spring.records]*5)
        groups = spring.groups*5
        p2 += possible_ways(records, groups)
    print("Part 2:", p2)

   
def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return [Springs.from_str(line) for line in fobj]



@dataclasses.dataclass(frozen=True)
class Springs:
    records: str
    groups: tuple[int]

    @classmethod
    def from_str(cls, s: str) -> Self:
        records, groups = s.strip().split()
        return cls(records=records, groups=tuple(map(int, groups.split(','))))


@cache
def possible_ways(s: str, groups: tuple[int]):
    if not groups:
        return '#' not in s
    ways = 0
    for idx in range(len(s) - sum(groups) + len(groups)):
        possible = '.'*idx + '#'*groups[0] + '.'
        for spring, possible_spring in zip(s, possible):
            if spring != possible_spring and spring != '?':
                break
        else:
            ways += possible_ways(s[len(possible):], groups[1:])
    return ways



if __name__ == '__main__':
    program()

