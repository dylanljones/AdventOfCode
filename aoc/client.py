# coding: utf-8
#
# This code is part of aoc.
#
# Copyright (c) 2022, Dylan Jones

import os
import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

URL = "https://adventofcode.com/{year}/day/{day}"
STATS_URL = "https://adventofcode.com/{year}/leaderboard/self"

USER_AGENT = "github.com/dylanljones/aoc2022"

RE_RIGHT_ANSWER = re.compile("That's the right answer.")
RE_WRONG_ANSWER = re.compile(r"(That's not the right answer.).*If you're stuck,(.*?)")
RE_WAIT_ANSWER = re.compile(
    r"(You gave an answer too recently.).*(You have (.*?) left to wait.)"
)
RE_UNAVAILABLE = re.compile(
    r"Please don't repeatedly request this endpoint before it unlocks! "
    r"The calendar countdown is synchronized with the server time."
)


class AOCException(Exception):
    pass


class PuzzleNotAvailable(AOCException):
    pass


def load_token():
    file = "token.txt"
    if not os.path.exists(file):
        project_root = os.path.dirname(os.path.dirname(__file__))
        file = os.path.join(project_root, "token.txt")

    with open(file, "r") as fh:
        return fh.read().strip()


def user_session(token, headers=None):
    sess = requests.Session()
    if headers is not None:
        sess.headers.update(headers)
    sess.headers.update({"User-Agent": USER_AGENT})
    sess.cookies.update({"session": token})
    return sess


def _parse_duration(s):
    """Parse a string like 01:11:16 (hours, minutes, seconds) into a timedelta"""
    if s == ">24h":
        return timedelta(hours=24)
    h, m, s = [int(x) for x in s.split(":")]
    return timedelta(hours=h, minutes=m, seconds=s).total_seconds()


def get_easter_eggs(soup):
    # Most puzzles have exactly one easter-egg, but 2018/12/17 had two..
    eggs = soup.find_all(["span", "em", "code"], class_=None, attrs={"title": bool})
    return [egg["title"] for egg in eggs]


def get_text(article):
    """Format the whole article text"""
    try:
        lines = [element for element in list(article)[1:] if element.text.strip()]
        text = "\n\n".join(element.text.strip() for element in lines)
        text = ".\n".join(text.split(". "))
        return text
    except TypeError:
        return None


def get_test_input(article, pre_idx=0):
    """Extract the test input"""
    try:
        block = article.find_all(["pre"])[pre_idx]
        data = block.text
    except TypeError:
        data = None
    return data


def get_test_answer(article, code_idx=-1):
    """Extract the test answer"""
    try:
        block = article.find_all("code")[code_idx]
        text = block.text
        if "=" in text:
            text = text.split("=", maxsplit=1)[-1]
        try:
            answer = int(text)
        except ValueError:
            answer = text
    except TypeError:
        answer = None
    return answer


def get_answer(p):
    prefix = "Your puzzle answer was"
    text = str(p.text)
    if not text.startswith(prefix):
        return None
    text = text.replace(prefix, "")
    return text[:-1].strip()


def parse_submit_msg(text):
    match = RE_WRONG_ANSWER.search(text)
    if match:
        msg = f"{match.group(1).strip()}."
        return 1, msg

    match = RE_WAIT_ANSWER.search(text)
    if match:
        msg = f"{match.group(1).strip()} {match.group(2)}"
        return 1, msg

    match = RE_RIGHT_ANSWER.search(text)
    if match:
        return 0, match[0].strip()
    elif "Did you already complete it?" in text:
        return 0, "Already completed"
    else:
        # unexpected output
        raise ValueError(f"Could not parse response message: {text}")


class Client:
    def __init__(self, token: str = "", headers: dict = None):
        if not token:
            token = load_token()
        self.token = token
        self.session = user_session(token, headers)

    @property
    def auth(self) -> dict:
        return {"session": self.token}

    @property
    def token_sanitized(self) -> str:
        return f"...{self.token[-4:]}"

    @staticmethod
    def get_puzzle_url(year, day):
        return URL.format(year=year, day=day)

    def get_user_stats(self, year: int = None) -> dict:
        if year is None:
            year = datetime.now().year

        days = set(str(i) for i in range(26))
        url = STATS_URL.format(year=year)
        res = self.session.get(url)
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

    def getall_user_stats(self):
        now = datetime.now()
        results = dict()
        for year in range(2015, now.year + 1):
            stats = self.get_user_stats(year)
            if stats:
                results[year] = stats
        return results

    def get_puzzle(
        self,
        year,
        day,
        test_input_idx_1=0,
        test_input_idx_2=0,
        test_solution_idx_1=-1,
        test_solution_idx_2=-1,
    ):
        url = URL.format(year=year, day=day)
        res = self.session.get(url)
        if RE_UNAVAILABLE.match(res.text):
            raise PuzzleNotAvailable(f"{year}/{day} not available!")

        soup = BeautifulSoup(res.text, "html.parser")
        data = dict()
        eggs = get_easter_eggs(soup)
        article = soup.find_all("article")[0]
        title = article.h2.text.replace("-", "").strip()
        text1 = get_text(article)
        if test_input_idx_1 is not None:
            test_input = get_test_input(article, test_input_idx_1)
            test_answer1 = get_test_answer(article, test_solution_idx_1)
        else:
            test_input = None
            test_answer1 = None

        p = soup.main.find_all("p", recursive=False)[0]
        answer1 = get_answer(p)

        try:
            article = soup.find_all("article")[1]
        except IndexError:
            text2 = None
            test_input2 = None
            test_answer2 = None
            answer2 = None

        if article:
            try:
                text2 = get_text(article)
            except IndexError:
                text2 = None
            if test_input_idx_2 is not None:
                try:
                    test_input2 = get_test_input(article, test_input_idx_2)
                except IndexError:
                    test_input2 = test_input
            else:
                test_input2 = test_input
            try:
                test_answer2 = get_test_answer(article, test_solution_idx_2)
            except IndexError:
                test_answer2 = None
            try:
                p = soup.main.find_all("p", recursive=False)[1]
                answer2 = get_answer(p)
            except IndexError:
                answer2 = None

        data["title"] = title
        data["easter_eggs"] = eggs
        # data["test_input"] = test_input
        data["test_input_idx"] = test_input_idx_1

        data["part_1"] = {
            "text": text1,
            "test_input": test_input,
            "test_answer": test_answer1,
            "test_answer_idx": test_solution_idx_1,
            "answer": answer1,
        }
        data["part_2"] = {
            "text": text2,
            "test_input": test_input2,
            "test_answer": test_answer2,
            "test_answer_idx": test_solution_idx_2,
            "answer": answer2,
        }

        return data

    def get_input(self, year, day):
        url = URL.format(year=year, day=day) + "/input"
        res = self.session.get(url)
        if not res.ok:
            if res.status_code == 404:
                raise PuzzleNotAvailable(f"{year}/{day} not available")
        return res.text

    def submit(self, year, day, part, answer):
        url = URL.format(year=year, day=day) + "/answer"
        data = {"level": part, "answer": str(answer)}
        res = self.session.post(url, data=data)
        soup = BeautifulSoup(res.text, "html.parser")
        err, msg = parse_submit_msg(soup.article.text)
        return err, msg

    def __repr__(self):
        return f"<{self.__class__.__name__}(token={self.token_sanitized})>"
