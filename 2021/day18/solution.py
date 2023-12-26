# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-26

import math
import re
from itertools import permutations

import aoc

RE_PAIR = re.compile(r"\[\d+,\d+]")


def explode(line: str) -> str:
    offset = 0
    for p in RE_PAIR.findall(line):
        match = re.search(re.escape(p), line[offset:])
        nle = line[: match.start() + offset].count("[")
        nri = line[: match.start() + offset].count("]")
        if nle - nri >= 4:
            x, y = match.group()[1:-1].split(",")
            # split the string into two parts at the pair
            # flip left side around so we get the first num going backwards
            left = line[: match.start() + offset][::-1]
            right = line[match.end() + offset :]

            # look left
            match_left = re.search("\d+", left)
            if match_left:
                # need to find the rightmost match not the first
                i, j = match_left.start(), match_left.end()
                amt = int(left[i:j][::-1]) + int(x)
                left = f"{left[:i]}{str(amt)[::-1]}{left[j:]}"

            # look right
            match_right = re.search("\d+", right)
            if match_right:
                i, j = match_right.start(), match_right.end()
                amt = int(right[i:j]) + int(y)
                right = f"{right[:i]}{amt}{right[j:]}"

            line = f"{left[::-1]}0{right}"
            break
        else:
            offset += match.end()
    return line


def split(line):
    dd = re.search(r"\d\d", line)
    if dd:
        left = line[: dd.start()]
        right = line[dd.end() :]
        left_digit = int(math.floor(int(dd.group()) / 2))
        right_digit = int(math.ceil(int(dd.group()) / 2))
        line = f"{left}[{left_digit},{right_digit}]{right}"
    return line


def reduce(line: str):
    exploded = explode(line)
    if exploded != line:
        return reduce(exploded)

    splitd = split(line)
    if splitd != line:
        return reduce(splitd)

    return splitd


def add(line):
    if " + " in line:
        line = f"[{line.split(' + ')[0]},{line.split(' + ')[1]}]"
    return line


def magnitude(line):
    while line.count(",") > 1:
        for p in RE_PAIR.findall(line):
            pair = re.search(re.escape(p), line)
            i, j = pair.start(), pair.end()
            left_digit, right_digit = p[1:-1].split(",")
            line = f"{line[:i]}{int(left_digit) * 3 + int(right_digit) * 2}{line[j:]}"
    left_digit, right_digit = line[1:-1].split(",")
    return int(left_digit) * 3 + int(right_digit) * 2


class Solution(aoc.Puzzle):
    day = 18
    year = 2021

    test_input_idx_1 = -2
    test_solution_idx_2 = -4

    def solution_1(self, data: str):
        lines = data.splitlines()
        final_sum = ""
        while lines:
            line1 = lines.pop(0)
            if not final_sum:
                final_sum = f"{line1} + {lines.pop(0)}"
            else:
                final_sum = f"{final_sum} + {line1}"
            final_sum = reduce(add(final_sum))
        return magnitude(final_sum)

    def solution_2(self, data: str):
        lines = data.splitlines()
        mag = {magnitude(reduce(add(f"{a} + {b}"))) for a, b in permutations(lines, 2)}
        return max(mag)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
