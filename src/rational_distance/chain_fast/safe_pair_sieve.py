"""Mathematically safe early pair sieve for chain-fast."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Orientation = Literal["OE", "EO"]


def classify_orientation(s: int, t: int) -> Orientation:
    """Classify one oriented primitive triple leg ordering.

    ``OE`` means ``s`` is odd and ``t`` is even.
    ``EO`` means ``s`` is even and ``t`` is odd.
    """
    if s % 2 == 1 and t % 2 == 0:
        return "OE"
    if s % 2 == 0 and t % 2 == 1:
        return "EO"
    raise ValueError("Expected one odd leg and one even leg")


def v2(value: int) -> int:
    """Return the 2-adic valuation of a positive integer."""
    if value <= 0:
        raise ValueError("v2 is defined here only for positive integers")
    count = 0
    while value % 2 == 0:
        value //= 2
        count += 1
    return count


@dataclass(frozen=True)
class SafePairDecision:
    allow_pair: bool
    require_n_multiple_of_4: bool = False


def decide_safe_pair_sieve(
    s1: int,
    t1: int,
    s2: int,
    t2: int,
) -> SafePairDecision:
    """Apply the proven early necessary conditions for one ordered triple pair."""
    orientation_t1 = classify_orientation(s1, t1)
    orientation_t2 = classify_orientation(s2, t2)

    if orientation_t1 == orientation_t2:
        return SafePairDecision(allow_pair=False)

    if orientation_t1 == "OE" and orientation_t2 == "EO":
        if v2(t1) != v2(s2):
            return SafePairDecision(allow_pair=False)
        return SafePairDecision(allow_pair=True, require_n_multiple_of_4=True)

    return SafePairDecision(allow_pair=True, require_n_multiple_of_4=False)


def passes_n_mod4_requirement(decision: SafePairDecision, n_value: int) -> bool:
    """Return whether the post-construction ``N`` value passes the safe mod-4 rule."""
    if not decision.allow_pair:
        return False
    if not decision.require_n_multiple_of_4:
        return True
    return n_value % 4 == 0
