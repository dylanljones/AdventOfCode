# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-05

import aoc


def parse_input(data):
    lines = [line.strip() for line in data.splitlines(keepends=False)]

    seed_line = lines.pop(0)
    seeds = [int(x) for x in seed_line.replace("seeds: ", "").strip().split()]

    conversions = list()
    assert lines.pop(0) == ""
    while lines:
        lines.pop(0)  # Section header line
        line = lines.pop(0)
        maps = list()
        while line:
            dst_strt, src_strt, rng = [int(n) for n in line.split()]
            maps.append((dst_strt, src_strt, rng))
            if not lines:
                break
            line = lines.pop(0)
        conversions.append(maps)

    return seeds, conversions


def apply_range(conv, ranges):
    out = list()
    for dst_strt, src_strt, rng in conv:
        src_end = src_strt + rng
        new = list()
        while ranges:
            a, b = ranges.pop(0)
            before = a, min(b, src_strt)
            middle = max(a, src_strt), min(src_end, b)
            after = max(a, src_end), b
            if before[1] > before[0]:
                new.append(before)
            if middle[1] > middle[0]:
                out.append(
                    (middle[0] - src_strt + dst_strt, middle[1] - src_strt + dst_strt)
                )
            if after[1] > after[0]:
                new.append(after)
        ranges = new
    return ranges + out


class Solution(aoc.Puzzle):
    _file = __file__
    test_input_idx_2 = None

    def __init__(self):
        super().__init__(2023, 5)

    def solution_1(self, data: str):
        seeds, conversions = parse_input(data)
        location_numbers = set()
        for num in seeds:
            for conv in conversions:
                for dst_strt, src_strt, rng in conv:
                    if src_strt <= num < src_strt + rng:
                        num = dst_strt + (num - src_strt)
                        break
            location_numbers.add(num)
        result = min(location_numbers)
        return result

    def solution_2(self, data: str):
        seed_ranges, conversions = parse_input(data)
        pairs = list(zip(seed_ranges[::2], seed_ranges[1::2]))

        min_locnums = set()
        for start, size in pairs:
            ranges = [(start, start + size)]
            for conv in conversions:
                ranges = apply_range(conv, ranges)
            min_locnums.add(min(ranges)[0])
        return min(min_locnums)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
