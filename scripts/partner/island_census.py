#!/usr/bin/env python3
"""Cross-window island census (wl096 follow-up).

For each BFS window (e.g. 1M / 2M / 7M) classify every non-giant component as
``branch`` (truncated: some concordant partner pair exceeds the window, via the
complete range-free kernel) or ``island`` (untruncated / partner-closed). Then,
using the smallest window's islands as the reference set, answer two questions
for each larger window:

  * do all reference islands reappear as an IDENTICAL separate component
    (independent BFS run + a different concordant kernel => cross-confirmation)?
  * did NEW islands appear, split into
      - newly-closed : all coords <= ref window but was a branch at ref window
      - brand-new    : contains a vertex with coordinate > ref window
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument(
        "--window",
        action="append",
        nargs=2,
        metavar=("MAX_VALUE", "COMPONENTS_JSONL"),
        required=True,
        help="repeat; first given window is the reference. "
        "e.g. --window 1000000 a.jsonl --window 7000000 b.jsonl",
    )
    _ = p.add_argument(
        "--out", type=Path,
        default=Path("results/partner/island_census.json"))
    return p.parse_args()


def main() -> int:
    from rational_distance.concordant.fast_multi_n import exact_concordant_pair

    def classify(verts: list[tuple[int, int]], window: int) -> tuple[int, bool]:
        max_k, trunc = 0, False
        for a, b in verts:
            if a < 2:
                continue
            ns = exact_concordant_pair(a, b)
            if len(ns) > max_k:
                max_k = len(ns)
            for ni, nj in combinations(ns, 2):
                if max(ni, nj) > window:
                    trunc = True
        return max_k, trunc

    args = parse_args()
    windows = [(int(w), Path(f)) for w, f in args.window]
    ref_w = windows[0][0]

    result = {"reference_window": ref_w, "windows": []}
    ref_islands: set[frozenset[tuple[int, int]]] = set()

    for wi, (w, path) in enumerate(windows):
        comps = [json.loads(line) for line in path.open()]
        giant = max(c["size"] for c in comps)
        total = sum(c["size"] for c in comps)
        n_branch = n_island = 0
        khist: dict[int, int] = {}
        islands_here: set[frozenset[tuple[int, int]]] = set()
        matched = brand_new = newly_closed = 0
        for c in comps:
            if c["size"] == giant:
                continue
            verts = [(a, b) for a, b in c["vertices"]]
            fs = frozenset(verts)
            max_k, trunc = classify(verts, w)
            if trunc:
                n_branch += 1
                continue
            n_island += 1
            khist[max_k] = khist.get(max_k, 0) + 1
            islands_here.add(fs)
            if wi > 0:
                if fs in ref_islands:
                    matched += 1
                elif max(max(a, b) for a, b in verts) > ref_w:
                    brand_new += 1
                else:
                    newly_closed += 1
        entry = {
            "window": w,
            "giant_size": giant,
            "giant_pct": round(giant / total * 100, 2),
            "branches_truncated": n_branch,
            "islands": n_island,
            "island_k_hist": dict(sorted(khist.items())),
        }
        if wi == 0:
            ref_islands = islands_here
        else:
            entry["ref_islands_reappearing_identically"] = matched
            entry["ref_islands_total"] = len(ref_islands)
            entry["new_islands_brand_new_coord_gt_ref"] = brand_new
            entry["new_islands_newly_closed"] = newly_closed
        result["windows"].append(entry)
        print(json.dumps(entry, ensure_ascii=False))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
