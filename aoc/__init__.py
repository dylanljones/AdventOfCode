# coding: utf-8
#
# This code is part of aoc2022.
#
# Copyright (c) 2022, Dylan Jones

"""Advent of Code helper package"""

from .client import Client
from .puzzle import Puzzle


def parse_numbers_comma(s: str, type_: type = int) -> list:
    return [type_(x) for x in s.split(",")]
