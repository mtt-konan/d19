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

For a sieve that IS sound on the non-coprime half-space, use
``gcd_aware_kills`` / ``guaranteed_divisor`` below: they are built from the
gcd-aware mod-12 theorem (MATH §8.5.2, wl098/wl099) and reduce to this
coprime sieve (divisor 12) when gcd(A, B) = 1.
"""

from __future__ import annotations

from math import gcd


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


def _v(n: int, p: int) -> int:
    """p-adic valuation of n (n != 0)."""
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def guaranteed_divisor(A: int, B: int) -> int:
    """Largest D proven to divide *every* concordant N of (A, B).

    From the gcd-aware mod-12 theorem and its 2-adic refinement (MATH §8.5.2,
    wl098/wl099), with g = gcd(A, B):

      - 3-part:  3 | N  iff  3 ∤ g          -> factor 3 when v3(g) == 0, else 1
      - 2-part:  v2(g) == 0 -> 4 | N        -> factor 4
                 v2(g) == 1 -> 8 | N        -> factor 8 (refinement)
                 v2(g) >= 2 -> no guarantee -> factor 1

    For gcd(A, B) = 1 this returns 12 (recovering the coprime mod-12 theorem);
    e.g. g = 2 gives 24. This is SOUND for every (A, B) (unlike
    ``classify_reduced_pair``, which is coprime-only).
    """
    g = gcd(A, B)
    p2 = {0: 4, 1: 8}.get(_v(g, 2), 1)
    p3 = 3 if _v(g, 3) == 0 else 1
    return p2 * p3


def gcd_aware_kills(A: int, B: int) -> bool:
    """Return True iff a closure for (A, B) is impossible by the divisibility
    argument: every concordant N is divisible by ``D = guaranteed_divisor``, so
    each closure value N_i ± N_j is divisible by D; a closure therefore requires
    D | (A + B) (inside-square sum) or D | |A - B| (full plane). If neither
    holds, no closure is possible.

    SOUND for any (A, B) — this is the gcd-aware generalization of the
    coprime-only ``classify_reduced_pair`` safe sieve.
    """
    d = guaranteed_divisor(A, B)
    return (A + B) % d != 0 and abs(A - B) % d != 0


__all__ = [
    "allow_reduced_pair",
    "classify_reduced_pair",
    "gcd_aware_kills",
    "guaranteed_divisor",
]
