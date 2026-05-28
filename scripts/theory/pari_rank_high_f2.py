#!/usr/bin/env python3
"""Run PARI ellrank on every F₂-rank ≥ threshold pair in a classified catalog.

Reads a JSONL produced by `scripts/classify_multi_n_by_f2_rank.py` (e.g.
`results/multi_concordant_N_max50000_classified.jsonl`), filters to pairs
with `f2_rank >= --min-f2-rank`, and calls `compute_rank` from the
analysis module on each. Output is a new JSONL augmenting each row with:

  rank_lower, rank_upper, sha2_lower, n_generators, pari_elapsed_s

Prints a rank-distribution histogram and the top pairs sorted by
``(rank_upper, rank_lower, f2_rank)`` descending.

Usage::

    uv run python scripts/pari_rank_high_f2.py \
        --in  results/multi_concordant_N_max50000_classified.jsonl \
        --out results/multi_concordant_N_max50000_pari_rank.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument("--in", dest="in_path", type=Path, required=True)
    _ = p.add_argument("--out", dest="out_path", type=Path, required=True)
    _ = p.add_argument("--min-f2-rank", type=int, default=3)
    _ = p.add_argument("--effort", type=int, default=1, help="PARI ellrank effort")
    _ = p.add_argument("--top", type=int, default=30)
    return p.parse_args()


def main() -> int:
    from rational_distance.concordant.analysis import compute_rank

    args = parse_args()
    if not args.in_path.exists():
        print(f"Input not found: {args.in_path}", file=sys.stderr)
        return 2
    args.out_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    with args.in_path.open("r", encoding="utf-8") as fin:
        for raw in fin:
            line = raw.strip()
            if not line:
                continue
            entry = json.loads(line)
            if int(entry.get("f2_rank", 0)) >= args.min_f2_rank:
                rows.append(entry)

    print(
        f"selected {len(rows)} pairs with f2_rank >= {args.min_f2_rank} "
        f"from {args.in_path}"
    )

    failed = 0
    rank_hist: Counter[tuple[int, int]] = Counter()
    sha2_hist: Counter[int] = Counter()
    started = time.perf_counter()

    with args.out_path.open("w", encoding="utf-8") as fout:
        for idx, entry in enumerate(rows, start=1):
            a = int(entry["A"])  # type: ignore[arg-type]
            b = int(entry["B"])  # type: ignore[arg-type]
            t0 = time.perf_counter()
            try:
                _, (lower, upper), sha2_lower, gens = compute_rank(
                    a, b, effort=args.effort
                )
            except Exception as exc:
                print(f"  [{idx:>3}] ({a}, {b}): PARI failed: {exc}")
                failed += 1
                continue
            elapsed = time.perf_counter() - t0
            rank_hist[(int(lower), int(upper))] += 1
            sha2_hist[int(sha2_lower)] += 1
            out_entry = {
                **entry,
                "rank_lower": int(lower),
                "rank_upper": int(upper),
                "sha2_lower": int(sha2_lower),
                "n_generators": len(gens),
                "pari_elapsed_s": round(elapsed, 4),
            }
            fout.write(json.dumps(out_entry) + "\n")
            if idx % 20 == 0 or idx == len(rows):
                print(
                    f"  [{idx:>3}/{len(rows)}] ({a:>6}, {b:>6}): "
                    f"rank {lower}/{upper} sha2≥{sha2_lower}  "
                    f"{elapsed:.2f}s"
                )

    total_elapsed = time.perf_counter() - started
    print()
    print(f"processed: {len(rows)} pairs in {total_elapsed:.1f}s "
          f"({failed} PARI failures)")
    print(f"output:    {args.out_path}")
    print()

    print("rank (lower / upper) distribution:")
    for (lo, hi), count in sorted(rank_hist.items()):
        marker = " ←" if lo == hi else "  "
        certified = "certified" if lo == hi else "bounds only"
        print(f"  {lo}/{hi}: {count:>4}  ({certified}){marker}")
    print()

    print("sha2_lower distribution:")
    for sha2, count in sorted(sha2_hist.items()):
        print(f"  sha2 ≥ {sha2}: {count:>4}")
    print()

    rows_with_rank = []
    with args.out_path.open("r", encoding="utf-8") as fin:
        for raw in fin:
            line = raw.strip()
            if line:
                rows_with_rank.append(json.loads(line))

    rows_with_rank.sort(
        key=lambda r: (
            -int(r["rank_upper"]),
            -int(r["rank_lower"]),
            -int(r["f2_rank"]),
            int(r["A"]),
        )
    )
    print(f"Top {min(args.top, len(rows_with_rank))} pairs by rank_upper:")
    for r in rows_with_rank[: args.top]:
        certified = "*" if r["rank_lower"] == r["rank_upper"] else " "
        print(
            f"  {certified} A={r['A']:>6} B={r['B']:>6}  "
            f"k={r['n_concordant']}  F₂={r['f2_rank']}  "
            f"rank {r['rank_lower']}/{r['rank_upper']}  "
            f"sha2≥{r['sha2_lower']}"
        )
    print("  '*' marks pairs with certified rank (lower == upper).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
