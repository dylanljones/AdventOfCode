# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import os
from collections import deque

import numpy as np

import aoc


def parse_map(data):
    start, end = None, None
    height_map = list()
    for r, line in enumerate(data.splitlines(keepends=False)):
        row = list()
        for c, char in enumerate(line):
            if char == "S":
                start = (r, c)
                height = ord("a") - 97
            elif char == "E":
                end = (r, c)
                height = ord("z") - 97
            else:
                height = ord(char) - 97
            row.append(height)
        height_map.append(row)
    return np.array(height_map), tuple(start), tuple(end)


def get_neighbors(hmap, pos):
    for dx, dy in [(+1, 0), (-1, 0), (0, +1), (0, -1)]:
        pos1 = [pos[0] + dx, pos[1] + dy]
        if 0 <= pos1[0] < hmap.shape[0] and 0 <= pos1[1] < hmap.shape[1]:
            yield tuple(pos1)


class Solution(aoc.Puzzle):
    test_answer_idx_2 = -2

    def __init__(self):
        super().__init__(2022, 12, root=os.path.dirname(__file__))

    def solution_1(self, data: str):
        hmap, start, end = parse_map(data)
        visited = np.zeros_like(hmap).astype(bool)
        heap = deque()
        heap.append((0, start))
        total_steps = 0
        while heap:
            steps, pos = heap.popleft()

            if visited[*pos] == 1:
                continue
            visited[*pos] = 1
            if pos == end:
                total_steps = steps
                break

            for neighbor in get_neighbors(hmap, pos):
                hdiff = hmap[*neighbor] - hmap[*pos]
                if hdiff <= 1:
                    heap.append((steps + 1, neighbor))

        return total_steps

    def solution_2(self, data: str):
        hmap, start, end = parse_map(data)
        visited = np.zeros_like(hmap).astype(bool)
        heap = deque()
        heap.append((0, end))
        total_steps = 0
        while heap:
            steps, pos = heap.popleft()

            if visited[*pos] == 1:
                continue
            visited[*pos] = 1
            if hmap[*pos] == 0:
                total_steps = steps
                break

            for neighbor in get_neighbors(hmap, pos):
                hdiff = hmap[*neighbor] - hmap[*pos]
                if hdiff >= -1:
                    heap.append((steps + 1, neighbor))

        return total_steps


def main():
    puzzle = Solution()
    puzzle.run(test_only=False, text=False)


if __name__ == "__main__":
    main()
