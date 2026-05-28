#!/usr/bin/env python3
"""Path A experiment: analyze E(Q) structure of k=2 multi-N pairs.

For each k=2 multi-N pair ``(A, B)`` with concordant_N = ``{N_1, N_2}`` (safe
sieve passed, no closure), compute on ``E_{A,B}: Y² = X(X+A²)(X+B²)``:

- ``P_1 = (N_1², Y_1)``, ``P_2 = (N_2², Y_2)`` — the two square-X points.
- ``P_1 + P_2`` via PARI ``elladd`` (group law on E(Q)).
- Is ``P_1 + P_2`` a torsion point?
- ``ellbil(E, P_1, P_2)`` — Néron-Tate height pairing.
- ``δ := S - (N_1 + N_2)`` — closure residue (always > 0 in scanned range
  since no closure was found; sign tells which side).

Goal: spot any pattern correlating ``P_1 + P_2`` (group-theoretic position)
with ``δ`` (closure residue). If ``P_1 + P_2`` is **always** torsion, that's
a strong structural claim. If ``δ`` correlates with height pairing sign /
magnitude, that's another lead.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from math import gcd, isqrt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from rational_distance.concordant.fast_multi_n import fast_multi_concordant_pairs
from rational_distance.concordant.heegner_height import (
    _curve,
    _finite_torsion_points,
)
from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair


# Module-level cached PARI instance (single-process; cypari2 state isn't safe
# across forks, and spawning Python processes for PARI rank work has costly
# init).
_pari_cache: object | None = None


def _ensure_pari():
    """Lazy import PARI; cache to avoid reinit cost."""
    global _pari_cache
    if _pari_cache is None:
        from rational_distance.concordant.analysis import _ensure_pari as _ep

        _pari_cache = _ep()
    return _pari_cache


def _isqrt_exact(n: int) -> int | None:
    if n < 0:
        return None
    s = isqrt(n)
    return s if s * s == n else None


def _square_x_point(pari, A: int, B: int, N: int):
    """Return PARI point ``(N², Y)`` on ``E_{A,B}`` with Y > 0.

    By Ono's identity, ``Y_N = N · √(N²+A²) · √(N²+B²)`` is rational.
    """
    a_root = _isqrt_exact(N * N + A * A)
    b_root = _isqrt_exact(N * N + B * B)
    if a_root is None or b_root is None:
        raise ValueError(f"({A}, {B}, {N}) is not concordant (N²+A² or N²+B² not square)")
    y = N * a_root * b_root
    return pari(f"[{N * N}, {y}]")


def _point_xy_strings(point) -> tuple[str, str] | None:
    try:
        if len(point) < 2:
            return None
        return str(point[0]), str(point[1])
    except Exception:
        return None


def _is_identity(pari, point) -> bool:
    """Detect the point at infinity (PARI returns ``[0]`` for O)."""
    try:
        return len(point) < 2
    except Exception:
        return False


def _torsion_lookup(pari, E, point, torsion_table: list[tuple[str, list[int]]]) -> str | None:
    """Return torsion label if ``point`` matches a known torsion point, else None."""
    if _is_identity(pari, point):
        return "O"
    xy = _point_xy_strings(point)
    if xy is None:
        return None
    for label, coords in torsion_table:
        try:
            if int(point[0]) == coords[0] and int(point[1]) == coords[1]:
                return label
        except Exception:
            continue
    return None


@dataclass
class FiberRow:
    A: int
    B: int
    S: int  # A + B
    N_1: int
    N_2: int
    delta: int  # S - (N_1 + N_2)
    rank_lower: int
    rank_upper: int
    P_sum_xy: tuple[str, str] | None  # PARI repr of P_1 + P_2
    P_sum_torsion: str | None  # torsion label, or None
    height_pairing: float | None  # ellbil(E, P_1, P_2)
    h1: float | None  # ellheight(E, P_1)
    h2: float | None  # ellheight(E, P_2)


def analyze_pair(
    pari, A: int, B: int, N_1: int, N_2: int, *, effort: int = 1
) -> FiberRow:
    """Compute E(Q) group-theoretic data for one k=2 multi-N pair.

    ``effort`` is forwarded to ``ellrank``. Effort=1 is fast but can give
    spurious ``lower=0`` (cf. wl036); auto-upgrade to effort=2 is left to the
    caller for imprecise rows.
    """
    S = A + B
    delta = S - (N_1 + N_2)

    E = _curve(A, B, pari)
    P_1 = _square_x_point(pari, A, B, N_1)
    P_2 = _square_x_point(pari, A, B, N_2)
    P_sum = pari.elladd(E, P_1, P_2)

    try:
        if effort <= 0:
            rank_info = pari.ellrank(E)
        else:
            rank_info = pari.ellrank(E, effort)
        rank_lower = int(rank_info[0])
        rank_upper = int(rank_info[1])
    except Exception:
        rank_lower = -1
        rank_upper = -1

    torsion_table = _finite_torsion_points(A, B)
    p_sum_label = _torsion_lookup(pari, E, P_sum, torsion_table)
    p_sum_xy = _point_xy_strings(P_sum)

    try:
        pairing = float(pari.ellbil(E, P_1, P_2))
    except Exception:
        pairing = None

    try:
        h1 = float(pari.ellheight(E, P_1))
    except Exception:
        h1 = None
    try:
        h2 = float(pari.ellheight(E, P_2))
    except Exception:
        h2 = None

    return FiberRow(
        A=A,
        B=B,
        S=S,
        N_1=N_1,
        N_2=N_2,
        delta=delta,
        rank_lower=rank_lower,
        rank_upper=rank_upper,
        P_sum_xy=p_sum_xy,
        P_sum_torsion=p_sum_label,
        height_pairing=pairing,
        h1=h1,
        h2=h2,
    )


def collect_k2_pairs(max_hyp: int, limit: int) -> list[tuple[int, int, int, int]]:
    """Return up to ``limit`` k=2 multi-N pairs (A, B, N_1, N_2) with safe pass."""
    pairs = fast_multi_concordant_pairs(max_hyp)
    out: list[tuple[int, int, int, int]] = []
    for (a, b), ns in pairs.items():
        if len(ns) != 2:
            continue
        if not allow_reduced_pair(a, b):
            continue
        out.append((a, b, ns[0], ns[1]))
        if len(out) >= limit:
            break
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Path A: analyze E(Q) sums P_{N_1} + P_{N_2} on k=2 multi-N pairs."
    )
    parser.add_argument("--max-hyp", type=int, default=10000)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--jsonl-out", type=Path, default=None)
    parser.add_argument(
        "--effort",
        type=int,
        default=1,
        help="PARI ellrank effort. effort=1 is fast but can give spurious "
        "lower=0; imprecise rows are then auto-recomputed with --rerank-effort.",
    )
    parser.add_argument(
        "--rerank-effort",
        type=int,
        default=2,
        help="Effort used to rerun imprecise (lower<upper) rows. 0 disables.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only collect k=2 pairs, don't call PARI.",
    )
    args = parser.parse_args()

    pairs = collect_k2_pairs(args.max_hyp, args.limit)
    print(f"[phase] collected {len(pairs)} k=2 safe-pass multi-N pairs (max_hyp={args.max_hyp})")

    if args.dry_run:
        for a, b, n1, n2 in pairs:
            print(f"  ({a}, {b}) N=[{n1}, {n2}]  S={a+b}  N1+N2={n1+n2}  delta={a+b-n1-n2}")
        return

    pari = _ensure_pari()
    rows: list[FiberRow] = []
    torsion_counts: Counter[str] = Counter()
    print(f"[phase] PARI analysis (effort={args.effort})…")
    for i, (a, b, n1, n2) in enumerate(pairs, 1):
        try:
            row = analyze_pair(pari, a, b, n1, n2, effort=args.effort)
        except Exception as exc:
            print(f"  [{i:3d}] ({a}, {b}) FAILED: {exc}")
            continue
        rows.append(row)
        label = row.P_sum_torsion if row.P_sum_torsion else "non-torsion"
        torsion_counts[label] += 1
        pairing_str = f"{row.height_pairing:+.5f}" if row.height_pairing is not None else "—"
        h1_str = f"{row.h1:.5f}" if row.h1 is not None else "—"
        h2_str = f"{row.h2:.5f}" if row.h2 is not None else "—"
        print(
            f"  [{i:3d}] (A={a}, B={b}) N=[{n1}, {n2}] delta={row.delta:+d} "
            f"rank=[{row.rank_lower},{row.rank_upper}] "
            f"P1+P2_torsion={label} <P1,P2>={pairing_str} h(P1)={h1_str} h(P2)={h2_str}"
        )

    # Auto-rerank imprecise rows.
    if args.rerank_effort > args.effort:
        imprecise_idx = [
            i for i, r in enumerate(rows) if r.rank_lower != r.rank_upper
        ]
        if imprecise_idx:
            print(
                f"[phase] reranking {len(imprecise_idx)} imprecise rows "
                f"with effort={args.rerank_effort}…"
            )
            for i in imprecise_idx:
                r = rows[i]
                try:
                    new_row = analyze_pair(
                        pari, r.A, r.B, r.N_1, r.N_2, effort=args.rerank_effort
                    )
                except Exception as exc:
                    print(f"  ({r.A},{r.B}) RERANK FAILED: {exc}")
                    continue
                print(
                    f"  ({r.A},{r.B}) rank: [{r.rank_lower},{r.rank_upper}] "
                    f"→ [{new_row.rank_lower},{new_row.rank_upper}]"
                )
                rows[i] = new_row

    print("=" * 72)
    print(f"k=2 pairs analyzed: {len(rows)}")
    ranks_counter = Counter(r.rank_lower for r in rows)
    print("rank_lower distribution: " + str(dict(sorted(ranks_counter.items()))))
    rank_lt_2 = sum(1 for r in rows if r.rank_lower < 2)
    imprecise = sum(1 for r in rows if r.rank_lower != r.rank_upper)
    print(f"rank<2 (post-rerank): {rank_lt_2}    imprecise: {imprecise}")
    print("P_{N_1} + P_{N_2} torsion classification:")
    for label, count in torsion_counts.most_common():
        print(f"  {label:>20s}: {count}")

    if args.jsonl_out is not None:
        args.jsonl_out.parent.mkdir(parents=True, exist_ok=True)
        with args.jsonl_out.open("w") as fh:
            for row in rows:
                fh.write(json.dumps(asdict(row)) + "\n")
        print(f"wrote {len(rows)} rows to {args.jsonl_out}")


if __name__ == "__main__":
    main()
