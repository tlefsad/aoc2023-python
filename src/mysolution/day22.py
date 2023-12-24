#!/usr/bin/env python3
"""Solution to Day n: _
https://adventofcode.com/2023/day/n
"""

from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import itertools
import re
from collections import defaultdict, deque

        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        puzzle = read_input(fobj)


    p1 = p1_solve(puzzle)
    print("Part 1:", p1)

    p2 = p2_solve(puzzle)
    print("Part 2:", p2)

   
def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return Puzzle.from_str(fobj.read())


@dataclasses.dataclass
class Puzzle:
    children: dict[int, set[int]]
    parents: dict[int, set[int]]

    @classmethod
    def from_str(cls, s: str) -> Self:
        x, y, z = np.indices((10, 10, 321))
        voxelarray = np.zeros((10, 10, 321), dtype=bool)
        grid = np.empty(voxelarray.shape, dtype=object)

        bricks = []
        children = defaultdict(set)
        parents = defaultdict(set)
        voxelarray[:,:,0] = True


        # it = itertools.cycle(mcolors.TABLEAU_COLORS)
        # colors = np.empty(voxelarray.shape, dtype=object)
        # colors[voxelarray] = 'grey'
        for line in s.strip().splitlines():
            x1, y1, z1, x2, y2, z2 = map(int, re.split(r'\D', line))
            brick = (x >= x1) & (x <= x2) & (y >= y1) & (y <= y2) & (z >= z1) & (z <= z2)
            bricks.append((z2, brick))
                        
        for idx, (_, brick) in enumerate(sorted(bricks, key=lambda x: x[0])):
            while not (voxelarray & brick).any():
                brick = np.roll(brick, -1, axis=2)
            else:
                for base in set(grid[(voxelarray & brick)]):
                    parents[idx].add(base)
                    children[base].add(idx)

                brick = np.roll(brick, 1, axis=2)

            voxelarray |= brick
            grid[brick] = idx
            # colors[brick] = next(it)

        # ax = plt.figure().add_subplot(projection='3d')
        # ax.voxels(voxelarray, facecolors=colors, edgecolor='k')

        # plt.show()
        return cls(children=children, parents=parents)
       

def p1_solve(puzzle):
    ans = 0
    for brick in puzzle.parents.keys():
        if all(len(puzzle.parents[b]) > 1 for b in puzzle.children[brick]):
            ans += 1
    return ans


def p2_solve(puzzle):
    ans = 0
    for start in puzzle.parents.keys():
        falls = {start}
        q = deque([start])
        while q:
            brick = q.popleft()
            for b in puzzle.children[brick]:
                if not (puzzle.parents[b] - falls):
                    falls.add(b)
                    q.append(b)

        ans += len(falls) - 1
    return ans


if __name__ == '__main__':
    program()

