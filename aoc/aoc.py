# coding: utf-8
#
# This code is part of aoc2022.
#
# Copyright (c) 2022, Dylan Jones

import os
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

USER_AGENT = "github.com/dylanljones/aoc2022"
URL = "https://adventofcode.com/{year}/day/{day}"
STATS_URL = "https://adventofcode.com/{year}/leaderboard/self"


def user_session(token, headers=None):
    sess = requests.Session()
    if headers is not None:
        sess.headers.update(headers)
    sess.headers.update({"User-Agent": USER_AGENT})
    sess.cookies.update({"session": token})
    return sess


class PuzzleNotAvailable(Exception):
    pass


def load_token():
    file = "token.txt"
    if not os.path.exists(file):
        project_root = os.path.dirname(os.path.dirname(__file__))
        file = os.path.join(project_root, "token.txt")

    with open(file, "r") as fh:
        return fh.read().strip()


def get_input(root, user, year, day):
    file = os.path.join(root, "input.txt")
    if os.path.exists(file):
        # Use cached data
        with open(file, "r") as fh:
            data = fh.read()
    else:
        # Download and cache data
        url = URL.format(year=year, day=day) + "/input"
        headers = {"User-Agent": USER_AGENT}
        res = requests.get(url, cookies=user.auth, headers=headers)
        if not res.ok:
            if res.status_code == 404:
                raise PuzzleNotAvailable(
                    "{}/{:02d} not available yet".format(year, day)
                )
        data = res.text
        with open(file, "w") as fh:
            fh.write(data)

    return data


def _parse_duration(s):
    """Parse a string like 01:11:16 (hours, minutes, seconds) into a timedelta"""
    if s == ">24h":
        return timedelta(hours=24)
    h, m, s = [int(x) for x in s.split(":")]
    return timedelta(hours=h, minutes=m, seconds=s).total_seconds()


class User:
    def __init__(self, token=""):
        if not token:
            token = load_token()
        self.token = token

    @property
    def auth(self):
        return {"session": self.token}

    @property
    def token_sanitized(self):
        return f"...{self.token[-4:]}"

    def __repr__(self):
        return f"<{self.__class__.__name__}(token={self.token_sanitized})>"

    def get_stats(self, year=None, session=None):
        if year is None:
            year = datetime.now().year
        if session is None:
            session = user_session(self.token)

        days = set(str(i) for i in range(26))
        url = STATS_URL.format(year=year)
        res = session.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        if soup.article is None and "You haven't collected any stars" in soup.main.text:
            return dict()

        stats_txt = soup.article.pre.text
        lines = [x for x in stats_txt.splitlines() if x.split()[0] in days]
        results = dict()
        for line in reversed(lines):
            vals = line.split()
            day = int(vals[0])
            results[day] = {}
            results[day]["part 1"] = {
                "time": _parse_duration(vals[1]),
                "rank": int(vals[2]),
                "score": int(vals[3]),
            }
            if vals[4] != "-":
                results[day]["part 2"] = {
                    "time": _parse_duration(vals[4]),
                    "rank": int(vals[5]),
                    "score": int(vals[6]),
                }
        return results

    def getall_stats(self, session=None):
        if session is None:
            session = user_session(self.token)
        now = datetime.now()
        results = dict()
        for year in range(2015, now.year + 1):
            stats = self.get_stats(year, session=session)
            if stats:
                results[year] = stats
        return results


