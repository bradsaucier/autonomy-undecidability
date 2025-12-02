from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class Action(str, Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"
    STAY = "S"


@dataclass(frozen=True)
class ControllerResult:
    action: Action
    success_signal: bool


def step(pos: Tuple[int, int], action: Action) -> Tuple[int, int]:
    r, c = pos
    if action == Action.UP:
        return (r - 1, c)
    if action == Action.DOWN:
        return (r + 1, c)
    if action == Action.LEFT:
        return (r, c - 1)
    if action == Action.RIGHT:
        return (r, c + 1)
    return (r, c)
