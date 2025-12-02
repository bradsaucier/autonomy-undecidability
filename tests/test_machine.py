from __future__ import annotations

import pytest

from computational_autonomy.machine import Machine, MachineProgram


def test_loop_never_halts_within_any_bound() -> None:
    m = Machine(program=MachineProgram.LOOP, x=10)
    assert m.simulate(0) is None
    assert m.simulate(10) is None
    assert m.simulate(100) is None


def test_halt_halts_when_bound_is_sufficient() -> None:
    m = Machine(program=MachineProgram.HALT, x=3)
    assert m.simulate(0) is None
    assert m.simulate(1) is None
    assert m.simulate(2) is None
    assert m.simulate(3) == 0
    assert m.simulate(10) == 0


def test_negative_bound_rejected() -> None:
    m = Machine(program=MachineProgram.HALT, x=1)
    with pytest.raises(ValueError):
        _ = m.simulate(-1)
