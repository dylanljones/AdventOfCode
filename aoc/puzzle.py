# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

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
    test_input_idx = 0
    test_answer_idx_1 = -1
    test_answer_idx_2 = -1
    day = None
    year = None

    _file = __file__

    def __init__(self, year=-1, day=-1, root="", token="", headers=None):
        dirname = os.path.dirname(self._file)
        if Puzzle.day is not None:
            day = Puzzle.day
        if Puzzle.year is not None:
            year = Puzzle.year

        if year == -1:
            path = os.path.dirname(self._file)
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
        if not reload and os.path.exists(file):
            with open(file, "r") as fh:
                info = dict(json.load(fh))
            # Check if indices still match:
            inp_idx = info.get("test_input_idx", None)
            ans_idx1 = info["part_1"].get("test_answer_idx", None)
            ans_idx2 = info["part_2"].get("test_answer_idx", None)
            if (
                inp_idx != self.test_input_idx
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
                self.test_input_idx,
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

    def run(self, puzzle_only=False, test_only=False, text=False, rerun=True):
        header = f"DAY {self.day:02}: {self.url}"
        print(header)
        print("-" * len(header))

        test_data = self.get_test_input(part=1)
        data = self.get_input()

        print("[Part 1]")
        print()
        test_answer = self.solution_1(test_data)
        self.runs_sol1 += 1
        if test_answer is not None:
            if not puzzle_only:
                print(f"Your test answer was     {test_answer}")
                if self.test_answer_1 is not None:
                    if not test_answer == self.test_answer_1:
                        raise TestAnswerError(test_answer, self.test_answer_1)

            answer = self.answer_1
            if rerun or answer is None:
                if text:
                    print(self.text_1)
                    print()
                if not test_only:
                    t0 = time.perf_counter()
                    result = self.solution_1(data)
                    print("Result", result)
                    t = time.perf_counter() - t0
                    if answer is None:
                        answer = result
                    answer = type(result)(answer)
                    if result != answer:
                        raise AnswerError(result, answer)
                    self.info["part_1"]["time"] = t
                    self.save_info()
                    self.runs_sol1 += 1
                    if self.answer_1 is None:
                        err, msg = self.submit(1, answer)
                        if err:
                            raise ValueError(msg)
                        print(f"\033[32m{msg}\033[m")
                        self.load_info(reload=True)
                    print(f"Your puzzle answer was   {answer}")
                    print(f"Time: {t * 1000:.4f} ms")
            else:
                print(f"Your puzzle answer was   {answer}")
                print(f"Time: {self.info['part_1'].get('time', 0) * 1000:.4f} ms")
        else:
            print("No solution implemented")
        print()

        print("[Part 2]")
        print()
        if not self.text_2:
            return
        test_data = self.get_test_input(part=2)
        test_answer = self.solution_2(test_data)
        self.runs_sol2 += 1
        if test_answer is not None:
            if not puzzle_only:
                print(f"Your test answer was     {test_answer}")
                if self.test_answer_2 is not None:
                    if not test_answer == self.test_answer_2:
                        raise TestAnswerError(test_answer, self.test_answer_2)

            answer = self.answer_2
            if rerun or answer is None:
                if text:
                    print(self.text_2)
                    print()
                if not test_only:
                    t0 = time.perf_counter()
                    result = self.solution_2(data)
                    t = time.perf_counter() - t0
                    if answer is None:
                        answer = result
                    answer = type(result)(answer)
                    if result != answer:
                        raise AnswerError(result, answer)
                    self.info["part_2"]["time"] = t
                    self.save_info()
                    self.runs_sol2 += 1
                    if self.answer_2 is None:
                        err, msg = self.submit(2, answer)
                        if err:
                            raise ValueError(msg)
                        print(f"\033[32m{msg}\033[m")
                        self.load_info(reload=True)
                    print(f"Your puzzle answer was   {answer}")
                    print(f"Time: {t * 1000:.4f} ms")
            else:
                print(f"Your puzzle answer was   {answer}")
                print(f"Time: {self.info['part_2'].get('time', 0) * 1000:.4f} ms")
        else:
            print("No solution implemented")
