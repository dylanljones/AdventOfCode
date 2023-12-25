# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2021-12-12

from collections import defaultdict

import aoc


def parse_input(data: str) -> dict[str, list[str]]:
    connections = defaultdict(list)
    for line in data.splitlines(keepends=False):
        a, b = line.split("-")
        connections[a].append(b)
        connections[b].append(a)
    return connections


def find_paths(connections: dict[str, list[str]], visit_twice: bool = False):
    n = 0
    queue = [("start", {"start"}, False)]
    while queue:
        p, seen, visited = queue.pop()
        if p == "end":
            n += 1
            continue
        for c in connections[p]:
            if c not in seen:
                new_seen = set(seen)
                if c.islower():
                    new_seen.add(c)
                queue.append((c, new_seen, visited))
            elif c in seen and not visited and c not in ["start", "end"]:
                if visit_twice:
                    queue.append((c, seen, bool(c)))
    return n


class Solution(aoc.Puzzle):
    day = 12
    year = 2021
    test_input_idx_1 = -1
    test_solution_idx_1 = -2

    def solution_1(self, data: str):
        connections = parse_input(data)
        return find_paths(connections)

    def solution_2(self, data: str):
        connections = parse_input(data)
        return find_paths(connections, visit_twice=True)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
