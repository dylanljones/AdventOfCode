# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-01

import aoc


class Solution(aoc.Puzzle):
    _file = __file__

    def __init__(self):
        super().__init__(2023, 3)

    def solution_1(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        num_start = set()
        for r, row in enumerate(lines):
            for c, char in enumerate(row):
                if char.isdigit() or char == ".":
                    continue
                # positions of symbols, look for numbers in the vicinity
                for dr in range(r - 1, r + 2):
                    for dc in range(c - 1, c + 2):
                        if 0 <= dr < len(lines) and 0 <= dc < len(lines[dr]):
                            if not lines[dr][dc].isdigit():
                                continue
                            while dc > 0 and lines[dr][dc - 1].isdigit():
                                dc -= 1
                            num_start.add((dr, dc))
        result = 0
        for r, c in num_start:
            s = ""
            while c < len(lines[r]) and lines[r][c].isdigit():
                s += lines[r][c]
                c += 1
            result += int(s)
        return result

    def solution_2(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        result = 0
        for r, row in enumerate(lines):
            for c, char in enumerate(row):
                if char != "*":
                    continue
                num_start = set()
                # positions of symbols, look for numbers in the vicinity
                for dr in range(r - 1, r + 2):
                    for dc in range(c - 1, c + 2):
                        if 0 <= dr < len(lines) and 0 <= dc < len(lines[dr]):
                            if not lines[dr][dc].isdigit():
                                continue
                            while dc > 0 and lines[dr][dc - 1].isdigit():
                                dc -= 1
                            num_start.add((dr, dc))
                if len(num_start) != 2:
                    continue

                numbers = list()
                for nr, nc in num_start:
                    s = ""
                    while nc < len(lines[nr]) and lines[nr][nc].isdigit():
                        s += lines[nr][nc]
                        nc += 1
                    numbers.append(int(s))
                result += numbers[0] * numbers[1]
        return result


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
