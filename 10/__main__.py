import unittest
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Self


def read_file(file_name: str) -> list[str]:
    with (Path(__file__).parent / file_name).open() as f:
        return [line.strip() for line in f.readlines()]


@dataclass(frozen=True)
class Tile:
    x: int
    y: int
    north: bool = False
    east: bool = False
    south: bool = False
    west: bool = False

    def connected_tiles_indexes(self) -> list[tuple[int, int]]:
        tiles = []
        if self.north:
            tiles.append((self.x, self.y - 1))
        if self.east:
            tiles.append((self.x + 1, self.y))
        if self.south:
            tiles.append((self.x, self.y + 1))
        if self.west:
            tiles.append((self.x - 1, self.y))
        return tiles

    @classmethod
    @property
    @cache
    def _letters_mapping(cls) -> dict[str, dict]:
        return {
            "|": dict(north=True, south=True),
            "-": dict(east=True, west=True),
            "L": dict(north=True, east=True),
            "J": dict(north=True, west=True),
            "7": dict(south=True, west=True),
            "F": dict(south=True, east=True),
        }

    @classmethod
    def from_letter(cls, x: int, y: int, letter: str) -> Self:
        return cls(x, y, **cls._letters_mapping.get(letter, {}))


@dataclass(frozen=True)
class Field:
    start_tile: Tile
    tiles: dict[tuple[int, int], Tile]

    def connected_tiles(self, tile: Tile) -> list[Tile]:
        return [self.tiles[idx] for idx in tile.connected_tiles_indexes()]

    def find_loop(self) -> dict[tuple[int, int], Tile]:
        loop: list[Tile] = [self.start_tile]
        while True:
            current_tile = loop[-1]
            try:
                previous_tile = loop[-2]
            except IndexError:
                previous_tile = None
            next_tile = next(
                t for t in self.connected_tiles(current_tile) if t != previous_tile
            )
            if next_tile == self.start_tile:
                break
            loop.append(next_tile)
        return {(t.x, t.y): t for t in loop}

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        start_tile_idx = None
        tiles: dict[tuple[int, int], Tile] = {}
        for y, line in enumerate(lines):
            for x, letter in enumerate(line):
                if letter == "S":
                    start_tile_idx = (x, y)
                else:
                    tiles[x, y] = Tile.from_letter(x, y, letter)

        assert start_tile_idx
        start_tile_connections = {}
        try:
            if tiles[start_tile_idx[0], start_tile_idx[1] - 1].south:
                start_tile_connections["north"] = True
        except KeyError:
            pass
        try:
            if tiles[start_tile_idx[0] + 1, start_tile_idx[1]].west:
                start_tile_connections["east"] = True
        except KeyError:
            pass
        try:
            if tiles[start_tile_idx[0], start_tile_idx[1] + 1].north:
                start_tile_connections["south"] = True
        except KeyError:
            pass
        try:
            if tiles[start_tile_idx[0] - 1, start_tile_idx[1]].east:
                start_tile_connections["west"] = True
        except KeyError:
            pass

        start_tile = Tile(*start_tile_idx, **start_tile_connections)
        tiles[start_tile_idx] = start_tile
        return cls(
            start_tile,
            tiles,
        )


class PartOne:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def parse_input(self) -> Field:
        lines = read_file(self.file_name)
        return Field.from_lines(lines)

    def solve(self) -> int:
        field = self.parse_input()
        half_loop_length = len(field.find_loop()) / 2
        return int(half_loop_length)


class PartOneTestCase(unittest.TestCase):
    def test_parse_input(self):
        field = PartOne("sample_1.txt").parse_input()
        self.assertEqual(field.start_tile, Tile(1, 1, east=True, south=True))
        self.assertEqual(field.tiles[1, 3], Tile(1, 3, north=True, east=True))

    def test_sample_1(self):
        found_solution = PartOne("sample_1.txt").solve()
        self.assertEqual(found_solution, 4)

    def test_sample_2(self):
        found_solution = PartOne("sample_2.txt").solve()
        self.assertEqual(found_solution, 8)

    def test_solve(self):
        found_solution = PartOne("input.txt").solve()
        self.assertEqual(found_solution, 6831)


if __name__ == "__main__":
    unittest.main()
