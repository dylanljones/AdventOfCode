# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import importlib
import json
import os
import time

from .client import AOCException, Client


class TestAnswerError(AOCException):
    def __init__(self, actual, expected):
        msg = f"Your test answer '{actual}' is incorrect, expected '{expected}'."
        super().__init__(msg)


class AnswerError(AOCException):
    def __init__(self, actual, answer):
        msg = f"Your answer '{actual}' does not match the submitted answer '{answer}'."
        super().__init__(msg)


class Puzzle:
    file = None
    day = None
    year = None

    test_input_idx_1 = 0
    test_input_idx_2 = 0
    test_input_1 = None
    test_solution_1 = None
    test_answer_idx_1 = -1
    test_answer_idx_2 = -1
    test_input_2 = None
    test_solution_2 = None
    second_test_input = None

    def __init__(self, year=-1, day=-1, root="", token="", headers=None):
        if self.file is None:
            m = importlib.import_module(self.__module__)
            self.file = m.__file__

        dirname = os.path.dirname(self.file)
        if Puzzle.day is not None:
            day = Puzzle.day
        if Puzzle.year is not None:
            year = Puzzle.year

        if year == -1:
            path = os.path.dirname(self.file)
            year_dir, day_dir = os.path.split(path)
            year_dir = os.path.split(year_dir)[1]
            year = int(year_dir.replace("year", "").strip("_"))
            day = int(day_dir.replace("day", "").strip("_"))
        elif day == -1:
            path = os.path.dirname(__file__)
            day_dir = os.path.split(path)[1]
            day = int(day_dir.replace("day", "").strip("_"))

        self.year = year
        self.day = day
        self.root = root or dirname
        self.client = Client(token, headers)
        self.info = None

        self.runs_sol1 = 0
        self.runs_sol2 = 0
        self.runs = {1: 0, 2: 0}

        self.load_info(reload=False)

    @property
    def url(self):
        return self.client.get_puzzle_url(self.year, self.day)

    @property
    def title(self):
        return self.info["title"]

    @property
    def text_1(self):
        return self.info["part_1"]["text"]

    @property
    def text_2(self):
        return self.info["part_2"]["text"]

    @property
    def test_input(self):
        return self.info["test_input"]

    @property
    def test_answer_1(self):
        return self.info["part_1"]["test_answer"]

    @property
    def test_answer_2(self):
        return self.info["part_2"]["test_answer"]

    @property
    def answer_1(self):
        return self.info["part_1"]["answer"]

    @answer_1.setter
    def answer_1(self, value):
        msg = self.submit(1, value)
        print(msg)

    @property
    def answer_2(self):
        return self.info["part_2"]["answer"]

    @answer_2.setter
    def answer_2(self, value):
        msg = self.submit(2, value)
        print(msg)

    def load_info(self, reload=True):
        file = os.path.join(self.root, f"info_{self.year}_{self.day:02}.json")
        load = reload
        info = dict()
        if self.test_input_1 is not None:
            self.test_input_idx_1 = None
        if self.test_solution_1 is not None:
            self.test_answer_idx_1 = None
        if self.test_input_2 is not None:
            self.test_input_idx_2 = None
        if self.test_solution_2 is not None:
            self.test_answer_idx_2 = None
        if not reload and os.path.exists(file):
            with open(file, "r") as fh:
                info = dict(json.load(fh))

            # Check if indices still match:
            inp_idx = info.get("test_input_idx", None)
            ans_idx1 = info["part_1"].get("test_answer_idx", None)
            ans_idx2 = info["part_2"].get("test_answer_idx", None)
            if (
                inp_idx != self.test_input_idx_1
                or ans_idx1 != self.test_answer_idx_1
                or ans_idx2 != self.test_answer_idx_2
            ):
                load = True
        else:
            load = True

        if load:
            info = self.client.get_puzzle(
                self.year,
                self.day,
                self.test_input_idx_1,
                self.test_input_idx_2,
                self.test_answer_idx_1,
                self.test_answer_idx_2,
            )
            if self.root and not os.path.exists(self.root):
                os.makedirs(self.root)
            with open(file, "w") as fh:
                json.dump(info, fh, indent=4)

        self.info = info

    def save_info(self):
        file = os.path.join(self.root, f"info_{self.year}_{self.day:02}.json")
        if self.root and not os.path.exists(self.root):
            os.makedirs(self.root)
        with open(file, "w") as fh:
            json.dump(self.info, fh, indent=4)

    def get_input(self, reload=False):
        file = os.path.join(self.root, f"input_{self.year}_{self.day:02}.txt")
        if not reload and os.path.exists(file):
            # Use cached data
            with open(file, "r") as fh:
                data = fh.read()
        else:
            # Download and cache data
            data = self.client.get_input(self.year, self.day)
            with open(file, "w") as fh:
                fh.write(data)
        return data

    def get_test_input(self, part=1):
        return self.info[f"part_{part}"]["test_input"]

    def submit(self, part, answer):
        return self.client.submit(self.year, self.day, part, answer)

    def solution_1(self, data: str):
        return None

    def solution_2(self, data: str):
        return None

    def run_test(self, part, puzzle_only):
        solution_func = self.solution_1 if part == 1 else self.solution_2

        test_data = self.get_test_input(part=part)
        if test_data is None:
            test_data = self.test_input_1 if part == 1 else self.test_input_2
        test_solution = self.info[f"part_{part}"]["test_answer"]
        if test_solution is None:
            test_solution = self.test_solution_1 if part == 1 else self.test_solution_2

        test_available = test_data is not None and test_solution is not None
        solution_available = True
        if test_available and not puzzle_only:
            test_answer = solution_func(test_data)
            if test_answer is None:
                solution_available = False
            if solution_available:
                self.runs[part] += 1
                print(f"Your test answer was     {test_answer}")
                if not test_answer == test_solution:
                    raise TestAnswerError(test_answer, test_solution)
            else:
                print("No solution implemented")
        return test_available, solution_available

    def run_puzzle(self, part, test_only=False, text=False, rerun=True):
        solution_func = self.solution_1 if part == 1 else self.solution_2

        solution = self.info[f"part_{part}"]["answer"]
        puzzle_text = self.info[f"part_{part}"]["text"]

        if rerun or solution is None:
            if text:
                print(puzzle_text)
                print()
            if not test_only:
                data = self.get_input()
                t0 = time.perf_counter()
                result = solution_func(data)
                if result is None:
                    print("No solution implemented")
                else:
                    print("Result", result)
                    t = time.perf_counter() - t0
                    if solution is None:
                        solution = result
                    solution = type(result)(solution)
                    if result != solution:
                        raise AnswerError(result, solution)
                    self.info[f"part_{part}"]["time"] = t
                    self.save_info()
                    self.runs[part] += 1
                    if self.info[f"part_{part}"]["answer"] is None:
                        err, msg = self.submit(part, solution)
                        if err:
                            raise ValueError(msg)
                        print(f"\033[32m{msg}\033[m")
                        self.load_info(reload=True)
                    print(f"Your puzzle answer was   {solution}")
                    print(f"Time: {t * 1000:.4f} ms")
        else:
            print(f"Your puzzle answer was   {solution}")
            print(f"Time: {self.info[f'part_{part}'].get('time', 0) * 1000:.4f} ms")

    def run(self, puzzle_only=False, test_only=False, text=False, rerun=True):
        header = f"DAY {self.day:02}: {self.url}"
        print(header)
        print("-" * len(header))

        print("[Part 1]")
        print()
        part = 1
        test_available, solution_available = self.run_test(part, puzzle_only)
        if solution_available and not test_only:
            self.run_puzzle(part, test_only, text, rerun)
        print()

        print("[Part 2]")
        print()
        part = 2
        if not self.info[f"part_{part}"]["text"]:
            return
        test_available, solution_available = self.run_test(part, puzzle_only)
        if solution_available and not test_only:
            self.run_puzzle(part, test_only, text, rerun)
