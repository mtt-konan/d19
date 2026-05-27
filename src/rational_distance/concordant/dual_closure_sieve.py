"""Dual-side chain-closure mod p² sieve.

Mathematical foundation
=======================

Partner identity (see ``docs/PARTNER_GRAPH_THEORY.md`` §2.5): if ``(A, B)``
is a multi-N pair with ``concordant_N(A, B) ⊇ {N_i, N_j}``, then the pair
``(N_i, N_j)`` is itself a multi-N pair, with ``A, B ∈ concordant_N(N_i, N_j)``.

For a Harborth 4-chain counterexample we additionally need

    N_i + N_j = A + B   (closure)

By symmetry, the pair ``(N_i, N_j)`` (as a new "AB" candidate) must satisfy
the same chain-closure condition: there must exist ``M_1, M_2 ∈
concordant_N(N_i, N_j)`` with ``M_1 + M_2 = N_i + N_j``. Setting
``M_1 = A, M_2 = B`` shows this is automatic. Hence ``(N_i, N_j)`` itself
must pass ``chain_closure_mod_sieve``.

If for **every** pair ``(N_i, N_j) ∈ concordant_N(A, B)`` (after reduction)
``chain_closure_mod_sieve`` proves no chain solution, then no Harborth
counterexample can use ``(A, B)`` — regardless of which two concordant N's
are chosen as the closure pair.

This module provides that test, reusing
``chain_closure_sieve.killed_at_modulus`` for the per-pair check.
"""

from __future__ import annotations

from collections.abc import Sequence
from math import gcd

from rational_distance.concordant.chain_closure_sieve import (
    DEFAULT_PRIME_SQUARE_MODULI,
    killed_at_modulus,
)


def _reduced_pair(p: int, q: int) -> tuple[int, int]:
    """Return ``(p, q)`` divided by their gcd, with the smaller value first."""
    g = gcd(p, q)
    a = p // g
    b = q // g
    return (a, b) if a <= b else (b, a)


def dual_pair_killed(
    n_i: int,
    n_j: int,
    moduli: Sequence[int] = DEFAULT_PRIME_SQUARE_MODULI,
) -> int | None:
    """Return the first modulus M in ``moduli`` that proves ``(N_i, N_j)``
    has no chain-closing solution, or None if no modulus kills it.

    The pair ``(N_i, N_j)`` is reduced (divided by gcd) before applying
    ``chain_closure_mod_sieve`` — the mod p² test depends on the reduced
    representative.

    A degenerate ``N_i == N_j`` case is treated as killed (a self-paired
    concordant N cannot give a Harborth 4-chain because the four vertices
    must be distinct); the returned modulus is then ``0`` as a sentinel.
    """
    if n_i == n_j:
        return 0
    a, b = _reduced_pair(n_i, n_j)
    for m in moduli:
        if killed_at_modulus(a, b, m):
            return m
    return None


def all_n_pairs_killed(
    ns: Sequence[int],
    moduli: Sequence[int] = DEFAULT_PRIME_SQUARE_MODULI,
) -> bool:
    """Return True iff every distinct pair ``(N_i, N_j)`` from ``ns`` is
    killed at some modulus in ``moduli``.

    If ``len(ns) < 2`` the function returns True (no Harborth closure pair
    can be formed, so the AB candidate is vacuously dead by closure).
    """
    if len(ns) < 2:
        return True
    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            if dual_pair_killed(ns[i], ns[j], moduli) is None:
                return False
    return True


def find_surviving_n_pair(
    ns: Sequence[int],
    moduli: Sequence[int] = DEFAULT_PRIME_SQUARE_MODULI,
) -> tuple[int, int] | None:
    """Return the first ``(N_i, N_j)`` pair in ``ns`` that is **not** killed
    by any modulus, or None if every pair is killed.

    Useful for diagnostics: a surviving pair is the candidate that needs
    deeper analysis (PARI ellrank, Heegner, etc.).
    """
    if len(ns) < 2:
        return None
    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            if dual_pair_killed(ns[i], ns[j], moduli) is None:
                return (ns[i], ns[j])
    return None


__all__ = [
    "all_n_pairs_killed",
    "dual_pair_killed",
    "find_surviving_n_pair",
]
