# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import re

import aoc

RE_MOVE = re.compile(r"move (.*?) from (.*?) to (.*?)$")


def _extract_crates(line, w, s):
    items = list()
    for i in range(0, w, s):
        items.append(line[i : i + s].strip().replace("[", "").replace("]", ""))
    return items


def parse_puzzle(data: str):
    lines = data.splitlines()

    line = lines.pop(0)
    width, step = len(line), 4
    num = int((width - step + 1) / step) + 1
    crates = [list() for _ in range(num)]
    while line:
        for i, val in enumerate(_extract_crates(line, width, step)):
            if val and not val.isdigit():
                crates[i].append(val)
        line = lines.pop(0)
    for i in range(num):
        crates[i] = crates[i][::-1]

    moves = list()
    for line in lines:
        moves.append([int(x) for x in RE_MOVE.search(line).groups()])

    return crates, moves


class Solution(aoc.Puzzle):
    year = 2022
    day = 5

    def solution_1(self, data: str):
        crates, moves = parse_puzzle(data)
        for move in moves:
            qty, src, dst = move[0], move[1] - 1, move[2] - 1
            for _ in range(qty):
                crates[dst].append(crates[src].pop())
        tops = [crate[-1] for crate in crates]
        return "".join(tops)

    def solution_2(self, data: str):
        crates, moves = parse_puzzle(data)
        for move in moves:
            qty, src, dst = move[0], move[1] - 1, move[2] - 1
            chunk = [crates[src].pop() for _ in range(qty)]
            for item in chunk[::-1]:
                crates[dst].append(item)

        tops = [crate[-1] for crate in crates]
        return "".join(tops)


def main():
    puzzle = Solution()
    puzzle.run()


if __name__ == "__main__":
    main()
