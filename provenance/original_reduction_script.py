"""
Archived script placed here for provenance.

This file is intentionally not imported by the package.
It demonstrates an earlier single-file implementation of the same idea.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


class Cell(str, Enum):
    EMPTY = "."
    OBSTACLE = "X"
    HAZARD = "H"
    GOAL = "G"


class Action(str, Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"
    STAY = "S"


@dataclass(frozen=True)
class Env:
    grid: List[List[Cell]]
    start: Tuple[int, int]

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0])

    def at(self, r: int, c: int) -> Cell:
        return self.grid[r][c]


class Program(str, Enum):
    HALT = "halt"
    LOOP = "loop"


@dataclass(frozen=True)
class Machine:
    program: Program
    x: int

    def simulate(self, bound: int) -> Optional[int]:
        if self.program == Program.LOOP:
            return None
        steps = 0
        v = self.x
        while steps < bound:
            if v <= 0:
                return 0
            v -= 1
            steps += 1
        return None


def step(pos: Tuple[int, int], act: Action) -> Tuple[int, int]:
    r, c = pos
    if act == Action.UP:
        return (r - 1, c)
    if act == Action.DOWN:
        return (r + 1, c)
    if act == Action.LEFT:
        return (r, c - 1)
    if act == Action.RIGHT:
        return (r, c + 1)
    return pos


def good_policy(env: Env, pos: Tuple[int, int]) -> Tuple[Action, bool]:
    r, c = pos
    for act in [Action.RIGHT, Action.DOWN, Action.LEFT, Action.UP]:
        nr, nc = step((r, c), act)
        if not env.in_bounds(nr, nc):
            continue
        cell = env.at(nr, nc)
        if cell == Cell.OBSTACLE or cell == Cell.HAZARD:
            continue
        if cell == Cell.GOAL:
            return (act, True)
    for act in [Action.RIGHT, Action.DOWN, Action.LEFT, Action.UP]:
        nr, nc = step((r, c), act)
        if not env.in_bounds(nr, nc):
            continue
        cell = env.at(nr, nc)
        if cell == Cell.OBSTACLE or cell == Cell.HAZARD:
            continue
        return (act, False)
    return (Action.STAY, False)


def run(program: Program, x: int, bound: int, max_steps: int) -> Tuple[bool, bool]:
    env = Env(
        grid=[
            [Cell.EMPTY, Cell.EMPTY, Cell.OBSTACLE, Cell.EMPTY, Cell.EMPTY],
            [Cell.EMPTY, Cell.HAZARD, Cell.EMPTY, Cell.OBSTACLE, Cell.EMPTY],
            [Cell.EMPTY, Cell.EMPTY, Cell.OBSTACLE, Cell.EMPTY, Cell.EMPTY],
            [Cell.EMPTY, Cell.OBSTACLE, Cell.EMPTY, Cell.EMPTY, Cell.GOAL],
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
        ],
        start=(0, 0),
    )

    m = Machine(program=program, x=x)
    halted = m.simulate(bound) is not None

    pos = env.start
    safe = env.at(*pos) != Cell.HAZARD
    success = False

    for _ in range(max_steps):
        if halted:
            act, sig = good_policy(env, pos)
        else:
            act, sig = (Action.STAY, False)

        nxt = step(pos, act)
        if env.in_bounds(*nxt) and env.at(*nxt) != Cell.OBSTACLE:
            pos = nxt

        if env.at(*pos) == Cell.HAZARD:
            safe = False
        if env.at(*pos) == Cell.GOAL and sig:
            success = True
            break

    return safe, success


if __name__ == "__main__":
    print(run(Program.HALT, x=10, bound=200, max_steps=60))
    print(run(Program.LOOP, x=10, bound=200, max_steps=60))
