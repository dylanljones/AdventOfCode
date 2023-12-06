# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-12-04

import aoc


class Solution(aoc.Puzzle):
    year = 2023
    day = 4

    def solution_1(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        total_points = 0
        for line in lines:
            card, data = line.split(":")
            winning, given = data.split("|")
            winning = {int(x) for x in winning.split()}
            given = {int(x) for x in given.split()}
            winners = given & winning
            if winners:
                points = 2 ** (len(winners) - 1)
                total_points += points
        return total_points

    def solution_2(self, data: str):
        lines = [line.strip() for line in data.splitlines(keepends=False)]
        cards = dict()
        for line in lines:
            card, data = line.split(":")
            card = int(card.replace("Card", "").strip())
            winning, given = data.split("|")
            winning = {int(x) for x in winning.split()}
            given = {int(x) for x in given.split()}
            cards[card] = (winning, given)

        cardlist = list(cards.keys())
        total = len(cardlist)
        while cardlist:
            new_cardlist = list()
            for i in cardlist:
                winning, given = cards[i]
                n_winners = len(given & winning)
                if n_winners:
                    new_cardlist += [i + j + 1 for j in range(n_winners)]
            total += len(new_cardlist)
            cardlist = new_cardlist
        return total


if __name__ == "__main__":
    puzzle = Solution()
    puzzle.run(test_only=False)
