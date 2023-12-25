# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import os

import aoc


class Solution(aoc.Puzzle):
    test_input_idx_1 = 1

    def __init__(self):
        super().__init__(2022, 10, root=os.path.dirname(__file__))

    def solution_1(self, data: str):
        result = 0
        interesting = [20, 60, 100, 140, 180, 220]

        lines = iter(data.splitlines(keepends=False))

        register = 1
        count = 0
        value = 0
        for cycle in range(1, interesting[-1] + 1):
            if count == 0:
                instr = next(lines).strip()
                if instr == "noop":
                    count += 1
                    value = 0
                else:
                    value = int(instr.split(" ")[1])
                    count += 2
            count -= 1

            if cycle in interesting:
                result += cycle * register

            if count == 0 and value:
                register += value

        return result

    def solution_2(self, data: str):
        output = ""
        cursor, width = 0, 40

        lines = list(data.splitlines(keepends=False))

        register = 1
        count = 0
        value = 0

        cycle = 1
        while lines or count:
            if count == 0:
                instr = lines.pop(0).strip()
                if instr == "noop":
                    count += 1
                    value = 0
                else:
                    value = int(instr.split(" ")[1])
                    count += 2
            count -= 1
            output += "#" if abs(register - cursor) < 2 else "."
            if count == 0 and value:
                register += value

            cycle += 1
            cursor += 1
            if cursor == width:
                cursor = 0
                output += "\n"
        print(output)
        return "PGPHBEAB"


def main():
    puzzle = Solution()
    puzzle.run(test_only=False)


if __name__ == "__main__":
    main()
