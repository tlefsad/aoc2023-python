#!/usr/bin/env python3
"""Solution to Day 1: Trebuchet?! 
https://adventofcode.com/2023/day/1
"""
from __future__ import annotations

import dataclasses
from enum import StrEnum
from functools import cached_property
from typing import TextIO, Self

import more_itertools

from helpers.cli import command_with_input_file, open_input_file


@command_with_input_file
def program(input_file: str) -> None:
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        document = read_input(fobj)

    # Part 1: find the sum of all of the calibration values.
    p1_calibration_values = sum(line.fst_calibration_value for line in document)
    print("Part 1:", p1_calibration_values)

    # Part 2: find the sum of all of the calibration values.
    #         (somes of digits are spelled out with letters)
    p2_calibration_values = sum(line.snd_calibration_value for line in document)
    print("Part 2:", p2_calibration_values)


def read_input(fobj: TextIO) -> list[Line]:
    """Reads and parses input file according to problem statement.
    """
    return [Line.from_str(line) for line in fobj]

LETTERS = (
    "zero", "one", "two", "three", "four", 
    "five", "six", "seven", "eight", "nine", 
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
)

@dataclasses.dataclass(frozen=True)
class Line:
    text: str

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls(text=s.strip())

    @cached_property
    def fst_calibration_value(self) -> int:
        digits = more_itertools.map_except(int, self.text, ValueError)
        first_digit = more_itertools.first(digits, 0)
        last_digit = more_itertools.last(digits, first_digit) 
        return first_digit*10 + last_digit
   
    @cached_property
    def snd_calibration_value(self) -> int:
        candidates = []
        for idx, letter in enumerate(LETTERS):
            if (pos:=self.text.find(letter)) != -1:
                candidates.append((pos, idx%10))

                rpos = self.text.rfind(letter)
                candidates.append((rpos, idx%10))

        return min(candidates)[1]*10 + max(candidates)[1]

if __name__ == '__main__':
    program()

