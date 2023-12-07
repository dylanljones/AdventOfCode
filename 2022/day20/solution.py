# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2022-12-20

from itertools import cycle

import aoc


def mix(numbers, rounds=1):
    mixed = list(enumerate(numbers))
    cyc = cycle(mixed.copy())
    n = len(numbers)
    nm = n - 1
    for _ in range(rounds * len(numbers)):
        curr = next(cyc)
        idx_old = mixed.index(curr)
        idx_new = (idx_old + curr[1] + nm) % nm
        mixed.remove(curr)
        mixed.insert(idx_new, curr)
    return mixed


class Solution(aoc.Puzzle):
    day = 20
    year = 2022
    test_input_idx_2 = None

    def solution_1(self, data: str):
        numbers = [int(line.strip()) for line in data.splitlines(keepends=False)]
        zero = (numbers.index(0), 0)
        mixed = mix(numbers)
        i0 = mixed.index(zero)
        res = sum([mixed[(i0 + i) % len(numbers)][1] for i in [1000, 2000, 3000]])
        return res

    def solution_2(self, data: str):
        key = 811589153
        numbers = [int(line.strip()) * key for line in data.splitlines(keepends=False)]
        zero = (numbers.index(0), 0)
        mixed = mix(numbers, rounds=10)
        i0 = mixed.index(zero)
        res = sum([mixed[(i0 + i) % len(numbers)][1] for i in [1000, 2000, 3000]])
        return res


def new_index(sequence, idx, delta):
    n = len(sequence)
    new_idx = (idx + delta) % (n - 1)
    return new_idx


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
