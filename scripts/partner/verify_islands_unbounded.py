#!/usr/bin/env python3
"""Definitive island-closure test: unbounded BFS, NO max_value cap (wl096).

The ``island`` label in ``comp0_island_analysis.py`` is a per-vertex check
(every concordant partner pair stays <= window). This script upgrades that to
a direct, window-free proof: for every component classified as an island,
start a BFS from its vertex set and expand with the complete, range-free
kernel ``exact_concordant_pair`` (which fully factors A^2/B^2, so the concordant
set per vertex is the entire FINITE set — no upper bound). Confirm the BFS
closes to EXACTLY the original vertex set (never escapes), i.e. the component
is a genuine finite component of the infinite graph G_M.

A vertex cap (len(S)*20+200) guards against runaway in case of any kernel
disagreement; exceeding it is reported as a leak (expected: none).

Also reports the global maximum coordinate ever reached by ANY island BFS:
because it is finite and < window, pushing max_value -> infinity adds nothing.
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
        "--components",
        type=Path,
        default=Path("results/partner/partner_full_bfs_components.jsonl"),
    )
    _ = p.add_argument("--window", type=int, default=1_000_000)
    _ = p.add_argument(
        "--out",
        type=Path,
        default=Path("results/partner/island_unbounded_bfs.json"),
    )
    return p.parse_args()


def main() -> int:
    from rational_distance.concordant.fast_multi_n import exact_concordant_pair

    args = parse_args()
    window = int(args.window)

    def neighbors(v: tuple[int, int]) -> list[tuple[int, int]]:
        a, b = v
        if a < 2:
            return []
        ns = exact_concordant_pair(a, b)
        return [(ni, nj) if ni < nj else (nj, ni)
                for ni, nj in combinations(ns, 2)]

    def is_island(verts: list[tuple[int, int]]) -> bool:
        for a, b in verts:
            if a < 2:
                continue
            ns = exact_concordant_pair(a, b)
            if any(max(ni, nj) > window for ni, nj in combinations(ns, 2)):
                return False
        return True

    comps = []
    with Path(args.components).open() as f:
        for line in f:
            comps.append(json.loads(line))
    giant = max(c["size"] for c in comps)

    n_islands = n_closed = n_leaked = 0
    global_max_coord = 0
    leaks = []

    for c in comps:
        if c["size"] == giant:
            continue
        verts = [(a, b) for a, b in c["vertices"]]
        if not is_island(verts):
            continue
        n_islands += 1
        S = set(verts)
        cap = len(S) * 20 + 200
        R = set(S)
        frontier = list(S)
        leaked = False
        while frontier and not leaked:
            nf = []
            for v in frontier:
                for u in neighbors(v):
                    if u[0] > global_max_coord:
                        global_max_coord = u[0]
                    if u[1] > global_max_coord:
                        global_max_coord = u[1]
                    if u not in R:
                        R.add(u)
                        nf.append(u)
                        if len(R) > cap:
                            leaked = True
                            break
                if leaked:
                    break
            frontier = nf
        if leaked or R != S:
            n_leaked += 1
            leaks.append({"component_id": c["component_id"],
                          "orig": len(S), "reached": len(R), "leaked": leaked})
        else:
            n_closed += 1

    out = {
        "window": window,
        "islands_tested": n_islands,
        "closed_to_exact_original_set": n_closed,
        "leaked_beyond_original": n_leaked,
        "global_max_coord_reached": global_max_coord,
        "leaks": leaks,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with Path(args.out).open("w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"islands tested (unbounded BFS, NO window cap): {n_islands}")
    print(f"  closed to EXACTLY original vertex set: {n_closed}")
    print(f"  leaked / grew beyond original:         {n_leaked}")
    print(f"  global max coordinate ever reached:    {global_max_coord} "
          f"(< window {window} => infinite window adds nothing)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
