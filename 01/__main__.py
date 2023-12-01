import unittest
from pathlib import Path


def file_lines(file_name: str) -> list[str]:
    with (Path(__file__).parent / file_name).open() as f:
        return f.readlines()


def solve_part_one(file_name):
    def parse_line(line: str) -> int:
        digits = [char for char in line if char.isdigit()]
        return int(f"{digits[0]}{digits[-1]}")

    line_results = [parse_line(line) for line in file_lines(file_name)]
    return sum(line_results)


def solve_part_two(file_name):
    def parse_line(line: str) -> int:
        for i in range(len(line)):
            first_number = get_number(i, line)
            if first_number is not None:
                break

        for i in range(len(line) - 1, -1, -1):
            last_number = get_number(i, line)
            if last_number is not None:
                break

        return int(f"{first_number}{last_number}")

    def get_number(i: int, line: str) -> int | None:
        spelled_numbers = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }

        if line[i].isdigit():
            return int(line[i])

        for spelled, value in spelled_numbers.items():
            if line[i:].startswith(spelled):
                return value

    return sum(parse_line(line) for line in file_lines(file_name))


class Part1TestCase(unittest.TestCase):
    def test_sample(self):
        found_solution = solve_part_one("sample_part1.txt")
        self.assertEqual(found_solution, 142)

    def test_solve_part_one(self):
        found_solution = solve_part_one("input.txt")
        self.assertEqual(found_solution, 54239)


class Part2TestCase(unittest.TestCase):
    def test_sample(self):
        found_solution = solve_part_two("sample_part2.txt")
        self.assertEqual(found_solution, 281)

    def test_solve(self):
        found_solution = solve_part_two("input.txt")
        self.assertEqual(found_solution, 55343)


if __name__ == "__main__":
    unittest.main()
