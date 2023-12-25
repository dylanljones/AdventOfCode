# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-25


import aoc


def parse_input(data: str) -> list[int]:
    return [int(x) for x in data.strip().splitlines()]


class Solution(aoc.Puzzle):
    year = 2021
    day = 1

    def solution_1(self, data):
        dd = parse_input(data)
        return sum(dd[i + 1] > dd[i] for i in range(len(dd) - 1))

    def solution_2(self, data):
        dd = parse_input(data)
        return sum(sum(dd[i + 1 : i + 4]) > sum(dd[i : i + 3]) for i in range(len(dd)))


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run()
