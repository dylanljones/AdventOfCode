# coding: utf-8
#
# This code is part of aoc2022.
#
# Copyright (c) 2022, Dylan Jones

from aoc import Puzzle


class Solution(Puzzle):
    def __init__(self):
        super().__init__(2022, 1)

    def solution_1(self, data: str) -> int:
        blocks = data.split("\n\n")
        totals = [sum(int(x) for x in block.splitlines()) for block in blocks]
        return max(totals)

    def solution_2(self, data: str) -> int:
        blocks = data.split("\n\n")
        totals = [sum(int(x) for x in block.splitlines()) for block in blocks]
        totals.sort(reverse=True)
        return sum(totals[:3])


def main():
    puzzle = Solution()
    puzzle.run()


if __name__ == "__main__":
    main()
