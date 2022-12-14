# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import os
import numpy as np
import aoc

DIRECTIONS = {
    "R": np.array([+1, 0]),
    "L": np.array([-1, 0]),
    "U": np.array([0, +1]),
    "D": np.array([0, -1]),
}


class Solution(aoc.Puzzle):

    test_input_idx = 3
    test_answer_idx_2 = -7

    def __init__(self):
        super().__init__(2022, 9, root=os.path.dirname(__file__))

    @staticmethod
    def solution(data, num_knots):
        positions = np.zeros((num_knots, 2), int)
        visited = set()
        visited.add(tuple(positions[-1]))
        for line in data.splitlines(keepends=False):
            direction, qty = line.strip().split(" ")
            move = DIRECTIONS[direction]
            for _ in range(int(qty)):
                positions[0] += move
                for i in range(1, num_knots):
                    diff = positions[i - 1] - positions[i]
                    dist = np.sqrt(np.sum(diff**2))
                    if abs(dist) >= 2:
                        positions[i] += np.sign(diff)
                visited.add(tuple(positions[-1]))

        return len(visited)

    def solution_1(self, data: str) -> int:
        return self.solution(data, num_knots=2)

    def solution_2(self, data: str) -> int:
        return self.solution(data, num_knots=10)


def main():
    puzzle = Solution()
    puzzle.run(test_only=False, text=False)


if __name__ == "__main__":
    main()
