# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-07

from collections import Counter

import aoc

FIVE = 6
FOUR = 5
FULL = 4
THREE = 3
TWO = 2
ONE = 1
HIGH = 0

CARDS = "A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"
CARDS2 = "A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"


def get_type(hand):
    counts = Counter(hand)
    most = [x[1] for x in counts.most_common()]
    if len(most) == 1:
        # Five of a kind
        assert most[0] == 5
        return FIVE
    elif most[0] == 4:
        # Four of a kind
        assert most[1] == 1
        return FOUR
    elif most[0] == 3 and most[1] == 2:
        # Full house
        return FULL
    elif most[0] == 3 and most[1] == 1:
        # Three of a kind
        return THREE
    elif most[0] == 2 and most[1] == 2:
        # Two pair
        return TWO
    elif most[0] == 2 and most[1] == 1:
        # One pair
        return ONE
    elif all(x == 1 for x in most):
        # High card
        return HIGH


def apply_joker(hand):
    if "J" not in hand:
        return hand

    n_joker = hand.count("J")
    hand = hand.replace("J", "")

    # Add joker to most common card
    most_common = Counter(hand).most_common()
    if len(most_common) == 0:
        hand = CARDS2[0] * n_joker
    else:
        card = most_common[0][0]
        hand += card * n_joker

    return hand


class Hand:
    def __init__(self, hand, bid, use_joker=False):
        self.hand = hand
        self.bid = int(bid)
        self.use_joker = use_joker

        if use_joker:
            hand = apply_joker(hand)
        self.type = get_type(hand)

    def __eq__(self, other):
        return self.hand == other.hand

    def __gt__(self, other):
        if self.type == other.type:
            cards = CARDS2 if self.use_joker else CARDS
            for c1, c2 in zip(self.hand, other.hand):
                if cards.index(c1) < cards.index(c2):
                    return True
                elif cards.index(c1) > cards.index(c2):
                    return False
        else:
            return self.type > other.type

    def __lt__(self, other):
        return not self.__gt__(other)

    def __repr__(self):
        return f"{self.hand} ({self.type})"


class Solution(aoc.Puzzle):
    day = 7
    year = 2023

    def solution_1(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        hands = [Hand(*line.split(" ")) for line in lines]
        winnings = sum(hand.bid * (i + 1) for i, hand in enumerate(sorted(hands)))
        return winnings

    def solution_2(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        hands = [Hand(*line.split(" "), use_joker=True) for line in lines]
        winnings = sum(hand.bid * (i + 1) for i, hand in enumerate(sorted(hands)))
        return winnings


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
