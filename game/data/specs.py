from dataclasses import dataclass
from typing import Optional


@dataclass
class Element:
    name: str
    colour: Optional[str]
    font: str
    wins_against: list[str]


@dataclass
class Player:
    name: str
    element: Optional[Element] = None
    total_win_count: int = 0
    battles_fought: int = 0
    active_score: int = 0


@dataclass
class Record:
    high_score: int = 0
    player: Optional[str] = None
