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
        0             & v_{0z}-v_{1z} & v_{1y}-v_{0y} &       0 & z_1-z_0 & y_0-y_1 \\
        v_{1z}-v_{0z} &            0  & v_{0x}-v_{1x} & z_0-z_1 &       0 & x_1-x_0 \\
        v_{0y}-v_{1y} & v_{1x}-v_{0x} &             0 &       0 & y_1-y_0 & x_0-x_1 \\
                    0 & v_{0z}-v_{2z} & v_{2y}-v_{0y} &       0 & z_2-z_0 & y_0-y_2 \\
        v_{2z}-v_{0z} &             0 & v_{0x}-v_{2x} & z_0-z_2 &       0 & x_2-x_0 \\
        v_{0y}-v_{2y} & v_{2x}-v_{0x} &             0 & y_2-y_0 & x_0-x_2 &       0
        \end{pmatrix}
        \begin{pmatrix}
            x \\ y \\ z \\ v_x \\ v_y \\ v_z
        \end{pmatrix}
        =
        \begin{pmatrix}
            (y_0 v_{0z} - v_{0y} z_0) - (y_1 v_{1z} - v_{1y} z_1) \\
            (z_0 v_{0x} - v_{0z} x_0) - (z_1 v_{1x} - v_{1z} x_1) \\
            (x_0 v_{0y} - v_{0x} y_0) - (x_1 v_{1y} - v_{1x} y_1) \\
            (y_0 v_{0z} - v_{0y} z_0) - (y_2 v_{2z} - v_{2y} z_2) \\
            (z_0 v_{0x} - v_{0z} x_0) - (z_2 v_{2x} - v_{2z} x_2) \\
            (x_0 v_{0y} - v_{0x} y_0) - (x_2 v_{2y} - v_{2x} y_2)
        \end{pmatrix}
    """
    (x0, y0, z0), (vx0, vy0, vz0) = stones[i]
    (x1, y1, z1), (vx1, vy1, vz1) = stones[j]
    (x2, y2, z2), (vx2, vy2, vz2) = stones[k]

    a = np.zeros((6, 6), np.float64)
    b = np.zeros(6, np.float64)

    a[0, 1] = vz0 - vz1
    a[0, 2] = vy1 - vy0
    a[0, 4] = z1 - z0
    a[0, 5] = y0 - y1

    a[1, 0] = vz1 - vz0
    a[1, 2] = vx0 - vx1
    a[1, 3] = z0 - z1
    a[1, 5] = x1 - x0

    a[2, 0] = vy0 - vy1
    a[2, 1] = vx1 - vx0
    a[2, 3] = y1 - y0
    a[2, 4] = x0 - x1

    a[3, 1] = vz0 - vz2
    a[3, 2] = vy2 - vy0
    a[3, 4] = z2 - z0
    a[3, 5] = y0 - y2

    a[4, 0] = vz2 - vz0
    a[4, 2] = vx0 - vx2
    a[4, 3] = z0 - z2
    a[4, 5] = x2 - x0

    a[5, 0] = vy0 - vy2
    a[5, 1] = vx2 - vx0
    a[5, 3] = y2 - y0
    a[5, 4] = x0 - x2

    b[0] = (y0 * vz0 - vy0 * z0) - (y1 * vz1 - vy1 * z1)
    b[1] = (z0 * vx0 - vz0 * x0) - (z1 * vx1 - vz1 * x1)
    b[2] = (x0 * vy0 - vx0 * y0) - (x1 * vy1 - vx1 * y1)
    b[3] = (y0 * vz0 - vy0 * z0) - (y2 * vz2 - vy2 * z2)
    b[4] = (z0 * vx0 - vz0 * x0) - (z2 * vx2 - vz2 * x2)
    b[5] = (x0 * vy0 - vx0 * y0) - (x2 * vy2 - vx2 * y2)

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
