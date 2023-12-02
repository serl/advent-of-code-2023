import functools
import operator
import re
import unittest
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Self


class PartOne:
    @dataclass(frozen=True)
    class Game:
        ID: int
        sets: list[dict[str, int]]

        @classmethod
        def from_line(cls, line: str) -> Self:
            game_match = re.match(r"Game (\d+): (.*)", line)
            assert game_match is not None

            game_sets_str = game_match.group(2).split("; ")
            game_sets = [
                {color: int(num) for num, color in re.findall(r"(\d+) (\w+)", game_set)}
                for game_set in game_sets_str
            ]

            return cls(
                ID=int(game_match.group(1)),
                sets=game_sets,
            )

        def possible(self, bag: dict[str, int]) -> bool:
            for set in self.sets:
                if not all(
                    color in bag and bag[color] >= num for color, num in set.items()
                ):
                    return False
            return True

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    @staticmethod
    def read_file(file_name: str) -> list[str]:
        with (Path(__file__).parent / file_name).open() as f:
            return f.readlines()

    def solve(self) -> int:
        bag_contents = {"blue": 14, "red": 12, "green": 13}
        lines = self.read_file(self.file_name)
        games = [PartOne.Game.from_line(line) for line in lines]
        return sum(game.ID for game in games if game.possible(bag_contents))


class PartOneTestCase(unittest.TestCase):
    def test_parse_line(self):
        line = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
        game = PartOne.Game.from_line(line)
        self.assertEqual(game.ID, 1)
        self.assertEqual(
            game.sets,
            [
                {"blue": 3, "red": 4},
                {"red": 1, "green": 2, "blue": 6},
                {"green": 2},
            ],
        )

    def test_game_possible(self):
        game = PartOne.Game(
            ID=1,
            sets=[
                {"blue": 3, "red": 4},
                {"red": 1, "green": 2, "blue": 6},
                {"green": 2},
            ],
        )
        self.assertTrue(game.possible({"blue": 10, "red": 10, "green": 10}))
        self.assertFalse(game.possible({"blue": 1}))

    def test_sample(self):
        found_solution = PartOne("sample.txt").solve()
        self.assertEqual(found_solution, 8)

    def test_solve(self):
        found_solution = PartOne("input.txt").solve()
        self.assertEqual(found_solution, 2632)


class PartTwo(PartOne):
    class Game(PartOne.Game):
        def minimum_set(self) -> dict[str, int]:
            min_set = defaultdict(lambda: 0)
            for set in self.sets:
                for color, num in set.items():
                    min_set[color] = max(min_set[color], num)
            return min_set

        def minimum_set_power(self) -> int:
            return self.power(self.minimum_set())

        @staticmethod
        def power(set: dict[str, int]) -> int:
            return functools.reduce(operator.mul, set.values(), 1)

    def solve(self) -> int:
        lines = self.read_file(self.file_name)
        games = [PartTwo.Game.from_line(line) for line in lines]
        return sum(game.minimum_set_power() for game in games)


class PartTwoTestCase(unittest.TestCase):
    def test_game_minimum_set(self):
        game = PartTwo.Game.from_line(
            "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
        )
        self.assertEqual(
            game.minimum_set(),
            {
                "red": 4,
                "green": 2,
                "blue": 6,
            },
        )

    def test_game_power(self):
        self.assertEqual(
            PartTwo.Game.power(
                {
                    "red": 1,
                    "green": 2,
                }
            ),
            2,
        )
        self.assertEqual(
            PartTwo.Game.power(
                {
                    "red": 4,
                    "green": 2,
                    "blue": 6,
                }
            ),
            48,
        )

    def test_sample(self):
        found_solution = PartTwo("sample.txt").solve()
        self.assertEqual(found_solution, 2286)

    def test_solve(self):
        found_solution = PartTwo("input.txt").solve()
        self.assertEqual(found_solution, 69629)


if __name__ == "__main__":
    unittest.main()
