import re
import unittest
from pathlib import Path
from typing import Self
import math


def read_file(file_name: str) -> list[str]:
    with (Path(__file__).parent / file_name).open() as f:
        return [line.strip() for line in f.readlines()]


class Graph(dict[str, dict[str, str]]):
    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        graph = cls()
        for line in lines:
            match = re.fullmatch(r"([\w]{3}) = \(([\w]{3}), ([\w]{3})\)", line)
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


class PartTwo(PartOne):
    def solve(self) -> int:
        instructions, graph = self.parse_input()

        steps = 1
        current_nodes = [graph[node] for node in graph.keys() if node.endswith("A")]
        minimum_steps = [0] * len(current_nodes)
        for which in infinite_instructions(instructions):
            next_nodes = [node[which] for node in current_nodes]
            for i, node in enumerate(next_nodes):
                if minimum_steps[i] == 0 and node.endswith("Z"):
                    minimum_steps[i] = steps
            if all(s > 0 for s in minimum_steps):
                break
            current_nodes = [graph[next_node] for next_node in next_nodes]
            steps += 1

        return math.lcm(*minimum_steps)


class PartTwoTestCase(unittest.TestCase):
    def test_sample_3(self):
        found_solution = PartTwo("sample_3.txt").solve()
        self.assertEqual(found_solution, 6)

    def test_solve(self):
        found_solution = PartTwo("input.txt").solve()
        self.assertEqual(found_solution, 9064949303801)


if __name__ == "__main__":
    unittest.main()
