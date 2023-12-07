import re
import unittest
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Self


def read_file(file_name: str) -> list[str]:
    with (Path(__file__).parent / file_name).open() as f:
        return [line.strip() for line in f.readlines()]


class PartOne:
    @dataclass(frozen=True)
    class Hand:
        cards: str
        bid: int

        CARDS_ORDER = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

        @classmethod
        def from_line(cls, line: str) -> Self:
            line_match = re.fullmatch(
                r"([" + "".join(cls.CARDS_ORDER) + r"]{5}) (\d+)", line
            )
            assert line_match
            return cls(
                cards=line_match[1],
                bid=int(line_match[2]),
            )

        @property
        def count_cards(self) -> dict[str, int]:
            return {
                card: count for card, count in Counter(self.cards).items() if count >= 2
            }

        @property
        def type(self) -> int:
            match sorted(self.count_cards.values()):
                case [5]:
                    return 0
                case [4]:
                    return 1
                case [2, 3]:
                    return 2
                case [3]:
                    return 3
                case [2, 2]:
                    return 4
                case [2]:
                    return 5
                case _:
                    return 6

        def nth_card_value(self, index: int) -> int:
            return self.CARDS_ORDER.index(self.cards[index])

        def sort_key(self) -> int:
            factors = [
                self.type * len(self.CARDS_ORDER) ** 5,
                self.nth_card_value(0) * len(self.CARDS_ORDER) ** 4,
                self.nth_card_value(1) * len(self.CARDS_ORDER) ** 3,
                self.nth_card_value(2) * len(self.CARDS_ORDER) ** 2,
                self.nth_card_value(3) * len(self.CARDS_ORDER) ** 1,
                self.nth_card_value(4) * len(self.CARDS_ORDER) ** 0,
            ]
            return sum(factors)

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def parse_input(self) -> list[Hand]:
        lines = read_file(self.file_name)
        return [self.Hand.from_line(line) for line in lines]

    def solve(self) -> int:
        hands = self.parse_input()
        sorted_hands = reversed(sorted(hands, key=self.Hand.sort_key))

        return sum((i + 1) * hand.bid for i, hand in enumerate(sorted_hands))


class PartOneTestCase(unittest.TestCase):
    def test_hand_parse(self):
        hand = PartOne.Hand.from_line("T55J5 684")
        self.assertEqual(hand.cards, "T55J5")
        self.assertEqual(hand.bid, 684)

    def test_hand_count_type(self):
        hand = PartOne.Hand("T55J5", 0)
        self.assertEqual(hand.count_cards, {"5": 3})
        self.assertEqual(hand.type, 3)
        self.assertEqual(hand.nth_card_value(0), 4)

        hand = PartOne.Hand("AAAAA", 0)
        self.assertEqual(hand.count_cards, {"A": 5})
        self.assertEqual(hand.type, 0)
        self.assertEqual(hand.nth_card_value(0), 0)

        hand = PartOne.Hand("AA8AA", 0)
        self.assertEqual(hand.count_cards, {"A": 4})
        self.assertEqual(hand.type, 1)
        self.assertEqual(hand.nth_card_value(0), 0)
        self.assertEqual(hand.nth_card_value(2), 6)

        hand = PartOne.Hand("23332", 0)
        self.assertEqual(hand.count_cards, {"3": 3, "2": 2})
        self.assertEqual(hand.type, 2)
        self.assertEqual(hand.nth_card_value(0), 12)

        hand = PartOne.Hand("TTT98", 0)
        self.assertEqual(hand.count_cards, {"T": 3})
        self.assertEqual(hand.type, 3)
        self.assertEqual(hand.nth_card_value(0), 4)

        hand = PartOne.Hand("23432", 0)
        self.assertEqual(hand.count_cards, {"2": 2, "3": 2})
        self.assertEqual(hand.type, 4)
        self.assertEqual(hand.nth_card_value(0), 12)

        hand = PartOne.Hand("A23A4", 0)
        self.assertEqual(hand.count_cards, {"A": 2})
        self.assertEqual(hand.type, 5)
        self.assertEqual(hand.nth_card_value(0), 0)

        hand = PartOne.Hand("23456", 0)
        self.assertEqual(hand.count_cards, {})
        self.assertEqual(hand.type, 6)
        self.assertEqual(hand.nth_card_value(0), 12)

    def test_hand_sort(self):
        hands = PartOne("sample.txt").parse_input()
        sorted_hands = sorted(hands, key=PartOne.Hand.sort_key)
        self.assertEqual(sorted_hands[0].cards, "QQQJA")
        self.assertEqual(sorted_hands[1].cards, "T55J5")
        self.assertEqual(sorted_hands[2].cards, "KK677")
        self.assertEqual(sorted_hands[3].cards, "KTJJT")
        self.assertEqual(sorted_hands[4].cards, "32T3K")

    def test_sample(self):
        found_solution = PartOne("sample.txt").solve()
        self.assertEqual(found_solution, 6440)

    def test_solve(self):
        found_solution = PartOne("input.txt").solve()
        self.assertEqual(found_solution, 251545216)


class PartTwo(PartOne):
    class Hand(PartOne.Hand):
        CARDS_ORDER = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

        @property
        def count_cards(self) -> dict[str, int]:
            raw_count = Counter(self.cards)

            jokers = raw_count.pop("J") if "J" in raw_count else 0
            try:
                best_card, best_card_count = raw_count.most_common(1)[0]
            except IndexError:
                best_card = self.CARDS_ORDER[0]
                best_card_count = 0

            raw_count[best_card] = best_card_count + jokers

            return {card: count for card, count in raw_count.items() if count >= 2}


class PartTwoTestCase(unittest.TestCase):
    def test_sample(self):
        found_solution = PartTwo("sample.txt").solve()
        self.assertEqual(found_solution, 5905)

    def test_solve(self):
        found_solution = PartTwo("input.txt").solve()
        self.assertEqual(found_solution, 250384185)


if __name__ == "__main__":
    unittest.main()
