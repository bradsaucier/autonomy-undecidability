[![quality-gate](https://github.com/bradsaucier/autonomy-undecidability/actions/workflows/quality_gate.yml/badge.svg)](https://github.com/bradsaucier/autonomy-undecidability/actions/workflows/quality_gate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

# Computational Autonomy and Undecidability

## 1 Overview

This repository studies a limit on software verification for general programs. If "full computational autonomy" is treated as a nontrivial semantic property of a program's behavior across all inputs, then deciding whether an arbitrary program has that property is undecidable by Rice's Theorem.

This repository includes a small Python simulation that illustrates the shape of a reduction from the Halting Problem to a concrete autonomy-style property in a toy environment. The simulation is bounded and does not implement a halting oracle. Its purpose is to connect the formal result to practical intuition: unbounded, universal guarantees are not available in general, so real assurance comes from bounded checks, containment, and explicit assumptions.

## 2 What the demo shows and what it does not

### 2.1 What it shows

The demo demonstrates a standard reduction pattern.

1. A controller simulates a simple machine for a fixed number of steps B.
2. If the machine halts within B steps, the controller uses a policy that reaches a goal while avoiding hazards.
3. If the machine does not halt within B steps, the controller uses a policy that never reaches the goal.

### 2.2 What it does not show

Because the simulation is bounded, the demo only distinguishes "halts within B steps" from "does not halt within B steps". This is an executable approximation used to make the idea concrete.

## 3 Installation

### 3.1 Requirements

Python 3.10 or later.

### 3.2 Install with pip

pip install .

For development:

pip install -e ".[dev]"

## 4 Run the demo

autonomy-demo --program halt --x 10 --bound 200 --max-steps 60 --render

You can also run the module entry point:

python -m computational_autonomy.cli --program halt --x 10 --bound 200 --max-steps 60 --render

## 5 Run verification

ruff check .
ruff format --check .
mypy src
pytest --cov

## 6 Citation

If you use this work academically, cite the repository and the included paper. See CITATION.cff.

## 7 About the author

Bradley Saucier
B.S. in Computer Science (expected May 2026), Southern New Hampshire University
B.A., Columbia University School of General Studies
A.A.S., Community College of the Air Force

## 8 Disclaimer

This is personal academic work created for learning and research. It is not affiliated with, endorsed by, or representative of any employer, government organization, or agency.
