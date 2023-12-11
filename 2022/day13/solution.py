# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import ast

import aoc


def parse_pairs(data: str):
    pairs = list()
    lines = [line.strip() for line in data.splitlines(keepends=False)]
    for i in range(0, len(lines), 3):
        p1 = ast.literal_eval(lines[i])
        p2 = ast.literal_eval(lines[i + 1])
        pairs.append((p1, p2))
    return pairs


def list_less(l1, l2):
    if isinstance(l1, int):
        # Mixed types; convert left to list
        l1 = [l1]
    if isinstance(l2, int):
        # Mixed types; convert right to list
        l2 = [l2]
    # print(f"compare_lists({l1}; {l2})")

    for i in range(max(len(l1), len(l2))):
        try:
            item1 = l1[i]
        except IndexError:
            # Left side ran out of items, so inputs are in the right order
            return True
        try:
            item2 = l2[i]
        except IndexError:
            # Right side ran out of items, so inputs are not in the right order
            return False

        if isinstance(item1, list) or isinstance(item2, list):
            # Nested list
            ordered = list_less(item1, item2)
            if ordered is not None:
                return ordered
        elif item1 < item2:
            # Left side is smaller, so inputs are in the right order
            return True
        elif item1 > item2:
            # Right side is smaller, so inputs are not in the right order
            return False

    return None


class Packet:
    def __init__(self, data):
        self.p = data

    def __repr__(self):
        return f"{self.__class__.__name__}({self.p})"

    def __eq__(self, other):
        return self.p == other.p

    def __lt__(self, other):
        return list_less(self.p, other.p)

    def __gt__(self, other):
        return other.__lt__(self)


def parse_packets(data: str):
    packets = list()
    lines = [line.strip() for line in data.splitlines(keepends=False)]
    for i in range(0, len(lines), 3):
        p1 = ast.literal_eval(lines[i])
        p2 = ast.literal_eval(lines[i + 1])
        packets.append(Packet(p1))
        packets.append(Packet(p2))
    return packets


class Solution(aoc.Puzzle):
    year = 2022
    day = 13

    def solution_1(self, data: str):
        pairs = parse_pairs(data)
        indices = list()
        for i, (p1, p2) in enumerate(pairs):
            if list_less(p1, p2):
                indices.append(i + 1)
        return sum(indices)

    def solution_2(self, data: str):
        d1 = Packet([[2]])
        d2 = Packet([[6]])
        packets = parse_packets(data)
        packets.append(d1)
        packets.append(d2)
        packets.sort()

        i1 = packets.index(d1) + 1
        i2 = packets.index(d2) + 1
        return i1 * i2


def main():
    puzzle = Solution()
    puzzle.run(test_only=False, text=False)


if __name__ == "__main__":
    main()
