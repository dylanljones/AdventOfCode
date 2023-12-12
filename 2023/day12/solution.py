# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-12

from functools import cache

import aoc

OPERATIONAL = 0
DAMAGED = 1
UNKNOWN = 2
NUMBERS = {".": OPERATIONAL, "#": DAMAGED, "?": UNKNOWN}


def parse_input(data):
    for line in data.splitlines(keepends=False):
        record, groups = line.split(" ")
        record = tuple(NUMBERS[x] for x in record)
        groups = tuple(int(x) for x in groups.split(","))
        yield record, groups


@cache
def find_arragments(record, groups):
    if len(groups) == 0:
        # No more groups to fit
        return int(sum(x == DAMAGED for x in record) == 0)
    elif sum(groups) > len(record):
        # No combination of groups can fit in the record
        return 0

    if record[0] == OPERATIONAL:
        return find_arragments(record[1:], groups)

    i, j = 0, 0
    if record[0] == UNKNOWN:
        # Able to start on next position
        j = find_arragments(record[1:], groups)

    if (
        all(x for x in record[: groups[0]])
        and (record[groups[0]] if len(record) > groups[0] else 0) != 1
    ):
        # Able to start on this position
        i = find_arragments(record[groups[0] + 1 :], groups[1:])
    return i + j


class Solution(aoc.Puzzle):
    day = 12
    year = 2023
    test_input_idx_1 = 1

    def solution_1(self, data: str):
        return sum(find_arragments(*x) for x in parse_input(data))

    def solution_2(self, data: str):
        factor = 5
        result = 0
        for record, groups in parse_input(data):
            record = tuple(((list(record) + [UNKNOWN]) * factor)[:-1])
            groups *= factor
            result += find_arragments(record, groups)
        return result


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
