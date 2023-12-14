# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-14

import numpy as np

import aoc


def parse_input(data: str):
    chars = {".": 0, "O": 1, "#": 2}
    return np.array([[chars[x] for x in line] for line in data.splitlines()])


def tilt_up(arr):
    for row in range(1, arr.shape[0]):
        cols = np.where(np.logical_and(arr[row, :] == 1, arr[row - 1, :] == 0))[0]
        for col in cols:
            r = row
            while r > 0 and arr[r - 1, col] == 0:
                r -= 1
            arr[r, col] = 1
            arr[row, col] = 0


def tilt_cycle(arr):
    for _ in range(4):
        # Tilt platform up
        tilt_up(arr)
        # Rotate platform clockwise
        arr[:] = np.rot90(arr, k=-1)


def calc_score(arr):
    return sum(np.sum(arr[r, :] == 1) * (arr.shape[0] - r) for r in range(arr.shape[0]))


class Solution(aoc.Puzzle):
    day = 14
    year = 2023
    test_solution_idx_2 = -2

    def solution_1(self, data: str):
        arr = parse_input(data)
        tilt_up(arr)
        return calc_score(arr)

    def solution_2(self, data: str):
        arr = parse_input(data)

        cycles = 1000000000
        states = dict()
        start, size = 0, 0
        for i in range(cycles):
            tilt_cycle(arr)
            # Extract positions of round rocks
            state = tuple(tuple(pos) for pos in np.argwhere(arr == 1))
            # Look for a state that has already been seen
            if state in states:
                start, size = states[state], i - states[state]
                break
            else:
                states[state] = i

        # Complete the remaining cycles
        cycles_left = (cycles - (start + 1)) % size
        for i in range(cycles_left):
            tilt_cycle(arr)

        return calc_score(arr)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
