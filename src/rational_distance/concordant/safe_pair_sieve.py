"""Safe sieve for reduced concordant batch pairs."""

from __future__ import annotations


def classify_reduced_pair(A: int, B: int) -> str:
    """Classify a reduced ``(A, B)`` pair for the experimental safe sieve.

    This helper is intentionally narrow: it only targets the reduced batch
    pairs produced by ``generate_ab_pairs()``. In that stream, both-even pairs
    should not appear after reduction, so the only practical rejection reasons
    are mixed parity and the odd/odd mod-4 mismatch.
    """

    if (A ^ B) & 1:
        return "mixed_parity"
    if (A & 1) and ((A + B) % 4 != 0):
        return "odd_odd_wrong_mod4"
    return "pass"


def allow_reduced_pair(A: int, B: int) -> bool:
    """Return whether a reduced batch pair survives the safe sieve."""

    return classify_reduced_pair(A, B) == "pass"


__all__ = ["allow_reduced_pair", "classify_reduced_pair"]
