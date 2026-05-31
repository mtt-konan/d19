"""Shared data types for the proof_status module.

This module is intentionally minimal and import-light: methods.py, schema.py and
workflow.py all depend on these dataclasses but should not need to import each
other for type information.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

# A pair-level conclusion. Values are stored verbatim in SQLite.
PairStatus = Literal[
    "unknown",  # not yet attempted, or all attempted methods were inconclusive
    "no_solution",  # mathematically proven that no full chain solution exists
    "solution_found",  # a full chain solution was constructed (would refute Harborth!)
    "hard_case",  # all currently available methods returned inconclusive
]

# A single method's outcome on one pair.
MethodOutcome = Literal[
    "pass",  # the pair passes this method's necessary conditions (continue trying)
    "no_solution",  # this method proves the pair has no full chain solution
    "solution_found",  # this method actually constructed a full chain solution
    "inconclusive",  # the method ran but cannot decide; try the next method
    "error",  # the method raised; details captured in notes
    "skipped",  # the method was not run (e.g. dependency missing)
]


@dataclass(frozen=True)
class MethodResult:
    """Outcome of running one judgement method on one (A, B) pair."""

    method: str
    outcome: MethodOutcome
    details: dict[str, object] = field(default_factory=dict)
    elapsed_s: float = 0.0
    notes: str = ""


@dataclass(frozen=True)
class PairProofStatus:
    """Aggregated proof status for a single (A, B) pair."""

    A: int
    B: int
    status: PairStatus
    method: str | None
    rank_lower: int | None
    rank_upper: int | None
    concordant_n_count: int | None
    chain_compatible_count: int | None
    notes: str
    updated_at: str
    f2_rank: int | None = None


__all__ = [
    "MethodOutcome",
    "MethodResult",
    "PairProofStatus",
    "PairStatus",
]
