# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import aoc


class Solution(aoc.Puzzle):
    test_solution_idx_1 = -9
    test_solution_idx_2 = -9

    def __init__(self):
        super().__init__(2022, 6)

    @staticmethod
    def get_unique_section(data: str, n: int):
        chars = list(data)
        i = 0
        for i in range(0, len(chars)):
            chunk = chars[i : i + n]
            if len(set(chunk)) == len(chunk):
                break
        idx = i + n
        return idx

    def solution_1(self, data: str) -> int:
        return self.get_unique_section(data, 4)

    def solution_2(self, data: str) -> int:
        return self.get_unique_section(data, 14)


def main():
    puzzle = Solution()
    puzzle.run()


if __name__ == "__main__":
    main()
