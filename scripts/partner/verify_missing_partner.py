#!/usr/bin/env python3
"""Verify whether 'missing' partner pairs are really multi-N pairs.

For each missing partner from partner_pair_graph.py, run the authoritative
exhaustive factor_concordant search; if it returns >=2 N, then the catalog
genuinely missed it (fast scanner has a bug or scope issue). If it returns
0 or 1 N, then the partner relation reduces something away and the catalog
is correct.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument(
        "--in",
        dest="in_path",
        type=Path,
        default=Path("results/partner_pair_missing.jsonl"),
    )
    _ = p.add_argument("--max-samples", type=int, default=20)
    return p.parse_args()


def main() -> int:
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )

    args = parse_args()

    seen: set[tuple[int, int]] = set()
    rows: list[dict[str, object]] = []
    with args.in_path.open() as f:
        for line in f:
            r = json.loads(line)
            key = (int(r["partner_A"]), int(r["partner_B"]))
            if key in seen:
                continue
            seen.add(key)
            rows.append(r)
            if len(rows) >= args.max_samples:
                break

    print(f"Verifying {len(rows)} unique missing partners with factor_search ...")
    print()

    really_multi = 0
    really_single = 0
    really_empty = 0

    for r in rows:
        a = int(r["partner_A"])
        b = int(r["partner_B"])
        ns = find_concordant_by_factorization(a, b)
        n_count = len(ns)
        if n_count >= 2:
            really_multi += 1
            tag = "MULTI (catalog missed!)"
        elif n_count == 1:
            really_single += 1
            tag = "single (not multi-N)"
        else:
            really_empty += 1
            tag = "empty (no concordant N)"

        src = (int(r["source_A"]), int(r["source_B"]))
        print(f"  ({a:>5}, {b:>5})  k={n_count}  {tag}")
        print(f"      from {src}  via N=({r['from_N_i']}, {r['from_N_j']})")
        if n_count <= 5:
            print(f"      N = {ns}")

    print()
    print(f"Summary of {len(rows)} sampled missing partners:")
    print(f"  k >= 2 (catalog miss):     {really_multi}")
    print(f"  k == 1:                    {really_single}")
    print(f"  k == 0:                    {really_empty}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
