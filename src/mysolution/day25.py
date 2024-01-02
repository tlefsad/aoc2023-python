#!/usr/bin/env python3
"""Solution to Day n: _
https://adventofcode.com/2023/day/n
"""

from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
import networkx as nx
import itertools
import math

        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        puzzle = read_input(fobj)

    p1 = solve(puzzle)
    print("Part 1:", p1)

   
def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return Puzzle.from_str(fobj.read())


@dataclasses.dataclass
class Puzzle:
    graph: nx.Graph

    @classmethod
    def from_str(cls, s: str) -> Self:
        graph = nx.Graph()
        for line in s.strip().splitlines():
            u, nodes = line.strip().split(':')
            for v in nodes.strip().split(' '):
                graph.add_edge(u, v, capacity=1.0)
        return cls(graph=graph)


def solve(puzzle):
    graph = puzzle.graph
    
    for s, t in itertools.combinations(graph.nodes, 2):
        cut_value, (reachable, non_reachable) = nx.minimum_cut(graph, s, t)
        if cut_value == 3:
            return len(reachable) * len(non_reachable)

    # cutset = nx.minimum_edge_cut(graph)
    # graph.remove_edges_from(cutset)
    # return math.prod(len(c) for c in nx.connected_components(graph))

if __name__ == '__main__':
    program()

