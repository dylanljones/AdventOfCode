# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-08

from itertools import cycle
from math import lcm

import aoc


def parse_input(data: str):
    lines = [line.strip() for line in data.splitlines(keepends=False)]
    instructions = cycle(list(lines.pop(0)))
    assert lines.pop(0) == ""
    elements = dict()
    next_elements = dict()
    for line in lines:
        el, p2 = line.split(" = ")
        next_els = p2.replace("(", "").replace(")", "").split(", ")
        elements[el] = next_els
        next_elements[(el, "L")] = next_els[0]
        next_elements[(el, "R")] = next_els[1]
    return instructions, elements, next_elements


class Solution(aoc.Puzzle):
    day = 8
    year = 2023
    test_input_idx_1 = -1
    test_answer_idx_1 = -5
    test_answer_idx_2 = -3

    def solution_1(self, data: str):
        instructions, _, next_elements = parse_input(data)
        el, steps = "AAA", 0
        while el != "ZZZ":
            steps += 1
            el = next_elements[(el, next(instructions))]
        return steps

    def solution_2(self, data: str):
        instructions, elements, next_elements = parse_input(data)
        start = {el for el in elements if el[-1] == "A"}

        loop_sizes = list()
        for el in start:
            # Find first occurence of Z
            current, step = el, 0
            while current[-1] != "Z":
                step += 1
                current = next_elements[(current, next(instructions))]
            # Find second occurence of Z
            step = 1
            current = next_elements[(current, next(instructions))]
            while current[-1] != "Z":
                step += 1
                current = next_elements[(current, next(instructions))]
            loop_sizes.append(step)

        steps = lcm(*loop_sizes)
        return steps


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
