# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-18

import numpy as np

import aoc

DIRS = {
    "R": (+1, 0),
    "L": (-1, 0),
    "U": (0, +1),
    "D": (0, -1),
}
ORDER = "RDLU"


def find_vertices(data, use_color=False):
    pos = np.array([0, 0])
    vertices = [pos.copy()]
    for dir_, steps, color in map(str.split, data.splitlines(keepends=False)):
        if use_color:
            steps, dir_ = int(color[2:-2], 16), ORDER[int(color[-2])]
        else:
            steps = int(steps)
        pos += np.array(DIRS[dir_]) * steps
        vertices.append(pos.copy())

    return np.array(vertices)


def shoelace(vertices):
    xs, ys = vertices.T
    n = ((xs * (np.roll(ys, 1) - np.roll(ys, -1))).sum()) / 2
    n += sum(abs(np.diff(ys)) + abs(np.diff(xs))) / 2
    return int(n) + 1


class Solution(aoc.Puzzle):
    day = 18
    year = 2023

    def solution_1(self, data: str):
        verts = find_vertices(data)
        n = shoelace(verts)
        return n

    def solution_2(self, data: str):
        verts = find_vertices(data, use_color=True)
        print(verts)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(puzzle_only=False)
