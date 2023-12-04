import re
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Self


def read_file(file_name: str) -> list[str]:
    with (Path(__file__).parent / file_name).open() as f:
        return [line.strip() for line in f.readlines()]


class PartOne:
    @dataclass(frozen=True)
    class Card:
        id: int
        winning: set[int]
        having: set[int]

        @classmethod
        def from_line(cls, line: str) -> Self:
            line_match = re.fullmatch(r"Card\s+(\d+): ([\d\s]+) \| ([\d\s]+)", line)
            assert line_match
            return cls(
                id=int(line_match.group(1)),
                winning=set(map(int, re.findall(r"\d+", line_match.group(2)))),
                having=set(map(int, re.findall(r"\d+", line_match.group(3)))),
            )

        @property
        def points(self) -> int:
            count_having = len(self.winning.intersection(self.having))
            if count_having > 0:
                return 2 ** (count_having - 1)
            return 0

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def solve(self) -> int:
        lines = read_file(self.file_name)
        cards = [PartOne.Card.from_line(line) for line in lines]
        return sum(card.points for card in cards)


class PartOneTestCase(unittest.TestCase):
    def test_parse_card(self):
        card = PartOne.Card.from_line(
            "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
        )
        self.assertEqual(card.id, 1)
        self.assertEqual(card.winning, {41, 48, 83, 86, 17})
        self.assertEqual(card.having, {83, 86, 6, 31, 17, 9, 48, 53})

    def test_card_points(self):
        winning_card = PartOne.Card(
            id=1,
            winning={41, 48, 83, 86, 17},
            having={83, 86, 6, 31, 17, 9, 48, 53},
        )

        self.assertEqual(winning_card.points, 8)

        losing_card = PartOne.Card(
            id=6,
            winning={31, 18, 13, 56, 72},
            having={74, 77, 10, 23, 35, 67, 36, 11},
        )
        self.assertEqual(losing_card.points, 0)

    def test_sample(self):
        found_solution = PartOne("sample.txt").solve()
        self.assertEqual(found_solution, 13)

    def test_solve(self):
        found_solution = PartOne("input.txt").solve()
        self.assertEqual(found_solution, 26218)


if __name__ == "__main__":
    unittest.main()
