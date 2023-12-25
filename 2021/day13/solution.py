# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2021-12-13

import aoc


def parse_input(data: str):
    lines = data.splitlines(keepends=False)
    points = set()
    while lines[0]:
        line = lines.pop(0)
        x, y = line.split(",")
        points.add((int(x), int(y)))
    lines.pop(0)
    folds = list()
    while lines:
        line = lines.pop(0).replace("fold along ", "")
        axis, val = line.split("=")
        axis = 0 if axis == "x" else 1
        folds.append((axis, int(val)))
    return points, folds


def fold_points(points, axis, val):
    new_points = set()
    for p in points:
        p = list(p)
        if p[axis] >= val:
            p[axis] = val - (p[axis] - val)
        new_points.add(tuple(p))
    return new_points


def visualize(points):
    max_x = max(points, key=lambda p: p[0])[0]
    max_y = max(points, key=lambda p: p[1])[1]
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in points:
                print("#", end="")
            else:
                print(".", end="")
        print()


class Solution(aoc.Puzzle):
    day = 13
    year = 2021
    test_input_idx_1 = 1
    test_input_idx_2 = None

    def solution_1(self, data: str):
        points, folds = parse_input(data)
        axis, val = folds[0]
        points = fold_points(points, axis, val)
        n_points = len(points)
        return n_points

    def solution_2(self, data: str):
        points, folds = parse_input(data)
        for axis, val in folds:
            points = fold_points(points, axis, val)
        visualize(points)
        return "EBLUBRFH"


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
