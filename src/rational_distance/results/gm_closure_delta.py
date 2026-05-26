from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class DeltaRow:
    N1: int
    N2: int
    delta: int


@dataclass(frozen=True)
class PairDeltaSummary:
    A: int
    B: int
    target: int
    k: int
    total_pairs: int
    min_abs_delta: int | None
    closest_rows: list[DeltaRow]


def summarize_pair_deltas(A: int, B: int, Ns: Iterable[int]) -> PairDeltaSummary:
    ns = sorted(int(n) for n in Ns)
    target = A + B
    rows = [
        DeltaRow(N1=n1, N2=n2, delta=target - (n1 + n2))
        for n1, n2 in combinations(ns, 2)
    ]
    if not rows:
        return PairDeltaSummary(
            A=A,
            B=B,
            target=target,
            k=len(ns),
            total_pairs=0,
            min_abs_delta=None,
            closest_rows=[],
        )

    min_abs_delta = min(abs(row.delta) for row in rows)
    closest_rows = [row for row in rows if abs(row.delta) == min_abs_delta]
    return PairDeltaSummary(
        A=A,
        B=B,
        target=target,
        k=len(ns),
        total_pairs=len(rows),
        min_abs_delta=min_abs_delta,
        closest_rows=closest_rows,
    )
