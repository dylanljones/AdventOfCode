# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2021-12-11

import numpy as np

import aoc


def parse_input(data):
    return np.array([list(map(int, line)) for line in data.splitlines(keepends=False)])


def neighbors(grid, r, c):
    max_r, max_c = grid.shape
    deltas = (-1, 0), (+1, 0), (0, -1), (0, +1), (1, 1), (-1, -1), (-1, 1), (+1, -1)
    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        if 0 <= nr < max_r and 0 <= nc < max_c:
            yield nr, nc


def step(grid):
    grid += 1

    flashes = set((r, c) for r, c in np.array(np.where(grid > 9)).T)
    new_flashes = flashes
    while new_flashes:
        next_flashes = set()
        for r, c in new_flashes.copy():
            for nr, nc in neighbors(grid, r, c):
                p = (nr, nc)
                grid[p] += 1
                if grid[p] > 9 and (p not in flashes):
                    next_flashes.add(p)
        flashes |= next_flashes
        new_flashes = next_flashes

    for r, c in flashes:
        grid[r, c] = 0
    return len(flashes)


class Solution(aoc.Puzzle):
    day = 11
    year = 2021
    test_input_idx_2 = None
    test_solution_idx_2 = -2

    def solution_1(self, data: str):
        grid = parse_input(data)
        return sum(step(grid) for _ in range(100))

    def solution_2(self, data: str):
        grid = parse_input(data)
        total = grid.size
        i = 0
        while True:
            i += 1
            n = step(grid)
            if n == total:
                break
        return i


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
