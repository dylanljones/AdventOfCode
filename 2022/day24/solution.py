# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2022-12-24

import aoc

DIRECTIONS = {
    "^": (-1, 0),
    "v": (+1, 0),
    "<": (0, -1),
    ">": (0, +1),
}
STEPS = {(0, 0), (-1, 0), (+1, 0), (0, -1), (0, +1)}


def parse_input(data: str):
    lines = [line.strip() for line in data.splitlines(keepends=False)]
    size = (len(lines), len(lines[0]))
    blizzards = list()
    start, end = (-1, 0), (1000, 0)
    for c, char in enumerate(lines[0]):
        if char == ".":
            start = (0, c)
    for c, char in enumerate(lines[-1]):
        if char == ".":
            end = (len(lines) - 1, c)
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char not in (".", "#"):
                blizzards.append(Blizzard((r, c), char))
    return start, end, size, blizzards


def visualize(size, start, end, blizzards, positions):
    height, width = size
    grid = [["."] * width for _ in range(height)]
    # Add Boundary
    for r in range(height):
        grid[r][0] = "#"
        grid[r][-1] = "#"
    for c in range(width):
        grid[0][c] = "#"
        grid[-1][c] = "#"
    grid[start[0]][start[1]] = "."
    grid[end[0]][end[1]] = "."
    # Add blizzards
    for bliz in blizzards:
        r, c = bliz.pos
        grid[r][c] = bliz.char
    # Add positions
    for pos in positions:
        r, c = pos
        grid[r][c] = "o"
    # Print
    for line in grid:
        print("".join(line))
    print()


class Blizzard:
    def __init__(self, pos, char):
        self.pos = pos
        self.char = char
        self.direction = DIRECTIONS[char]

    def move(self, size):
        height, width = size
        r, c = self.pos
        dr, dc = self.direction
        r_new, c_new = r + dr, c + dc
        if r_new <= 0:
            r_new = height - 2
        if r_new >= height - 1:
            r_new = 1
        if c_new <= 0:
            c_new = width - 2
        if c_new >= width - 1:
            c_new = 1
        self.pos = (r_new, c_new)


def simulate_blizzards(blizzards, size):
    for bliz in blizzards:
        bliz.move(size)


def propose_moves(position, blizzards, size):
    r, c = position
    if r == 0:
        if any(bliz.pos == (1, c) for bliz in blizzards):
            return {(0, c)}
        return {(0, c), (1, c)}
    elif r == size[0] - 1:
        if any(bliz.pos == (size[0] - 2, c) for bliz in blizzards):
            return {(size[0] - 1, c)}
        return {(size[0] - 1, c), (size[0] - 2, c)}
    proposals = set()
    for dr, dc in STEPS:
        new_pos = (r + dr, c + dc)
        if not (0 < new_pos[0] < size[0] - 1):
            continue
        if not (0 < new_pos[1] < size[1] - 1):
            continue
        if any(bliz.pos == new_pos for bliz in blizzards):
            continue
        proposals.add(new_pos)
    return proposals


def get_snapshot(pos, blizzards):
    bliz_positions = tuple(bliz.pos for bliz in blizzards)
    return pos, bliz_positions


def find_path(size, blizzards, start, last_pos):
    positions = [start]
    minutes = 0
    while True:
        minutes += 1
        # Move the blizzards
        simulate_blizzards(blizzards, size)
        # Propose steps for all previous positions
        new_positions = set()
        for pos in positions:
            proposals = propose_moves(pos, blizzards, size)
            new_positions.update(proposals)
        # Update positions
        positions = new_positions
        # Check if last position before end is in positions
        if last_pos in positions:
            break

    minutes += 1  # Add last minute
    return minutes


class Solution(aoc.Puzzle):
    day = 24
    year = 2022
    test_input_idx_1 = -2
    test_answer_idx_1 = -3

    def solution_1(self, data: str):
        start, end, size, blizzards = parse_input(data)
        last_pos = (end[0] - 1, end[1])
        minutes = find_path(size, blizzards, start, last_pos)
        return minutes

    def solution_2(self, data: str):
        start, end, size, blizzards = parse_input(data)
        total_minutes = 0

        _start = start
        last_pos = (end[0] - 1, end[1])
        minutes = find_path(size, blizzards, _start, last_pos)
        print(f"== Found exit in {minutes} Minutes ==")
        total_minutes += minutes

        _start = end
        last_pos = (start[0] + 1, start[1])
        minutes = find_path(size, blizzards, _start, last_pos)
        print(f"== Found entrance in {minutes} Minutes == ")
        total_minutes += minutes

        _start = start
        last_pos = (end[0] - 1, end[1])
        minutes = find_path(size, blizzards, _start, last_pos)
        print(f"== Found exit in {minutes} Minutes ==")
        total_minutes += minutes

        print("Total Minutes:", total_minutes)
        return total_minutes - 2


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(rerun=False)
