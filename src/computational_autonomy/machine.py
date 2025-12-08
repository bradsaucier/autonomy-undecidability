from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class MachineProgram(str, Enum):
    """A tiny stand-in for a program.

    1. HALT halts after decrementing x to 0.
    2. LOOP never halts.
    """

    HALT = "halt"
    LOOP = "loop"


@dataclass(frozen=True)
class Machine:
    """A minimal register-style machine with one register x.

    The purpose is to supply a concrete object that can be simulated for B steps.
    """

    program: MachineProgram
    x: int

    def simulate(self, bound: int) -> Optional[int]:
        """Simulate up to bound steps.

        Returns an integer result if the program halts within the bound.
        Returns None if it does not halt within the bound.
        """
        if bound < 0:
            raise ValueError("bound must be nonnegative")

        if self.program == MachineProgram.LOOP:
            return None

        # HALT: decrement x once per step until it reaches 0.
        # It halts within the bound iff bound >= x when x > 0.
        if self.x <= 0:
            return 0
        return 0 if bound >= self.x else None
