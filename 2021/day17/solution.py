# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-26

import aoc

Point = tuple[int, ...]


def parse_input(data: str) -> tuple[Point, Point]:
    xr, yr = data.split(": ")[1].split(", ")
    xlim = tuple(map(int, xr.replace("x=", "").split("..")))
    ylim = tuple(map(int, yr.replace("y=", "").split("..")))
    return xlim, ylim


def hits_target(target: tuple[Point, Point], vel: Point) -> bool:
    x, y = 0, 0
    vx, vy = vel
    xlim, ylim = target
    while True:
        if x > xlim[1]:
            return False
        if vx == 0 and not (xlim[0] <= x <= xlim[1]):
            return False
        if vy < 0 and y < ylim[0]:
            return False

        if xlim[0] <= x <= xlim[1] and ylim[0] <= y <= ylim[1]:
            return True

        x += vx
        y += vy
        if vx > 0:
            vx -= 1
        vy -= 1


class Solution(aoc.Puzzle):
    day = 17
    year = 2021
    test_solution_idx_1 = -4
    test_solution_idx_2 = -2

    def solution_1(self, data: str):
        xlim, ylim = parse_input(data)
        vy = abs(ylim[0]) - 1
        return round(((0.5 + vy) ** 2) / 2)

    def solution_2(self, data: str):
        target = xlim, ylim = parse_input(data)
        y_max = max(abs(ylim[0]), abs(ylim[1]))
        velocities = 0
        for vx in range(xlim[1] + 1):
            for vy in range(-y_max, y_max + 1):
                velocities += hits_target(target, (vx, vy))
        return velocities


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
