from __future__ import annotations

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
