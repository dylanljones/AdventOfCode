# coding: utf-8
#
# This code is part of aoc2022.
#
# Copyright (c) 2022, Dylan Jones

from aoc import Puzzle


def parse_ranges(line):
    s1, s2 = line.split(",")
    start, end = s1.split("-")
    range_1 = int(start), int(end)
    start, end = s2.split("-")
    range_2 = int(start), int(end)
    return range_1, range_2


class Solution(Puzzle):
    def __init__(self):
        super().__init__(2022, 4)

    def solution_1(self, data: str):
        lines = data.splitlines(keepends=False)
        count = 0
        for line in lines:
            range_1, range_2 = parse_ranges(line)
            if (range_1[0] >= range_2[0]) and (range_1[1] <= range_2[1]):
                # range 1 fully contained in range 2
                count += 1
            elif (range_2[0] >= range_1[0]) and (range_2[1] <= range_1[1]):
                # range 2 fully contained in range 1
                count += 1
        return count

    def solution_2(self, data: str):
        lines = data.splitlines(keepends=False)
        count = 0
        for line in lines:
            range_1, range_2 = parse_ranges(line)
            print(range_1, range_2)
            if range_2[0] <= range_1[0] <= range_2[1]:
                count += 1
            elif range_2[0] <= range_1[1] <= range_2[1]:
                count += 1
            elif range_1[0] <= range_2[0] <= range_1[1]:
                count += 1
            elif range_1[0] <= range_2[1] <= range_1[1]:
                count += 1

        return count
        # return count


def main():
    puzzle = Solution()
    puzzle.run(text=False, test_only=False)


if __name__ == "__main__":
    main()
