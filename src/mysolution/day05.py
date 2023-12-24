#!/usr/bin/env python3
"""Solution to Day 5: 
https://adventofcode.com/2023/day/5
"""
from __future__ import annotations

from typing import TextIO
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from functools import cached_property
import itertools
import more_itertools
import collections


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        almanac = read_input(fobj)

    # Part 1: find the sum of 
    p1 = almanac.p1_solve()
    print("Part 1:", p1)

    p2 = almanac.p2_solve()
    print("Part 2:", p2)


def read_input(fobj: TextIO) -> list[Game]:
    """Reads and parses input file according to problem statement.
    """
    return Almanac.from_str(fobj.read())


@dataclasses.dataclass
class Almanac:
    seeds: list[int]
    maps: list[list[tuple[int, int, int]]]

    @classmethod
    def from_str(cls, s: str) -> Self:
        seeds_line, *lines = s.strip().split("\n\n")
        seeds = list(more_itertools.map_except(int, seeds_line.split(), ValueError))

        maps = []
        for idx, line in enumerate(lines):
            ranges = more_itertools.map_except(int, line.split(), ValueError)
            mp = []
            for dst, src, length in more_itertools.batched(ranges, 3):
                mp.append((src, src+length, dst - src))

            maps.append(mp)

        return cls(
            seeds=seeds,
            maps=maps,
        )


    def p1_solve(self):
        ans = []
        for seed in self.seeds:
            for ranges in self.maps:
                for start, end, val in ranges:
                    if start <= seed < end:
                        seed += val
                        break
            ans.append(seed)
        return min(ans)
                    

    def p2_solve(self):
        seeds = list((seed, seed+length) for seed, length in more_itertools.chunked(self.seeds, 2))
        for ranges in self.maps:
            new_seeds = []
            while seeds:
                seed_start, seed_end = seeds.pop()
                for range_start, range_end, val in ranges:
                    start = max(seed_start, range_start)
                    end = min(seed_end, range_end)
                    if start < end:
                        new_seeds.append((start + val, end + val))
                        if start > seed_start:
                            seeds.append((seed_start, start))
                        if seed_end > end:
                            seeds.append((end, seed_end))
                        break
                else:
                    # not overlapped
                    new_seeds.append((seed_start, seed_end))
            seeds = new_seeds
        return min(seeds)[0]



if __name__ == '__main__':
    program()

