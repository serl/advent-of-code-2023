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
    class Number:
        value: int
        row: int
        column: int
        length: int

        @classmethod
        def parse_lines(cls, lines: list[str]) -> list[Self]:
            found = []
            for line_idx, line in enumerate(lines):
                for match in re.finditer(r"(\d+)", line):
                    found.append(
                        cls(
                            value=int(match.group(1)),
                            row=line_idx,
                            column=match.start(1),
                            length=match.end(1) - match.start(1),
                        )
                    )
            return found

        def has_adjacent_symbol(self, lines: list[str]) -> bool:
            for row in range(self.row - 1, self.row + 2):
                for column in range(self.column - 1, self.column + self.length + 1):
                    try:
                        char = lines[row][column]
                    except IndexError:
                        continue
                    if not char.isdigit() and char != ".":
                        # print(f"{row=} {column=} {char=}")
                        return True
            return False

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def solve(self) -> int:
        lines = read_file(self.file_name)
        numbers = PartOne.Number.parse_lines(lines)
        return sum(
            number.value for number in numbers if number.has_adjacent_symbol(lines)
        )


class PartOneTestCase(unittest.TestCase):
    def test_find_numbers(self):
        numbers = PartOne.Number.parse_lines(
            [
                "467..114..",
                "...*......",
                "..35..633.",
            ]
        )
        self.assertEqual(
            numbers,
            [
                PartOne.Number(467, 0, 0, 3),
                PartOne.Number(114, 0, 5, 3),
                PartOne.Number(35, 2, 2, 2),
                PartOne.Number(633, 2, 6, 3),
            ],
        )

    def test_has_adjacent_symbol_never(self):
        def assertNotAdjacent(lines):
            numbers = PartOne.Number.parse_lines(lines)
            for number in numbers:
                self.assertFalse(number.has_adjacent_symbol(lines))

        assertNotAdjacent(
            [
                "123.4..",
                "45...6.",
            ]
        )

        assertNotAdjacent(
            [
                "123",
            ]
        )

        assertNotAdjacent(
            [
                ".....",
                "..1..",
                ".....",
            ]
        )
        assertNotAdjacent(
            [
                "+++++",
                "+...+",
                "+.1.+",
                "+...+",
                "+++++",
            ]
        )

    def test_has_adjacent_symbol_sample(self):
        lines = read_file("sample.txt")

        self.assertTrue(PartOne.Number(467, 0, 0, 3).has_adjacent_symbol(lines))
        self.assertFalse(PartOne.Number(114, 0, 5, 3).has_adjacent_symbol(lines))
        self.assertTrue(PartOne.Number(35, 2, 2, 2).has_adjacent_symbol(lines))
        self.assertTrue(PartOne.Number(633, 2, 6, 3).has_adjacent_symbol(lines))
        self.assertTrue(PartOne.Number(617, 4, 0, 3).has_adjacent_symbol(lines))
        self.assertFalse(PartOne.Number(58, 5, 7, 2).has_adjacent_symbol(lines))
        self.assertTrue(PartOne.Number(592, 6, 2, 3).has_adjacent_symbol(lines))
        self.assertTrue(PartOne.Number(755, 7, 6, 3).has_adjacent_symbol(lines))
        self.assertTrue(PartOne.Number(664, 9, 1, 3).has_adjacent_symbol(lines))
        self.assertTrue(PartOne.Number(598, 9, 5, 3).has_adjacent_symbol(lines))

    def test_has_adjacent_symbol_input(self):
        lines = [
            "...................*.....*.....*......@.....*............../....566........+.....................*906....................%..................",
            "....459.78$.775.768..62...345.537......122.803.142*758...148...*....992................711....316.........#...............521.298*590..289..",
            "....*.................#.........................................444............382.....*...@...............753.......927................/...",
        ]
        numbers = PartOne.Number.parse_lines(lines)
        for number in numbers:
            self.assertEqual(
                number.has_adjacent_symbol(lines),
                number.value not in {775, 992, 382, 927},
            )

    def test_sample(self):
        found_solution = PartOne("sample.txt").solve()
        self.assertEqual(found_solution, 4361)

    def test_solve(self):
        found_solution = PartOne("input.txt").solve()
        self.assertEqual(found_solution, 540025)


class PartTwo:
    @dataclass(frozen=True)
    class Gear:
        part_numbers: tuple[int, int]

        def get_ratio(self):
            return self.part_numbers[0] * self.part_numbers[1]

        @classmethod
        def parse_lines(cls, lines: list[str]) -> list[Self]:
            found = []
            for line_idx, line in enumerate(lines):
                # print(line)
                for match in re.finditer(r"(\*)", line):
                    # print(f"{match.start(0)=}")
                    part_numbers = cls._find_numbers(line, match.start(0))
                    if line_idx > 0:
                        part_numbers.extend(
                            cls._find_numbers(lines[line_idx - 1], match.start(0))
                        )
                    try:
                        part_numbers.extend(
                            cls._find_numbers(lines[line_idx + 1], match.start(0))
                        )
                    except IndexError:
                        pass

                    # print(part_numbers)
                    if len(part_numbers) == 2:
                        found.append(cls(tuple(part_numbers)))
            return found

        @staticmethod
        def _find_numbers(line: str, column: int) -> list[int]:
            output = []
            # print(f"Looking {line=}")

            for match in re.finditer(r"\d+", line):
                if match.start(0) - 1 <= column <= match.end(0):
                    output.append(int(match.group(0)))

            return output

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def solve(self) -> int:
        lines = read_file(self.file_name)
        gears = PartTwo.Gear.parse_lines(lines)
        return sum(gear.get_ratio() for gear in gears)


class PartTwoTestCase(unittest.TestCase):
    def test_gear_parse_single_line(self):
        gears = PartTwo.Gear.parse_lines(["...123*456...12..34*"])
        self.assertEqual(len(gears), 1)
        self.assertEqual(gears[0].part_numbers, (123, 456))

    def test_gear_parse_multiple_lines(self):
        gears = PartTwo.Gear.parse_lines(
            [
                "467..114..",
                "...*......",
                "..35..633.",
            ]
        )
        self.assertEqual(len(gears), 1)
        self.assertEqual(gears[0].part_numbers, (467, 35))

    def test_gear_parse_multiple_lines_all_positions(self):
        lines_possible = [
            [
                "467*......",
                ".35...633.",
            ],
            [
                "467*......",
                "..35..633.",
            ],
            [
                "467*......",
                "...35.633.",
            ],
            [
                "467*......",
                "....35.633",
            ],
        ]
        for lines in lines_possible:
            gears = PartTwo.Gear.parse_lines(lines)
            self.assertEqual(len(gears), 1)
            self.assertEqual(gears[0].part_numbers, (467, 35))

    def test_sample_ratios(self):
        lines = read_file("sample.txt")
        gears = PartTwo.Gear.parse_lines(lines)
        self.assertEqual(len(gears), 2, gears)
        self.assertEqual(gears[0].part_numbers, (467, 35))
        self.assertEqual(gears[1].part_numbers, (755, 598))
        self.assertEqual(gears[0].get_ratio(), 16345)
        self.assertEqual(gears[1].get_ratio(), 451490)

    def test_sample(self):
        found_solution = PartTwo("sample.txt").solve()
        self.assertEqual(found_solution, 467835)

    def test_solve(self):
        found_solution = PartTwo("input.txt").solve()
        self.assertEqual(found_solution, 84584891)


if __name__ == "__main__":
    unittest.main()
