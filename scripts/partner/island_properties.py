#!/usr/bin/env python3
"""Characterize the genuine islands of G_M (wl096 follow-up).

Restricted study of *only* the untruncated, partner-closed components (the
"islands" from ``comp0_island_analysis.py``). For each island, using the
complete range-free kernel ``exact_concordant_pair``, measure:

  structure : size, circuit rank (tree vs cyclic), #hubs (k>=3) vs leaves,
              whether it is a single-hub star (size == 1 + C(max_k, 2)),
              and the degree law deg == C(k, 2) (sum check vs edge count);
  closure   : count of N_i + N_j == A + B (Harborth condition) over all verts;
  arithmetic: gcd(A, B) of the dominant hub, coprime vs non-coprime, and the
              gcd x max_k cross-tab; for non-coprime hubs whether the reduced
              primitive (A/g, B/g) is itself a multi-N pair / a comp0 vertex.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from math import comb, gcd
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument(
        "--components", type=Path,
        default=Path("results/partner/partner_full_bfs_components.jsonl"))
    _ = p.add_argument(
        "--layers", type=Path,
        default=Path("results/partner/comp0_island_analysis_1M.jsonl"),
        help="jsonl with {component_id, layer} to select layer==island")
    _ = p.add_argument(
        "--out", type=Path,
        default=Path("results/partner/island_properties_1M.json"))
    return p.parse_args()


def main() -> int:
    from rational_distance.concordant.fast_multi_n import exact_concordant_pair

    args = parse_args()
    layer = {}
    with args.layers.open() as f:
        for line in f:
            r = json.loads(line)
            layer[r["component_id"]] = r["layer"]

    comps = [json.loads(line) for line in args.components.open()]
    giant = max(c["size"] for c in comps)
    comp0 = next(({(a, b) for a, b in c["vertices"]}
                 for c in comps if c["size"] == giant), set())

    size_hist: Counter[int] = Counter()
    k_hist: Counter[int] = Counter()
    cr_hist: Counter[int] = Counter()
    single_star = multi_hub = deg_ok = deg_bad = closure_total = 0
    coprime = noncoprime = red_multiN = red_in_comp0 = 0
    gcd_hist: Counter[int] = Counter()
    cop_by_k: Counter[int] = Counter()
    noncop_by_k: Counter[int] = Counter()
    gcd_by_k: dict[int, Counter[int]] = defaultdict(Counter)
    max_coord = n = 0
    examples: list[dict] = []

    for c in comps:
        if layer.get(c["component_id"]) != "island":
            continue
        n += 1
        verts = [(a, b) for a, b in c["vertices"]]
        size_hist[c["size"]] += 1
        cr_hist[c["edges"] - c["size"] + 1] += 1
        deg_sum = n_hub = 0
        best = (0, (0, 0))
        for a, b in verts:
            max_coord = max(max_coord, a, b)
            if a < 2:
                continue
            ns = exact_concordant_pair(a, b)
            k = len(ns)
            deg_sum += comb(k, 2)
            if k >= 3:
                n_hub += 1
            if k > best[0]:
                best = (k, (a, b))
            for ni, nj in combinations(ns, 2):
                if ni + nj == a + b:
                    closure_total += 1
        mk, hub = best
        k_hist[mk] += 1
        deg_ok += deg_sum == 2 * c["edges"]
        deg_bad += deg_sum != 2 * c["edges"]
        if n_hub <= 1 and c["size"] == 1 + comb(mk, 2):
            single_star += 1
        if n_hub > 1:
            multi_hub += 1
        g = gcd(hub[0], hub[1])
        gcd_hist[g] += 1
        gcd_by_k[mk][g] += 1
        if g == 1:
            coprime += 1
            cop_by_k[mk] += 1
        else:
            noncoprime += 1
            noncop_by_k[mk] += 1
            ra, rb = hub[0] // g, hub[1] // g
            rk = len(exact_concordant_pair(ra, rb)) if ra >= 2 else 0
            red_multiN += rk >= 2
            red_in_comp0 += (ra, rb) in comp0
            if len(examples) < 15 and mk >= 4:
                examples.append({"hub": list(hub), "gcd": g,
                                 "reduced": [ra, rb], "reduced_k": rk,
                                 "island_size": c["size"], "max_k": mk})

    out = {
        "islands": n,
        "total_vertices": sum(s * c for s, c in size_hist.items()),
        "max_size": max(size_hist),
        "size_hist": dict(sorted(size_hist.items())),
        "max_k_hist": dict(sorted(k_hist.items())),
        "circuit_rank_hist": dict(sorted(cr_hist.items())),
        "trees_cr0": cr_hist[0],
        "single_hub_star": single_star,
        "multi_hub": multi_hub,
        "degree_law_Ck2_ok": deg_ok,
        "degree_law_Ck2_bad": deg_bad,
        "closure_hits_total": closure_total,
        "max_coord": max_coord,
        "coprime_hubs": coprime,
        "noncoprime_hubs": noncoprime,
        "gcd_hist_top": dict(sorted(gcd_hist.items(),
                                    key=lambda x: -x[1])[:15]),
        "coprime_x_max_k": dict(sorted(cop_by_k.items())),
        "noncoprime_x_max_k": dict(sorted(noncop_by_k.items())),
        "gcd_by_max_k_top": {k: dict(sorted(gcd_by_k[k].items(),
                                            key=lambda x: -x[1])[:6])
                             for k in sorted(gcd_by_k)},
        "noncoprime_reduced_is_multiN": red_multiN,
        "noncoprime_reduced_in_comp0": red_in_comp0,
        "examples_highk_noncoprime": examples,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    for key in ("islands", "max_size", "max_k_hist", "circuit_rank_hist",
                "single_hub_star", "multi_hub", "degree_law_Ck2_ok",
                "closure_hits_total", "coprime_hubs", "noncoprime_hubs",
                "coprime_x_max_k", "noncoprime_x_max_k", "gcd_by_max_k_top",
                "noncoprime_reduced_is_multiN", "noncoprime_reduced_in_comp0"):
        print(f"{key}: {out[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
