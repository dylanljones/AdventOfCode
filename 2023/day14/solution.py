# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-14

import numpy as np

import aoc

EMPTY = 0
ROUND = 1
SQUARE = 2


def parse_input(data: str):
    chars = {".": EMPTY, "O": ROUND, "#": SQUARE}
    return np.array([[chars[x] for x in line] for line in data.splitlines()])


def tilt_up(arr):
    for row in range(1, arr.shape[0]):
        candiddates = np.logical_and(arr[row, :] == ROUND, arr[row - 1, :] == EMPTY)
        cols = np.where(candiddates)[0]
        for col in cols:
            r = row
            while r > 0 and arr[r - 1, col] == EMPTY:
                r -= 1
            arr[r, col] = ROUND
            arr[row, col] = EMPTY


def tilt_cycle(arr):
    for _ in range(4):
        # Tilt platform up
        tilt_up(arr)
        # Rotate platform clockwise
        arr[:] = np.rot90(arr, k=-1)


def calc_score(a):
    return sum(np.sum(a[r, :] == ROUND) * (a.shape[0] - r) for r in range(a.shape[0]))


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
            state = tuple(tuple(pos) for pos in np.argwhere(arr == ROUND))
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
