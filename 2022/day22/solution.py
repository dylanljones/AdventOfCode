# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-08

import cmath
import re

import numpy as np

import aoc

EMTPY = 0
OPEN = 1
WALL = 2
TILES = {" ": EMTPY, ".": OPEN, "#": WALL}
DIRS = {"R": -1j, "L": 1j}
RE_CMD = re.compile(r"(\d+)([R|L])?")


def parse_input(data: str):
    data, cmds = data.split("\n\n")
    cmds = [(int(d), DIRS.get(r, 1)) for d, r in RE_CMD.findall(cmds)]
    data = data.split("\n")
    width = max(map(len, data))
    grid = np.array([[TILES[x] for x in list(f"{line:<{width}}")] for line in data])
    grid = np.pad(grid, 1, mode="constant", constant_values=0)
    return grid, cmds


def move(grid, trans, z, dz, dist):
    for _ in range(dist):
        nz = z + dz
        ndz = dz
        if (nz, dz) in trans:
            nz, ndz = trans[(nz, dz)]
        if grid[int(nz.real), int(nz.imag)] == WALL:
            break
        z, dz = nz, ndz
    return z, dz


def periodic_trans(grid):
    """Periodic transformation"""
    n, m = grid.shape
    trans = dict()
    top = np.argmax(grid != EMTPY, axis=0) + 1j * np.arange(m)
    bottom = n - 1 - np.argmax(grid[::-1] != EMTPY, axis=0) + 1j * np.arange(m)
    left = np.argmax(grid != EMTPY, axis=1) * 1j + np.arange(n)
    right = (m - 1 - np.argmax(grid[:, ::-1] != EMTPY, axis=1)) * 1j + np.arange(n)
    for to, bo in zip(top, bottom):
        trans[(to - 1, -1 + 0j)] = bo, -1 + 0j
        trans[(bo + 1, 1 + 0j)] = to, 1 + 0j
    for le, ri in zip(left, right):
        trans[(le - 1j, -1j)] = ri, -1j
        trans[(ri + 1j, 1j)] = le, 1j
    return trans


def cube_trans(grid):
    """Transformation for surface on cube"""
    at_forward_up = (-1, -1, -1), (0, 1, 0), (0, 0, 1)
    side = int(np.sqrt(np.sum(grid != EMTPY) / 6))
    z, dz = 1j * np.argmax(grid[1] != EMTPY), 1j
    corners, trans = dict(), dict()
    for _ in range(14):
        at, forward, up = np.array(at_forward_up)
        zs = z + np.arange(side) * dz
        key = tuple(at), tuple(at + 2 * forward)
        if key in corners:
            zs0, dz0 = corners[key]
            for z0, z1 in zip(zs0[::-1], zs):
                trans[(z0, dz0 * 1j)] = z1 - dz * 1j, dz / 1j
                trans[(z1, dz * 1j)] = z0 - dz0 * 1j, dz0 / 1j
        else:
            corners[key[::-1]] = zs, dz

        i = z + (side - 1j) * dz
        turn_right = grid[int(i.real), int(i.imag)] == EMTPY
        i = z + side * dz
        go_forward = grid[int(i.real), int(i.imag)] == EMTPY
        at += 2 * forward
        if turn_right:
            forward = np.cross(forward, up)
            z += (side - 1j) * dz
            dz *= -1j
        elif go_forward:
            s = at @ up
            forward, up = -s * up, s * forward
            z += side * dz
        else:
            up = np.cross(forward, up)
            forward = -forward
            z += (side - 1) * dz
            dz *= 1j
        at_forward_up = at, forward, up
    return trans


def walk_path(grid, cmds, trans):
    z, dz = 1 + 1j * np.argmax(grid[1] != EMTPY), 1j
    for step, rot in cmds:
        z, dz = move(grid, trans, z, dz, step)
        dz *= rot
    face = int(1 - 2 * cmath.phase(dz) / np.pi) % 4
    return z.real, z.imag, face


class Solution(aoc.Puzzle):
    day = 22
    year = 2022
    test_input_idx_2 = None

    def solution_1(self, data: str):
        grid, cmds = parse_input(data)
        r, c, f = walk_path(grid, cmds, periodic_trans(grid))
        return int(1000 * r + 4 * c + f)

    def solution_2(self, data: str):
        grid, cmds = parse_input(data)
        r, c, f = walk_path(grid, cmds, cube_trans(grid))
        return int(1000 * r + 4 * c + f)


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run()
