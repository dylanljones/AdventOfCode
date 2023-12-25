# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import re

import aoc

RE_LINE = re.compile(
    r"Sensor at x=(.*?), y=(.*?): closest beacon is at x=(.*?), y=(.*?)$"
)

Point = tuple[int, int]


def manhattan(a: Point, b: Point) -> int:
    """Return the Manhattan distance"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Sensor:
    """A sensor has its center position and its exclusion range"""

    def __init__(self, pos: Point, beacon: Point) -> None:
        self.position: Point = pos
        self.beacon: Point = beacon
        self.range: int = manhattan(beacon, self.position)

    def in_range(self, point: Point) -> bool:
        """Check if point is int the sensor's exclusion range"""
        return manhattan(self.position, point) <= self.range


def parse_input(data: str) -> list[Sensor]:
    sensors = list()
    for line in data.splitlines():
        match = RE_LINE.match(line)
        pos = int(match[1]), int(match[2])
        beacon = int(match[3]), int(match[4])
        sensors.append(Sensor(pos, beacon))
    return sensors


def range_overlap(a: Point, b: Point) -> bool:
    a_in_b = b[0] <= a[0] <= b[1] or b[0] <= a[0] <= b[1]
    b_in_a = a[0] <= b[0] <= a[1] or a[0] <= b[0] <= a[1]
    return a_in_b or b_in_a


def add_range(ranges: list[Point], x0: int, x1: int) -> list[Point]:
    new_ranges = list()
    additional = list()
    for a, b in ranges:
        if range_overlap((a, b), (x0, x1)):
            additional.append((min(a, x0), max(b, x1)))
        else:
            new_ranges.append((a, b))
    if len(additional):
        mins = min(map(lambda tup: tup[0], additional))
        maxe = max(map(lambda tup: tup[1], additional))
        new_ranges.append((mins, maxe))
    else:
        new_ranges.append((x0, x1))
    return new_ranges


def remove_range(ranges: list[Point], x: int) -> list[Point]:
    new_ranges = list()
    for a, b in ranges:
        if a < x < b:
            new_ranges.append((a, x - 1))
            new_ranges.append((x + 1, b))
        elif x == a:
            new_ranges.append((x + 1, b))
        elif x == b:
            new_ranges.append((a, x - 1))
        else:
            new_ranges.append((a, b))
    return new_ranges


def get_unavailable(sensors: list[Sensor], y: int) -> list[Point]:
    ranges = list()
    occupied = list()
    for sensor in sensors:
        distance = sensor.range - abs(y - sensor.position[1])
        if distance <= 0:
            continue

        if sensor.beacon[1] == y:
            occupied.append(sensor.beacon[0])
        if sensor.position[1] == y:
            occupied.append(sensor.position[0])

        x0 = sensor.position[0] - distance
        x1 = sensor.position[0] + distance
        ranges = add_range(ranges, x0, x1)

    for pos in occupied:
        ranges = remove_range(ranges, pos)

    return ranges


def is_free(sensors: list[Sensor], point: Point) -> bool:
    """Check if point is outside the exclusion range of all sensors"""
    for sensor in sensors:
        if sensor.in_range(point):
            return False
    return True


def find_beacon(sensors: list[Sensor], ymax: int) -> Point:
    # Calculate all of the lines that pass along the confines of each sensor's
    # exclusion zone. A line is defined as y=mx+q where m is either 1 or -1.
    lines = dict()
    for sensor in sensors:
        top_asc = True, sensor.position[1] - sensor.range - 1 - sensor.position[0]
        top_des = False, sensor.position[1] - sensor.range - 1 + sensor.position[0]
        bot_asc = True, sensor.position[1] + sensor.range + 1 - sensor.position[0]
        bot_des = False, sensor.position[1] + sensor.range + 1 + sensor.position[0]
        for line in [top_asc, top_des, bot_asc, bot_des]:
            # Number of occurrences of each line
            if line in lines:
                lines[line] += 1
            else:
                lines[line] = 1

    # Only keep the lines that appear at least two times.
    # A single free spot lies where 4 lines intersect (2 rising and 2 descending)
    asc_lines, des_lines = list(), list()
    for line, count in lines.items():
        if count > 1:
            if line[0]:
                des_lines.append(line[1])
            else:
                asc_lines.append(line[1])
    # Calculate the intersections between all the rising and descending lines
    points = list()
    for asc_q in asc_lines:
        for des_q in des_lines:
            x = (asc_q - des_q) // 2
            y = x + des_q
            points.append((x, y))

    # Check which of the intersections is the free point
    for p in points:
        if 0 <= p[1] <= ymax and 0 <= p[0] <= ymax and is_free(sensors, p):
            return p

    raise ValueError("No beacon found")


class Solution(aoc.Puzzle):
    year = 2022
    day = 15
    test_solution_idx_1 = -2

    def solution_1(self, data: str):
        y = 10 if self.is_test else 2_000_000
        sensors = parse_input(data)
        count = 0
        for a, b in get_unavailable(sensors, y):
            count += b - a + 1
        return count

    def solution_2(self, data: str):
        ymax = 20 if self.is_test else 4_000_000
        sensors = parse_input(data)
        p = find_beacon(sensors, ymax)
        return int(4_000_000 * p[0] + p[1])


def main():
    puzzle = Solution()
    puzzle.run(puzzle_only=False)


if __name__ == "__main__":
    main()
