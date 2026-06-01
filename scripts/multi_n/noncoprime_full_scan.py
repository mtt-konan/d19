"""Full-space (coprime + non-coprime) multi-N closure scan via the sound
3-stage pipeline (wl101 plan):

    gcd_aware_kills (D_g, O(1))
        -> chain_closure mod-p^2 (STANDARD, full_plane)
            -> GEN-CLOSURE (exact_concordant_pair complete set + 4 relations)

This is the coprime-only generator with the two non-coprime filters REMOVED
(fast_multi_n.py:214-218), so every multi-N pair with both legs <= max_hyp is
covered, gcd-tagged, and decided. Any closure hit is a Harborth counterexample
candidate and is reported loudly.

Usage: PYTHONPATH=src python scripts/multi_n/noncoprime_full_scan.py [max_hyp]
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter, defaultdict
from math import gcd
from pathlib import Path

from rational_distance.concordant.chain_closure_sieve import (
    STANDARD_MODULI,
    find_killer_modulus,
)
from rational_distance.concordant.fast_multi_n import (
    exact_concordant_pair,
    iter_concordant_a_n,
)
from rational_distance.concordant.safe_pair_sieve import gcd_aware_kills


def full_multi_concordant_pairs(max_hyp: int) -> dict[tuple[int, int], list[int]]:
    """All (A,B), A<B<=max_hyp with >=2 shared concordant N — NO coprime/parity
    filter (covers the non-coprime half-space)."""
    a_sets: dict[int, list[int]] = defaultdict(list)
    for a, n in iter_concordant_a_n(max_hyp):
        a_sets[n].append(a)

    pairs_with_n: dict[tuple[int, int], list[int]] = defaultdict(list)
    for n, a_set in a_sets.items():
        if len(a_set) < 2:
            continue
        a_set.sort()
        m = len(a_set)
        for i in range(m):
            ai = a_set[i]
            for j in range(i + 1, m):
                pairs_with_n[(ai, a_set[j])].append(n)
    return {k: sorted(v) for k, v in pairs_with_n.items() if len(v) >= 2}


def closes(a: int, b: int, s: list[int]) -> bool:
    targets = {a + b, abs(a - b)}
    return any(
        (s[i] + s[j]) in targets or abs(s[i] - s[j]) in targets
        for i in range(len(s))
        for j in range(i + 1, len(s))
    )


def main() -> None:
    max_hyp = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000
    t0 = time.perf_counter()
    pairs = full_multi_concordant_pairs(max_hyp)
    t_gen = time.perf_counter() - t0

    total = len(pairs)
    coprime = noncoprime = 0
    dg_killed = chain_killed = gen_survivors = closures = 0
    gen_mismatch = 0
    surv_gcd = Counter()
    closure_hits: list[tuple[int, int, list[int]]] = []

    for (a, b), ns in pairs.items():
        g = gcd(a, b)
        if g == 1:
            coprime += 1
        else:
            noncoprime += 1
        # stage 1: D_g sound sieve
        if gcd_aware_kills(a, b):
            dg_killed += 1
            continue
        # stage 2: chain_closure mod-p^2
        if find_killer_modulus(a, b, full_plane=True, moduli=STANDARD_MODULI) is not None:
            chain_killed += 1
            continue
        # stage 3: GEN-CLOSURE on the complete concordant set
        s = exact_concordant_pair(a, b)
        if s != ns:
            gen_mismatch += 1
        gen_survivors += 1
        surv_gcd[g] += 1
        if closes(a, b, s):
            closures += 1
            closure_hits.append((a, b, s))

    dt = time.perf_counter() - t0
    out = {
        "max_hyp": max_hyp,
        "total_multi_n_pairs": total,
        "coprime_pairs": coprime,
        "noncoprime_pairs": noncoprime,
        "stage1_Dg_killed": dg_killed,
        "stage2_chain_killed": chain_killed,
        "stage3_gen_survivors": gen_survivors,
        "closures": closures,
        "gen_complete_set_mismatch": gen_mismatch,
        "survivor_gcd_dist": dict(sorted(surv_gcd.items())),
        "closure_hits": closure_hits,
        "gen_seconds": round(t_gen, 1),
        "total_seconds": round(dt, 1),
    }
    print(json.dumps(out, indent=2))

    outdir = Path(__file__).resolve().parents[2] / "results/multi_n"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"full_scan_max{max_hyp}.json").write_text(json.dumps(out, indent=2))

    if closures:
        print(f"\n*** {closures} CLOSURE HIT(S) — HARBORTH COUNTEREXAMPLE CANDIDATE(S) ***")
        for a, b, s in closure_hits[:20]:
            print(f"    (A,B)=({a},{b}) gcd={gcd(a,b)} N={s} A+B={a+b} |A-B|={abs(a-b)}")
    else:
        print(f"\nNO closure up to max_hyp={max_hyp} "
              f"(coprime + non-coprime), {total} multi-N pairs decided.")


if __name__ == "__main__":
    main()
