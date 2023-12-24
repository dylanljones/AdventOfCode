# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-24

from itertools import combinations

import numpy as np
import numpy.linalg as la

import aoc


def parse_input(data: str):
    stones = list()
    for line in data.splitlines(keepends=False):
        pos, vel = line.split(" @ ")
        pos = tuple(map(int, pos.split(", ")))
        vel = tuple(map(int, vel.split(", ")))
        stones.append((pos, vel))
    return stones


def intersection(s1, s2):
    """Solve for the intersection of two lines in 2D space

    The lines are defined by their position and velocity vectors:
    .. math::
        \vec{r}_1(t) = \vec{p}_1 + t_1 \vec{v}_1 \\
        \vec{r}_2(t) = \vec{p}_2 + t_2 \vec{v}_2

    We solve for the parameters $t_1$ and $t_2$ such that the two lines intersect:
    .. math::
        \vec{r}_1(t_1) = \vec{r}_2(t_2)

    If the lines are parallel, no intersection is found. If one of the times
    is negative, the intersection is in the past and is discarded.
    """
    p1, v1 = s1
    p2, v2 = s2
    if v1[0] / v2[0] == v1[1] / v2[1]:
        return 0, 0  # Parallel, no intersection
    # Solve for parameters t1 and t2
    num = p2[1] - p1[1] + (p1[0] - p2[0]) / v2[0] * v2[1]
    denom = v1[1] - v1[0] * v2[1] / v2[0]
    t1 = num / denom
    t2 = (p1[0] - p2[0] + t1 * v1[0]) / v2[0]
    if t1 < 0 or t2 < 0:
        return 0, 0  # In the past
    # Calculate intersection points from btoh lines
    x1, y1 = p1[0] + t1 * v1[0], p1[1] + t1 * v1[1]
    x2, y2 = p2[0] + t2 * v2[0], p2[1] + t2 * v2[1]
    # Check if intersection is valid
    rtol = 1e-8
    assert abs(x1 - x2) / abs(x1) < rtol and abs(y1 - y2) / abs(y2) < rtol
    return x1, y1


def cross_matrix(v):
    """Skew-symmetric matrix for cross product"""
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])


def find_rock_solution(stones, i=0, j=1, k=2):
    r"""Find the solution for the rock to hit all hail stones

    for the rock with p_0 and v_0, the hail stones with p_i and v_i, it follows that

    .. math::
        p_0 + t_i v_0 = p_i + t_i v_i  ->  (p_0 - p_i) = -t_i (v_0 - v_i)

    applying the cross product with (v_0 - v_i) on both sides yields

    .. math::
        (p_0 - p_i) x (v_0 - v_i) = -t_i (v_0 - v_i) x (v_0 - v_i) = 0

    We need six equations to solve for the six unknowns in p_0 and v_0. We can
    use the first three stones to solve the equations above with i=0, i=1 and i=0, i=2.
    The cross product can be written as a skew-symmetric matrix multiplication.
    The total system of equations is then

    .. math::
        \begin{pmatrix}
            V_{01} & P_{01} \\
            V_{02} & P_{02}
        \end{pmatrix}
        \begin{pmatrix}
            x \\ y \\ z \\ v_x \\ v_y \\ v_z
        \end{pmatrix}
        =
        \begin{pmatrix}
            B_1 \\ B_2
        \end{pmatrix}

    where the blocks $V_{ij}$ and $P_{ij}$ are the skew-symmetric matrices for

    .. math::
        V_{ij} = v_i - v_j  and P_{ij} = p_i - p_j

    and $B_i$ are the right hand sides of the equations:

    .. math::
        B_i = -p_0 x v_0 + p_i x v_i

    """
    p1, v1 = stones[i]
    p2, v2 = stones[j]
    p3, v3 = stones[k]
    p1, v1 = np.array(p1), np.array(v1)
    p2, v2 = np.array(p2), np.array(v2)
    p3, v3 = np.array(p3), np.array(v3)

    a11 = +cross_matrix(v1) - cross_matrix(v2)
    a21 = +cross_matrix(v1) - cross_matrix(v3)
    a12 = -cross_matrix(p1) + cross_matrix(p2)
    a22 = -cross_matrix(p1) + cross_matrix(p3)
    a = np.block([[a11, a12], [a21, a22]])

    b = np.zeros(6, np.float64)
    b[0:3] = -np.cross(p1, v1) + np.cross(p2, v2)
    b[3:6] = -np.cross(p1, v1) + np.cross(p3, v3)

    vec = la.solve(a, b)
    pos, vel = vec[:3], vec[3:]
    return np.round(pos), np.round(vel)


class Solution(aoc.Puzzle):
    day = 24
    year = 2023
    test_solution_idx_1 = -3
    test_solution_idx_2 = -2

    def solution_1(self, data: str):
        bounds = (7, 27) if self.is_test else (200000000000000, 400000000000000)
        stones = parse_input(data)
        n = 0
        for s1, s2 in combinations(stones, 2):
            x, y = intersection(s1, s2)
            if (bounds[0] <= x <= bounds[1]) and (bounds[0] <= y <= bounds[1]):
                n += 1
        return n

    def solution_2(self, data: str):
        stones = parse_input(data)
        pos, vel = find_rock_solution(stones)
        result = int(pos.sum())
        return result


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(puzzle_only=False)