class Puzzle:

    test_answer_1 = None
    test_answer_2 = None

    def __init__(self, year, day, user=None, root=""):
        if not user:
            user = User()

        self.year = year
        self.day = day
        self.user = user
        self.url = URL.format(year=year, day=day)
        self.session = user_session(self.user.token)
        self.root = root
        self.soup = None

    @property
    def title(self):
        article = self.soup.find_all("article")[0]
        return article.h2.text.replace("-", "").split(":", maxsplit=1)[1].strip()

    @property
    def text_1(self):
        return self.get_text(1)

    @property
    def text_2(self):
        return self.get_text(2)

    @property
    def answer_1(self):
        return self.get_answer(1)

    @answer_1.setter
    def answer_1(self, value):
        msg = self.submit(1, value)
        print(msg)

    @property
    def answer_2(self):
        return self.get_answer(2)

    @answer_2.setter
    def answer_2(self, value):
        msg = self.submit(2, value)
        print(msg)

    def load_info(self, reload=False, session=None):
        file = os.path.join(self.root, "info.html")
        if not reload and os.path.exists(file):
            with open(file, "rb") as fh:
                text = fh.read()
        else:
            if session is None:
                session = self.session
            res = session.get(self.url)
            text = res.text
            if self.root and not os.path.exists(self.root):
                os.makedirs(self.root)
            with open(file, "wb") as fh:
                fh.write(res.content)

        soup = BeautifulSoup(text, "html.parser")
        content = soup.main
        self.soup = content

    def get_text(self, part):
        try:
            article = self.soup.find_all("article")[part - 1]
            return "".join(child.text for child in list(article)[1:])
        except IndexError:
            return None

    def get_answer(self, part):
        element = self.soup.find_all("p", recursive=False)[part - 1]
        prefix = "Your puzzle answer was"
        text = str(element.text)
        if not text.startswith(prefix):
            return None
        text = text.replace(prefix, "")
        return text[:-1].strip()

    def get_input(self, session=None):
        if session is None:
            session = self.session

        file = os.path.join(self.root, "input.txt")
        if os.path.exists(file):
            # Use cached data
            with open(file, "r") as fh:
                data = fh.read()
        else:
            # Download and cache data
            res = session.get(self.url + "/input")
            if not res.ok:
                if res.status_code == 404:
                    raise PuzzleNotAvailable(f"{self.year}/{self.day} not available")
            data = res.text

            with open(file, "w") as fh:
                fh.write(data)

        return data

    def get_test_input(self):
        block = self.soup.find_all("pre")[0]
        return block.text

    def get_test_answer(self, part):
        try:
            article = self.soup.find_all("article")[part - 1]
            block = article.find_all("code")[-1]
            answer = int(block.text)
        except TypeError as e:
            print(e)
            answer = self.test_answer_1 if part == 1 else self.test_answer_2
        return answer

    def submit(self, part, answer, session=None):
        if session is None:
            session = self.session
        data = {"level": part, "answer": str(answer)}
        res = session.post(self.url + "/answer", data=data)
        soup = BeautifulSoup(res.text, "html.parser")
        message = soup.article.text
        return message

    def __repr__(self):
        return f"<{self.__class__.__name__}(year: {self.year}, day: {self.day})>"

    def solution_1(self, data):
        return None

    def solution_2(self, data):
        return None

    def run(self):
        print(f"DAY {self.day:02}")
        print("-------")

        self.load_info()
        test_data = self.get_test_input()
        data = self.get_input()

        print("[Part 1]")
        test_answer = self.solution_1(test_data)
        if test_answer is not None:
            print(f"Your test answer was     {test_answer}")
            test_answer_1 = self.get_test_answer(1)
            if test_answer_1 is not None:
                assert test_answer == test_answer_1, "Test answer is not correct!"
        else:
            print("No solution implemented")

        answer_1 = self.answer_1
        if not answer_1:
            print(self.text_1)
            print()
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
            test_answer_2 = self.get_test_answer(2)
            if test_answer_2 is not None:
                assert test_answer == test_answer_2, "Test answer is not correct!"
        else:
            print("No solution implemented")

        answer_2 = self.answer_2
        if not answer_2:
            print(self.text_2)
            print()
            answer = self.solution_2(data)
            if answer is not None:
                msg = self.submit(2, answer)
                if "That's not the right answer" in msg:
                    raise ValueError(msg)
                print(msg)
                self.load_info(reload=True)
        else:
            print(f"Your puzzle answer was   {answer_2}")
