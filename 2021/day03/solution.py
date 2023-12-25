# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-25

import aoc


def get_most_common_bit(numbers, i):
    op = 1 << i
    count = 0
    for num in numbers:
        if num & op:
            count += 1
    return 0 if count < (len(numbers) / 2) else 1


class Solution(aoc.Puzzle):
    year = 2021
    day = 3

    def solution_1(self, data: str):
        lines = data.splitlines(keepends=False)
        width = len(lines[0])
        numbers = [int(line, 2) for line in lines]
        n = len(lines)
        bits = list()
        for i in range(width):
            op = 1 << i
            count = 0
            for num in numbers:
                if num & op:
                    count += 1
            bits.append(int(count <= (n / 2)))

        gamma = int("".join(str(i) for i in bits[::-1]), 2)
        epsilon = int("".join(str(1 - i) for i in bits[::-1]), 2)
        return gamma * epsilon

    def solution_2(self, data: str):
        lines = data.splitlines(keepends=False)
        width = len(lines[0])
        numbers = [int(line, 2) for line in lines]

        o2, co2 = 0, 0
        number_list = numbers.copy()
        for i in range(width - 1, -1, -1):
            mc = get_most_common_bit(number_list, i)
            new_numbers = list()
            op = 1 << i
            for num in number_list:
                if bool(num & op) == mc:
                    new_numbers.append(num)
            number_list = new_numbers
            if len(number_list) == 1:
                o2 = number_list[0]
                break

        number_list = numbers.copy()
        for i in range(width - 1, -1, -1):
            mc = 1 - get_most_common_bit(number_list, i)
            new_numbers = list()
            op = 1 << i
            for num in number_list:
                if bool(num & op) == mc:
                    new_numbers.append(num)
            number_list = new_numbers
            if len(number_list) == 1:
                co2 = number_list[0]
                break
        return o2 * co2


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run()
