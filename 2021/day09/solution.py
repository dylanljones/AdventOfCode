# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-25

from itertools import product

import numpy as np

import aoc


def parse_input(data: str):
    lines = [line for line in data.splitlines(keepends=False)]
    height, width = len(lines), len(lines[0])
    grid = np.zeros((height, width), dtype=np.int8)
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            grid[r, c] = int(char)
    return grid


def iter_neighbors(grid, r, c):
    max_r, max_c = grid.shape
    for dr, dc in ((-1, 0), (+1, 0), (0, -1), (0, +1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < max_r and 0 <= nc < max_c:
            yield nr, nc


def get_lowpoints(grid):
    max_r, max_c = grid.shape
    lowpoints = set()
    for r, c in product(range(max_r), range(max_c)):
        lowpoint = True
        for nr, nc in iter_neighbors(grid, r, c):
            if grid[nr, nc] <= grid[r, c]:
                lowpoint = False
                break
        if lowpoint:
            lowpoints.add((r, c))
    return lowpoints


class Solution(aoc.Puzzle):
    day = 9
    year = 2021

    def solution_1(self, data: str):
        grid = parse_input(data)
        lowpoints = get_lowpoints(grid)
        # Return the sum of the lowpoint risk values
        result = sum(grid[r, c] + 1 for r, c in lowpoints)
        return result

    def solution_2(self, data: str):
        grid = parse_input(data)
        lowpoints = get_lowpoints(grid)
        # Find basin sizes
        basin_sizes = list()
        for lowpoint in lowpoints:
            queue = [lowpoint]
            basin = set()
            while queue:
                pos = queue.pop(0)
                for nr, nc in iter_neighbors(grid, *pos):
                    nb = nr, nc
                    if grid[nb] != 9 and grid[nb] > grid[pos] and nb not in basin:
                        basin.add((nr, nc))
                        queue.append(nb)
            basin_sizes.append(len(basin) + 1)
        # Return the product of the 3 largest basins
        basin_sizes.sort(reverse=True)
        result = np.prod(basin_sizes[:3])
        return result


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
