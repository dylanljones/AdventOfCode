# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-06

import math

import aoc


def solve_roots_int(t, d):
    sqrt = math.sqrt(t * t / 4 - d)
    s1, s2 = round(t / 2 - sqrt), round(t / 2 + sqrt)
    # Fix lower and upper bounds due to rounding errors
    while s1 * (t - s1) <= d:
        s1 += 1
    while s2 * (t - s2) <= d:
        s2 -= 1
    return s1, s2


class Solution(aoc.Puzzle):
    _file = __file__
    day = 6
    year = 2023
    test_answer_idx_1 = -4

    def solution_1(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        times = [int(x) for x in lines[0].replace("Time: ", "").split()]
        dists = [int(x) for x in lines[1].replace("Distance: ", "").split()]
        wins = 1
        for t, d in zip(times, dists):
            s1, s2 = solve_roots_int(t, d)
            n_win = s2 - s1 + 1
            wins *= n_win
        return wins

    def solution_2(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        t = int(lines[0].replace("Time: ", "").replace(" ", ""))
        d = int(lines[1].replace("Distance: ", "").replace(" ", ""))
        s1, s2 = solve_roots_int(t, d)
        n_win = s2 - s1 + 1
        return n_win


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
