# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-25

import aoc


class Solution(aoc.Puzzle):
    year = 2021
    day = 2

    def solution_1(self, data: str):
        lines = data.splitlines(keepends=False)
        pos = [0, 0]
        for line in lines:
            direction, value = line.split()
            value = int(value)
            if direction == "forward":
                pos[0] += value
            elif direction == "backward":
                pos[0] -= value
            elif direction == "up":
                pos[1] -= value
            elif direction == "down":
                pos[1] += value
        return pos[0] * pos[1]

    def solution_2(self, data: str):
        lines = data.splitlines(keepends=False)
        aim = 0
        pos = [0, 0]
        for line in lines:
            direction, value = line.split()
            value = int(value)
            if direction == "forward":
                pos[0] += value
                pos[1] += value * aim
            elif direction == "backward":
                pos[0] -= value
                pos[1] -= value * aim
            elif direction == "up":
                aim -= value
            elif direction == "down":
                aim += value
        return pos[0] * pos[1]


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run()
