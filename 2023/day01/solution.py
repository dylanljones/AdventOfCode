# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-01

import aoc

NUMBERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


class Solution(aoc.Puzzle):
    def __init__(self):
        super().__init__(2023, 1)

    def solution_1(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        cal_sum = 0
        for line in lines:
            digits = [c for c in line if c.isdigit()]
            cal_sum += int(digits[0] + digits[-1])
        return cal_sum

    def solution_2(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        cal_sum = 0
        for line in lines:
            digits = []
            for i, c in enumerate(line):
                if c.isdigit():
                    digits.append(str(c))
                for d, word in enumerate(NUMBERS):
                    if line[i:].startswith(word):
                        digits.append(str(d + 1))
            cal_sum += int(digits[0] + digits[-1])
        return cal_sum


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
