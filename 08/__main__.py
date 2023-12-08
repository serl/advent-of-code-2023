import re
import unittest
from pathlib import Path
from typing import Self


def read_file(file_name: str) -> list[str]:
    with (Path(__file__).parent / file_name).open() as f:
        return [line.strip() for line in f.readlines()]


class Graph(dict[str, dict[str, str]]):
    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        graph = cls()
        for line in lines:
            match = re.fullmatch(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", line)
            assert match
            graph[match[1]] = {"L": match[2], "R": match[3]}
        return graph


def infinite_instructions(instructions):
    while True:
        yield from instructions


class PartOne:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def parse_input(self) -> tuple[str, Graph]:
        lines = read_file(self.file_name)
        instructions = lines[0]
        graph = Graph.from_lines(lines[2:])
        return instructions, graph

    def solve(self) -> int:
        instructions, graph = self.parse_input()

        steps = 1
        current_node = graph["AAA"]
        for which in infinite_instructions(instructions):
            next_node = current_node[which]
            if next_node == "ZZZ":
                return steps
            current_node = graph[next_node]
            steps += 1


class PartOneTestCase(unittest.TestCase):
    def test_parse(self):
        instructions, graph = PartOne("sample_1.txt").parse_input()
        self.assertEqual(instructions, "RL")
        self.assertEqual(len(graph), 7)
        self.assertEqual(
            list(graph.keys()), ["AAA", "BBB", "CCC", "DDD", "EEE", "GGG", "ZZZ"]
        )
        self.assertEqual(graph["AAA"], {"L": "BBB", "R": "CCC"})

    def test_sample_1(self):
        found_solution = PartOne("sample_1.txt").solve()
        self.assertEqual(found_solution, 2)

    def test_sample_2(self):
        found_solution = PartOne("sample_2.txt").solve()
        self.assertEqual(found_solution, 6)

    def test_solve(self):
        found_solution = PartOne("input.txt").solve()
        self.assertEqual(found_solution, 12737)


if __name__ == "__main__":
    unittest.main()
