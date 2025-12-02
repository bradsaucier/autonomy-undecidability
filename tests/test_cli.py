from __future__ import annotations

import re

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
    rc = main(["--program", "halt", "--x", "1", "--bound", "10", "--max-steps", "5"])
    assert rc == 0
    out = capsys.readouterr().out
    assert re.search(r"^safe=(True|False)$", out, flags=re.MULTILINE)
    assert re.search(r"^success=(True|False)$", out, flags=re.MULTILINE)
    assert re.search(r"^steps=\d+$", out, flags=re.MULTILINE)
