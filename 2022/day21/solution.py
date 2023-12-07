# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2022-12-21

import re

import aoc

MATH_OP = re.compile(r"(\w+) ([+\-*/]) (\w+)")


def parse_input(data: str) -> dict:
    lines = [line.strip() for line in data.splitlines(keepends=False)]
    monkeys = dict()
    for line in lines:
        name, text = line.split(": ")
        number, operation = None, None
        if text.isdigit():
            number = int(text)
        else:
            match = MATH_OP.match(text)
            operation = match.groups()
        monkeys[name] = [number, operation]
    return monkeys


def solve_monkey(monkeys: dict, name: str) -> float:
    monkey = monkeys[name]
    if monkey[0] is not None:
        return monkey[0]
    a, op, b = monkey[1]
    num_a = solve_monkey(monkeys, a)
    num_b = solve_monkey(monkeys, b)
    return eval(f"{num_a} {op} {num_b}")


class Solution(aoc.Puzzle):
    day = 21
    year = 2022
    test_answer_idx_1 = -2
    test_answer_idx_2 = -4

    def solution_1(self, data: str):
        monkeys = parse_input(data)
        result = solve_monkey(monkeys, "root")
        return int(result)

    def solution_2(self, data: str):
        monkeys = parse_input(data)
        _, (a, _, b) = monkeys["root"]
        monkeys["root"] = [None, (a, "-", b)]

        prev_humn = monkeys["humn"][0]
        prev_error = abs(solve_monkey(monkeys, "root"))

        # First guess for our number
        humn = 0
        monkeys["humn"][0] = humn
        error = abs(solve_monkey(monkeys, "root"))

        # Learning rate of the minimization algorithm (gradient descent)
        rate = 0.1
        while error > 1e-1:
            # Calculate the gradient between the previous two guesses
            try:
                grad = (humn - prev_humn) / (error - prev_error)
            except ZeroDivisionError:
                grad = 1 if error < prev_error else -1

            # Update previous guesses
            prev_humn = humn
            prev_error = error

            # Update our guess
            humn -= rate * grad * error
            monkeys["humn"][0] = humn

            # Calculate the error of our new guess
            error = abs(solve_monkey(monkeys, "root"))

        result = round(humn)
        return result


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
