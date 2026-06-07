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


@dataclass(frozen=True)
class FullPlaneDeltaRow:
    N1: int
    N2: int
    relation: str
    lhs: int
    rhs: int
    signed_delta: int


@dataclass(frozen=True)
class FullPlanePairDeltaSummary:
    A: int
    B: int
    k: int
    total_relation_rows: int
    min_abs_delta: int | None
    closest_rows: list[FullPlaneDeltaRow]
    closure_hits: list[FullPlaneDeltaRow]
    min_abs_delta_by_relation: dict[str, int]


def summarize_pair_deltas(A: int, B: int, Ns: Iterable[int]) -> PairDeltaSummary:
    ns = sorted(int(n) for n in Ns)
    target = A + B
    rows = [DeltaRow(N1=n1, N2=n2, delta=target - (n1 + n2)) for n1, n2 in combinations(ns, 2)]
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


def summarize_full_plane_pair_deltas(
    A: int,
    B: int,
    Ns: Iterable[int],
) -> FullPlanePairDeltaSummary:
    """Summarize distance to the full-plane GEN-CLOSURE relations.

    Sum relations allow using the same concordant ``N`` twice, matching
    ``analysis.gen_closure_hit``. Difference relations require two distinct
    ``N`` values because ``|N-N|`` is not a vertical separation.
    """
    ns = sorted(int(n) for n in Ns)
    ab_sum = A + B
    ab_diff = abs(A - B)
    rows: list[FullPlaneDeltaRow] = []

    for i, n1 in enumerate(ns):
        for n2 in ns[i:]:
            lhs = n1 + n2
            rows.append(
                FullPlaneDeltaRow(
                    N1=n1,
                    N2=n2,
                    relation="sum=A+B",
                    lhs=lhs,
                    rhs=ab_sum,
                    signed_delta=ab_sum - lhs,
                )
            )
            rows.append(
                FullPlaneDeltaRow(
                    N1=n1,
                    N2=n2,
                    relation="sum=|A-B|",
                    lhs=lhs,
                    rhs=ab_diff,
                    signed_delta=ab_diff - lhs,
                )
            )

            if n1 == n2:
                continue

            lhs = abs(n2 - n1)
            rows.append(
                FullPlaneDeltaRow(
                    N1=n1,
                    N2=n2,
                    relation="diff=A+B",
                    lhs=lhs,
                    rhs=ab_sum,
                    signed_delta=ab_sum - lhs,
                )
            )
            rows.append(
                FullPlaneDeltaRow(
                    N1=n1,
                    N2=n2,
                    relation="diff=|A-B|",
                    lhs=lhs,
                    rhs=ab_diff,
                    signed_delta=ab_diff - lhs,
                )
            )

    if not rows:
        return FullPlanePairDeltaSummary(
            A=A,
            B=B,
            k=len(ns),
            total_relation_rows=0,
            min_abs_delta=None,
            closest_rows=[],
            closure_hits=[],
            min_abs_delta_by_relation={},
        )

    min_abs_delta = min(abs(row.signed_delta) for row in rows)
    closest_rows = [row for row in rows if abs(row.signed_delta) == min_abs_delta]
    closure_hits = [row for row in rows if row.signed_delta == 0]
    min_by_relation: dict[str, int] = {}
    for row in rows:
        abs_delta = abs(row.signed_delta)
        old = min_by_relation.get(row.relation)
        if old is None or abs_delta < old:
            min_by_relation[row.relation] = abs_delta
    return FullPlanePairDeltaSummary(
        A=A,
        B=B,
        k=len(ns),
        total_relation_rows=len(rows),
        min_abs_delta=min_abs_delta,
        closest_rows=closest_rows,
        closure_hits=closure_hits,
        min_abs_delta_by_relation=min_by_relation,
    )
