# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2022-12-19

import re

import aoc

RE_LINE = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore\. "
    r"Each clay robot costs (\d+) ore\. "
    r"Each obsidian robot costs (\d+) ore and (\d+) clay\. "
    r"Each geode robot costs (\d+) ore and (\d+) obsidian\."
)


def parse_input(data):
    if data.startswith("Blueprint 1:\n"):
        # Fix wrapped lines of example input
        data = data.replace("\n", "").replace("  ", " ")
        data = data.replace(".Blueprint", ".\nBlueprint")
    blueprints = dict()
    for line in data.splitlines(keepends=False):
        match = RE_LINE.match(line)
        blueprint = int(match.group(1))
        blueprints[blueprint] = {
            "ore": {"ore": int(match.group(2))},
            "clay": {"ore": int(match.group(3))},
            "obsidian": {"ore": int(match.group(4)), "clay": int(match.group(5))},
            "geode": {"ore": int(match.group(6)), "obsidian": int(match.group(7))},
        }
    return blueprints


class Blueprint:
    def __init__(self, id_, blueprint):
        self.id = id_
        self.costs = blueprint
        self.useful = {
            "ore": max(
                self.costs["clay"]["ore"],
                self.costs["obsidian"]["ore"],
                self.costs["geode"]["ore"],
            ),
            "clay": self.costs["obsidian"]["clay"],
            "obsidian": self.costs["geode"]["obsidian"],
            "geode": float("inf"),
        }

    def __repr__(self):
        return f"Blueprint {self.id}: {self.costs}"


class State:
    def __init__(self, robots=None, resources=None, ignored=None):
        self.robots = robots or {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        self.resources = resources or {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        self.ignored = ignored or list()

    def can_afford(self, cost):
        return all(self.resources[k] >= v for k, v in cost.items())

    def start_build(self, blueprint, robot):
        """Reduces the resources for building a robot"""
        costs = blueprint.costs[robot]
        for item, amount in costs.items():
            assert self.resources[item] >= amount
            self.resources[item] -= amount

    def end_build(self, robot):
        """Increases the robot count"""
        self.robots[robot] += 1

    def collect(self):
        for robot, amount in self.robots.items():
            self.resources[robot] += amount

    def copy(self):
        return State(self.robots.copy(), self.resources.copy(), self.ignored.copy())

    def __gt__(self, other):
        return self.resources["geode"] > other.resources["geode"]

    def __repr__(self):
        return f"Robots:    {self.robots}\nResources: {self.resources}\n"


def evaluate(blueprint, prior_states, timelimit=26):
    time_remaining = timelimit - len(prior_states)
    state = prior_states[-1]

    # determine options for what to build in the next state
    options = list()
    if time_remaining >= 0:
        # look for something affordable and useful and not ignored last time
        for robot, cost in blueprint.costs.items():
            if (
                state.robots[robot] < blueprint.useful[robot]
                and state.can_afford(cost)
                and robot not in state.ignored
            ):
                options.append(robot)
        # geodes before anything else, don't bother with other types at the end
        if "geode" in options:
            options = ["geode"]
        elif time_remaining < 1:
            options = []
        else:
            # cutting off plans that build resources more than 2 phases back
            if (
                state.robots["clay"] > 3
                or state.robots["obsidian"]
                or "obsidian" in options
            ) and "ore" in options:
                options.remove("ore")
            if (
                state.robots["obsidian"] > 3
                or state.robots["geode"]
                or "geode" in options
            ) and "clay" in options:
                options.remove("clay")
        # add new resources
        next_state = state.copy()
        next_state.collect()

        # the 'do nothing' option
        next_state.ignored += options
        results = [evaluate(blueprint, prior_states + [next_state], timelimit)]
        # the rest of the options
        for opt in options:
            next_state_opt = next_state.copy()
            next_state_opt.ignored = []
            next_state_opt.robots[opt] += 1
            next_state_opt.start_build(blueprint, opt)
            results.append(
                evaluate(blueprint, prior_states + [next_state_opt], timelimit)
            )

        return max(results)

    return prior_states[-1].resources["geode"], prior_states


class Solution(aoc.Puzzle):
    day = 19
    year = 2022

    def solution_1(self, data: str):
        blueprints = parse_input(data)
        result = 0
        for id_, blueprint in blueprints.items():
            blueprint = Blueprint(id_, blueprint)
            states = [State()]
            x = evaluate(blueprint, states, 24)
            result += x[0] * blueprint.id
        return result

    def solution_2(self, data: str):
        blueprints = parse_input(data)
        keys = list(blueprints.keys())
        if len(keys) > 3:
            keys = keys[:3]
        blueprints = {k: blueprints[k] for k in keys}
        result = 1
        for id_, blueprint in blueprints.items():
            blueprint = Blueprint(id_, blueprint)
            states = [State()]
            x = evaluate(blueprint, states, 32)
            result *= x[0]
        return result


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(puzzle_only=True)
