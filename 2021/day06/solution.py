# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-25

import collections

import aoc


def simulate(data: str, num_days: int) -> int:
    state = collections.Counter(list(map(int, data.split(","))))
    for day in range(num_days):
        new_state = collections.Counter({6: state[0], 8: state[0]})
        new_state.update({k - 1: v for k, v in state.items() if k > 0})
        state = new_state
    return sum(state.values())


class Solution(aoc.Puzzle):
    year = 2021
    day = 6

    def solution_1(self, data: str):
        return simulate(data, num_days=80)

    def solution_2(self, data: str):
        return simulate(data, num_days=256)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run()
