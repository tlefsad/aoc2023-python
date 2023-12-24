#!/usr/bin/env python3
"""Solution to Day 6: Wait For It
https://adventofcode.com/2023/day/6
"""
from __future__ import annotations

from typing import TextIO
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
import more_itertools
from bisect import bisect_right


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        record = read_input(fobj)

    # Part 1: find the number of ways that could beat the record in each race.
    p1 = beating_ways(record.races)
    print("Part 1:", p1)

    # Part 1: find the number of ways that could beat the record in one much longer race.
    p2 = beating_ways(record.longer_races)
    print("Part 2:", p2)


def read_input(fobj: TextIO) -> Record:
    """Reads and parses input file according to problem statement.
    """
    return Record.from_str(fobj.read())


@dataclasses.dataclass(frozen=True)
class Record:
    races: tuple[tuple[int, int]]
    longer_races: tuple[tuple[int, int]]

    @classmethod
    def from_str(cls, s: str) -> Self:
        time_records, dist_records = s.strip().splitlines()
        races = tuple(zip(
            more_itertools.map_except(int, time_records.split(), ValueError),
            more_itertools.map_except(int, dist_records.split(), ValueError)
        ))
        longer_races = ((
            int("".join(t for t in time_records if t.isdigit())),
            int("".join(d for d in dist_records if d.isdigit()))
        ),)

        return cls(
            races=races,
            longer_races=longer_races
        )

def beating_ways(races: tuple[tuple[int, int]]) -> int:
    ways = 1
    for time, dist in races:
        time_range = range((time+1)//2)
        ways *= time + 1 - 2 * bisect_right(time_range, dist, key=lambda t: (time-t)*t)
    return ways


if __name__ == '__main__':
    program()

