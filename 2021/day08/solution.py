# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-25

import collections

import aoc


def parse_input(data: str):
    data = data.replace("|\n", "| ")  # Fix test input data
    lines = [line.strip() for line in data.splitlines(keepends=False)]
    for line in lines:
        inp, out = line.split(" | ")
        inp = inp.split(" ")
        out = out.split(" ")
        yield inp, out


def clean_input(signal, digits):
    """Remove already found signal"""
    for d in digits:
        if signal.count(digits[d]) > 0:
            signal.remove(digits[d])


def analyze_signal(signal: list[str]) -> dict[str, int]:
    lengths = {2: 1, 5: [2, 3, 5], 4: 4, 6: [6, 9, 0], 3: 7, 7: 8}
    wires = collections.defaultdict(set)
    digits, encoding = dict(), dict()
    # find 1, 4, 7, 8
    for d in signal:
        if isinstance(lengths[len(d)], int):
            digits[lengths[len(d)]] = d
            encoding[d] = lengths[len(d)]
    clean_input(signal, digits)

    # find 6, 3
    for d in signal:
        if len(d) == 6:
            if len(set(digits[1]) - set(d)) == 1:
                digits[6] = d
                encoding[d] = 6
                wires[3] = set(digits[1]) - set(d)
                wires[6] = set(digits[1]) - wires[3]
        elif len(d) == 5:
            if len(set(d) - set(digits[7])) == 2:
                digits[3] = d
                encoding[d] = 3

    clean_input(signal, digits)

    # find 9, 0
    for item in signal:
        if len(item) == 6:
            if len(set(digits[8]) - set(digits[3]) - set(item)) == 1:
                digits[9] = item
                encoding[item] = 9
                wires[5] = set(digits[8]) - set(digits[3]) - set(item)
                wires[2] = set(digits[9]) - set(digits[3])
                wires[4] = set(digits[4]) - set(digits[7]) - wires[2]
                wires[7] = set(digits[3]) - set(digits[7]) - wires[4]
            elif len(set(digits[8]) - set(digits[3]) - set(item)) == 0:
                digits[0] = item
                encoding[item] = 0
    clean_input(signal, digits)

    # find 5, 2
    for item in signal:
        if len(set(digits[9]) - wires[3] - set(item)) == 0:
            digits[5] = item
            encoding[item] = 5
        else:
            digits[2] = item
            encoding[item] = 2
    clean_input(signal, digits)
    wires[1] = set(digits[7]) - set(digits[1])

    return encoding


def decode_digit(encoding, digit):
    d = set(digit)
    for k, v in encoding.items():
        if set(k) == d:
            return v
    return None


class Solution(aoc.Puzzle):
    year = 2021
    day = 8
    test_input_idx_1 = 2
    test_input_idx_2 = 2
    test_solution_idx_1 = -5

    def solution_1(self, data: str):
        lengths = {2: 1, 4: 4, 3: 7, 7: 8}
        return sum(sum(len(d) in lengths for d in dd) for _, dd in parse_input(data))

    def solution_2(self, data: str):
        result = 0
        for signal, digits in parse_input(data):
            value = 0
            encoding = analyze_signal(signal)
            for d in digits:
                value = value * 10 + decode_digit(encoding, d)
            result += value
        return result


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
