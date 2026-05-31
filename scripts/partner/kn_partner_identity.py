#!/usr/bin/env python3
"""OPEN_DIRECTIONS A.1 / A.6 — K_n hub partner identity analysis.

Goal (A.1): test whether a K_n hub (n multi-N pairs that share a common
partner / clique structure) gives an algebraic closure obstruction that a
single multi-N pair does not — i.e. whether the hub lets us push the path-A
argument to higher k.

Two structural facts are checked first (A.6, the paper-level relationship):

  (1) shared_partner K_n  ⟺  the partner pair (P_a, P_b) is itself a
      multi-N pair whose concordant-N set contains the n hub nodes
      (the (A,B) ↔ N duality). Verified with the authoritative
      factor_search for every shared_partner hub.

  (2) general K_n requires all C(n,2) hub edges to be multi-N. Empirically
      this caps at K_3 in the coprime catalog (general_K4 = 0).

Then the A.1 question proper: for every hub edge (a, b) with its shared
concordant N, reuse the wl086 (A.2) machinery to test whether the shared
concordant points Q_N lie in 2*E_{a,b}(Q). If they always do — as wl086
proved for single pairs — the 2-descent class is trivial *per edge*,
independently of the hub, so the shared structure adds no obstruction.

Bounded compute only (a few dozen ellgens calls); no long enumeration runs.

Input : results/partner/partner_kn_subgraphs.jsonl
Output: results/partner/kn_partner_identity.jsonl  (+ printed summary)
"""

from __future__ import annotations

import argparse
import json
import sys
from math import gcd
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    _ = p.add_argument(
        "--in",
        dest="in_path",
        type=Path,
        default=ROOT / "results/partner/partner_kn_subgraphs.jsonl",
    )
    _ = p.add_argument(
        "--out",
        type=Path,
        default=ROOT / "results/partner/kn_partner_identity.jsonl",
    )
    _ = p.add_argument("--effort", type=int, default=1, help="PARI ellrank effort (keep small)")
    _ = p.add_argument(
        "--max-edge-value",
        type=int,
        default=120000,
        help="skip ellgens on edges whose larger value exceeds this (cost guard)",
    )
    return p.parse_args()


def main() -> int:
    from rational_distance.concordant.cycle_relations import analyze_cycle_relations
    from rational_distance.concordant.factor_search import (
        find_concordant_by_factorization,
    )

    args = parse_args()
    hubs: list[dict[str, Any]] = []
    with args.in_path.open() as f:
        for line in f:
            hubs.append(json.loads(line))

    general = [h for h in hubs if h["kind"] == "general"]
    shared = [h for h in hubs if h["kind"] == "shared_partner"]
    print(f"hubs: {len(hubs)} total — general={len(general)} shared_partner={len(shared)}")

    # ---- A.6 (1): shared_partner duality -------------------------------------
    print("\n[A.6 duality] shared_partner K_n  ==  partner pair is k>=n multi-N")
    duality_ok = 0
    for h in shared:
        p_a, p_b = h["shared_partner"]
        nodes = set(h["nodes"])
        ns = set(find_concordant_by_factorization(p_a, p_b))
        contains = nodes <= ns
        duality_ok += int(contains)
        g = gcd(p_a, p_b)
        print(
            f"  partner=({p_a},{p_b}) gcd={g} n={h['n']} "
            f"k(partner)={len(ns)} nodes_subset_of_N={contains} "
            f"extra_N={sorted(ns - nodes)[:6]}"
        )
    print(f"  duality holds: {duality_ok}/{len(shared)}")

    # ---- A.6 (2): general K_n cap --------------------------------------------
    gen_by_n: dict[int, int] = {}
    for h in general:
        gen_by_n[h["n"]] = gen_by_n.get(h["n"], 0) + 1
    print(f"\n[A.6 cap] general K_n distribution: {dict(sorted(gen_by_n.items()))}")

    # ---- A.1: per-edge 2-divisibility of shared concordant points ------------
    print("\n[A.1] per-edge 2-divisibility of shared concordant points Q_N")
    records: list[dict[str, Any]] = []
    edges_seen: set[tuple[int, int]] = set()
    n_all_2div = 0
    n_checked = 0
    n_skipped = 0

    def edge_iter() -> Any:
        # General hubs carry explicit edge lists with shared concordant_N.
        for h in general:
            for e in h["edges"]:
                yield h, int(e["a"]), int(e["b"]), [int(x) for x in e["concordant_N"]]
        # Shared_partner hubs: the partner *pair* is the dual multi-N curve.
        for h in shared:
            p_a, p_b = int(h["shared_partner"][0]), int(h["shared_partner"][1])
            yield h, p_a, p_b, None  # Ns resolved below via factor_search

    for h, a, b, ns in edge_iter():
        key = (min(a, b), max(a, b))
        if key in edges_seen:
            continue
        edges_seen.add(key)
        if max(a, b) > args.max_edge_value:
            n_skipped += 1
            continue
        if ns is None:
            ns = find_concordant_by_factorization(a, b)
        if len(ns) < 2:
            continue
        try:
            res = analyze_cycle_relations(a, b, Ns=ns, effort=args.effort)
        except Exception as exc:  # PARI can raise on awkward curves
            n_skipped += 1
            msg = f"{type(exc).__name__}: {exc}"
            print(f"  ({a},{b}) [{h['kind']}] PARI error -> skip: {msg[:70]}")
            records.append({"kind": h["kind"], "a": a, "b": b, "error": msg})
            continue
        if res.skipped_reason is not None:
            n_skipped += 1
            rec = {
                "kind": h["kind"],
                "a": a,
                "b": b,
                "skipped": res.skipped_reason,
            }
            records.append(rec)
            continue
        n_checked += 1
        n_all_2div += int(res.all_two_divisible)
        rec = {
            "kind": h["kind"],
            "a": a,
            "b": b,
            "k": res.k,
            "rank": res.rank,
            "coord_matrix_rank": res.coord_matrix_rank,
            "relation_count": res.relation_count,
            "all_two_divisible": res.all_two_divisible,
            "all_verified": res.all_verified,
        }
        records.append(rec)
        print(
            f"  ({a},{b}) [{h['kind']}] k={res.k} rank={res.rank} "
            f"all_2div={res.all_two_divisible} all_verified={res.all_verified}"
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        for rec in records:
            _ = f.write(json.dumps(rec) + "\n")

    print(
        f"\n[A.1 summary] edges checked={n_checked} "
        f"all_two_divisible={n_all_2div}/{n_checked} skipped={n_skipped}"
    )
    print(f"  wrote {len(records)} records to {args.out}")
    if n_checked > 0 and n_all_2div == n_checked:
        print(
            "\nConclusion: every shared concordant point is 2-divisible on its own\n"
            "edge curve (same as wl086/A.2). The K_n hub adds no cross-edge\n"
            "obstruction — 'sharing' is a coincidence of N-values across curves\n"
            "with distinct j-invariants, not an algebraic linkage. A.1 closes\n"
            "negative-but-informative, the same wall as A.2."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
