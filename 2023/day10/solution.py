# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-10

from itertools import chain, pairwise

import aoc

NORTH = (-1, 0)
SOUTH = (+1, 0)
EAST = (0, +1)
WEST = (0, -1)
NEIGHBOR_DIRS = [NORTH, SOUTH, EAST, WEST]

CONNECTIONS = {
    "|": (NORTH, SOUTH),
    "-": (EAST, WEST),
    "L": (NORTH, EAST),
    "J": (NORTH, WEST),
    "7": (SOUTH, WEST),
    "F": (SOUTH, EAST),
    ".": (),
    "S": (),
}


def parse_input(data: str):
    graph = dict()
    start = ()
    sr, sc = 0, 0
    for r, line in enumerate(data.splitlines(keepends=False)):
        for c, char in enumerate(line):
            graph[(r, c)] = [(r + dr, c + dc) for dr, dc in CONNECTIONS[char]]
            if char == "S":
                start = sr, sc = (r, c)
    graph[start] = [
        (sr + dr, sc + dc)
        for dr, dc in NEIGHBOR_DIRS
        if start in graph.get((sr + dr, sc + dc), [])
    ]
    return graph, start


def find_loop(graph, start):
    path = [start]
    next_pos = graph[start][0]
    while next_pos != start:
        path.append(next_pos)
        next_pos = next(pos for pos in graph[next_pos] if pos != path[-2])
    return path


def scale2(positions):
    # Scale everything up by 2
    scaled = {(2 * r, 2 * y) for r, y in positions}
    # Add the missing nodes
    for a, b in pairwise(chain(positions, positions[:-1])):
        scaled.add((a[0] + b[0], a[1] + b[1]))
    return scaled


def outside_tiles(loop):
    max_r, max_c = map(max, zip(*loop))
    outside = (
        set(
            chain(
                ((r, 0) for r in range(max_r + 1)),
                ((r, max_c) for r in range(max_r + 1)),
                ((0, c) for c in range(max_c + 1)),
                ((max_r, c) for c in range(max_c + 1)),
            )
        )
        - loop
    )
    queue = list(outside)
    while queue:
        r, c = queue.pop()
        for dr, dc in NEIGHBOR_DIRS:
            nr, nc = nb = r + dr, c + dc
            if (
                (0 <= nr <= max_r)
                and (0 <= nc <= max_c)
                and nb not in outside
                and nb not in loop
            ):
                outside.add(nb)
                queue.append(nb)
    return outside


class Solution(aoc.Puzzle):
    day = 10
    year = 2023
    test_input_idx_1 = -5
    test_solution_1 = 8
    test_input_idx_2 = -2

    def solution_1(self, data: str):
        graph, start = parse_input(data)
        loop = find_loop(graph, start)
        return len(loop) // 2

    def solution_2(self, data: str):
        graph, start = parse_input(data)
        loop = find_loop(graph, start)
        # Total nodes without loop
        max_r, max_c = map(max, zip(*loop))
        n_total = (max_r + 1) * (max_c + 1) - len(loop)
        # Scale everything up by 2
        scaled = scale2(loop)
        # Find outside tiles
        outside = outside_tiles(scaled)
        # Count unscaled outside tiles
        n_outside = sum(r % 2 + c % 2 == 0 for r, c in outside)
        # Return the number of inside tiles
        n_inside = n_total - n_outside
        return n_inside


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
