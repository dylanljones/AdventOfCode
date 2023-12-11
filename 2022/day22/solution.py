# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2022-12-22

import numpy as np

import aoc


def parse_path(line):
    steps = list()
    path = list(line)
    while path:
        chars = ""
        while path and path[0].isdigit():
            chars += path.pop(0)
        steps.append(int(chars))
        while path and path[0].isalpha():
            steps.append(path.pop(0))
    return steps


def parse_input(data: str):
    lines = [line for line in data.splitlines(keepends=False)]
    while lines[-1] == "":
        lines.pop(-1)
    steps = parse_path(lines.pop(-1))
    while lines[-1] == "":
        lines.pop(-1)
    return lines, steps


class Board:
    def __init__(self, tiles):
        self.tiles = tiles

    def get_tiles(self, r=None, c=None):
        for tile in self.tiles:
            if r is not None and tile[0] != r:
                continue
            if c is not None and tile[1] != c:
                continue
            yield tile

    def get_tile(self, r, c):
        for tile in self.get_tiles(r=r, c=c):
            return tile[2]

    def start_position(self):
        cols = list(tile[1] for tile in self.get_tiles(r=0) if tile[2] == ".")
        c = min(cols)
        return 0, c


class Player:
    def __init__(self, pos, facing):
        self.pos = np.array(pos)
        self.facing = facing
        self.direction = np.array([0, 0])
        self.update_direction()

    def __repr__(self):
        return f"Player(pos={self.pos}, facing={self.facing})"

    def move(self, board, steps):
        pos = self.pos
        if self.facing in [0, 0.5]:
            tiles_in_dir = list(board.get_tiles(r=pos[0]))
        else:
            tiles_in_dir = list(board.get_tiles(c=pos[1]))
        for i in range(steps):
            new_pos = pos + self.direction
            tile = board.get_tile(*new_pos)
            if tile is None:
                # Wrap position
                if self.facing == 0.0:
                    new_pos[1] = min(tile[1] for tile in tiles_in_dir)
                elif self.facing == 0.5:
                    new_pos[1] = max(tile[1] for tile in tiles_in_dir)
                elif self.facing == 0.25:
                    new_pos[0] = min(tile[0] for tile in tiles_in_dir)
                elif self.facing == 0.75:
                    new_pos[0] = max(tile[0] for tile in tiles_in_dir)
            tile = board.get_tile(*new_pos)
            if tile == "#":
                break
            pos = new_pos
        self.pos = pos

    def update_direction(self):
        if self.facing == 0:
            self.direction = np.array([0, +1])
        elif self.facing == 0.25:
            self.direction = np.array([+1, 0])
        elif self.facing == 0.5:
            self.direction = np.array([0, -1])
        elif self.facing == 0.75:
            self.direction = np.array([-1, 0])
        else:
            raise ValueError(f"Invalid facing: {self.facing}")

    def turn(self, direction):
        direction = direction.lower()
        if direction == "l":
            self.facing = (self.facing - 0.25) % 1.0
        elif direction == "r":
            self.facing = (self.facing + 0.25) % 1.0
        else:
            raise ValueError(f"Invalid direction: {direction}")
        self.update_direction()


class Solution(aoc.Puzzle):
    day = 22
    year = 2022
    test_input_idx_2 = None

    def solution_1(self, data: str):
        lines, path = parse_input(data)
        tiles = list()
        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                if char != " ":
                    tiles.append((r, c, char))
        board = Board(tiles)
        start = board.start_position()
        player = Player(start, 0)
        for step in path:
            if isinstance(step, int):
                player.move(board, step)
            else:
                player.turn(step)

        r, c = player.pos
        angle = player.facing * 4
        result = 1000 * (r + 1) + 4 * (c + 1) + angle
        return result

    def solution_2(self, data: str):
        lines, path = parse_input(data)
        nrows = len(lines)
        ncols = 0
        for line in lines:
            ncols = max(len(line), ncols)
        data = np.zeros((nrows, ncols), dtype=np.int8)
        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                if char == ".":
                    data[r, c] = 1
                elif char == "#":
                    data[r, c] = 2
        n = len(np.where(data != 0)[0])
        side = int(np.sqrt(n / 6))

        ny = nrows // side
        nx = ncols // side
        cube_sides = np.zeros((ny, nx))
        for r in range(ny):
            for c in range(nx):
                i, j = r * side, c * side
                cube_sides[r, c] = int(data[i, j] > 0)
        print(cube_sides)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(puzzle_only=True, test_only=False, rerun=False)
