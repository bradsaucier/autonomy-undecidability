from __future__ import annotations

from computational_autonomy.cli import main

if __name__ == "__main__":
    raise SystemExit(
        main(
            [
                "--program",
                "halt",
                "--x",
                "10",
                "--bound",
                "200",
                "--max-steps",
                "60",
                "--render",
            ]
        )
    )
