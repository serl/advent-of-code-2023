import re
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Self


def read_file(file_name: str) -> list[str]:
    with (Path(__file__).parent / file_name).open() as f:
        return [line.strip() for line in f.readlines()]


@dataclass
class PartOne:
    @dataclass(frozen=True)
    class Map:
        source_category: str
        destination_category: str
        ranges: list["Range"]

        def map(self, source: int) -> int:
            for range in self.ranges:
                if mapped := range.map(source):
                    return mapped
            return source

        @classmethod
        def from_block(cls, lines: list[str]) -> Self:
            header_match = re.fullmatch(r"(\w+)-to-(\w+) map:", lines[0])
            assert header_match
            return cls(
                header_match[1],
                header_match[2],
                [cls.Range.from_line(line) for line in lines[1:]],
            )

        @dataclass(frozen=True)
        class Range:
            destination_start: int
            source_start: int
            length: int

            def map(self, source: int) -> int | None:
                if self.source_start <= source < self.source_start + self.length:
                    delta = source - self.source_start
                    return self.destination_start + delta

            @classmethod
            def from_line(cls, line: str) -> Self:
                match = re.fullmatch(r"(\d+)\s(\d+)\s(\d+)", line)
                assert match
                return cls(int(match[1]), int(match[2]), int(match[3]))

    file_name: str
    seeds: list[int] | None = None
    maps: list[Map] | None = None

    def seed_to_location(self, seed: int) -> int:
        assert self.maps

        current = seed
        for map in self.maps:
            current = map.map(current)
        return current

    def solve(self) -> int:
        self.parse()
        assert self.seeds

        seeds_to_end = {seed: self.seed_to_location(seed) for seed in self.seeds}

        return min(seeds_to_end.values())

    def parse(self) -> None:
        lines = read_file(self.file_name)

        self.seeds = list(map(int, re.findall(r"\d+", lines[0])))

        self.maps = []
        block = []
        for line in lines[2:] + [None]:
            if line:
                block.append(line)
            else:
                self.maps.append(self.Map.from_block(block))
                block = []


class PartOneTestCase(unittest.TestCase):
    def test_map_range(self):
        r = PartOne.Map.Range.from_line("30 3 2")

        # from_line
        self.assertEqual(r.destination_start, 30)
        self.assertEqual(r.source_start, 3)
        self.assertEqual(r.length, 2)

        # map
        self.assertIsNone(r.map(2))
        self.assertEqual(r.map(3), 30)
        self.assertEqual(r.map(4), 31)
        self.assertIsNone(r.map(5))

    def test_map(self):
        lines = [
            "seed-to-soil map:",
            "50 98 2",
            "52 50 48",
        ]
        m = PartOne.Map.from_block(lines)

        # from_block
        self.assertEqual(m.source_category, "seed")
        self.assertEqual(m.destination_category, "soil")
        self.assertEqual(m.ranges[0].destination_start, 50)
        self.assertEqual(m.ranges[0].source_start, 98)
        self.assertEqual(m.ranges[0].length, 2)
        self.assertEqual(m.ranges[1].destination_start, 52)
        self.assertEqual(m.ranges[1].source_start, 50)
        self.assertEqual(m.ranges[1].length, 48)

        # map
        self.assertEqual(m.map(79), 81)
        self.assertEqual(m.map(14), 14)
        self.assertEqual(m.map(55), 57)
        self.assertEqual(m.map(13), 13)

    def test_parse(self):
        solver = PartOne("sample.txt")
        solver.parse()
        self.assertEqual(solver.seeds, [79, 14, 55, 13])
        self.assertEqual(len(solver.maps), 7)

    def test_seed_to_location(self):
        solver = PartOne("sample.txt")
        solver.parse()

        self.assertEqual(solver.seed_to_location(79), 82)
        self.assertEqual(solver.seed_to_location(14), 43)
        self.assertEqual(solver.seed_to_location(55), 86)
        self.assertEqual(solver.seed_to_location(13), 35)

    def test_sample(self):
        found_solution = PartOne("sample.txt").solve()
        self.assertEqual(found_solution, 35)

    def test_solve(self):
        found_solution = PartOne("input.txt").solve()
        self.assertEqual(found_solution, 323142486)


if __name__ == "__main__":
    unittest.main()
