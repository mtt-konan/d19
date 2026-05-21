"""Proof-status pipeline for reduced concordant ``(A, B)`` pairs.

This package answers a different question from ``concordant``:

- ``concordant`` asks *"does this pair give a chain solution?"* and produces
  diagnostics about how close it came.
- ``proof_status`` asks *"can we mathematically prove this pair has no chain
  solution?"* and accumulates verdicts into a SQLite database.

See docs/THEORY_DIRECTIONS_ADVANCED.md for the long-term theoretical roadmap
this module operationalises.

Public API
----------
We deliberately re-export only data types and the most commonly used entry
points. Submodules (``schema``, ``methods``, ``workflow``) should be imported
explicitly when needed; this avoids cyclic imports through the package root.
"""

from rational_distance.proof_status.types import (
    MethodOutcome,
    MethodResult,
    PairProofStatus,
    PairStatus,
)

__all__ = [
    "MethodOutcome",
    "MethodResult",
    "PairProofStatus",
    "PairStatus",
]
