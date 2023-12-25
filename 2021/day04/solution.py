# coding: utf-8
#
# This code is part of aoc2022.
#
# Copyright (c) 2022, Dylan Jones

import numpy as np

import aoc


def parse_input(data):
    lines = data.splitlines(keepends=False)
    numbers = [int(x) for x in lines.pop(0).split(",")]
    lines.pop(0)

    arrays = list()
    while len(lines):
        line = lines.pop(0).strip()
        if not line:
            break

        arr = list()
        while line and len(lines):
            arr.append([int(x) for x in line.split()])
            line = lines.pop(0).strip()
        if line:
            arr.append([int(x) for x in line.split()])
        arrays.append(arr)

    return numbers, np.array(arrays)


def check_board(mask):
    for r in range(mask.shape[0]):
        if np.array_equal(np.unique(mask[r, :]), [1]):
            return True
    for c in range(mask.shape[1]):
        if np.array_equal(np.unique(mask[:, c]), [1]):
            return True
    return False


def get_winner(boards):
    for i, board in enumerate(boards):
        if check_board(board):
            return i
    return None


class Solution(aoc.Puzzle):
    year = 2021
    day = 4

    def solution_1(self, data: str):
        numbers, arrays = parse_input(data)
        masks = np.zeros_like(arrays).astype(bool)

        draw = 0
        winner = None
        mask = None
        for num in numbers:
            masks[arrays == num] = 1
            idx = get_winner(masks)
            if idx is not None:
                draw = num
                winner = arrays[idx]
                mask = masks[idx]
                break
        return np.sum(winner[~mask]) * draw

    def solution_2(self, data: str):
        numbers, arrays = parse_input(data)
        active = list(numbers)
        masks = np.zeros_like(arrays).astype(bool)
        winners = list()

        for num in numbers:
            for i, board in enumerate(arrays):
                if i in active:
                    masks[i, arrays[i] == num] = 1
                    if check_board(masks[i]):
                        winners.append((i, num))
                        active.remove(i)

        idx, draw = winners[-1]
        mask = masks[idx].astype(bool)
        winner = arrays[idx]
        return np.sum(winner[~mask]) * draw


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
