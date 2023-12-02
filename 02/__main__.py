import re
import unittest
from dataclasses import dataclass
from pathlib import Path


class PartOne:
    @dataclass(frozen=True)
    class Game:
        ID: int
        sets: list[dict[str, int]]

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

    @staticmethod
    def parse_line(line: str) -> Game:
        game_match = re.match(r"Game (\d+): (.*)", line)
        assert game_match is not None

        game_sets_str = game_match.group(2).split("; ")
        game_sets = [
            {color: int(num) for num, color in re.findall(r"(\d+) (\w+)", game_set)}
            for game_set in game_sets_str
        ]

        return PartOne.Game(
            ID=int(game_match.group(1)),
            sets=game_sets,
        )

    def solve(self) -> int:
        bag_contents = {"blue": 14, "red": 12, "green": 13}
        lines = self.read_file(self.file_name)
        games = [self.parse_line(line) for line in lines]
        return sum(game.ID for game in games if game.possible(bag_contents))


class Part1TestCase(unittest.TestCase):
    def test_parse_line(self):
        line = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
        game = PartOne.parse_line(line)
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
        found_solution = PartOne("sample_part1.txt").solve()
        self.assertEqual(found_solution, 8)

    def test_solve_part_one(self):
        found_solution = PartOne("input.txt").solve()
        self.assertEqual(found_solution, 2632)


if __name__ == "__main__":
    unittest.main()
