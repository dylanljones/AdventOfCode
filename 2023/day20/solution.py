# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-20

import math

import aoc

BROADCAST = 0
FLIPFLOP = 1
CONJUNCTION = 2

LOW = False
HIGH = True


class Module:
    def __init__(self, name, mtype, dst):
        self.name = name
        self.type = mtype
        self.dst = dst

        self.state = LOW
        self.inputs = dict()

    def __repr__(self):
        return f"Module(name={self.name}, mtype={self.type}, dst={self.dst})"


def parse_input(data: str):
    modules = dict()

    for line in data.splitlines():
        name, destinations = line.split(" -> ")
        if name == "broadcaster":
            mtype = BROADCAST
        else:
            mtype, name = name[0], name[1:]
            if mtype == "%":
                mtype = FLIPFLOP
            elif mtype == "&":
                mtype = CONJUNCTION
            else:
                raise ValueError(f"Unknown module type: {mtype}")
        destinations = destinations.split(", ")
        mod = Module(name, mtype, destinations)
        modules[mod.name] = mod

    # Add inputs
    for name, mod in modules.items():
        for name2, mod2 in modules.items():
            if name in mod2.dst:
                mod.inputs[name2] = LOW

    return modules


def count_pulses(modules: dict):
    start = ("broadcaster", LOW)
    low, high = 0, 0
    for _ in range(1000):
        queue = [start]
        while queue:
            src, pulse = queue.pop(0)

            if pulse == LOW:
                low += 1
            else:
                high += 1

            dst = list()
            output = pulse

            if src in modules and modules[src].type == BROADCAST:
                dst = modules[src].dst
            elif src in modules and modules[src].type == FLIPFLOP and pulse == LOW:
                output = modules[src].state = not modules[src].state
                dst = modules[src].dst
            elif src in modules and modules[src].type == CONJUNCTION:
                output = not all(modules[src].inputs.values())
                dst = modules[src].dst

            for name in dst:
                queue.append((name, output))
                if name in modules and modules[name].type == CONJUNCTION:
                    modules[name].inputs[src] = output

    return low * high


def count_pulse_cycles(modules: dict):
    start = ("broadcaster", LOW)

    main_mod = ""
    for mod in modules.values():
        if "rx" in mod.dst:
            main_mod = mod.name
            break

    cycles = {name: 0 for name in modules[main_mod].inputs.keys()}
    count = 0
    while not all(cycles.values()):
        count += 1
        queue = [start]
        while queue:
            src, pulse = queue.pop(0)

            dst = list()
            output = pulse

            if src in modules and modules[src].type == BROADCAST:
                dst = modules[src].dst
            elif src in modules and modules[src].type == FLIPFLOP and pulse == LOW:
                output = modules[src].state = not modules[src].state
                dst = modules[src].dst
            elif src in modules and modules[src].type == CONJUNCTION:
                output = not all(modules[src].inputs.values())
                dst = modules[src].dst

                if src == main_mod and any(modules[src].inputs.values()):
                    for n in modules[src].inputs:
                        if modules[src].inputs[n]:
                            cycles[n] = count

            for name in dst:
                queue.append((name, output))
                if name in modules and modules[name].type == CONJUNCTION:
                    modules[name].inputs[src] = output

    return math.prod(cycles.values())


class Solution(aoc.Puzzle):
    day = 20
    year = 2023
    test_solution_idx_1 = -6

    def solution_1(self, data: str):
        modules = parse_input(data)
        return count_pulses(modules)

    def solution_2(self, data: str):
        modules = parse_input(data)
        return count_pulse_cycles(modules)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(puzzle_only=True)
