# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2021-12-10

import aoc

OPENING = list("([{<")
CLOSING = list(")]}>")
POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def check_syntax(line: str):
    illegal_chars = {")": 0, "]": 0, "}": 0, ">": 0}
    stack = list()
    flag = True
    for char in line:
        if char in OPENING:
            stack.append(char)
        elif char in CLOSING:
            if stack.pop() != OPENING[CLOSING.index(char)]:
                illegal_chars[char] += 1
                flag = False
                break

    return illegal_chars, flag, stack


class Solution(aoc.Puzzle):
    day = 10
    year = 2021
    test_input_idx_1 = -1

    def solution_1(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        result = 0
        for line in lines:
            illegal, flag, stack = check_syntax(line)
            for char, count in illegal.items():
                result += count * POINTS[char]
        return result

    def solution_2(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        total_points = list()
        for line in lines:
            illegal, flag, stack = check_syntax(line)
            if flag:
                total = 0
                while len(stack):
                    t = stack.pop()
                    c = CLOSING[OPENING.index(t)]
                    total *= 5
                    total += CLOSING.index(c) + 1
                total_points.append(total)
        total_points.sort()
        return total_points[len(total_points) // 2]


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
