# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-25

import heapq
from collections import defaultdict

import numpy as np

import aoc

DIRECTIONS = (-1, 0), (+1, 0), (0, -1), (0, +1)


def parse_input(data: str) -> np.ndarray:
    return np.array([list(map(int, line)) for line in data.splitlines()])


def get_neighbors(shape, pos):
    for dr, dc in DIRECTIONS:
        new_pos = pos[0] + dr, pos[1] + dc
        if 0 <= new_pos[0] < shape[0] and 0 <= new_pos[1] < shape[1]:
            yield new_pos


def find_path_cost(grid: np.ndarray):
    """Dijkstra algorithm"""
    shape = grid.shape
    start = (0, 0)
    end = grid.shape[0] - 1, grid.shape[1] - 1

    cum_risk = defaultdict(lambda: np.inf)
    cum_risk[start] = 0
    queue, visited = list(), set()
    heapq.heappush(queue, (0, start))
    while queue:
        risk, pos = heapq.heappop(queue)
        if pos in visited:
            continue
        for dr, dc in DIRECTIONS:
            new_pos = (
                r,
                c,
            ) = pos[0] + dr, pos[1] + dc
            if 0 <= r < shape[0] and 0 <= c < shape[1] and new_pos not in visited:
                new_risk = min(cum_risk[new_pos], cum_risk[pos] + grid[new_pos])
                cum_risk[new_pos] = new_risk
                heapq.heappush(queue, (new_risk, new_pos))
        visited.add(pos)

    return cum_risk[end]


class Solution(aoc.Puzzle):
    day = 15
    year = 2021

    def solution_1(self, data: str):
        risk_map = parse_input(data)
        return find_path_cost(risk_map)

    def solution_2(self, data: str):
        map_s = parse_input(data)
        n = 5
        tiles = [[(map_s + i + j - 1) % 9 + 1 for j in range(n)] for i in range(n)]
        return find_path_cost(np.block(tiles))


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
