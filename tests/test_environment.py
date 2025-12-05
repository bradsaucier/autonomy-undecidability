from __future__ import annotations

import pytest

from computational_autonomy.environment import Cell, Environment


def test_from_strings_and_access() -> None:
    env = Environment.from_strings([".G", "HX"], start=(0, 0))
    assert env.height == 2
    assert env.width == 2
    assert env.at(0, 1) == Cell.GOAL
    assert env.is_goal(0, 1)
    assert env.is_hazard(1, 0)
    assert env.is_blocked(1, 1)


def test_out_of_bounds_raises() -> None:
    env = Environment.from_strings([".."], start=(0, 0))
    with pytest.raises(IndexError):
        _ = env.at(2, 2)


def test_render_renders_agent_and_cells() -> None:
    env = Environment.from_strings([".G", "HX"], start=(0, 0))
    rendered = env.render((1, 0))

    lines = rendered.splitlines()
    assert lines[0] == ".G"
    assert lines[1] == "AX"
