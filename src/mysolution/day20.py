#!/usr/bin/env python3
"""Solution to Day n: _
https://adventofcode.com/2023/day/n
"""

from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
from enum import StrEnum, unique, IntFlag
import dataclasses
from dataclasses import field
from collections import deque, defaultdict
import itertools
import math

        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        puzzle = read_input(fobj)


    p1 = solve(puzzle, range(1000))
    print("Part 1:", p1)

    p2 = solve(puzzle, itertools.count())
    print("Part 2:", p2)

   
def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return Puzzle.from_str(fobj.read())


@unique
class Pulse(IntFlag):
    LOW: int = 0
    HIGH: int = 1


@unique
class ModuleType(StrEnum):
    BUTTON: str = 'button'
    BROADCAST: str = 'broadcaster'
    FLIP_FLOP: str = '%'
    CONJUNCTION: str = '&'


@dataclasses.dataclass(frozen=True)
class Module:
    name: str
    module_type: ModuleType = field(compare=False)
    dests: list[str] = field(compare=False)
    
    @classmethod
    def from_str(cls, s: str) -> Self:
        name, dests = s.strip().split(' -> ')

        if name == 'broadcaster':
            return cls(name, ModuleType.BROADCAST, dests.split(', '))

        return cls(name[1:], ModuleType(name[0]), dests.split(', '))

    def __iter__(self):
        yield from self.dests
        

@dataclasses.dataclass
class Puzzle:
    modules: dict[str, Module]

    @classmethod
    def from_str(cls, s: str) -> Self:
        modules = {}
        for line in s.strip().splitlines():
            module = Module.from_str(line) 
            modules[module.name] = module
        return cls(modules=modules)


def solve(puzzle, cycles):
    modules = puzzle.modules

    pulses = defaultdict(dict)
    flipflops = dict()
    conjunctions = dict()

    for src, module in modules.items():
        for dest in module.dests:
            if dest not in modules:
                continue

            if modules[dest].module_type == ModuleType.CONJUNCTION:
                pulses[dest][src] = Pulse.LOW
                conjunctions[dest] = None

            if modules[dest].module_type == ModuleType.FLIP_FLOP:
                flipflops[dest] = 0

    
    counter = defaultdict(int)
    for cycle in cycles:
        q = deque([(Pulse.LOW, 'button', 'broadcaster')])
        counter[Pulse.LOW] += 1
        while q:
            pulse, src, dest = q.popleft()
            # print(f'{src} -{pulse.name.lower()}-> {dest}')
            
            if dest not in modules:
                continue

            module = modules[dest]
            match [module.module_type, pulse]:
                case [ModuleType.FLIP_FLOP, Pulse.HIGH]:
                    continue
                case [ModuleType.FLIP_FLOP, Pulse.LOW]:
                    flipflops[dest] ^= 1
                    pulse = Pulse(flipflops[dest])
                case [ModuleType.CONJUNCTION, _]:
                    pulses[dest][src] = pulse
                    pulse = ~Pulse(all(pulses[dest].values()))
            
            if (module.module_type == ModuleType.CONJUNCTION and 
                pulse == Pulse.HIGH and 
                conjunctions[dest] is None):

                conjunctions[dest] = cycle + 1

                if all(conjunctions.values()):
                    return math.lcm(*conjunctions.values())

            for next_dest in module:
                counter[pulse] += 1
                q.append((pulse, dest, next_dest))

    return counter[Pulse.LOW] * counter[Pulse.HIGH]


if __name__ == '__main__':
    program()

