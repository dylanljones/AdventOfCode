# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-18

from itertools import pairwise

import networkx as nx

import aoc

DIRS = {"R": 1 + 0j, "U": 0 + 1j, "L": -1 + 0j, "D": 0 - 1j}
ORDER = "RDLU"


def parse_input(data, use_color=False):
    graph = nx.Graph()
    a = 0j
    for line in data.splitlines():
        dir_, steps, color = line.split()
        if use_color:
            steps, dir_ = int(color[2:-2], 16), ORDER[int(color[-2])]
        else:
            steps = int(steps)
        direction = DIRS[dir_]
        b = a + steps * direction
        graph.add_node(a, dout=direction, steps=steps)
        graph.add_node(b, din=direction)
        graph.add_edge(a, b)
        a = b
    return graph


def shoelace(vertices):
    return sum((x1 * y2 - y1 * x2) for ((x1, y1), (x2, y2)) in pairwise(vertices)) / 2


def get_graph_volume(graph):
    turn_coords = {(-1j, -1j): 1, (-1j, 1j): 0, (1j, 1j): -1, (1j, -1j): 0}

    turn_total = sum(d["dout"] / d["din"] for (n, d) in graph.nodes(data=True))
    if turn_total == -4j:
        clockwise = 1
    elif turn_total == 4j:
        clockwise = -1
    else:
        raise ValueError("Invalid turn total: {}".format(turn_total))

    point = 0j
    outer_vertices = [point]
    for a, b in nx.find_cycle(graph, point):
        a = graph.nodes[a]
        b = graph.nodes[b]
        aturn = a["dout"] / a["din"] * clockwise
        bturn = b["dout"] / b["din"] * clockwise
        coords = turn_coords.get((aturn, bturn), 0)
        direction, steps = a["dout"], a["steps"] + coords
        point += direction * steps
        outer_vertices.append(point)

    vol = shoelace([(c.real, c.imag) for c in outer_vertices]) * -clockwise
    return int(vol)


class Solution(aoc.Puzzle):
    day = 18
    year = 2023

    def solution_1(self, data: str):
        graph = parse_input(data)
        return get_graph_volume(graph)

    def solution_2(self, data: str):
        graph = parse_input(data, use_color=True)
        return get_graph_volume(graph)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(puzzle_only=False)
