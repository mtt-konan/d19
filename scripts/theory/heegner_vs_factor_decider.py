"""方向五 audit — is a Heegner canonical-height bound needed to make the
integer-N concordance problem decidable?  (Answer: no.)

Background
----------
THEORY_DIRECTIONS_ADVANCED.md 方向五 frames the Heegner method as: scan the
rank-one Mordell-Weil generator's multiples ``nG+T`` for a point with
``x = N²`` (concordant N), and "upgrade to no_solution once a canonical-height
bound H certifies the bounded scan ``|n|≤M`` is exhaustive."

But the pipeline already contains an *exhaustive, height-bound-free, all-ranks*
decider for concordant integer N:
``concordant.factor_search.find_concordant_by_factorization`` recovers **every**
integer N with ``N²+A²=□`` and ``N²+B²=□`` from divisor pairs of ``B²−A²``
(provably complete; no upper-bound parameter).  It runs before ``heegner`` in
``DEFAULT_METHOD_PIPELINE``.

This script demonstrates, on the residual hard_cases (reduced safe-pass pairs at
a small ``max_hyp``):
  * factorization decides every pair in milliseconds, finding concordant N far
    beyond any bounded MW-multiple / ``ellratpoints`` height window;
  * the rank-one Heegner scan either does not apply (rank≠1) or sees only a
    strict subset of those N — so it adds nothing to the decision.

See worklog 092 and OPEN_DIRECTIONS B.6/wl077 (the complementary height-bound
obstruction, also closed).

Run (PARI only used for the optional rank column):
    PYTHONPATH=src PARI_MT_ENGINE=single uv run python \
        scripts/theory/heegner_vs_factor_decider.py --max-hyp 500
"""

from __future__ import annotations

import argparse
import time

from rational_distance.concordant.analysis import check_chain_compatibility
from rational_distance.concordant.factor_search import find_concordant_by_factorization
from rational_distance.concordant.pairs import generate_ab_pairs
from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair


def inconclusive_hard_cases(max_hyp: int) -> list[tuple[int, int, list[int]]]:
    """Reduced safe-pass pairs with >=2 concordant N, none chain-compatible.

    These are exactly the pairs the ``heegner`` method is invoked on (every
    earlier exhaustive method returned ``inconclusive`` rather than terminating).
    """
    out: list[tuple[int, int, list[int]]] = []
    for a, b in generate_ab_pairs(max_hyp):
        if not allow_reduced_pair(a, b):
            continue
        ns = find_concordant_by_factorization(a, b)
        if len(ns) >= 2 and not any(check_chain_compatibility(a, b, n) for n in ns):
            out.append((a, b, ns))
    return out


def summarize_factor_decider(max_hyp: int) -> dict:
    """Run the exhaustive factor decider over all safe-pass pairs and tally."""
    t0 = time.perf_counter()
    buckets = {"no_concordant": 0, "single": 0, "multi_no_close": 0, "chain_found": 0}
    max_concordant_n = 0
    for a, b in generate_ab_pairs(max_hyp):
        if not allow_reduced_pair(a, b):
            continue
        ns = find_concordant_by_factorization(a, b)
        if not ns:
            buckets["no_concordant"] += 1
            continue
        max_concordant_n = max(max_concordant_n, max(ns))
        if len(ns) == 1:
            buckets["single"] += 1
            continue
        if any(check_chain_compatibility(a, b, n) for n in ns):
            buckets["chain_found"] += 1
        else:
            buckets["multi_no_close"] += 1
    return {
        "elapsed_ms": (time.perf_counter() - t0) * 1000.0,
        "buckets": buckets,
        "max_concordant_n": max_concordant_n,
    }


def _scan_rank_one(a: int, b: int):
    """Optional rank-1 Heegner scan; returns (rank_str, concordant_n_seen)."""
    try:
        from rational_distance.concordant.heegner_height import scan_rank_one_height
    except Exception as exc:  # pragma: no cover - environment without cypari2
        return f"unavailable:{exc}", []
    scan = scan_rank_one_height(a, b)
    if scan.rank_lower is None:
        return f"skipped:{scan.skipped_reason}", []
    rank = f"[{scan.rank_lower},{scan.rank_upper}]"
    if scan.skipped_reason:
        rank += f"/{scan.skipped_reason}"
    return rank, sorted(set(scan.concordant_n))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-hyp", type=int, default=500)
    ap.add_argument(
        "--with-rank",
        action="store_true",
        help="run PARI rank-1 Heegner scan per inconclusive pair",
    )
    args = ap.parse_args()

    summary = summarize_factor_decider(args.max_hyp)
    print(f"== exhaustive factor decider, max_hyp={args.max_hyp} ==")
    print(f"  elapsed: {summary['elapsed_ms']:.1f} ms (all safe-pass pairs)")
    print(f"  buckets: {summary['buckets']}")
    print(f"  largest concordant N found: {summary['max_concordant_n']}")
    print(f"  chain-compatible (would refute Harborth): {summary['buckets']['chain_found']}")

    hard = inconclusive_hard_cases(args.max_hyp)
    print(f"\n== {len(hard)} 'inconclusive' hard_cases (heegner targets) ==")
    for a, b, ns in hard:
        line = f"(A,B)=({a},{b}) concordant_N(exhaustive)={ns} A+B={a + b}"
        if args.with_rank:
            rank, seen = _scan_rank_one(a, b)
            missed = [n for n in ns if n not in seen]
            line += f"\n    rank={rank}  heegner_scan_saw={seen}  MISSED_by_scan={missed}"
        print(line)


if __name__ == "__main__":
    main()
