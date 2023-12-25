# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-24

import itertools

import networkx as nx

import aoc


def parse_input(data: str):
    for line in data.splitlines(keepends=False):
        names = line.replace(":", "").split(" ")
        yield names[0], names[1:]


def mincut_networkx(connections):
    graph = nx.Graph()
    for a, others in connections:
        for b in others:
            graph.add_edge(a, b, capacity=1)
    na, nb = 0, 0
    for a, b in itertools.combinations(graph.nodes, 2):
        n_cuts, partition = nx.minimum_cut(graph, a, b)
        if n_cuts == 3:
            na, nb = len(partition[0]), len(partition[1])
            break
    return na * nb


class Solution(aoc.Puzzle):
    day = 25
    year = 2023
    test_input_idx_1 = 1
    part_2 = False

    def solution_1(self, data: str):
        conn = parse_input(data)
        return mincut_networkx(conn)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(puzzle_only=False)
