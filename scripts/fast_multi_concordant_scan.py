#!/usr/bin/env python3
"""Pivot-on-N fast multi-concordant-N scanner.

Replaces the (A,B)-outer brute force scan with the (N)-pivot enumeration in
`rational_distance.concordant.fast_multi_n`. Writes JSONL with the same
schema as `multi_concordant_n_scan.py` so it can be diffed against the
authoritative max_hyp=10000 ground truth.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fast pivot-on-N multi-concordant-N scanner"
    )
    _ = parser.add_argument("--max-hyp", type=int, default=2000)
    _ = parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output JSONL (default: results/multi_concordant_N_max{max_hyp}_fast.jsonl)",
    )
    return parser.parse_args()


def main() -> int:
    from rational_distance.concordant.fast_multi_n import fast_multi_concordant_pairs

    args = parse_args()
    max_hyp = cast(int, args.max_hyp)
    out_path = cast(Path | None, args.out)
    if out_path is None:
        out_path = ROOT / "results" / f"multi_concordant_N_max{max_hyp}_fast.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"max_hyp={max_hyp}")
    print(f"output: {out_path}")
    print()

    t0 = time.perf_counter()
    pairs = fast_multi_concordant_pairs(max_hyp=max_hyp)
    elapsed = time.perf_counter() - t0

    with out_path.open("w", encoding="utf-8") as fh:
        for (a, b), ns in sorted(pairs.items()):
            target = a + b
            ns_set = set(ns)
            closure_pairs: list[list[int]] = []
            for n1 in ns:
                n2 = target - n1
                if n2 != n1 and n2 in ns_set and n2 > 0:
                    closure_pairs.append([n1, n2])
            row = {
                "A": a,
                "B": b,
                "n_concordant": len(ns),
                "concordant_N": ns,
                "A_plus_B": target,
                "closure_pairs": closure_pairs,
            }
            _ = fh.write(json.dumps(row) + "\n")

    print(f"multi-N pairs: {len(pairs)}")
    print(f"elapsed: {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
