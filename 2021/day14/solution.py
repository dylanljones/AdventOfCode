# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2021-12-13

from collections import Counter
from itertools import pairwise

import aoc

Rules = dict[tuple[str, ...], str]


def parse_input(data: str) -> tuple[str, Rules]:
    template, data = data.split("\n\n")
    rules = dict()
    for line in data.splitlines():
        pair, char = line.split(" -> ")
        rules[tuple(pair)] = char
    return template, rules


def mc_polymer_elements(tmplt: str, rules: Rules, nsteps: int) -> list[tuple[str, int]]:
    # Represent the polymer as a list of pairs and their counts
    pairs = Counter(pairwise(tmplt))

    # Insert new pairs according to the rules
    for _ in range(nsteps):
        new_pairs = Counter()
        for pair, num in pairs.items():
            if pair in rules:
                char = rules[pair]
                new_pairs[(pair[0], char)] += num
                new_pairs[(char, pair[1])] += num
            else:
                new_pairs[pair] += num
        pairs = new_pairs

    # Count the number of each element
    counts = Counter()
    for pair, num in pairs.items():
        counts[pair[0]] += num
    counts[tmplt[-1]] += 1  # Add the last element of the template to counts

    # Return the most common elements
    return counts.most_common()


class Solution(aoc.Puzzle):
    day = 14
    year = 2021

    def solution_1(self, data: str):
        template, rules = parse_input(data)
        mc = mc_polymer_elements(template, rules, nsteps=10)
        return mc[0][1] - mc[-1][1]

    def solution_2(self, data: str):
        template, rules = parse_input(data)
        mc = mc_polymer_elements(template, rules, nsteps=40)
        return mc[0][1] - mc[-1][1]


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run()
