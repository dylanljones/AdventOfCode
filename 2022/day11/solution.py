# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones
import math
import os
import re
import aoc
from dataclasses import dataclass
from typing import Callable

RE_MONKEY = re.compile("Monkey (.*?):$")
RE_STARTING = re.compile("Starting items: (.*?)$")
RE_OPERATION = re.compile("Operation: (.*?)$")
RE_TEST = re.compile("Test: divisible by (.*?)$")
RE_TEST_TRUE = re.compile("If true: throw to monkey (.*?)$")
RE_TEST_FALSE = re.compile("If false: throw to monkey (.*?)$")


@dataclass
class Monkey:
    idx: int
    items: list
    operation: Callable
    div: int
    test_true: int
    test_false: int

    def get_dst(self, value):
        return self.test_true if value % self.div == 0 else self.test_false


def parse_monkey(lines):
    line = lines.pop(0)
    idx = int(RE_MONKEY.match(line).group(1))

    line = lines.pop(0)
    items = [int(x) for x in RE_STARTING.match(line).group(1).split(", ")]

    line = lines.pop(0)
    op = RE_OPERATION.match(line).group(1).strip()
    if op == "new = old * old":

        def fn(x):
            return x * x

    elif " * " in op:
        val = int(op.split(" ")[-1])

        def fn(x):
            return x * val

    else:
        val = int(op.split(" ")[-1])

        def fn(x):
            return x + val

    line = lines.pop(0)
    test = int(RE_TEST.match(line).group(1))
    line = lines.pop(0)
    test_true = int(RE_TEST_TRUE.match(line).group(1))
    line = lines.pop(0)
    test_false = int(RE_TEST_FALSE.match(line).group(1))

    return Monkey(idx, items, fn, test, test_true, test_false)


def parse_monkeys(data):
    lines = [line.strip() for line in data.splitlines(keepends=False)]
    monkeys = list()
    while lines:
        monkeys.append(parse_monkey(lines))
        if lines:
            lines.pop(0)
    return monkeys


class Solution(aoc.Puzzle):
    def __init__(self):
        super().__init__(2022, 11, root=os.path.dirname(__file__))

    def solution_1(self, data: str):
        num_rounds = 20
        monkeys = parse_monkeys(data)
        counts = [0] * len(monkeys)
        for r in range(num_rounds):
            for i, monkey in enumerate(monkeys):
                counts[i] += len(monkey.items)
                for lvl in monkey.items[:]:
                    new = monkey.operation(lvl) // 3
                    monkeys[monkey.get_dst(new)].items.append(new)
                monkey.items.clear()

        counts.sort()
        return counts[-1] * counts[-2]

    def solution_2(self, data: str):
        num_rounds = 10_000
        monkeys = parse_monkeys(data)
        counts = [0] * len(monkeys)
        div = math.prod(monkey.div for monkey in monkeys)

        for r in range(num_rounds):
            for i, monkey in enumerate(monkeys):
                counts[i] += len(monkey.items)
                for lvl in monkey.items[:]:
                    new = monkey.operation(lvl) % div
                    monkeys[monkey.get_dst(new)].items.append(new)
                monkey.items.clear()
        counts.sort()
        return counts[-1] * counts[-2]


def main():
    puzzle = Solution()
    puzzle.run(test_only=False, text=False)


if __name__ == "__main__":
    main()
