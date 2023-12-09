# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-09

import aoc


def compute_diffs(numbers):
    sequence = list()
    diff = numbers
    while not all(x == 0 for x in diff):
        sequence.append(diff)
        diff = [diff[i + 1] - diff[i] for i in range(len(diff) - 1)]
    sequence.append(diff)
    return sequence


class Solution(aoc.Puzzle):
    day = 9
    year = 2023
    test_input_idx_2 = None

    def solution_1(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        result = 0
        for line in lines:
            numbers = [int(num) for num in line.split(" ")]
            sequence = compute_diffs(numbers)
            sequence[-1].append(0)
            for i in range(len(sequence) - 1, 0, -1):
                sequence[i - 1].append(sequence[i][-1] + sequence[i - 1][-1])
            extrapolated = sequence[0][-1]
            result += extrapolated

        return result

    def solution_2(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        result = 0
        for line in lines:
            numbers = [int(num) for num in line.split(" ")]
            sequence = compute_diffs(numbers)
            sequence[-1].insert(0, 0)
            for i in range(len(sequence) - 1, 0, -1):
                sequence[i - 1].insert(0, sequence[i - 1][0] - sequence[i][0])
            extrapolated = sequence[0][0]
            result += extrapolated

        return result


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
