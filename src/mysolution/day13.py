#!/usr/bin/env python3
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
        patterns = read_input(fobj)
    
    p1 = sum(reflection(pattern, penalty=0) for pattern in patterns)
    print("Part 1:", p1)

    p2 = sum(reflection(pattern, penalty=1) for pattern in patterns)
    print("Part 2:", p2)


def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return [
        Pattern.from_str(pattern) 
        for pattern in fobj.read().strip().split('\n\n')
    ]

@dataclasses.dataclass(frozen=True)
class Pattern:
    rows: list[str]
    cols: list[str]
    nrow: int
    ncol: int

    def __repr__(self):
        return '\n'.join(self.rows) + '\n\n' + '\n'.join(self.cols)
    
    @classmethod
    def from_str(cls, s: str) -> Self:
        rows = [line for line in s.split('\n')]
        cols = list(''.join(col) for col in zip(*(s.split('\n'))))

        return cls(
            rows=rows,
            cols=cols,
            nrow=len(rows),
            ncol=len(cols),
        )


def expand_from_center(rows, i, j, penalty):
    cur_penalty = 0
    while i >= 0 and j < len(rows):
        if rows[i] != rows[j]:
            if cur_penalty:
                break
            else:
                cur_penalty += sum(l != r for l, r in zip(rows[i], rows[j]))
        i -= 1
        j += 1
    else:
        return cur_penalty == penalty
    return False


def reflection(pattern: Pattern, penalty: int):
    ans = 0
    for j in range(pattern.ncol-1):
        if expand_from_center(pattern.cols, j, j+1, penalty):
            ans += j+1
            break

    for i in range(pattern.nrow-1):
        if expand_from_center(pattern.rows, i, i+1, penalty):
            ans += (i+1)*100
            break
    return ans


if __name__ == '__main__':
    program()

