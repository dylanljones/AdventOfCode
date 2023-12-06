# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-04

import datetime
import sys
from argparse import ArgumentParser
from pathlib import Path

TEMPLATE = """\
# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   {year}-12-{day:02d}

import aoc


class Solution(aoc.Puzzle):
    day = {day}
    year = {year}

    def solution_1(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]

    def solution_2(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
"""


def main():
    now = datetime.datetime.now()

    parser = ArgumentParser()
    parser.add_argument("-d", "--day", type=int, default=now.day)
    parser.add_argument("-y", "--year", type=int, default=now.year)
    args = parser.parse_args(sys.argv[1:])

    year, day = args.year, args.day

    path = Path(str(year), f"day{day:02d}")
    path.mkdir(parents=True, exist_ok=True)

    file = path / "solution.py"
    src = TEMPLATE.format(day=day, year=year)
    file.write_text(src)

    file = path / "__init__.py"
    file.touch()


if __name__ == "__main__":
    main()
