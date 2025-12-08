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
    Otherwise it stays put.
    """

    machine: Machine
    bound: int

    def run_episode(
        self, env: Environment, max_steps: int
    ) -> Tuple[bool, bool, List[Tuple[int, int]]]:
        """Run a single episode.

        Returns (safe, success, trace) where:
        safe is True iff the agent never enters a hazard cell.
        success is True iff the agent reaches the goal.
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

            pos = step(pos, result.action)
            trace.append(pos)

            if env.is_hazard(*pos):
                safe = False

            if result.success_signal:
                success = True
                break

        return safe, success, trace

    @staticmethod
    def _good_policy(env: Environment, pos: Tuple[int, int]) -> ControllerResult:
        r, c = pos
        candidates = [Action.RIGHT, Action.DOWN, Action.LEFT, Action.UP]

        safe_actions: List[Action] = []
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

            safe_actions.append(act)

        if safe_actions:
            return ControllerResult(action=safe_actions[0], success_signal=False)

        return ControllerResult(action=Action.STAY, success_signal=False)
