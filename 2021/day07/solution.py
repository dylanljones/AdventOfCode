# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-25

import numpy as np

import aoc


def get_cost(x0: int, positions: list[int]) -> int:
    return sum(abs(x - x0) * (abs(x - x0) + 1) // 2 for x in positions)


class Solution(aoc.Puzzle):
    year = 2021
    day = 7
    test_solution_idx_1 = -7
    test_solution_idx_2 = -3

    def __init__(self):
        super().__init__(2021, 7)
        self.load_info()

    def solution_1(self, data: str):
        positions = list(map(int, data.split(",")))
        align = int(np.median(positions))
        return sum(abs(x - align) for x in positions)

    def solution_2(self, data: str):
        positions = list(map(int, data.split(",")))
        align = int(np.mean(positions))
        cost = get_cost(align, positions)
        direction = -1 if get_cost(align - 1, positions) < cost else +1
        while get_cost(align + direction, positions) < cost:
            align += direction
            cost = get_cost(align, positions)
        return get_cost(align, positions)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
