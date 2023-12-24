#!/usr/bin/env python3
from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from enum import IntEnum, StrEnum, unique 
import itertools
import more_itertools
from functools import cached_property, reduce
from collections import deque
from operator import sub


        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        maze = read_input(fobj)

    p1 = maze.bfs()
    print("Part 1:", p1)

    polygon = maze.dfs()
    p2 = int(area_by_shoelace(polygon) + 1 - len(polygon)/2)
    print("Part 2:", p2)

def read_input(fobj: TextIO):
    """Reads and parses input file according to problem statement.
    """
    return Maze.from_str(fobj.read())


N = (-1, 0, ('|', 'F', '7'))
S = ( 1, 0, ('|', 'L', 'J'))
E = ( 0, 1, ('-', '7', 'J'))
W = ( 0,-1, ('-', 'L', 'F'))

DIRECTIONS = {
    'S': [N, S, E, W],
    '|': [N, S],
    '-': [W, E],
    'J': [N, W],
    'L': [N, E],
    '7': [S, W],
    'F': [S, E],
}


@dataclasses.dataclass
class Maze:
    fst_grid: list[list[str]]
    snd_grid: list[list[str]]
    start: tuple[int, int] 
    nrow: int
    ncol: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        fst_grid, snd_grid, start = [], [], None
        for r, line in enumerate(s.strip().splitlines()):
            row = []
            for c, pipe in enumerate(line):
                if pipe == 'S':
                    start = (r, c)
                row.append(pipe)
            fst_grid.append(row[:])
            snd_grid.append(row[:])
        
        nrow, ncol = len(fst_grid), len(fst_grid[0])
        if start is None:
            raise ValueError("No starting position (S) from puzzle input.")

        return cls(fst_grid=fst_grid, snd_grid=snd_grid, start=start, nrow=nrow, ncol=ncol)

    def neighbors(self, grid, x, y) -> Iterable[tuple[int, int] | None]:
        if grid[x][y] == 'X':
            return

        for dx, dy, direction in DIRECTIONS[grid[x][y]]:
            if (0 <= (pos_x := x + dx) < self.nrow and 
                0 <= (pos_y := y + dy) < self.ncol and
                grid[pos_x][pos_y] in direction):

                yield (pos_x, pos_y)

    def bfs(self) -> int:
        q = deque([(self.start, 0)])
        ans = 0
        while q:
            (r, c), steps = q.popleft()
            ans = max(ans, steps)
            for i, j in self.neighbors(self.fst_grid, r, c):
                q.append(((i, j), steps+1))
            self.fst_grid[r][c] = 'X'
        return ans


    def dfs(self) -> list[tuple[int, int]]:
        q = deque([self.start])
        polygon = []
        while q:
            r, c = q.pop()
            polygon.append((r, c))
            for i, j in self.neighbors(self.snd_grid, r, c):
                q.append((i, j))
            self.snd_grid[r][c] = 'X'
        polygon.pop()
        return polygon


def area_by_shoelace(polygon):
    x, y = zip(*polygon)
    return abs(sum(x[i-1]*y[i]-x[i]*y[i-1] for i in range(len(x)))) / 2.
       

if __name__ == '__main__':
    program()

