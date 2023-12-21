# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-21

import matplotlib.pyplot as plt
import numpy as np

import aoc

DIRECTIONS = (0, 1), (1, 0), (0, -1), (-1, 0)


def parse_input(data: str):
    lines = data.splitlines(keepends=False)
    shape = len(lines), len(lines[0])
    start = 0, 0
    rocks = set()
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == "#":
                rocks.add((r, c))
            elif char == "S":
                start = r, c
    assert shape[0] == shape[1]
    return shape[0], rocks, start


def get_positions(n, rocks, start, n_steps):
    positions = {start}
    for _ in range(n_steps):
        new_positions = set()
        for curr in positions:
            for dr, dc in DIRECTIONS:
                pos = curr[0] + dr, curr[1] + dc
                if 0 <= pos[0] < n and 0 <= pos[1] < n and pos not in rocks:
                    new_positions.add(pos)
        positions = new_positions
    return positions


def fill_garden(n, rocks, positions):
    pos = np.array(list(positions), dtype=int)
    rocks = np.array(list(rocks), dtype=int)
    arr = np.zeros((n, n), dtype=np.int8)
    for r, c in rocks:
        arr[r, c] = 2
    for r, c in pos:
        arr[r, c] = 1
    return arr.T


def plot_gardens(n, rocks, plots):
    gardens = {}
    for (i, j), plot in plots.items():
        gardens[(i, j)] = fill_garden(n, rocks, plot)

    fig, axs = plt.subplots(5, 5, figsize=(12, 12))
    xc, yc = 2, 2
    for ax in axs.flat:
        ax.axis("off")
    for (x, y), g in gardens.items():
        axs[yc + y, xc + x].imshow(g)
    plt.show()


class Solution(aoc.Puzzle):
    day = 21
    year = 2023
    test_solution_idx_1 = -4
    test_solution_idx_2 = -3

    def solution_1(self, data: str):
        n, rocks, start = parse_input(data)
        n_steps = 6 if self.is_test else 64
        return len(get_positions(n, rocks, start, n_steps))

    def solution_2(self, data: str):
        """Quadratic interpolation did *not* work for my input, so i am using the
        'diamond' method. This method is based on the observation that the garden
        is filled in a diamond shape.
        Observations:

        - S is at the center of the grid in position (65,65)
        - The grid dimension is 131x131
        - The external border of the grid is empty (no obstacles)
        - In 64 steps one can barely reach the border of the grid!
          The first out-of-grid positions arrive for 66 steps.

        The first out-of-grid positions are in the middle of the external
        borders of the first "external" grids.
        """
        n, rocks, start = parse_input(data)
        n_steps = 26501365
        hn = n // 2  # 65
        plot = False

        # fully filled grids
        odd = get_positions(n, rocks, start, n_steps=3 * n)  # center
        even = get_positions(n, rocks, start, n_steps=2 * n)  # cross around center
        # diamonds extremes (corners)
        top = get_positions(n, rocks, start=(0, hn), n_steps=n - 1)
        bot = get_positions(n, rocks, start=(n - 1, hn), n_steps=n - 1)
        lef = get_positions(n, rocks, start=(hn, 0), n_steps=n - 1)
        rig = get_positions(n, rocks, start=(hn, 130), n_steps=n - 1)
        # smaller lateral grids
        lef_bot_s = get_positions(n, rocks, start=(n - 1, 0), n_steps=hn - 1)
        rig_bot_s = get_positions(n, rocks, start=(0, 0), n_steps=hn - 1)
        lef_top_s = get_positions(n, rocks, start=(n - 1, n - 1), n_steps=hn - 1)
        rig_top_s = get_positions(n, rocks, start=(0, 130), n_steps=hn - 1)
        # larger lateral grids
        lef_bot_b = get_positions(n, rocks, start=(n - 1, 0), n_steps=n + hn - 1)
        rig_bot_b = get_positions(n, rocks, start=(0, 0), n_steps=n + hn - 1)
        lef_top_b = get_positions(n, rocks, start=(n - 1, n - 1), n_steps=n + hn - 1)
        rig_top_b = get_positions(n, rocks, start=(0, n - 1), n_steps=n + hn - 1)

        if plot:
            plots = dict()
            plots[(0, 0)] = odd

            plots[(1, 0)] = even
            plots[(-1, 0)] = even
            plots[(0, 1)] = even
            plots[(0, -1)] = even

            plots[(2, 0)] = top
            plots[(-2, 0)] = bot
            plots[(0, 2)] = lef
            plots[(0, -2)] = rig

            plots[(-2, 1)] = lef_bot_s
            plots[(-1, 2)] = lef_bot_s
            plots[(1, 2)] = rig_bot_s
            plots[(2, 1)] = rig_bot_s

            plots[(-2, -1)] = lef_top_s
            plots[(-1, -2)] = lef_top_s
            plots[(2, -1)] = rig_top_s
            plots[(1, -2)] = rig_top_s

            plots[(-1, 1)] = lef_bot_b
            plots[(-1, -1)] = lef_top_b
            plots[(1, 1)] = rig_bot_b
            plots[(1, -1)] = rig_top_b

            plots[(-2, 2)] = []
            plots[(2, -2)] = []
            plots[(2, 2)] = []
            plots[(-2, -2)] = []

            plot_gardens(n, rocks, plots)

        romb_width = (n_steps - hn) // n

        nfull_odd = (romb_width // 2 * 2 - 1) ** 2
        nfull_even = (romb_width // 2 * 2) ** 2

        nodd = len(odd)
        neven = len(even)

        ncorners = len(top) + len(bot) + len(lef) + len(rig)
        nsmall = len(lef_bot_s) + len(rig_bot_s) + len(lef_top_s) + len(rig_top_s)
        nlarge = len(lef_bot_b) + len(lef_top_b) + len(rig_bot_b) + len(rig_top_b)

        total_full = nfull_odd * nodd + nfull_even * neven
        total = total_full + romb_width * nsmall + (romb_width - 1) * nlarge + ncorners

        return total


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(puzzle_only=True)
