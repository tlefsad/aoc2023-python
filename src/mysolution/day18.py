#!/usr/bin/env python3
"""Solution to Day n: _
https://adventofcode.com/2023/day/n
"""

from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from collections import defaultdict

        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        dig_plan = read_input(fobj)

    p1 = int(area_by_shoelace(dig_plan.fst_edges) + 1 - dig_plan.fst_points/2) + dig_plan.fst_points
    print("Part 1:", p1)

    p2 = int(area_by_shoelace(dig_plan.snd_edges) + 1 - dig_plan.snd_points/2) + dig_plan.snd_points
    print("Part 2:", p2)

   
def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return DigPlan.from_str(fobj.read())


@dataclasses.dataclass(frozen=True)
class DigPlan:
    fst_edges: list[tuple[int, int]]
    fst_points: int

    snd_edges: list[tuple[int, int]]
    snd_points: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        x, y = 0, 0
        fst_edges = []
        fst_points = 0
        for line in s.strip().splitlines():
            dir, length, color = line.strip().split()
            match dir:
                case 'U': dx, dy = 0, -int(length)
                case 'D': dx, dy = 0, int(length)
                case 'L': dx, dy = -int(length), 0
                case 'R': dx, dy = int(length), 0
            x, y = x + dx, y + dy
            fst_edges.append((x, y))
            fst_points += int(length) 

        x, y = 0, 0
        snd_edges = []
        snd_points = 0
        for line in s.strip().splitlines():
            *_, color = line.strip().split()
            code = color.strip('(#)')
            length, dir  = code[:-1], code[-1]
            match dir:
                case '0': dx, dy = int(length, 16), 0
                case '1': dx, dy = 0, int(length, 16)
                case '2': dx, dy = -int(length, 16), 0
                case '3': dx, dy = 0, -int(length, 16)
            x, y = x + dx, y + dy
            snd_edges.append((x, y))
            snd_points += int(length, 16)

        return cls(
            fst_edges=fst_edges, fst_points=fst_points, 
            snd_edges=snd_edges, snd_points=snd_points
        )


def area_by_shoelace(edges: list[tuple[int, int]]):
    x, y = zip(*edges)
    return abs(sum(x[i-1]*y[i]-x[i]*y[i-1] for i in range(len(x)))) / 2.
 

if __name__ == '__main__':
    program()

