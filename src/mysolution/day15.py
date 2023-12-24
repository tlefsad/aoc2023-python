#!/usr/bin/env python3
from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from enum import IntEnum, StrEnum, unique 
import itertools
import more_itertools
from functools import cached_property
from collections import defaultdict

        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        sequence = read_input(fobj)

    p1 = sum(hash_(procedure.string) for procedure in sequence)
    print("Part 1:", p1)

    p2 = focusing_power(sequence)
    print("Part 2:", p2)

   
def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return [Procedure.from_str(s) for s in fobj.read().strip().split(',')]


def hash_(string: Iterable) -> int:
    value = 0
    for char in string:
        value = ((value + ord(char)) * 17) % 256
    return value


@unique
class Operation(StrEnum):
    REMOVE: str = '-'
    ASSIGN: str = '='


@dataclasses.dataclass(frozen=True)
class Procedure:
    string: str
    operation: Operation
    label: str
    focal_length: int | None = None

    @classmethod
    def from_str(cls, s: str) -> Self:
        match tuple(s):
            case (*chars, '-'):
                return cls(
                    string=s, 
                    operation=Operation('-'), 
                    label="".join(chars)
                )
            
            case (*chars, '=', num):
                return cls(
                    string=s,
                    operation=Operation('='),
                    label="".join(chars), 
                    focal_length=int(num),
                )
            case _:
                raise ValueError


def focusing_power(sequence: list[Procedure]) -> int:
    boxes = defaultdict(dict)
    for procedure in sequence:
        box_id = hash_(procedure.label)
        match procedure.operation:
            case Operation.REMOVE:
                if procedure.label in boxes[box_id]:
                    boxes[box_id].pop(procedure.label)
            case Operation.ASSIGN:
                boxes[box_id][procedure.label] = procedure.focal_length

    return sum(
        (box_id + 1) * (slot_id + 1) * focal_length
        for box_id, box in boxes.items()
        for slot_id, focal_length in enumerate(box.values())
    )
            
           
if __name__ == '__main__':
    program()

