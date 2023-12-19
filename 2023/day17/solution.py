# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-17


import heapq

import numpy as np

import aoc


def parse_input(data: str):
    return np.array([[int(x) for x in line] for line in data.splitlines()])


def find_path_cost(grid, minval=1, maxval=3):
    """Dijkstra algorithm"""
    shape = grid.shape
    start = (0, 0)
    end = grid.shape[0] - 1, grid.shape[1] - 1

    queue = list()
    heapq.heappush(queue, (0, start, 0))
    heapq.heappush(queue, (0, start, 1))
    seen = set()
    cost = 0
    while queue:
        cost, pos, direction = heapq.heappop(queue)
        if pos == end:
            break
        if (pos, direction) in seen:
            continue
        seen.add((pos, direction))
        for s in [-1, 1]:
            new_cost = cost
            for i in range(1, maxval + 1):
                if direction == 1:
                    new_pos = pos[0], pos[1] + i * s
                else:
                    new_pos = pos[0] + i * s, pos[1]
                if not (0 <= new_pos[0] < shape[0] and 0 <= new_pos[1] < shape[1]):
                    break
                new_cost += grid[new_pos]
                if (new_pos, 1 - direction) in seen:
                    continue
                if i >= minval:
                    heapq.heappush(queue, (new_cost, new_pos, 1 - direction))

    return cost


class Solution(aoc.Puzzle):
    day = 17
    year = 2023
    test_solution_idx_2 = -4

    def solution_1(self, data: str):
        grid = parse_input(data)
        return find_path_cost(grid, minval=1, maxval=3)

    def solution_2(self, data: str):
        grid = parse_input(data)
        return find_path_cost(grid, minval=4, maxval=10)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
