# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import collections
import itertools

import aoc

DIRECTIONS = [
    (+1, 0, 0),
    (0, +1, 0),
    (0, 0, +1),
    (-1, 0, 0),
    (0, -1, 0),
    (0, 0, -1),
]


def get_faces(pos):
    x, y, z = pos
    for dx, dy, dz in DIRECTIONS:
        yield x + dx, y + dy, z + dz


def parse_data(data: str):
    return [tuple(int(x) for x in line.split(",")) for line in data.splitlines()]


class Solution(aoc.Puzzle):
    file = __file__

    def __init__(self):
        super().__init__()

    @staticmethod
    def surface_area(cubes: list[tuple]):
        coords = set()
        nfaces = 0
        for pos in cubes:
            nfaces += 6
            for face in get_faces(pos):
                if face in coords:
                    nfaces -= 2
            coords.add(pos)
        return coords, nfaces

    @staticmethod
    def get_coord_grid(points: list[tuple]):
        x0, x1 = +10000, -10000
        y0, y1 = +10000, -10000
        z0, z1 = +10000, -10000
        for x, y, z in points:
            x0, x1 = min(x0, x), max(x1, x)
            y0, y1 = min(y0, y), max(y1, y)
            z0, z1 = min(z0, z), max(z1, z)

        return {
            (x, y, z)
            for x, y, z in itertools.product(
                range(x0 - 1, x1 + 2), range(y0 - 1, y1 + 2), range(z0 - 1, z1 + 2)
            )
        }

    def solution_1(self, data: str):
        cubes = parse_data(data)
        _, nfaces = self.surface_area(cubes)
        return nfaces

    def solution_2(self, data: str):
        cubes = parse_data(data)
        coords, area = self.surface_area(cubes)
        all_coords = self.get_coord_grid(cubes)
        remaining = all_coords - coords
        queue = collections.deque([min(remaining)])
        while queue:
            pos = queue.pop()
            if pos in remaining:
                remaining.discard(pos)
            else:
                continue
            for p in get_faces(pos):
                queue.append(p)
        _, inner = self.surface_area(list(remaining))
        return area - inner


def main():
    puzzle = Solution()
    puzzle.run()


if __name__ == "__main__":
    main()
