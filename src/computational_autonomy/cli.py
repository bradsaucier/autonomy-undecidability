from __future__ import annotations

import argparse
import sys
from typing import Sequence, TypedDict

from .environment import Environment
from .machine import Machine, MachineProgram
from .reduction import ReductionController


class PresetSpec(TypedDict):
    rows: list[str]
    start: tuple[int, int]


def build_default_environment(preset: str) -> Environment:
    presets: dict[str, PresetSpec] = {
        "open": {
            "rows": [
                ".....",
                ".....",
                ".....",
                ".....",
                "....G",
            ],
            "start": (0, 0),
        },
        "default": {
            "rows": [
                "..X..",
                ".H.X.",
                "..X..",
                ".X..G",
                ".....",
            ],
            "start": (0, 0),
        },
    }

    spec = presets.get(preset)
    if spec is None:
        raise ValueError(f"unknown preset: {preset!r}")

    return Environment.from_strings(spec["rows"], start=spec["start"])


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

    program = MachineProgram(args.program)
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
