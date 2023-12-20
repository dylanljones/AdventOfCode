# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-19

import math
import re
from operator import gt, lt

import aoc

RE_WORK = re.compile(r"(\w+)\{([^}]+)\}")
RE_COND = re.compile(r"(\w+)(<|>)(\d+):(\w+)")
RE_PART = re.compile(r"x=(\d+),m=(\d+),a=(\d+),s=(\d+)")

PARTS = ["x", "m", "a", "s"]
OPERATORS = {">": gt, "<": lt}
MIN = 1
MAX = 4000


def parse_input(data: str):
    part1, part2 = data.split("\n\n")
    workflows = dict()
    parts = list()
    for name, rules in RE_WORK.findall(part1):
        conditional = RE_COND.findall(rules)
        final = rules.split(",")[-1]
        workflows[name] = conditional + [final]
    for vals in RE_PART.findall(part2):
        parts.append(dict(zip(PARTS, (int(x) for x in vals))))
    return workflows, parts


def run_workflows(workflows, parts):
    accepted = 0
    for part in parts:
        curr = "in"
        while curr not in ("A", "R"):
            for p, op, val, target in workflows[curr][:-1]:
                if OPERATORS[op](part[p], int(val)):
                    curr = target
                    break
            else:
                curr = workflows[curr][-1]
        if curr == "A":
            accepted += sum(part.values())
    return accepted


def get_combinations(workflows):
    start = ("in", {k: (MIN, MAX) for k in PARTS})
    queue = [start]
    accepted = 0
    while queue:
        curr, intervals = queue.pop()
        if curr in ("A", "R"):
            if curr == "A":
                accepted += math.prod(b - a + 1 for a, b in intervals.values())
            continue
        for p, op, val, res in workflows[curr][:-1]:
            val = int(val)

            a, b = intervals[p]
            if (op == ">" and val >= b) or (op == "<" and val <= a):
                continue

            if (op == ">" and val < a) or (op == "<" and val > b):
                queue.append((res, intervals))
                break

            if op == ">":
                transfer = (val + 1, b)
                passthrough = (a, val)
            else:
                transfer = (a, val - 1)
                passthrough = (val, b)

            intervals[p] = passthrough
            intervals2 = intervals.copy()
            intervals2[p] = transfer
            queue.append((res, intervals2))

        else:
            queue.append((workflows[curr][-1], intervals))

    return accepted


class Solution(aoc.Puzzle):
    day = 19
    year = 2023

    def solution_1(self, data: str):
        workflows, parts = parse_input(data)
        n = run_workflows(workflows, parts)
        return n

    def solution_2(self, data: str):
        workflows, _ = parse_input(data)
        n = get_combinations(workflows)
        return n


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
