from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from .controller import Action, ControllerResult, step
from .environment import Environment
from .machine import Machine


@dataclass(frozen=True)
class ReductionController:
    """A bounded reduction-style controller.

    It simulates a machine for up to bound steps exactly once at the beginning.
    If the machine halts within the bound, it uses a goal-seeking policy.
    Otherwise it uses an inert policy that never reaches the goal.

    This is an executable demonstration of the structure of a reduction.
    It does not decide halting.
    """

    machine: Machine
    bound: int

    def run_episode(
        self, env: Environment, max_steps: int
    ) -> Tuple[bool, bool, List[Tuple[int, int]]]:
        """Run one bounded episode.

        Returns a triple (safe, success, trace).

        safe is True if the agent never enters a hazard cell.
        success is True if the agent reaches the goal and raises success_signal.
        trace is the list of visited positions including the initial position.
        """
        if max_steps <= 0:
            raise ValueError("max_steps must be positive")

        halted = self.machine.simulate(self.bound) is not None
        pos = env.start
        safe = not env.is_hazard(*pos)
        trace: List[Tuple[int, int]] = [pos]
        success = False

        for _ in range(max_steps):
            if halted:
                result = self._good_policy(env, pos)
            else:
                result = ControllerResult(action=Action.STAY, success_signal=False)

            nxt = step(pos, result.action)
            if env.in_bounds(*nxt) and not env.is_blocked(*nxt):
                pos = nxt

            trace.append(pos)
            if env.is_hazard(*pos):
                safe = False
            if env.is_goal(*pos) and result.success_signal:
                success = True
                break

        return safe, success, trace

    @staticmethod
    def _good_policy(env: Environment, pos: Tuple[int, int]) -> ControllerResult:
        r, c = pos

        candidates = [Action.RIGHT, Action.DOWN, Action.LEFT, Action.UP]

        for act in candidates:
            nr, nc = step((r, c), act)
            if not env.in_bounds(nr, nc):
                continue
            if env.is_blocked(nr, nc):
                continue
            if env.is_hazard(nr, nc):
                continue
            if env.is_goal(nr, nc):
                return ControllerResult(action=act, success_signal=True)

        for act in candidates:
            nr, nc = step((r, c), act)
            if not env.in_bounds(nr, nc):
                continue
            if env.is_blocked(nr, nc):
                continue
            if env.is_hazard(nr, nc):
                continue
            return ControllerResult(action=act, success_signal=False)

        return ControllerResult(action=Action.STAY, success_signal=False)
