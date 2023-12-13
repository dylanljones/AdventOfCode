# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-13

import numpy as np

import aoc


def parse_input(data: str):
    for part in data.strip().split("\n\n"):
        yield np.array([[int(x == "#") for x in line] for line in part.splitlines()])


def reflection_score(pattern, smudge=0):
    # Flip rows
    for i in range(1, pattern.shape[0]):
        j = min(i, pattern.shape[0] - i)
        diffs = np.sum(np.flip(pattern[i - j : i, :], axis=0) ^ pattern[i : i + j, :])
        if diffs == smudge:
            return i * 100
    # Flip columns
    for i in range(1, pattern.shape[1]):
        j = min(i, pattern.shape[1] - i)
        diffs = np.sum(np.flip(pattern[:, i - j : i], axis=1) ^ pattern[:, i : i + j])
        if diffs == smudge:
            return i
    return 0


class Solution(aoc.Puzzle):
    day = 13
    year = 2023

    def solution_1(self, data: str):
        return sum(reflection_score(arr) for arr in parse_input(data))

    def solution_2(self, data: str):
        return sum(reflection_score(arr, smudge=1) for arr in parse_input(data))


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
