# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-15

from collections import OrderedDict, defaultdict

import aoc


def parse_input(data: str):
    return data.replace("\n", "").split(",")


def compute_hash(string):
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        _, value = divmod(value, 256)
    return value


class Solution(aoc.Puzzle):
    day = 15
    year = 2023

    def solution_1(self, data: str):
        sequence = parse_input(data)
        hash_sum = sum(compute_hash(s) for s in sequence)
        return hash_sum

    def solution_2(self, data: str):
        boxes = defaultdict(OrderedDict)
        for operation in parse_input(data):
            if "=" in operation:
                label, value = operation.split("=")
                value = int(value)
                box = compute_hash(label)
                boxes[box][label] = value
            else:
                label = operation.rstrip("-")
                box = compute_hash(label)
                if label in boxes[box]:
                    del boxes[box][label]

        result = 0
        for box, contents in boxes.items():
            for slot, lens in enumerate(contents.keys()):
                focal_power = contents[lens]
                val = (box + 1) * (slot + 1) * focal_power
                result += val
        return result


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
