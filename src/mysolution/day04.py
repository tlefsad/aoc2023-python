#!/usr/bin/env python3
"""Solution to Day 4: Scratchcards
https://adventofcode.com/2023/day/4
"""
from __future__ import annotations

from typing import TextIO
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from functools import cached_property


@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        cards = read_input(fobj)

    # Part 1: find the total points
    p1 = sum(card.points for card in cards)
    print("Part 1:", p1)

    # Part 2: find the total scratchcards
    p2 = total_scratchcards(cards)
    print("Part 2:", p2)


def read_input(fobj: TextIO) -> list[ScratchCard]:
    """Reads and parses input file according to problem statement.
    """
    return [ScratchCard.from_str(line) for line in fobj]


@dataclasses.dataclass(frozen=True)
class ScratchCard:
    win: set[str]

    @classmethod
    def from_str(cls, s: str) -> Self:
        card, numbers = s.strip().split(':')
        winning, having = numbers.strip().split('|')
        winning_numbers = set(winning.strip().split())
        having_numbers = set(having.strip().split())
        return cls(
            win=winning_numbers & having_numbers
        )

    @cached_property
    def points(self) -> int:
        n = len(self.win)
        return 2**(n-1) if n else 0


def total_scratchcards(cards: list[ScratchCard]) -> int:
    instances = [1]*len(cards)
    for i, card in enumerate(cards):
        for j in range(1, len(card.win)+1):
            instances[i+j] += instances[i] 
    return sum(instances)


if __name__ == '__main__':
    program()

