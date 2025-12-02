"""
Computational Autonomy and Undecidability.

This package contains a small, executable demonstration that illustrates the
structure of a reduction from bounded halting behavior to a bounded autonomy
property in a toy environment.

The demo is intentionally bounded. It is not a halting oracle.
"""

from __future__ import annotations

__all__ = [
    "Environment",
    "Cell",
    "ControllerResult",
    "Machine",
    "MachineProgram",
    "ReductionController",
]

from .controller import ControllerResult
from .environment import Cell, Environment
from .machine import Machine, MachineProgram
from .reduction import ReductionController
