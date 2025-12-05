from __future__ import annotations

import re
import runpy
import sys

import pytest

from computational_autonomy.cli import main, parse_args


def test_parse_args_minimal() -> None:
    args = parse_args(["--program", "halt"])
    assert args.program == "halt"
    assert args.x == 10
    assert args.bound == 200
    assert args.max_steps == 60
    assert args.render is False


def test_main_outputs_summary(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(
        [
            "--program",
            "halt",
            "--x",
            "1",
            "--bound",
            "10",
            "--max-steps",
            "5",
        ]
    )
    assert rc == 0

    out = capsys.readouterr().out
    assert re.search(r"^safe=(True|False)$", out, flags=re.MULTILINE)
    assert re.search(r"^success=(True|False)$", out, flags=re.MULTILINE)
    assert re.search(r"^steps=\d+$", out, flags=re.MULTILINE)


def test_main_renders_trajectory_when_requested(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main(
        [
            "--program",
            "halt",
            "--x",
            "1",
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


@pytest.mark.filterwarnings(
    "ignore:'computational_autonomy.cli' found in sys.modules:RuntimeWarning"
)
def test_cli_entrypoint_invokes_main(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    argv = [
        "autonomy-demo",
        "--program",
        "loop",
        "--x",
        "1",
        "--bound",
        "3",
        "--max-steps",
        "1",
    ]
    monkeypatch.setattr(sys, "argv", argv)

    with pytest.raises(SystemExit) as excinfo:
        runpy.run_module("computational_autonomy.cli", run_name="__main__")

    assert excinfo.value.code == 0

    out = capsys.readouterr().out
    assert "safe=" in out
    assert "steps=" in out
