Advent of Code
=================

[![AoC 2022](https://img.shields.io/badge/⭐_2022-48-yellow)](https://adventofcode.com/2022)
[![AoC 2023](https://img.shields.io/badge/⭐_2023-16-yellow)](https://adventofcode.com/2023)


🎄 My solutions for [Advent of Code]

## Python interface

The solutions in Python all use the included Python interface


### Advent of Code Client

This project includes a client for scraping data from [Advent of Code] and
submitting answers.

> Please do not spam the servers and cache the data!
> Caching is handled by the ``Puzzle`` object, not the client.

Since the puzzle inputs differ by user, a session token has to be supplied.
It can be either passed as argument to the client or stored in a file called
``token.txt``, located in the project root or the individual directories.

Example usage:
````python
from aoc import Client

client = Client()
# Load puzzle data
info = client.get_puzzle(year=2015, day=1)
input_data = client.get_input(year=2015, day=1)
user_stats = client.get_user_stats(year=2015)
# Compute your answers
...
# Submit your answers
client.submit(year=2015, day=1, part=1, answer=anser_part_1)
client.submit(year=2015, day=1, part=2, answer=anser_part_2)
````


### Advent of Code Puzzles

You can use the included ``Puzzle`` object to automatically download and cache the
puzzle data and can be used to supply and submit answers.

````python
from aoc import Puzzle


class Solution(Puzzle):
    year = 2015
    day = 1

    def solution_1(self, data: str):
        ...
        return answer

    def solution_2(self, data: str):
        ...
        return answer
````

The puzzle can then be run. Before submitting the answer to [Advent of Code], the solution
is checked against the example input and solution:
````python
sol = Solution()
sol.run(test_only=False, text=True)
````

If the first solution was correct, the ``Puzzle`` object will update the puzzle info
before running the second part.

You can initialize a solution directory with the included CLI script:
```bash
python create.py -d 1 -y 2015
```

[Advent of Code]: https://adventofcode.com
