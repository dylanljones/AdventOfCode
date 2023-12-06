# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import os

import aoc

SRC = complex(500, 0)

UP = complex(0, +1)
DOWN = complex(0, -1)
LEFT = complex(-1, -1)
RIGHT = complex(+1, -1)


def parse_data(data: str):
    occupied = set()
    for line in data.splitlines(keepends=False):
        points = list()
        for p in line.split(" -> "):
            x, y = p.split(",")
            points.append((int(x), int(y)))
        for i in range(1, len(points)):
            start = points[i - 1]
            end = points[i]
            if end[0] != start[0] and end[1] == start[1]:
                x0, x1 = min(start[0], end[0]), max(start[0], end[0])
                occupied.update([(x, start[1]) for x in range(x0, x1 + 1)])
            elif end[0] == start[0] and end[1] != start[1]:
                y0, y1 = min(start[1], end[1]), max(start[1], end[1])
                occupied.update([(start[0], y) for y in range(y0, y1 + 1)])
    return {complex(pos[0], -pos[1]) for pos in occupied}


def get_occupied_below(occupied, pos):
    # Find all occupied ositions below
    below = [z for z in occupied if z.real == pos.real and z.imag < pos.imag]
    if len(below) == 0:
        return None
    below.sort(key=lambda x: x.imag)
    # Return highest point
    return below[-1]


class Solution(aoc.Puzzle):
    test_answer_idx_1 = -3
    test_answer_idx_2 = -2

    def __init__(self):
        super().__init__(2022, 14, root=os.path.dirname(__file__))

    @staticmethod
    def simulate_sand(occupied, start, ymin=-20):
        pos = start
        while True:
            if pos + DOWN not in occupied:
                pos = pos + DOWN
            elif pos + LEFT not in occupied:
                pos = pos + LEFT
            elif pos + RIGHT not in occupied:
                pos = pos + RIGHT
            else:
                break
            if pos.imag < ymin:
                return None
        return pos

    @staticmethod
    def simulate_sand2(occupied, start):
        pos = start
        while True:
            # Find the next occupied position below
            below = get_occupied_below(occupied, pos)
            if below is None:
                # No occupied position below
                return None
            # Move sand ontop of occupied position below
            pos = below + UP
            if pos + LEFT not in occupied:
                # Try to move to lower left
                pos = pos + LEFT
            elif pos + RIGHT not in occupied:
                # Try to move to lower right
                pos = pos + RIGHT
            else:
                # Final position reached!
                break
        return pos

    @staticmethod
    def simulate_sand_floor(occupied, start, floor):
        pos = start
        while True:
            if pos + DOWN not in occupied:
                pos = pos + DOWN
            elif pos + LEFT not in occupied:
                pos = pos + LEFT
            elif pos + RIGHT not in occupied:
                pos = pos + RIGHT
            else:
                break
            if pos.imag == floor + 1:
                break
        return pos

    def solution_1(self, data: str):
        occupied = parse_data(data)
        count = 0
        while True:
            pos = self.simulate_sand2(occupied, SRC)
            if pos is None:
                break
            count += 1
            occupied.add(pos)
        return count

    def solution_2(self, data: str):
        occupied = parse_data(data)
        floor = min(p.imag for p in occupied) - 2
        count = 0
        while True:
            pos = self.simulate_sand_floor(occupied, SRC, floor)
            count += 1
            occupied.add(pos)
            if pos == SRC:
                break
        return count


def main():
    puzzle = Solution()
    puzzle.run()


if __name__ == "__main__":
    main()
