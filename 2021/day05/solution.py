# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-25

import collections

import aoc


def parse_input(data: str):
    for s in data.splitlines(keepends=False):
        p1, p2 = s.split(" -> ")
        x1, y1 = map(int, p1.split(","))
        x2, y2 = map(int, p2.split(","))
        yield x1, y1, x2, y2


class Solution(aoc.Puzzle):
    year = 2021
    day = 5
    test_input_idx_2 = None

    def solution_1(self, data: str):
        points = collections.Counter()
        for x1, y1, x2, y2 in parse_input(data):
            y1, y2 = min(y1, y2), max(y1, y2)
            x1, x2 = min(x1, x2), max(x1, x2)
            if x1 == x2:
                for y in range(y1, y2 + 1):
                    points[(x1, y)] += 1
            elif y1 == y2:
                for x in range(x1, x2 + 1):
                    points[x, y1] += 1
        return sum(v > 1 for v in points.values())

    def solution_2(self, data: str):
        points = collections.Counter()
        for x1, y1, x2, y2 in parse_input(data):
            dx, dy = 0, 0
            if x2 > x1:
                dx = 1
            elif x2 < x1:
                dx = -1
            if y2 > y1:
                dy = 1
            elif y2 < y1:
                dy = -1
            x, y = x1, y1
            while (x, y) != (x2, y2):
                points[x, y] += 1
                x, y = x + dx, y + dy
            points[x2, y2] += 1
        return sum(v > 1 for v in points.values())


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
