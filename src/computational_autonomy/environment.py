from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, List, Tuple


class Cell(str, Enum):
    EMPTY = "."
    OBSTACLE = "X"
    HAZARD = "H"
    GOAL = "G"


@dataclass(frozen=True)
class Environment:
    """A minimal grid world.

    The agent starts at a configured coordinate. Obstacles block movement.
    Hazards are unsafe. The goal cell indicates success when reached.
    """

    grid: List[List[Cell]]
    start: Tuple[int, int]

    @property
    def height(self) -> int:
        return len(self.grid)

    @property
    def width(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.height and 0 <= c < self.width

    def at(self, r: int, c: int) -> Cell:
        if not self.in_bounds(r, c):
            raise IndexError("out of bounds")
        return self.grid[r][c]

    def is_blocked(self, r: int, c: int) -> bool:
        return self.at(r, c) == Cell.OBSTACLE

    def is_hazard(self, r: int, c: int) -> bool:
        return self.at(r, c) == Cell.HAZARD

    def is_goal(self, r: int, c: int) -> bool:
        return self.at(r, c) == Cell.GOAL

    def render(self, agent_pos: Tuple[int, int]) -> str:
        ar, ac = agent_pos
        out: List[str] = []
        for r, row in enumerate(self.grid):
            line: List[str] = []
            for c, cell in enumerate(row):
                if (r, c) == (ar, ac):
                    line.append("A")
                else:
                    line.append(str(cell.value))
            out.append("".join(line))
        return "\n".join(out)

    @staticmethod
    def from_strings(rows: Iterable[str], start: Tuple[int, int]) -> Environment:
        row_list = list(rows)
        if not row_list:
            raise ValueError("rows must be non-empty")

        if any(row == "" for row in row_list):
            raise ValueError("rows must not contain empty strings")

        width = len(row_list[0])
        if width == 0:
            raise ValueError("rows must not contain empty strings")

        for row in row_list:
            if len(row) != width:
                raise ValueError("rows must be rectangular")

        grid: List[List[Cell]] = [[Cell(ch) for ch in row] for row in row_list]

        sr, sc = start
        if sr < 0 or sc < 0 or sr >= len(grid) or sc >= width:
            raise ValueError("start must be in bounds")

        return Environment(grid=grid, start=start)