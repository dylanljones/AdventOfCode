# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-11

from itertools import combinations

import aoc


def parse_input(data: str):
    lines = data.splitlines(keepends=False)
    galaxies = list()
    size = len(lines), len(lines[0])
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == "#":
                galaxies.append([r, c])
    return list(size), list(galaxies)


def expand_axis(size, galaxies, expand_to, axis):
    i = 0
    n_insert = expand_to - 1
    while i < size[axis]:
        if not any(g[axis] == i for g in galaxies):
            # No galaxy in row
            size[axis] += n_insert
            for g in galaxies:
                if g[axis] > i:
                    g[axis] += n_insert
            i += n_insert
        i += 1
    return size, galaxies


def expand(size, galaxies, expand_to=2):
    size, galaxies = expand_axis(size, galaxies, expand_to, axis=0)
    size, galaxies = expand_axis(size, galaxies, expand_to, axis=1)
    return size, galaxies


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Solution(aoc.Puzzle):
    day = 11
    year = 2023
    test_input_idx_2 = None
    test_solution_idx_2 = None

    def solution_1(self, data: str):
        size, galaxies = parse_input(data)
        size, galaxies = expand(size, galaxies, expand_to=2)
        dist_sum = sum(manhattan(g1, g2) for g1, g2 in combinations(galaxies, r=2))
        return dist_sum

    def solution_2(self, data: str):
        size, galaxies = parse_input(data)
        size, galaxies = expand(size, galaxies, expand_to=1_000_000)
        dist_sum = sum(manhattan(g1, g2) for g1, g2 in combinations(galaxies, r=2))
        return dist_sum


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
