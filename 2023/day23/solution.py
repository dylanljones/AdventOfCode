# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-23

from collections import defaultdict

import aoc

DIRECTIONS = (-1, 0), (0, 1), (1, 0), (0, -1)
SLOPES = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}


def parse_input(data: str):
    lines = data.splitlines(keepends=False)
    hike_map = dict()
    start, end = None, None
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if r == 0 and char == ".":
                start = r, c
            elif r == len(lines) - 1 and char == ".":
                end = r, c
            if char != "#":
                hike_map[r, c] = char
    return hike_map, start, end


def build_neighbor_dict(hike_map, ignore_slope=False):
    """Builds a dictionary of neighbors for each position in the map"""
    neighbors = dict()
    for pos in hike_map.keys():
        nn = set()
        r, c = pos
        if not ignore_slope and hike_map[pos] != ".":
            # Slope tile
            dr, dc = SLOPES[hike_map[pos]]
            new_pos = r + dr, c + dc
            nn.add(new_pos)
        else:
            # All directions
            for dr, dc in DIRECTIONS:
                new_pos = r + dr, c + dc
                if new_pos in hike_map:
                    nn.add(new_pos)
        neighbors[pos] = nn
    return neighbors


def find_junctions(neighbors, start, end):
    """Finds all junctions in the map"""
    junctions = {start, end}
    for pos, nn in neighbors.items():
        if len(nn) > 2:
            junctions.add(pos)
    return junctions


def junction_neighbors(neighbors, start, end):
    """Builds a dictionary of neighbors for each junction"""
    # Find junctions
    junctions = {start, end}
    for pos, nn in neighbors.items():
        if len(nn) > 2:
            junctions.add(pos)
    # Find neighbors for each junction and distance to them
    junc_neighbors = defaultdict(list)
    for p in junctions:
        queue = [p]
        seen = {p}
        dist = 0
        while queue:
            new_queue = []
            dist += 1
            for pos in queue:
                for n in neighbors[pos]:
                    if n not in seen:
                        if n in junctions:
                            junc_neighbors[p].append((n, dist))
                        else:
                            new_queue.append(n)
                        seen.add(n)
            queue = new_queue
    return junc_neighbors


def dfs(junc_neighbors, start, end):
    """Depth first search for the longest path"""
    best = 0
    queue = [(start, {start}, 0)]
    while queue:
        pos, path, dist = queue.pop()
        if pos == end:
            best = max(best, dist)
        for n, d in junc_neighbors[pos]:
            if n not in path:
                queue.append((n, path | {n}, dist + d))

    return best


def find_longest_path(hike_map, start, end, ignore_slope=False):
    neighbors = build_neighbor_dict(hike_map, ignore_slope=ignore_slope)
    junc_neighbors = junction_neighbors(neighbors, start, end)
    return dfs(junc_neighbors, start, end)


class Solution(aoc.Puzzle):
    day = 23
    year = 2023
    test_solution_idx_1 = -6
    test_solution_idx_2 = -2

    def solution_1(self, data: str):
        hike_map, start, end = parse_input(data)
        return find_longest_path(hike_map, start, end)

    def solution_2(self, data: str):
        hike_map, start, end = parse_input(data)
        return find_longest_path(hike_map, start, end, ignore_slope=True)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
