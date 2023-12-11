# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import itertools

import aoc

WIDTH = 7
JET = {"<": -1, ">": +1}
ROCKS = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(0, 0), (0, 1), (1, 0), (1, 1)},
]


def parse_data(data: str):
    return [JET[c] for c in data.strip()]


class Rock:
    def __init__(self, rock):
        self._coords = rock
        self.height = max(y for x, y in self._coords)
        self.width = max(x for x, y in self._coords)
        self.pos = (0, 0)

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @property
    def coords(self):
        return {(x + self.pos[0], y + self.pos[1]) for x, y in self._coords}

    def coords_at(self, x, y):
        return {(_x + x, _y + y) for _x, _y in self._coords}

    def set_pos(self, x, y):
        self.pos = (x, y)

    def movex(self, dx):
        xnew = self.pos[0] + dx
        if xnew < 0 or xnew >= WIDTH - self.width:
            return
        self.pos = (self.pos[0] + dx, self.pos[1])

    def movey(self, dy):
        self.pos = (self.pos[0], self.pos[1] + dy)

    def __eq__(self, other):
        return self._coords == other._coords and self.pos == other.pos  # noqa

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.coords}>"


class Solution(aoc.Puzzle):
    year = 2022
    day = 17
    test_input_idx_1 = 1
    test_solution_idx_2 = -2

    def __init__(self):
        super().__init__()

    @staticmethod
    def clear_unused_coords(coords):
        ymax = [max(y for x, y in coords if x == i) for i in range(WIDTH)]
        ymin = min(ymax)
        return ymin, set((x, y) for x, y in coords if y >= ymin)

    @staticmethod
    def get_fingerprint(irock, ijet, coords):
        ymax = [max(y for x, y in coords if x == i) for i in range(WIDTH)]
        ymin = min(ymax)
        upper_coords = tuple((x, y - ymin) for x, y in coords if y >= ymin)
        return irock, ijet, upper_coords

    def solution_1(self, data: str):
        num_rocks = 2022

        jets = itertools.cycle(enumerate(parse_data(data)))
        rocks = itertools.cycle(enumerate(ROCKS))

        ymax = 0
        coords = set((x, ymax) for x in range(WIDTH))  # floor
        r = 0
        while r < num_rocks:
            # Init rock
            ir, rock = next(rocks)
            rock = Rock(rock)
            rock.set_pos(2, ymax + 4)
            # Simulate rock:
            ij, jet = next(jets)
            rock.movex(jet)
            rock.movey(-1)
            while True:
                ij, jet = next(jets)
                if not (rock.coords_at(rock.x + jet, rock.y) & coords):
                    rock.movex(jet)
                if rock.coords_at(rock.x, rock.y - 1) & coords:
                    break
                else:
                    rock.movey(-1)
            # Update coords and offset
            coords |= rock.coords
            _, coords = self.clear_unused_coords(coords)
            # Update ymax
            ymax = max(y for x, y in coords)
            r += 1

        return ymax

    def solution_2(self, data: str):
        num_rocks = 1_000_000_000_000

        jets = itertools.cycle(enumerate(parse_data(data)))
        rocks = itertools.cycle(enumerate(ROCKS))

        ymax = 0
        coords = set((x, ymax) for x in range(WIDTH))  # floor
        fingerprints = dict()
        r = 0
        r_done = 0
        ymax_done = 0
        dy_done = 0
        height = -1
        while r < num_rocks:
            # Init rock
            ir, rock = next(rocks)
            rock = Rock(rock)
            rock.set_pos(2, ymax + 4)
            # Check fingerprints
            ij, jet = next(jets)
            fp = self.get_fingerprint(ir, ij, coords)
            if fp in fingerprints:
                r0, ymax0 = fingerprints[fp]
                period = r - r0
                remaining = num_rocks - r0
                n = remaining // period
                r_done = r + remaining % period
                ymax_done = ymax0 + n * (ymax - ymax0)
                dy_done = ymax
            else:
                fingerprints[fp] = (r, ymax)

            if r_done and r_done == r:
                height = ymax_done + (ymax - dy_done)
                break
            # Simulate rock:
            rock.movex(jet)
            rock.movey(-1)
            while True:
                ij, jet = next(jets)
                if not (rock.coords_at(rock.x + jet, rock.y) & coords):
                    rock.movex(jet)
                if rock.coords_at(rock.x, rock.y - 1) & coords:
                    break
                else:
                    rock.movey(-1)
            # Update coords and offset
            coords |= rock.coords
            y0, coords = self.clear_unused_coords(coords)
            # Update ymax
            ymax = max(y for x, y in coords)
            r += 1

        return height


def main():
    puzzle = Solution()
    puzzle.run()


if __name__ == "__main__":
    main()
