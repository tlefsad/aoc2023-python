#!/usr/bin/env python3
"""Solution to Day 8: 
https://adventofcode.com/2023/day/8
"""
from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from enum import IntEnum, StrEnum, unique 
import itertools
import math

        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        instructions, network = read_input(fobj)

    p1 = lookup(network, instructions, "AAA")
    print("Part 1:", p1)

    start_nodes = [node for node in network.nodes.keys() if node.endswith('A')]
    steps = (lookup(network, instructions, node) for node in start_nodes)
    p2 = math.lcm(*steps)
    print("Part 2:", p2)


def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    instructions, _, *network = fobj.readlines()
    return instructions.strip(), Network.from_str(network) 


@dataclasses.dataclass
class Network:
    nodes: dict[Node, dict[str, Node]]

    @classmethod
    def from_str(cls, s: str) -> Self:
        nodes = {}
        for line in s:
            match line.strip().split():
                case [name, '=', left, right]:
                    nodes[name] = {'L': left.strip('(,'),
                                   'R': right.strip(')')}

        return cls(nodes=nodes)
   

def lookup(network: Network, instructions: str, node: str) -> int:
    if node not in network.nodes:
        return 0

    it = itertools.cycle(instructions)
    steps = 0 
    while not node.endswith('Z'):
        instruction = next(it)
        node = network.nodes[node][instruction]
        steps += 1

    return steps



if __name__ == '__main__':
    program()

