# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-19

from dataclasses import dataclass
from operator import gt, lt
from typing import Callable

import aoc

PARTS = ["x", "m", "a", "s"]
MIN = 1
MAX = 4000


@dataclass
class Rule:
    target: str
    part: str = None
    opstr: str = None
    operator: Callable = None
    value: int = None

    @property
    def has_condition(self):
        return self.part is not None

    def get_target(self, parts: dict) -> str:
        if self.operator(parts[self.part], self.value):
            return self.target
        return ""

    def num_accepted(self, parts: list) -> dict:
        nums = dict()
        for part in parts:
            if self.has_condition:
                if self.part == part:
                    if self.opstr == ">":
                        nums[part] = MAX - self.value
                    else:
                        nums[part] = self.value - MIN

            elif self.target == "R":
                nums[part] = 0
            else:
                nums[part] = MAX - MIN + 1

        return nums


def parse_input(data: str):
    part1, part2 = data.split("\n\n")
    rules = dict()
    for line in part1.splitlines(keepends=False):
        name, items = line.split("{")
        name = name.strip()
        items = items[:-1].split(",")
        _rules = list()
        for item in items:
            if ":" in item:
                cond, target = item.split(":")
                opstr = ">" if ">" in cond else "<"
                op = gt if opstr == ">" else lt
                part, val = cond.split(opstr)
                rule = Rule(target, part, opstr, op, int(val))
            else:
                rule = Rule(item)
            _rules.append(rule)
        rules[name] = _rules

    parts = list()
    for line in part2.splitlines(keepends=False):
        line = line.strip()[1:-1]
        _parts = dict()
        for item in line.split(","):
            part, val = item.split("=")
            _parts[part] = int(val)
        parts.append(_parts)

    return rules, parts


def run_workflows(rule_dict, part_dict):
    workflow = "in"
    path = [workflow]
    while True:
        rules = rule_dict[workflow]
        for rule in rules:
            if rule.has_condition:
                workflow = rule.get_target(part_dict)
            else:
                workflow = rule.target
            if workflow:
                break

        path.append(workflow)
        if workflow == "A":
            return True
        elif workflow == "R":
            return False


class Solution(aoc.Puzzle):
    day = 19
    year = 2023

    def solution_1(self, data: str):
        rules, parts = parse_input(data)
        result = 0
        for part in parts:
            accept = run_workflows(rules, part)
            if accept:
                result += sum(part.values())
        return result

    def solution_2(self, data: str):
        pass


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
