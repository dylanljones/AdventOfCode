# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

from aoc import Puzzle


class Solution(Puzzle):
    year = 2022
    day = 2

    @staticmethod
    def compute_points(num_op, num_my):
        diff = num_op - num_my
        points = num_my
        if diff == 0:
            # Draw: 3 points
            points += 3
        elif diff in [+2, -1]:
            # Loss: 0 points
            points += 6
        return points

    def solution_1(self, data: str) -> int:
        lines = data.splitlines(keepends=False)
        points = 0
        for line in lines:
            op_move, my_move = line.split()
            num_op = ord(op_move) - 64  # 1: Rock, 2: Paper, 3: Scissors
            num_my = ord(my_move) - 87  # 1: Rock, 2: Paper, 3: Scissors
            points += self.compute_points(num_op, num_my)
        return points

    def solution_2(self, data: str) -> int:
        lines = data.splitlines(keepends=False)
        points = 0
        for line in lines:
            op_move, outcome = line.split()
            num_op = ord(op_move) - 64  # 1: Rock, 2: Paper, 3: Scissors
            num_out = ord(outcome) - 87  # 1: Loss, 2: Draw, 3: Win
            if num_out == 1:
                # Loss: Choose loosing move
                num_my = (num_op - 1) if num_op > 1 else 3
            elif num_out == 2:
                # Draw: Choose the same as oponent
                num_my = num_op
            else:
                # Win: choose winning move
                num_my = (num_op + 1) if num_op < 3 else 1
            points += self.compute_points(num_op, num_my)
        return points


def main():
    puzzle = Solution()
    puzzle.run()


if __name__ == "__main__":
    main()
