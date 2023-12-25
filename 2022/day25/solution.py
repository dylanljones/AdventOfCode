# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2022-12-25

import aoc

TESTS = """\
        1              1
        2              2
        3             1=
        4             1-
        5             10
        6             11
        7             12
        8             2=
        9             2-
       10             20
       15            1=0
       20            1-0
     2022         1=11-2
    12345        1-0---0
314159265  1121-1110-1=0
"""


def read_tests():
    tests = []
    for line in TESTS.splitlines(keepends=False):
        decimal, snafu = line.split()
        decimal = int(decimal.strip())
        snafu = snafu.strip()
        tests.append((snafu, decimal))
    return tests


def convert_snafu_to_decimal(snafu: str) -> int:
    numbers = []
    for i, char in enumerate(snafu[::-1]):
        if char == "-":
            num_base_5 = -1
        elif char == "=":
            num_base_5 = -2
        else:
            num_base_5 = int(char)
        num_base_10 = num_base_5 * 5**i
        numbers.append(num_base_10)
    return sum(numbers)


def convert_decimal_to_snafu(decimal: int) -> str:
    max_places = 0
    while 5**max_places < decimal:
        max_places += 1
    max_places -= 1
    max_places = max(max_places, 0)

    digits = []
    for i in range(max_places, -1, -1):
        digit, decimal = divmod(decimal, 5**i)
        digits.append(str(digit))

    for i in range(len(digits) - 1, -1, -1):
        if digits[i] == "3":
            digits[i] = "="
            if i == 0:
                digits = ["1"] + digits
            else:
                digits[i - 1] = str(int(digits[i - 1]) + 1)
        elif digits[i] == "4":
            digits[i] = "-"
            if i == 0:
                digits = ["1"] + digits
            else:
                digits[i - 1] = str(int(digits[i - 1]) + 1)
        elif digits[i] == "5":
            digits[i] = "0"
            if i == 0:
                digits = ["1"] + digits
            else:
                digits[i - 1] = str(int(digits[i - 1]) + 1)
    return "".join(digits)


def test_snafu_to_decimal():
    for snafu, decimal in read_tests():
        result = convert_snafu_to_decimal(snafu)
        assert result == decimal, f"{result} != {decimal}"


def test_decimal_to_snafu():
    for snafu, decimal in read_tests():
        result = convert_decimal_to_snafu(decimal)
        assert result == snafu, f"{result} != {snafu}"


class Solution(aoc.Puzzle):
    day = 25
    year = 2022
    test_solution_idx_1 = -1
    part_2 = False

    def solution_1(self, data: str):
        test_snafu_to_decimal()
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        sum_decimal = sum(convert_snafu_to_decimal(snafu) for snafu in lines)
        sum_snafu = convert_decimal_to_snafu(sum_decimal)
        return sum_snafu


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
