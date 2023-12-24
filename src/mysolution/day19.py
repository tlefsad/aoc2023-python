#!/usr/bin/env python3
"""Solution to Day n: _
https://adventofcode.com/2023/day/n
"""
from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from enum import StrEnum, unique
import re
import math


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        system = read_input(fobj)

    rating_ranges = list(rating_range(system.workflows))
    p1 = 0
    for parts in system.listed_parts:
        for ratings in rating_ranges: 
            if parts in ratings:
                p1 += sum(parts)
    print("Part 1:", p1)
     
    p2 = sum(math.prod(rating.stop - rating.start 
                        for rating in ratings) for ratings in rating_ranges)
    print("Part 2:", p2)

   
def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return System.from_str(fobj.read())


@dataclasses.dataclass(frozen=True, order=True)
class Part:
    xmas: tuple[int, ...]

    def __iter__(self):
        yield from self.xmas


@dataclasses.dataclass(frozen=True, order=True)
class RatingRange:
    xmas: tuple[range, ...]

    def __contains__(self, part: Part):
        return all(
            part in rating_range 
            for part, rating_range in zip(part, self.xmas)
        )

    def __iter__(self):
        yield from self.xmas


@dataclasses.dataclass(frozen=True)
class System:
    workflows: dict[str, tuple[list[str], str]]
    listed_parts: list[tuple[int, ...]]

    @classmethod
    def from_str(cls, s: str) -> Self:
        workflows_list, part_ratings = s.strip().split('\n\n')

        workflows = {}
        for line in workflows_list.strip().splitlines():
            name, *rules, default, _ = re.split(r'[{,}]', line.strip())
            workflows[name] = (rules, default)

        listed_parts = [
            Part(tuple(map(int, re.findall(r'\d+', part))))
            for part in part_ratings.strip().splitlines()
        ]

        return cls(workflows=workflows, listed_parts=listed_parts)


def rating_range(workflows: dict[str, tuple[list[str], str]]):
    stack = [('in', {r: range(1, 4001) for r in 'xmas'})]
    while stack:
        name, ratings = stack.pop()
        if name == 'R':
            continue

        if name == 'A':
            yield RatingRange(tuple(ratings.values()))
            continue

        rules, default = workflows[name]
        for rule in rules:
            key, op, num, _, dest = re.split(r'(\W+)', rule)
            if (val := int(num)) in ratings[key]:
                match op:
                    case '<':
                        stack.append((dest, ratings | {key: range(ratings[key].start, val)}))
                        ratings.update({key: range(val, ratings[key].stop)})
                    case '>':
                        stack.append((dest, ratings | {key: range(val+1, ratings[key].stop)}))
                        ratings.update({key: range(ratings[key].start, val+1)})

        stack.append((default, ratings))
    

if __name__ == '__main__':
    program()

