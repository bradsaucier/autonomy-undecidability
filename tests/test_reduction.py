from __future__ import annotations

import pytest

from computational_autonomy.controller import Action
from computational_autonomy.environment import Environment
from computational_autonomy.machine import Machine, MachineProgram
from computational_autonomy.reduction import ReductionController


def test_reduction_halt_path_can_succeed_and_stay_safe_with_trace() -> None:
    env = Environment.from_strings(
        [
            "..",
            ".G",
        ],
        start=(0, 0),
    )
    rc = ReductionController(machine=Machine(MachineProgram.HALT, x=0), bound=10)
    safe, success, trace = rc.run_episode(env, max_steps=10)

    assert safe is True
    assert success is True
    assert trace[0] == (0, 0)
    assert trace[-1] == (1, 1)
    assert trace[:3] == [(0, 0), (0, 1), (1, 1)]


def test_reduction_loop_path_does_not_succeed_and_trace_stays_put() -> None:
    env = Environment.from_strings(
        [
            "..",
            ".G",
        ],
        start=(0, 0),
    )
    rc = ReductionController(machine=Machine(MachineProgram.LOOP, x=0), bound=10)
    safe, success, trace = rc.run_episode(env, max_steps=5)

    assert safe is True
    assert success is False
    assert trace[0] == (0, 0)
    assert all(pos == (0, 0) for pos in trace)


def test_run_episode_rejects_nonpositive_max_steps() -> None:
    env = Environment.from_strings([".."], start=(0, 0))
    rc = ReductionController(machine=Machine(MachineProgram.LOOP, x=0), bound=5)

    with pytest.raises(ValueError):
        rc.run_episode(env, max_steps=0)


def test_run_episode_flags_hazard_when_start_in_hazard() -> None:
    env = Environment.from_strings(["H"], start=(0, 0))
    rc = ReductionController(machine=Machine(MachineProgram.LOOP, x=0), bound=5)

    safe, success, trace = rc.run_episode(env, max_steps=3)

    assert safe is False
    assert success is False
    assert trace[0] == (0, 0)


def test_good_policy_picks_safe_move_when_no_goal_neighbors() -> None:
    env = Environment.from_strings(
        [
            "...",
            ".X.",
            "...",
        ],
        start=(1, 1),
    )

    result = ReductionController._good_policy(env, (1, 1))

    assert result.action in {Action.RIGHT, Action.DOWN, Action.LEFT, Action.UP}
    assert result.success_signal is False


def test_good_policy_stays_put_when_surrounded_by_obstacles() -> None:
    env = Environment.from_strings(
        [
            "XXX",
            "XXX",
            "XXX",
        ],
        start=(1, 1),
    )

    result = ReductionController._good_policy(env, (1, 1))

    assert result.action == Action.STAY
    assert result.success_signal is False


def test_halted_controller_stays_put_when_surrounded_by_obstacles() -> None:
    env = Environment.from_strings(
        [
            "XXX",
            "XXX",
            "XXX",
        ],
        start=(1, 1),
    )

    rc = ReductionController(machine=Machine(MachineProgram.HALT, x=0), bound=5)
    safe, success, trace = rc.run_episode(env, max_steps=3)

    assert safe is True
    assert success is False
    assert all(pos == (1, 1) for pos in trace)


def test_good_policy_skips_out_of_bounds_neighbors() -> None:
    env = Environment.from_strings(
        [
            "X",
            "X",
        ],
        start=(0, 0),
    )

    result = ReductionController._good_policy(env, (0, 0))

    assert result.action == Action.STAY
    assert result.success_signal is False
