# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-25

import math
from dataclasses import dataclass

import aoc

OPS = {
    0: sum,
    1: math.prod,
    2: min,
    3: max,
    5: lambda ls: int(ls[0] > ls[1]),  # gt
    6: lambda ls: int(ls[0] < ls[1]),  # lt
    7: lambda ls: int(ls[0] == ls[1]),  # eq
}


@dataclass
class Packet:
    version: int
    id: int
    value: int = 0
    sub_packets: list["Packet"] = None

    def __post_init__(self):
        if self.sub_packets is None:
            self.sub_packets = list()

    def version_sum(self):
        total = self.version
        for packet in self.sub_packets:
            total += packet.version_sum()
        return total

    def evaluate(self):
        if self.id == 4:
            return self.value
        # Get values of sub packets and apply operator
        return OPS[self.id](tuple(p.evaluate() for p in self.sub_packets))


def _decode(bits: str, i: int = 0) -> tuple[Packet, int]:
    pv = int(bits[i : i + 3], 2)
    pid = int(bits[i + 3 : i + 6], 2)
    i += 6
    packet = Packet(pv, pid)
    if pid == 4:
        value_bits = ""
        while True:
            value_bits += bits[i + 1 : i + 5]
            i += 5
            if bits[i - 5] == "0":
                break
        packet.value = int(value_bits, 2)
    elif bits[i] == "0":
        j = i + 16 + int(bits[i + 1 : i + 16], 2)
        i += 16
        while i < j:
            sp, i = _decode(bits, i)
            packet.sub_packets.append(sp)
    else:
        n = int(bits[i + 1 : i + 12], 2)
        i += 12
        for _ in range(n):
            sp, i = _decode(bits, i)
            packet.sub_packets.append(sp)
    return packet, i


def decode(data: str) -> Packet:
    bits = bin(int("1" + data, 16))[3:]
    return _decode(bits)[0]


class Solution(aoc.Puzzle):
    day = 16
    year = 2021
    test_input_1 = "8A004A801A8002F478"
    test_solution_1 = 16
    test_input_2 = "880086C3E88112"
    test_solution_2 = 7

    def solution_1(self, data: str):
        return decode(data).version_sum()

    def solution_2(self, data: str):
        return decode(data).evaluate()


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
