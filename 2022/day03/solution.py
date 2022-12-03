# coding: utf-8
#
# This code is part of aoc2022.
#
# Copyright (c) 2022, Dylan Jones

from aoc import Puzzle


class Solution(Puzzle):
    def __init__(self):
        super().__init__(2022, 3)

    @staticmethod
    def get_priority(char):
        return ord(char) - 65 + 27 if char.isupper() else ord(char) - 97 + 1

    def solution_1(self, data: str):
        lines = data.splitlines(keepends=False)
        result = 0
        for line in lines:
            n = len(line) // 2
            department1, department2 = line[:n], line[n:]
            chars = list(set(department1) & set(department2))
            char = chars[0]
            result += self.get_priority(char)
        return result

    def solution_2(self, data: str):
        lines = data.splitlines(keepends=False)
        n_lines = len(lines)
        result = 0
        for i in range(0, n_lines, 3):
            block = lines[i : i + 3]
            chars = [set(line) for line in block]
            char = list(chars[0] & chars[1] & chars[2])[0]
            result += self.get_priority(char)
        return result


def main():
    puzzle = Solution()
    puzzle.run(text=False, test_only=False)


if __name__ == "__main__":
    main()
