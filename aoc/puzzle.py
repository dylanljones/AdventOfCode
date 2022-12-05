# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import os
import json
from .client import Client, AOCException


class TestAnswerError(AOCException):
    def __init__(self, actual, expected):
        msg = f"Your test answer '{actual}' is incorrect, expected '{expected}'."
        super().__init__(msg)


class Puzzle:

    test_input_idx = 0
    test_answer_idx_1 = -1
    test_answer_idx_2 = -1

    def __init__(self, year, day, root="", token="", headers=None):
        self.year = year
        self.day = day
        self.root = root
        self.client = Client(token, headers)
        self.info = None

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
        if not reload and os.path.exists(file):
            with open(file, "r") as fh:
                info = dict(json.load(fh))
        else:
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

    def get_test_input(self):
        return self.info["test_input"]

    def submit(self, part, answer):
        return self.client.submit(self.year, self.day, part, answer)

    def solution_1(self, data: str):
        return None

    def solution_2(self, data: str):
        return None

    def run(self, test_only=False, text=True):
        header = f"DAY {self.day:02}: {self.url}"
        print(header)
        print("-" * len(header))

        test_data = self.get_test_input()
        data = self.get_input()

        print("[Part 1]")
        test_answer = self.solution_1(test_data)
        if test_answer is not None:
            print(f"Your test answer was     {test_answer}")
            if self.test_answer_1 is not None:
                if not test_answer == self.test_answer_1:
                    raise TestAnswerError(test_answer, self.test_answer_1)
        else:
            print("No solution implemented")

        answer_1 = self.answer_1
        if not answer_1:
            if text:
                print(self.text_1)
                print()
            if not test_only:
                answer = self.solution_1(data)
                if answer is not None:
                    msg = self.submit(1, answer)
                    if "That's not the right answer" in msg:
                        raise ValueError(msg)
                    print(msg)
                    self.load_info(reload=True)
        else:
            print(f"Your puzzle answer was   {answer_1}")

        print("[Part 2]")
        if not self.text_2:
            return
        test_answer = self.solution_2(test_data)
        if test_answer is not None:
            print(f"Your test answer was     {test_answer}")
            if self.test_answer_2 is not None:
                if not test_answer == self.test_answer_2:
                    raise TestAnswerError(test_answer, self.test_answer_2)
        else:
            print("No solution implemented")

        answer_2 = self.answer_2
        if not answer_2:
            if text:
                print(self.text_2)
                print()
            if not test_only:
                answer = self.solution_2(data)
                if answer is not None:
                    msg = self.submit(2, answer)
                    if "That's not the right answer" in msg:
                        raise ValueError(msg)
                    print(msg)
                    self.load_info(reload=True)
        else:
            print(f"Your puzzle answer was   {answer_2}")
