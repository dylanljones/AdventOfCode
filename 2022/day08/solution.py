# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import os
import itertools
import numpy as np
import aoc


class Solution(aoc.Puzzle):

    test_input_idx = 0
    test_answer_idx_1 = -1
    test_answer_idx_2 = -2

    def __init__(self):
        super().__init__(2022, 8, root=os.path.dirname(__file__))

    def solution_1(self, data: str) -> int:
        trees = np.array([[int(x) for x in list(line)] for line in data.splitlines()])

        visible = np.zeros_like(trees, dtype=bool)
        visible[0, :] = 1
        visible[-1, :] = 1
        visible[:, 0] = 1
        visible[:, -1] = 1
        for i in range(1, trees.shape[0] - 1):
            # Visible from left
            max_size = trees[i, 0]
            for j in range(0, trees.shape[1] - 1):
                if trees[i, j + 1] > max_size:
                    visible[i, j + 1] = 1
                    max_size = trees[i, j + 1]
            # Visible from right
            max_size = trees[i, -1]
            for j in reversed(range(1, trees.shape[1])):
                if trees[i, j - 1] > max_size:
                    visible[i, j - 1] = 1
                    max_size = trees[i, j - 1]

        for j in range(1, trees.shape[1] - 1):
            # Visible from top
            max_size = trees[0, j]
            for i in range(0, trees.shape[0] - 1):
                if trees[i + 1, j] > max_size:
                    visible[i + 1, j] = 1
                    max_size = trees[i + 1, j]
            # Visible from bottom
            max_size = trees[-1, j]
            for i in reversed(range(1, trees.shape[0])):
                if trees[i - 1, j] > max_size:
                    visible[i - 1, j] = 1
                    max_size = trees[i - 1, j]

        return np.count_nonzero(visible)

    def solution_2(self, data: str) -> int:
        trees = np.array([[int(x) for x in list(line)] for line in data.splitlines()])
        n, m = trees.shape
        scores = np.zeros_like(trees)
        for row, col in itertools.product(range(1, n - 1), range(1, m - 1)):
            height = trees[row, col]
            counts = np.zeros(4, int)
            # right
            for j in range(col + 1, trees.shape[0]):
                counts[0] += 1
                if trees[row, j] >= height:
                    break
            # left
            for j in reversed(range(0, col)):
                counts[1] += 1
                if trees[row, j] >= height:
                    break
            # down
            for i in range(row + 1, trees.shape[1]):
                counts[2] += 1
                if trees[i, col] >= height:
                    break
            # up
            for i in reversed(range(0, row)):
                counts[3] += 1
                if trees[i, col] >= height:
                    break

            scores[row, col] = np.prod(counts)

        return np.max(scores)


def main():
    puzzle = Solution()
    puzzle.run()


if __name__ == "__main__":
    main()
