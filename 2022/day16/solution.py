# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones
import collections
import itertools
import re
import aoc

RE_LINE = re.compile(
    r"Valve (.*?) has flow rate=(.*?); tunnel.? lead.? to valve.? (.*?)$"
)


def parse_data(data: str):
    rates, tunnels = dict(), dict()
    for line in data.splitlines():
        match = RE_LINE.match(line)
        valve = match.group(1)
        rates[valve] = int(match.group(2))
        tunnels[valve] = match.group(3).split(", ")
    return rates, tunnels


class Solution(aoc.Puzzle):

    _file = __file__

    def __init__(self):
        super().__init__()

    @staticmethod
    def find_path(tunnels, a, b, maxlen=30):
        queue = [(a,)]
        while queue:
            path = queue.pop(0)
            if len(path) > maxlen:
                continue

            name = path[-1]
            if name == b:
                return path

            for p in tunnels[name]:
                if p not in path:
                    queue.append(path + (p,))
        return tuple()

    @staticmethod
    def compute_weights(tunnels, maxlen=10):
        paths = dict()
        names = list(tunnels.keys())
        for i, a in enumerate(names):
            for b in names[i:]:
                queue = [(a,)]
                while queue:
                    path = queue.pop(0)
                    if len(path) > maxlen:
                        continue

                    name = path[-1]
                    if name == b:
                        paths[(a, b)] = paths[(b, a)] = len(path)
                        break

                    for p in tunnels[name]:
                        if p not in path:
                            queue.append(path + (p,))
        return paths

    def solution_1(self, data: str):
        start, tmax = "AA", 30
        rates, tunnels = parse_data(data)

        names = {k for k, v in rates.items() if v}
        weights = self.compute_weights(tunnels, maxlen=tmax)

        queue = collections.deque([(0, 0, (start,), names)])
        best, seen = 0, set()
        while queue:
            press, time, path, others = queue.popleft()
            k = press, time, path, tuple(others)
            if k in seen:
                continue
            seen.add(k)

            name = path[-1]
            best = max(best, press)
            if time > tmax:
                continue
            for p in others:
                new_time = time + weights[(name, p)]
                if new_time < tmax:
                    new_press = press + (tmax - new_time) * rates[p]
                    new_others = others - {p}
                    queue.append((new_press, new_time, path + (p,), new_others))  # noqa

        return best

    def solution_2(self, data: str):
        start, tmax = "AA", 26
        rates, tunnels = parse_data(data)

        names = {k for k, v in rates.items() if v}
        weights = self.compute_weights(tunnels, maxlen=tmax)

        queue = collections.deque([(0, 0, (start,), set())])
        best = dict()
        while queue:
            press, time, path, seen = queue.popleft()
            name = path[-1]
            k = tuple(seen)
            best[k] = max(best.get(k, press), press)
            for p in names - seen:
                new_time = time + weights[(name, p)]
                if new_time < tmax:
                    new_press = press + (tmax - new_time) * rates[p]
                    new_others = seen | {p}
                    queue.append((new_press, new_time, path + (p,), new_others))  # noqa

        pressures = list()
        for (k1, v1), (k2, v2) in itertools.combinations(best.items(), r=2):
            if not set(k1) & set(k2):
                pressures.append(v1 + v2)
        return max(pressures)


def main():
    puzzle = Solution()
    puzzle.run()


if __name__ == "__main__":
    main()
