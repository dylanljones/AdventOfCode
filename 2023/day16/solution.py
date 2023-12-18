# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-16

import aoc


def parse_input(data: str):
    lines = [line.strip() for line in data.splitlines(keepends=False)]
    size = len(lines), len(lines[0])
    board = dict()
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char != ".":
                board[(r, c)] = char
    return board, size


class Beam:
    def __init__(self, pos, direction):
        self.pos = pos
        self.dir = direction
        self.next = self.next_pos()

    def next_pos(self):
        return self.pos[0] + self.dir[0], self.pos[1] + self.dir[1]

    def step(self):
        self.pos = self.next

    def update_next(self):
        self.next = self.next_pos()


def get_energized(board: dict, size: tuple, initial_beam: Beam):
    beams = [initial_beam]
    visited = {(beams[0].pos, beams[0].dir)}
    while beams:
        # Update beams
        for beam in beams.copy():
            next_tile = board.get(beam.next, ".")
            if next_tile == "|" and beam.dir[1] != 0:
                beam.step()
                beam.dir = (1, 0)
                beam.update_next()
                new_beam = Beam(beam.pos, (-1, 0))
                beams.append(new_beam)
            elif next_tile == "-" and beam.dir[0] != 0:
                beam.step()
                beam.dir = (0, 1)
                beam.update_next()
                new_beam = Beam(beam.pos, (0, -1))
                beams.append(new_beam)
            elif next_tile == "/":
                beam.step()
                beam.dir = (-beam.dir[1], -beam.dir[0])
                beam.update_next()
            elif next_tile == "\\":
                beam.step()
                beam.dir = (beam.dir[1], beam.dir[0])
                beam.update_next()
            elif not (0 <= beam.next[0] < size[0] and 0 <= beam.next[1] < size[1]):
                beams.remove(beam)
            else:
                beam.step()
                beam.update_next()

        # Remove beams that have been visited with same direction before
        for beam in beams.copy():
            if (beam.pos, beam.dir) in visited:
                beams.remove(beam)

        # Update visited
        for beam in beams:
            visited.add((beam.pos, beam.dir))

    energized = {pos for pos, _ in visited}
    return len(energized) - 1


class Solution(aoc.Puzzle):
    day = 16
    year = 2023
    test_solution_idx_2 = -2

    def solution_1(self, data: str):
        board, size = parse_input(data)
        return get_energized(board, size, Beam((0, -1), (0, 1)))

    def solution_2(self, data: str):
        board, size = parse_input(data)
        max_energized = 0
        # Top
        for c in range(size[1]):
            beam = Beam((-1, c), (1, 0))
            max_energized = max(max_energized, get_energized(board, size, beam))
        # Bottom
        for c in range(size[1]):
            beam = Beam((size[0], c), (-1, 0))
            max_energized = max(max_energized, get_energized(board, size, beam))
        # Left
        for r in range(size[0]):
            beam = Beam((r, -1), (0, 1))
            max_energized = max(max_energized, get_energized(board, size, beam))
        # Right
        for r in range(size[0]):
            beam = Beam((r, size[1]), (0, -1))
            max_energized = max(max_energized, get_energized(board, size, beam))

        return max_energized


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
