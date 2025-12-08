from __future__ import annotations

import re
import runpy
import sys

import pytest


def test_parse_args_minimal() -> None:
    from computational_autonomy.cli import parse_args

    args = parse_args(["--program", "halt"])
    assert args.program == "halt"
    assert args.x == 10
    assert args.bound == 200
    assert args.max_steps == 60
    assert args.render is False


def test_parse_args_all_values() -> None:
    from computational_autonomy.cli import parse_args

    args = parse_args(
        [
            "--preset",
            "open",
            "--program",
            "loop",
            "--x",
            "7",
            "--bound",
            "9",
            "--max-steps",
            "11",
            "--render",
        ]
    )
    assert args.preset == "open"
    assert args.program == "loop"
    assert args.x == 7
    assert args.bound == 9
    assert args.max_steps == 11
    assert args.render is True


def test_main_runs_and_prints_summary_default_preset(capsys: pytest.CaptureFixture[str]) -> None:
    from computational_autonomy.cli import main

    rc = main(["--program", "halt", "--x", "0", "--bound", "5", "--max-steps", "5"])
    assert rc == 0

    out = capsys.readouterr().out
    assert "safe=" in out
    assert "success=" in out
    assert "steps=" in out


def test_main_render_prints_grid(capsys: pytest.CaptureFixture[str]) -> None:
    from computational_autonomy.cli import main

    rc = main(
        [
            "--program",
            "halt",
            "--x",
            "0",
            "--bound",
            "10",
            "--max-steps",
            "5",
            "--render",
        ]
    )
    assert rc == 0

    out = capsys.readouterr().out
    lines = [ln for ln in out.splitlines() if ln]

    assert any("A" in ln for ln in lines)
    assert any(ln.startswith("safe=") for ln in lines)
    assert any(ln.startswith("success=") for ln in lines)
    assert any(ln.startswith("steps=") for ln in lines)


def test_module_entrypoint_runs(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PYTHONPATH", "src")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "autonomy-demo",
            "--program",
            "halt",
            "--x",
            "0",
            "--bound",
            "5",
        ],
    )

    sys.modules.pop("computational_autonomy.cli", None)

    with pytest.raises(SystemExit) as excinfo:
        runpy.run_module("computational_autonomy.cli", run_name="__main__")

    assert excinfo.value.code == 0

    out = capsys.readouterr().out
    assert re.search(r"safe=(True|False)", out)
    assert re.search(r"success=(True|False)", out)
    assert re.search(r"steps=\d+", out)


def test_build_default_environment_open_preset_has_goal_and_no_hazards() -> None:
    from computational_autonomy.cli import build_default_environment

    env = build_default_environment("open")
    assert env.height == 5
    assert env.width == 5
    assert env.is_goal(4, 4)

    for r in range(env.height):
        for c in range(env.width):
            assert env.is_hazard(r, c) is False


def test_build_default_environment_unknown_preset_rejected() -> None:
    from computational_autonomy.cli import build_default_environment

    with pytest.raises(ValueError):
        _ = build_default_environment("unknown")