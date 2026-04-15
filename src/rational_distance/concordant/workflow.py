"""High-level workflows for concordant pair diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt

from rational_distance.concordant.analysis import (
    ConcordantResult,
    _ensure_pari,
    analyze_pair,
    check_chain_compatibility,
    enumerate_multiples,
)


@dataclass(frozen=True)
class ChainCandidateDiagnostic:
    """Detailed chain-compatibility diagnostics for one concordant N."""

    n: int
    source: str
    b: int
    b_positive: bool
    b_in_concordant_set: bool
    b_source: str | None
    c1_ok: bool
    c2_ok: bool
    side_hit: str
    chain_ok: bool
    c1_nearest_square_delta: int
    c2_nearest_square_delta: int
    combined_delta: int


@dataclass(frozen=True)
class ConcordantPairDiagnostics:
    """Full diagnostics for a fixed (A, B) pair."""

    result: ConcordantResult
    deep_extra_n: list[int]
    all_concordant_n: list[int]
    mirror_hit_n: list[int]
    candidates: list[ChainCandidateDiagnostic]
    best_candidate: ChainCandidateDiagnostic | None

    @property
    def chain_compatible(self) -> list[int]:
        return self.result.chain_compatible

    @property
    def c1_hit_n(self) -> list[int]:
        return [candidate.n for candidate in self.candidates if candidate.c1_ok]

    @property
    def c2_hit_n(self) -> list[int]:
        return [candidate.n for candidate in self.candidates if candidate.c2_ok]

    @property
    def side_hit_n(self) -> list[int]:
        return [candidate.n for candidate in self.candidates if candidate.side_hit != "none"]


def _nearest_square_delta(n: int) -> int:
    """Distance from n to the nearest perfect square."""
    if n < 0:
        raise ValueError("nearest-square delta requires a non-negative integer")
    root = isqrt(n)
    floor_sq = root * root
    if floor_sq == n:
        return 0
    ceil_sq = (root + 1) * (root + 1)
    return min(n - floor_sq, ceil_sq - n)


def _candidate_source(n: int, base_n: set[int]) -> str:
    return "ellratpoints" if n in base_n else "deep"


def _side_hit(c1_ok: bool, c2_ok: bool) -> str:
    if c1_ok and c2_ok:
        return "both"
    if c1_ok:
        return "c1"
    if c2_ok:
        return "c2"
    return "none"


def _candidate_priority(candidate: ChainCandidateDiagnostic) -> tuple[int, int, int, int, int, int]:
    if candidate.side_hit == "both":
        side_rank = 0
    elif candidate.side_hit != "none":
        side_rank = 1
    else:
        side_rank = 2
    return (
        0 if candidate.chain_ok else 1,
        0 if candidate.b_positive else 1,
        side_rank,
        candidate.combined_delta,
        abs(candidate.b),
        candidate.n,
    )


def diagnose_pair(
    A: int,
    B: int,
    ec_bound: int = 100000,
    pari=None,
    *,
    deep: int = 0,
    normalize: bool = False,
) -> ConcordantPairDiagnostics:
    """Diagnose why a fixed (A, B) pair fails or nearly fits the chain constraint."""
    if pari is None:
        pari = _ensure_pari()

    result = analyze_pair(A, B, ec_bound=ec_bound, pari=pari, normalize=normalize)
    deep_extra_n: list[int] = []
    if deep > 0:
        deep_candidates = enumerate_multiples(result.A, result.B, max_depth=deep, pari=pari)
        deep_extra_n = sorted(n for n in deep_candidates if n not in result.concordant_n)

    base_n = set(result.concordant_n)
    all_concordant_n = sorted(base_n | set(deep_extra_n))
    all_n_set = set(all_concordant_n)

    candidates: list[ChainCandidateDiagnostic] = []
    mirror_hit_n: list[int] = []
    for n in all_concordant_n:
        b = result.A + result.B - n
        c1_sq = result.B * result.B + b * b
        c2_sq = result.A * result.A + b * b
        c1_delta = _nearest_square_delta(c1_sq)
        c2_delta = _nearest_square_delta(c2_sq)
        c1_ok = c1_delta == 0
        c2_ok = c2_delta == 0
        b_positive = b > 0
        source = _candidate_source(n, base_n)
        b_in_concordant_set = b in all_n_set
        if b_in_concordant_set:
            mirror_hit_n.append(n)
        candidate = ChainCandidateDiagnostic(
            n=n,
            source=source,
            b=b,
            b_positive=b_positive,
            b_in_concordant_set=b_in_concordant_set,
            b_source=_candidate_source(b, base_n) if b_in_concordant_set else None,
            c1_ok=c1_ok,
            c2_ok=c2_ok,
            side_hit=_side_hit(c1_ok, c2_ok),
            chain_ok=check_chain_compatibility(result.A, result.B, n),
            c1_nearest_square_delta=c1_delta,
            c2_nearest_square_delta=c2_delta,
            combined_delta=c1_delta + c2_delta,
        )
        candidates.append(candidate)

    best_candidate = next((candidate for candidate in candidates if candidate.chain_ok), None)
    if best_candidate is None and candidates:
        best_candidate = min(candidates, key=_candidate_priority)

    return ConcordantPairDiagnostics(
        result=result,
        deep_extra_n=deep_extra_n,
        all_concordant_n=all_concordant_n,
        mirror_hit_n=mirror_hit_n,
        candidates=candidates,
        best_candidate=best_candidate,
    )


__all__ = [
    "ChainCandidateDiagnostic",
    "ConcordantPairDiagnostics",
    "diagnose_pair",
]
