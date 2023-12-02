# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-01
import numpy as np

import aoc


def parse_game(line):
    game, cubes = line.split(":")
    game = int(game.replace("Game", "").strip())
    sets = list()
    for s in cubes.split(";"):
        x = dict()
        for part in s.split(","):
            part = part.strip().split(" ")
            x[part[1]] = int(part[0])
        sets.append(x)
    return game, sets


class Solution(aoc.Puzzle):
    _file = __file__

    def __init__(self):
        super().__init__(2023, 2)

    def solution_1(self, data: str):
        total = {"red": 12, "green": 13, "blue": 14}
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        result = 0
        for line in lines:
            game, cubes = line.split(":")
            game_id = int(game.replace("Game", "").strip())
            game_valid = True
            for text in cubes.split(";"):
                for part in text.split(","):
                    part = part.strip().split(" ")
                    color = part[1].strip()
                    number = int(part[0])
                    if number > total[color]:
                        game_valid = False
                        break
            if game_valid:
                result += game_id
        return result

    def solution_2(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        result = 0
        for line in lines:
            game, cubes = line.split(":")
            total = {"red": 0, "green": 0, "blue": 0}
            for text in cubes.split(";"):
                for part in text.split(","):
                    part = part.strip().split(" ")
                    color = part[1].strip()
                    number = int(part[0])
                    total[color] = max(total[color], number)
            set_pow = np.prod([v for v in total.values()])
            result += set_pow
        return result


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
