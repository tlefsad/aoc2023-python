#!/usr/bin/env python3
"""Solution to Day 7: 
https://adventofcode.com/2023/day/7
"""
from __future__ import annotations

from typing import TextIO, Iterable, Self
from helpers.cli import command_with_input_file, open_input_file
import dataclasses
from enum import IntEnum, StrEnum, unique 
from collections import Counter
from dataclasses import field

        
@command_with_input_file
def program(input_file):
    """Main program.
    """
    with open_input_file(input_file) as fobj:
        hands = read_input(fobj)

    fst_ranked_hands = sorted(get_hand(cards, cards, bid) for cards, bid in hands)
    print("Part 1:", total_winnings(fst_ranked_hands))

    snd_ranked_hands = sorted(get_hand(cards.replace('J', ''), 
                                       cards.replace('J', '?'), bid) for cards, bid in hands)
    print("Part 2:", total_winnings(snd_ranked_hands))


def read_input(fobj: TextIO) -> list[list[str]]:
    """Reads and parses input file according to problem statement.
    """
    return [line.strip().split() for line in fobj]


@unique
class Card(StrEnum):
    JOKER: str = '?'
    DEUCE: str = '2'
    THREE: str = '3'
    FOUR: str = '4'
    FIVE: str = '5'
    SIX: str = '6'
    SEVEN: str = '7'
    EIGHT: str = '8'
    NINE: str = '9'
    TEN: str = 'T'
    JACK: str = 'J'
    QUEEN: str = 'Q'
    KING: str = 'K'
    ACE: str = 'A' 

    def __lt__(self, other):
        return (self._member_names_.index(self.name) < 
                self._member_names_.index(other.name))


@unique
class Label(IntEnum):
    """
    The enum class for all hand classification labels.
    """
    HIGH_CARD: int = 1
    ONE_PAIR: int = 2
    TWO_PAIR: int = 3
    THREE_OF_A_KIND: int = 4
    FULL_HOUSE: int = 5
    FOUR_OF_A_KIND: int = 6
    FIVE_OF_A_KIND: int = 7

    @staticmethod
    def from_str(s: str) -> Label:
        match sorted(Counter(s).values()):
            case [1, 1, 1, 1, 1]:
                return Label.HIGH_CARD
            case [1, 1, 1, _]:
                return Label.ONE_PAIR
            case [1, 2, 2]:
                return Label.TWO_PAIR
            case [1, 1, _]:
                return Label.THREE_OF_A_KIND
            case [2, _]:
                return Label.FULL_HOUSE
            case [1, _]:
                return Label.FOUR_OF_A_KIND
            case _:
                return Label.FIVE_OF_A_KIND


@dataclasses.dataclass(order=True, frozen=True)
class Hand:
    label: Label
    cards: tuple[Card]
    bid: int = field(compare=False)


def get_hand(label_cards: str, cards: str, bid: str) -> Hand:
    return Hand(
        label=Label.from_str(label_cards),
        cards=tuple(Card(card) for card in cards),
        bid=int(bid)
    )

def total_winnings(ranked_hands: list[Hand]) -> int:
    return sum(hand.bid * (rank+1) for rank, hand in enumerate(ranked_hands))
    

if __name__ == '__main__':
    program()

