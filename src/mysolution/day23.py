#!/usr/bin/env python3
"""Solution to Day n: _
https://adventofcode.com/2023/day/n
"""

from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from collections import deque, defaultdict
import itertools
import heapq
from pprint import pprint


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
    grid: list[list[str]]
    slopes: list[tuple[int, int, str]]

    @classmethod
    def from_str(cls, s: str) -> Self:
        grid, slopes = [], []
        for r, line in enumerate(s.strip().splitlines()):
            row = []
            for c, char in enumerate(line.strip()):
                if char in '^v<>':
                    slopes.append((r, c, char))
                row.append(char)
            grid.append(row)

        return cls(grid=grid, slopes=slopes)


def p1_solve(puzzle):
    grid = puzzle.grid
    slopes = puzzle.slopes
    m, n = len(grid), len(grid[0])

    x, y = 0, grid[0].index('.')
    start = (x, y)
    end = (m-1, grid[m-1].index('.'))

    src, dir, dist = (x, y), 'v', 0
    q = deque([(src, x, y, dir, dist)])
    nodes = defaultdict(dict)

    while q:
        src, x, y, dir, dist = q.popleft()
        for dx, dy, new_dir, opposed in [(-1, 0, '^', 'v'), 
                                    (1, 0, 'v', '^'), 
                                    (0, -1, '<', '>'), 
                                    (0, 1, '>', '<')]:
            pos_x, pos_y = x + dx, y + dy
            if (pos_x < 0 or pos_x >= m or
                pos_y < 0 or pos_y >= n or 
                grid[pos_x][pos_y] == '#' or
                dir == opposed):
                continue

            if (pos_x, pos_y) == end:
                nodes[src][end] = dist + 1
                continue

            if grid[pos_x][pos_y] == '.':
                q.append((src, pos_x, pos_y, new_dir, dist+1))

            elif grid[pos_x][pos_y] != opposed:
                if (dest := (pos_x, pos_y)) not in nodes[src]:
                    nodes[src][dest] = dist + 1
                    q.append((dest, pos_x, pos_y, grid[pos_x][pos_y], 0))

    # print('\n'.join(f'{i:2} ' + ''.join(row) for i, row in enumerate(grid)))

    ans = []
    q = deque([(start, 0)])
    while q:
        src, dist = q.popleft()
        for dest, value in nodes[src].items():
            if dest == end:
                ans.append(dist+value)
            else:
                q.append((dest, dist + value))
    
    return max(ans)


DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def get_neighbors(grid, x, y):
    m, n = len(grid), len(grid[0])
    for dx, dy in DIRECTIONS:
        if (0 <= (new_x := x + dx) < m and 
            0 <= (new_y := y + dy) < n and
            grid[new_x][new_y] != '#'):
            yield new_x, new_y
        

# Copy pasterino
def p2_solve(puzzle):
    grid = puzzle.grid
    slopes = puzzle.slopes
    m, n = len(grid), len(grid[0])

    x, y = 0, grid[0].index('.')
    start = (x, y)
    end = (m-1, grid[m-1].index('.'))
    
    stack = [start]
    visited = set()
    graph = defaultdict(list)

    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue

        for new_x, new_y in get_neighbors(grid, x, y):
            dist = 1
            prev_x, prev_y = x, y
            pos_x, pos_y = new_x, new_y
            ended = False

            while True:
                neighbors = list(get_neighbors(grid, pos_x, pos_y))
                if neighbors == [(prev_x, prev_y)] and grid[x][y] in '^v><':
                    ended = True
                    break

                if len(neighbors) != 2:
                    break

                for neighbor in neighbors:
                    if neighbor != (prev_x, prev_y):
                        dist += 1
                        prev_x, prev_y = pos_x, pos_y
                        pos_x, pos_y = neighbor
                        break
            if ended:
                continue

            graph[x, y].append(((pos_x, pos_y), dist))
            stack.append((pos_x, pos_y))

        visited.add((x, y))

    ans = []
    stack = [(start, 0, {start})]
    while stack:
        u, dist, visited = stack.pop()
        if u == end:
            ans.append(dist)
            continue
        for v, d in graph[u]:
            if v not in visited:
                stack.append((v, dist + d, visited | {v}))
    return max(ans)


if __name__ == '__main__':
    program()

