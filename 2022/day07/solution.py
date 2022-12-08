# coding: utf-8
#
# This code is part of aoc2022.
#
# Copyright (c) 2022, Dylan Jones

import os
import numpy as np
import aoc

MAX_SIZE = 100000
DISC_SIZE = 70000000
DELETE_SIZE = 30000000


def dirsize1(files: dict, dirname: str) -> int:
    size = 0
    for key, val in files.items():
        if key.startswith(dirname + "/"):
            size += val
            if size > MAX_SIZE:
                return 0
    return size


def dirsize2(files: dict, dirname: str) -> int:
    size = 0
    for key, val in files.items():
        if key.startswith(dirname + "/"):
            size += val
    return size


class Solution(aoc.Puzzle):

    test_input_idx = 1
    test_answer_idx_1 = -1
    test_answer_idx_2 = -1

    def __init__(self):
        super().__init__(2022, 7)

    @staticmethod
    def parse_commands(data: str):
        paths = list()
        files = dict()
        current = "/"
        lines = data.splitlines(keepends=False)
        while lines:
            line = lines.pop(0).strip()
            assert line.startswith("$ ")
            line = line[2:]
            if line.startswith("cd"):
                arg = line[3:]
                if arg == "..":
                    current = os.path.dirname(current) or "/"
                else:
                    current = os.path.join(current, line[3:]).replace("\\", "/")
                    paths.append(current)
            elif line.startswith("ls"):
                # line = line[3:]
                while lines and not lines[0].startswith("$ "):
                    line = lines.pop(0).strip()
                    if not line.startswith("dir"):
                        size, name = line.split(" ")
                        path = os.path.join(current, name).replace("\\", "/")
                        files[path] = int(size)
        return paths, files

    def solution_1(self, data: str) -> int:
        dirs, files = self.parse_commands(data)

        size = sum(files.values())
        if size > MAX_SIZE:
            size = 0

        size += sum(dirsize1(files, name) for name in dirs)
        return size

    def solution_2(self, data: str) -> int:
        dirs, files = self.parse_commands(data)
        total = sum(files.values())
        required = DELETE_SIZE - (DISC_SIZE - total)
        sizes = [total] + [dirsize2(files, name) for name in dirs[1:]]
        idx = np.argsort(sizes)
        total_size = 0
        for i in idx:
            if sizes[i] >= required:
                total_size = sizes[i]
                break
        return total_size


def main():
    puzzle = Solution()
    # puzzle.load_info()
    puzzle.run(test_only=False, text=False)


if __name__ == "__main__":
    main()
