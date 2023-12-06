# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import os
import re

import numpy as np

import aoc

RE_LINE = re.compile(
    r"Sensor at x=(.*?), y=(.*?): closest beacon is at x=(.*?), y=(.*?)$"
)


def parse_data(data: str):
    rows = list()
    for line in data.splitlines():
        match = RE_LINE.match(line)
        sensor = complex(int(match[1]), int(match[2]))
        beacon = complex(int(match[3]), int(match[4]))
        rows.append((sensor, beacon))
    return np.array(rows)


def manhatten(pos1: complex, pos2: complex):
    diff = pos1 - pos2
    return np.abs(diff.real) + np.abs(diff.imag)


def get_edges(pos, distance):
    top_y = (pos + 1j * (distance + 0)).imag
    bot_y = (pos - 1j * (distance + 0)).imag
    x = pos.real
    yield pos - distance
    yield pos + distance
    for i in range(int(distance)):
        yield complex(x + i, top_y - i)
        yield complex(x - i, top_y - i)
        yield complex(x + i, bot_y + i)
        yield complex(x - i, bot_y + i)


def in_range(p, limits):
    return (limits[0] <= p.real <= limits[1]) and (limits[0] <= p.imag <= limits[1])


class Solution(aoc.Puzzle):
    test_answer_idx_1 = -2
    ROWS = [10, 2000000]
    LIMS = [[0, 20], [0, 4_000_000]]

    def __init__(self):
        super().__init__(2022, 15, root=os.path.dirname(__file__))

    def solution_1(self, data: str):
        positions = parse_data(data)
        sensors, beacons = positions.T
        distances = manhatten(sensors, beacons)

        x0 = np.median(sensors.real).astype(int)
        y = self.ROWS[self.runs_sol1]

        checked = list()
        start = complex(int(x0), y)
        count = 0
        if np.any(manhatten(sensors, start) <= distances) and start not in beacons:
            count += 1
            checked.append(start)

        max_dist = np.max(distances)
        step = 0
        while True:
            step += 1
            p1 = start - step
            p2 = start + step
            dists_p1 = manhatten(sensors, p1)  # Distances from point 1 to sensors
            dists_p2 = manhatten(sensors, p2)  # Distances from point 2 to sensors
            # Stop if points are far away enough
            if np.min(dists_p1) > max_dist and np.min(dists_p2) > max_dist:
                break
            # Add points if it is in the radius of any sensor
            if np.any(dists_p1 <= distances) and p1 not in beacons:
                count += 1
            if np.any(dists_p2 <= distances) and p2 not in beacons:
                count += 1
        return count

    @staticmethod
    def find_beacon(positions, limits):
        sensors, beacons = positions.T
        distances = manhatten(sensors, beacons)

        for i, (sens, beac) in enumerate(positions):
            print(f"\rChecking sensor {i+1}/{len(sensors)}", end="", flush=True)
            dist = distances[i]
            # Check points one step further away than nearest beacon
            for p in get_edges(sens, dist + 1):
                if in_range(p, limits) and p not in beacons:
                    # Check if point is in range of other beacon
                    for j, (sens2, beac2) in enumerate(positions):
                        dist2 = distances[j]
                        if manhatten(sens2, p) <= dist2:
                            break
                    else:
                        # If it is not, we have found the distress beacon
                        print(f": Found distress beacon at ({p.real}, {p.imag})!")
                        return p

    def solution_2(self, data: str):
        positions = parse_data(data)
        limits = self.LIMS[self.runs_sol2]
        p = self.find_beacon(positions, limits)
        result = int(4_000_000 * p.real + p.imag)
        return result


def main():
    puzzle = Solution()
    puzzle.run()


if __name__ == "__main__":
    main()
