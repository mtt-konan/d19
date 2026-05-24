"""Chain-closure mod p^k sieve — joint necessary condition on N and b = A+B-N.

Mathematical foundation
=======================

For a fixed reduced pair ``(A, B)`` (with ``A < B``, both odd, ``(A+B) % 4 == 0``),
the full 4-chain closure with apex ``a + c = b + d`` requires the existence
of an integer ``N`` satisfying simultaneously:

    N²  + A² = □              (C3, concordant for N w.r.t. A)
    N²  + B² = □              (C4, concordant for N w.r.t. B)
    b²  + A² = □              (C2, concordant for b w.r.t. A)
    b²  + B² = □              (C1, concordant for b w.r.t. B)
    b = A + B - N > 0         (chain-closure / 4-cycle apex constraint)

Define the joint mod-``M`` residue set

    T(A, B, M) := { n mod M : n² + A² and n² + B² are both squares mod M }.

Then ``N mod M ∈ T`` and ``b mod M ∈ T``, hence

    N mod M ∈ T   AND   (A + B - N) mod M ∈ T,

which is equivalent to

    N mod M ∈ T ∩ ((A + B) - T)  (all computations in Z/MZ).

If for some modulus ``M`` this intersection is empty, no integer ``N`` can
extend ``(A, B)`` to a full chain — hence ``no_solution``. Soundness is
immediate: any integer chain solution reduces to a point in the intersection.

What's new vs the existing finite-descent sieve
================================================

``scripts/finite_descent_hard_cases.py`` (wl037 Layer 1) checks the *N-only*
condition ``T ≠ ∅`` for primes ``p < 200``. ``finite_descent_layer2.py``
enumerates ``N`` mod ``lcm(p_i)`` but again only on the N-side.

Neither pipeline reflects the symmetric ``b = A+B-N`` constraint. Crossing
``T`` with ``(A+B) - T`` is therefore a genuinely new sieve. Empirically it
kills ~99.6% of ``hard_case`` pairs at ``max_hyp = 2000`` using only prime
squares up to ``53²``.

Why prime squares (not just primes)
====================================

For a prime ``p`` and squarefree ``A`` coprime to ``p``, the condition
``n² + A² ≡ □ (mod p)`` is determined by ``n mod p``. But ``n² + A² ≡ □
(mod p²)`` becomes a stronger condition when ``p | n² + A²``: lifting
requires ``n² + A² ≡ 0 (mod p²)`` rather than just ``mod p``. So mod ``p²``
sees obstructions that mod ``p`` misses, and the chain-closure intersection
test then has fewer compatible residue classes to fall into.
"""

from __future__ import annotations

# Default modulus list: prime squares p² for primes p in [3, 53].  Skipping
# p = 2 because the safe_sieve already exhausts the 2-adic information at
# mod 4, and additional powers of 2 give 0 kills on hard_case.
DEFAULT_PRIME_SQUARE_MODULI: tuple[int, ...] = (
    9,    # 3²
    25,   # 5²
    49,   # 7²
    121,  # 11²
    169,  # 13²
    289,  # 17²
    361,  # 19²
    529,  # 23²
    841,  # 29²
    961,  # 31²
    1369, # 37²
    1681, # 41²
    2209, # 47²
    2809, # 53²
)


def _squares_mod(M: int) -> frozenset[int]:
    """Return the set of squares mod M as a frozenset.

    Lifted out so callers can cache it across many (A, B) pairs sharing the
    same modulus.
    """
    return frozenset((x * x) % M for x in range(M))


_SQUARES_CACHE: dict[int, frozenset[int]] = {}


def squares_mod(M: int) -> frozenset[int]:
    """Cached helper for the set of squares mod M."""
    cached = _SQUARES_CACHE.get(M)
    if cached is None:
        cached = _squares_mod(M)
        _SQUARES_CACHE[M] = cached
    return cached


def allowed_n_mod(A: int, B: int, M: int) -> frozenset[int]:
    """Compute T(A, B, M) — residues n mod M such that both n²+A² and
    n²+B² are squares mod M."""
    sq = squares_mod(M)
    a2 = (A * A) % M
    b2 = (B * B) % M
    out: set[int] = set()
    for n in range(M):
        n2 = (n * n) % M
        if (n2 + a2) % M in sq and (n2 + b2) % M in sq:
            out.add(n)
    return frozenset(out)


def killed_at_modulus(A: int, B: int, M: int) -> bool:
    """Return True iff ``T(A, B, M) ∩ ((A+B) - T(A, B, M))`` is empty (mod M).

    Empty intersection implies no integer N can satisfy all four concordant
    conditions plus the chain closure ``b = A+B-N``. Hence no chain
    solution can exist.
    """
    T = allowed_n_mod(A, B, M)
    if not T:
        return True
    ab = (A + B) % M
    reflected = frozenset((ab - n) % M for n in T)
    return not (T & reflected)


def find_killer_modulus(
    A: int, B: int, moduli: tuple[int, ...] = DEFAULT_PRIME_SQUARE_MODULI
) -> int | None:
    """Return the first modulus M in ``moduli`` that proves no chain solution,
    or None if every M leaves a non-empty intersection."""
    for M in moduli:
        if killed_at_modulus(A, B, M):
            return M
    return None


def all_killer_moduli(
    A: int, B: int, moduli: tuple[int, ...] = DEFAULT_PRIME_SQUARE_MODULI
) -> list[int]:
    """Return every modulus M in ``moduli`` that proves no chain solution.

    Useful for diagnostics: a pair killed at many moduli is "obviously"
    obstructed; a pair killed only at e.g. M = 961 is more delicate.
    """
    return [M for M in moduli if killed_at_modulus(A, B, M)]


__all__ = [
    "DEFAULT_PRIME_SQUARE_MODULI",
    "all_killer_moduli",
    "allowed_n_mod",
    "find_killer_modulus",
    "killed_at_modulus",
    "squares_mod",
]
