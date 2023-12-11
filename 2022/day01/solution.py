# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

from aoc.puzzle import Puzzle


class Solution(Puzzle):
    year = 2022
    day = 1

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
