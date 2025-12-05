from __future__ import annotations

import argparse
import sys
from typing import Sequence

from .environment import Environment
from .machine import Machine, MachineProgram
from .reduction import ReductionController


def build_default_environment(preset: str) -> Environment:
    if preset == "open":
        rows = [
            ".....",
            ".....",
            ".....",
            ".....",
            "....G",
        ]
        return Environment.from_strings(rows, start=(0, 0))

    rows = [
        "..X..",
        ".H.X.",
        "..X..",
        ".X..G",
        ".....",
    ]
    return Environment.from_strings(rows, start=(0, 0))


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="autonomy-demo", add_help=True)
    p.add_argument("--preset", choices=["default", "open"], default="default")
    p.add_argument("--program", choices=["halt", "loop"], required=True)
    p.add_argument("--x", type=int, default=10)
    p.add_argument("--bound", type=int, default=200)
    p.add_argument("--max-steps", type=int, default=60)
    p.add_argument("--render", action="store_true")
    return p.parse_args(list(argv))


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    env = build_default_environment(args.preset)

    program = MachineProgram.HALT if args.program == "halt" else MachineProgram.LOOP
    m = Machine(program=program, x=args.x)
    rc = ReductionController(machine=m, bound=args.bound)

    safe, success, trace = rc.run_episode(env, max_steps=args.max_steps)

    if args.render:
        print(env.render(trace[0]))
        for pos in trace[1:]:
            print()
            print(env.render(pos))

    print()
    print(f"safe={safe}")
    print(f"success={success}")
    print(f"steps={len(trace) - 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
