import re
import unittest
from itertools import pairwise
from pathlib import Path


def read_file(file_name: str) -> list[str]:
    with (Path(__file__).parent / file_name).open() as f:
        return [line.strip() for line in f.readlines()]


class PartOne:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def parse_input(self) -> list[list[int]]:
        lines = read_file(self.file_name)
        return [self.parse_line(line) for line in lines]

    @staticmethod
    def parse_line(line) -> list[int]:
        return list(map(int, re.findall(r"(-?[\d]+)", line)))

    def solve(self) -> int:
        lines = self.parse_input()
        return sum(self.extrapolate_value(line) for line in lines)

    @classmethod
    def extrapolate_value(cls, line: list[int]) -> int:
        sublists = cls.get_sublists(line)
        result = 0
        for sublist in reversed(sublists):
            last_value = sublist[-1]
            result += last_value
        return result

    @staticmethod
    def get_sublists(line: list[int]) -> list[list[int]]:
        def _get_sublist(line: list[int]) -> list[int] | None:
            if all(value == 0 for value in line):
                return None
            return [items[1] - items[0] for items in pairwise(line)]

        lists = [line]
        while sublist := _get_sublist(lists[-1]):
            lists.append(sublist)
        return lists


class PartOneTestCase(unittest.TestCase):
    def test_parse_line(self):
        line = PartOne.parse_line("-7 -5 2 14 31 53 80 112")
        self.assertEqual(line, [-7, -5, 2, 14, 31, 53, 80, 112])

    def test_parse(self):
        lines = PartOne("sample.txt").parse_input()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], [0, 3, 6, 9, 12, 15])
        self.assertEqual(lines[1], [1, 3, 6, 10, 15, 21])
        self.assertEqual(lines[2], [10, 13, 16, 21, 30, 45])

    def test_extrapolate_value(self):
        self.assertEqual(PartOne.extrapolate_value([0, 3, 6, 9, 12, 15]), 18)
        self.assertEqual(PartOne.extrapolate_value([1, 3, 6, 10, 15, 21]), 28)
        self.assertEqual(PartOne.extrapolate_value([10, 13, 16, 21, 30, 45]), 68)

    def test_get_sublists(self):
        self.assertEqual(
            PartOne.get_sublists([10, 13, 16, 21, 30, 45]),
            [
                [10, 13, 16, 21, 30, 45],
                [3, 3, 5, 9, 15],
                [0, 2, 4, 6],
                [2, 2, 2],
                [0, 0],
            ],
        )

    def test_sample(self):
        found_solution = PartOne("sample.txt").solve()
        self.assertEqual(found_solution, 114)

    def test_solve(self):
        found_solution = PartOne("input.txt").solve()
        self.assertEqual(found_solution, 1853145119)


class PartTwo(PartOne):
    @classmethod
    def extrapolate_value(cls, line: list[int]) -> int:
        sublists = cls.get_sublists(line)
        result = 0
        for sublist in reversed(sublists):
            first_value = sublist[0]
            result = first_value - result
        return result


class PartTwoTestCase(unittest.TestCase):
    def test_extrapolate_value(self):
        self.assertEqual(PartTwo.extrapolate_value([0, 3, 6, 9, 12, 15]), -3)
        self.assertEqual(PartTwo.extrapolate_value([1, 3, 6, 10, 15, 21]), 0)
        self.assertEqual(PartTwo.extrapolate_value([10, 13, 16, 21, 30, 45]), 5)

    def test_sample(self):
        found_solution = PartTwo("sample.txt").solve()
        self.assertEqual(found_solution, 2)

    def test_solve(self):
        found_solution = PartTwo("input.txt").solve()
        self.assertEqual(found_solution, 923)


if __name__ == "__main__":
    unittest.main()
