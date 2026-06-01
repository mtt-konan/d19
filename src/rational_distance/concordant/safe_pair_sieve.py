"""Safe sieve for reduced concordant batch pairs.

⚠️ Soundness is CONDITIONAL on coprime (reduced) input. The two rejection
rules below are exactly the mod-2 / mod-4 corollary of the coprime-leg mod-12
theorem (MATH.md §8.5.1): for gcd(A, B) = 1 every concordant N is divisible by
12, so any closure value N_i + N_j is even and ≡ 0 (mod 4), forcing A + B even
and 4 | (A + B). Hence for a coprime pair:

  - mixed parity            (A + B odd)        ⟹ no closure possible -> reject
  - both odd, (A+B) % 4 != 0 (A + B ≡ 2 mod 4) ⟹ no closure possible -> reject

This is NOT valid for non-coprime (A, B): the mod-12 theorem fails there
(e.g. (6, 15) -> N = 8, (8, 20) -> N = 15), both-even pairs occur (and `pass`
unrejected here), and a non-coprime counterexample is never reduced away —
gcd(A, B) = 1 is a search-space normalization, NOT WLOG (the minimal
counterexample only forces gcd(A, B, N_1, N_2) = 1). The non-coprime (A, B)
half-space is the §8.6 gap; see MATH.md §8.6.
"""

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
