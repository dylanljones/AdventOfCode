# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2022-12-23

from collections import defaultdict, deque

import aoc

N = (-1, 0)
NW = (-1, -1)
NE = (-1, +1)
S = (+1, 0)
SW = (+1, -1)
SE = (+1, +1)
W = (0, -1)
E = (0, +1)

VECTORS = [N, NW, NE, S, SW, SE, W, E]
DIRECTIONS = [
    ([N, NE, NW], N),
    ([S, SE, SW], S),
    ([W, NW, SW], W),
    ([E, NE, SE], E),
]


def get_neighbors(pos, directions=None):
    if directions is None:
        directions = VECTORS
    r, c = pos
    positions = {(r + dr, c + dc) for dr, dc in directions}
    return positions


def parse_input(data: str):
    lines = [line.strip() for line in data.splitlines(keepends=False)]
    elves = set()
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == "#":
                elves.add((r, c))
    return elves


def move_elves(elves, directions):
    # First half: Propose moves
    proposals = dict()
    for elve in elves:
        # Check if elve has adjacent neighbors
        if get_neighbors(elve).isdisjoint(elves):
            # Elve has no adjacent neighbors, do nothing
            continue

        # Iterate over all directions
        for direction_checks, proposed_dir in directions:
            if get_neighbors(elve, direction_checks).isdisjoint(elves):
                # Elve has no neighbors in this direction, move in proposed dir
                new = (elve[0] + proposed_dir[0], elve[1] + proposed_dir[1])
                proposals[elve] = new
                break  # stop at the first valid direction

    # Second half: Check how many elves have proposed the same move
    elves_per_pos = defaultdict(list)
    for elve, prop in proposals.items():
        elves_per_pos[prop].append(elve)

    # Move elves that have made a unique proposal
    moved = 0
    for new, old in elves_per_pos.items():
        if len(old) == 1:
            elves.add(new)
            elves.remove(old[0])
            moved += 1

    # Rotate directions
    directions.rotate(-1)

    return moved


class Solution(aoc.Puzzle):
    day = 23
    year = 2022
    test_input_idx_1 = -8
    test_input_idx_2 = None
    test_answer_idx_2 = -2

    def solution_1(self, data: str):
        elves = parse_input(data)
        directions = deque(DIRECTIONS.copy())

        # Run rounds
        for it in range(10):
            move_elves(elves, directions)

        # Compute number of empty tiles
        rows = [r for r, _ in elves]
        cols = [c for _, c in elves]
        rlim = min(rows), max(rows)
        clim = min(cols), max(cols)
        n_tiles = (rlim[1] - rlim[0] + 1) * (clim[1] - clim[0] + 1)
        n_empty = n_tiles - len(elves)
        return n_empty

    def solution_2(self, data: str):
        elves = parse_input(data)
        directions = deque(DIRECTIONS.copy())
        # Run rounds until no elves have moved
        round_num = 1
        while move_elves(elves, directions) > 0:
            round_num += 1
        return round_num


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
