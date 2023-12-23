# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-22

import itertools
from collections import defaultdict

import aoc

Brick = list[tuple[int]]
Grid = dict[tuple[int, ...], int]


def parse_input(data: str) -> list[Brick]:
    # Parse start and end points
    points = list()
    for i, line in enumerate(data.splitlines(keepends=False)):
        a, b = line.split("~")
        points.append((tuple(map(int, a.split(","))), tuple(map(int, b.split(",")))))
    # Sort points by z-coordinate
    points = sorted(points, key=lambda b: min(b[0][-1], b[1][-1]))
    # Create bricks coordinates
    bricks = list()
    for a, b in points:
        xx = range(min(a[0], b[0]), max(a[0], b[0]) + 1)
        yy = range(min(a[1], b[1]), max(a[1], b[1]) + 1)
        zz = range(min(a[2], b[2]), max(a[2], b[2]) + 1)
        bricks.append(list(itertools.product(xx, yy, zz)))
    return bricks


def settle_bricks(bricks: list[Brick]) -> Grid:
    # Create grid of bricks with position as key and brick id as value
    grid = defaultdict(int)
    for i, coords in enumerate(bricks, start=1):
        for p in coords:
            grid[p] = i
    # Settle each brick starting from the lowest
    for i, coords in enumerate(bricks, start=1):
        # Check if brick can fall
        while all(grid[x, y, z - 1] in (0, i) and z > 1 for x, y, z in coords):
            # Remove old points from grid
            for p in coords:
                grid[p] = 0
            # Update positions of brick
            for j, p in enumerate(coords):
                coords[j] = (p[0], p[1], p[2] - 1)
            # Add new points to grid
            for p in coords:
                grid[p] = i
    return grid


def get_supports(bricks: list[Brick], grid: Grid) -> tuple[dict, dict]:
    supported, supports = defaultdict(set), defaultdict(set)
    for i, coords in enumerate(bricks, start=1):
        supports[i] = set()
        for x, y, z in coords:
            i_above = grid[(x, y, z + 1)]
            if i_above not in (0, i):
                supported[i_above].add(i)
                supports[i].add(i_above)
    return supported, supports


class Solution(aoc.Puzzle):
    day = 22
    year = 2023

    def solution_1(self, data: str):
        bricks = parse_input(data)
        grid = settle_bricks(bricks)
        supported, supports = get_supports(bricks, grid)
        result = 0
        for i, tops in supports.items():
            if all(supported[j] - {i} for j in tops):
                result += 1
        return result

    def solution_2(self, data: str):
        bricks = parse_input(data)
        grid = settle_bricks(bricks)
        supported, supports = get_supports(bricks, grid)

        result = 0
        for idx in range(1, len(bricks) + 1):
            queue = [idx]
            fallen = set()
            while queue:
                i = queue.pop(0)
                if i in fallen:
                    continue
                fallen.add(i)
                # For each brick on top of i, check if it would fall
                for j in supports[i]:
                    if j in fallen:
                        # Brick j has already fallen
                        continue
                    if supported[j] and not supported[j] - fallen:
                        # Brick j would fall
                        queue.append(j)
            n_fallen = len(fallen - {idx})
            result += n_fallen

        return result


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(puzzle_only=False)
