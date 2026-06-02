"""Optimized full-space (coprime + non-coprime) multi-N closure scan (wl103).

Same sound 3-stage pipeline as `noncoprime_full_scan.py`
(`gcd_aware_kills -> chain_closure mod-p^2 -> GEN-CLOSURE`) but built to scale
to max_hyp=1e6+:

* generation + multi-N pair extraction use the Cython kernel
  (`_concordant_gen.generate` + `emit_pairs(..., coprime_only=False)`) and numpy
  sort/dedup — no Python relation dict (which OOMs past ~2e6);
* the multi-N pairs are kept as a packed int64 numpy array of pkeys
  (pkey = A*factor + B), ~8 bytes/pair;
* the 3-stage judging is parallelized over `--workers` processes, each decoding
  its slice of pkeys and returning aggregate counts only (tiny IPC).

Any closure hit is a Harborth counterexample candidate and is reported loudly.

Usage:
    PYTHONPATH=src python scripts/multi_n/noncoprime_full_scan_fast.py \
        --max-hyp 1000000 --workers 2
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from math import gcd
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))


def multi_n_pkeys(max_hyp: int) -> tuple[np.ndarray, int]:
    """Return (sorted int64 array of pkeys for every multi-N pair, factor).

    pkey = A*factor + B with A<B<=max_hyp; a pkey present means that (A,B) share
    >= 2 concordant N. NO coprime/parity filter (covers non-coprime).
    """
    import _concordant_gen as cy  # type: ignore[import-not-found]

    n_arr, a_arr = cy.generate(max_hyp)
    order = np.argsort(n_arr, kind="quicksort")
    n_arr = n_arr[order]
    a_arr = a_arr[order]
    del order
    change = np.flatnonzero(np.diff(n_arr)) + 1
    starts = np.concatenate(([0], change))
    ends = np.concatenate((change, [n_arr.shape[0]]))
    keep = (ends - starts) >= 2
    ms = starts[keep].astype(np.int64)
    me = ends[keep].astype(np.int64)
    maxbucket = int((me - ms).max()) if ms.shape[0] else 0
    factor = max_hyp + 1
    pk, _nn = cy.emit_pairs(n_arr, a_arr, ms, me, factor, maxbucket, 0, 1, False)
    del n_arr, a_arr, ms, me
    # a pkey occurring k>=2 times == pair sharing k distinct concordant N
    pk.sort()
    uniq, counts = np.unique(pk, return_counts=True)
    return uniq[counts >= 2], factor


def _judge_slice(args: tuple) -> dict:
    """Worker: decode a slice of pkeys, run the 3-stage pipeline, return counts."""
    from rational_distance.concordant.chain_closure_sieve import (
        STANDARD_MODULI,
        find_killer_modulus,
    )
    from rational_distance.concordant.fast_multi_n import exact_concordant_pair
    from rational_distance.concordant.safe_pair_sieve import gcd_aware_kills

    pkeys, factor = args
    coprime = noncoprime = dg = chain = surv = clos = 0
    surv_gcd: Counter[int] = Counter()
    hits: list[tuple[int, int, list[int]]] = []
    for pkey in pkeys:
        a = int(pkey) // factor
        b = int(pkey) % factor
        g = gcd(a, b)
        if g == 1:
            coprime += 1
        else:
            noncoprime += 1
        if gcd_aware_kills(a, b):
            dg += 1
            continue
        if find_killer_modulus(a, b, full_plane=True, moduli=STANDARD_MODULI) is not None:
            chain += 1
            continue
        s = exact_concordant_pair(a, b)
        surv += 1
        surv_gcd[g] += 1
        targets = {a + b, abs(a - b)}
        if any(
            (s[i] + s[j]) in targets or abs(s[i] - s[j]) in targets
            for i in range(len(s))
            for j in range(i + 1, len(s))
        ):
            clos += 1
            hits.append((a, b, s))
    return {
        "coprime": coprime, "noncoprime": noncoprime, "dg": dg, "chain": chain,
        "surv": surv, "clos": clos, "surv_gcd": surv_gcd, "hits": hits,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    _ = ap.add_argument("--max-hyp", type=int, default=1_000_000)
    _ = ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()
    max_hyp: int = args.max_hyp
    workers: int = args.workers

    t0 = time.perf_counter()
    pkeys, factor = multi_n_pkeys(max_hyp)
    t_gen = time.perf_counter() - t0
    total = int(pkeys.shape[0])

    chunks = np.array_split(pkeys, max(workers, 1))
    payload = [(c, factor) for c in chunks]
    if workers > 1:
        import multiprocessing as mp

        with mp.get_context("spawn").Pool(workers) as pool:
            parts = pool.map(_judge_slice, payload)
    else:
        parts = [_judge_slice(p) for p in payload]

    agg = {"coprime": 0, "noncoprime": 0, "dg": 0, "chain": 0, "surv": 0, "clos": 0}
    surv_gcd: Counter[int] = Counter()
    hits: list[tuple[int, int, list[int]]] = []
    for p in parts:
        for k in agg:
            agg[k] += p[k]
        surv_gcd.update(p["surv_gcd"])
        hits.extend(p["hits"])
    dt = time.perf_counter() - t0

    out = {
        "max_hyp": max_hyp,
        "workers": workers,
        "total_multi_n_pairs": total,
        "coprime_pairs": agg["coprime"],
        "noncoprime_pairs": agg["noncoprime"],
        "stage1_Dg_killed": agg["dg"],
        "stage2_chain_killed": agg["chain"],
        "stage3_gen_survivors": agg["surv"],
        "closures": agg["clos"],
        "survivor_gcd_dist": dict(sorted(surv_gcd.items())),
        "closure_hits": hits[:50],
        "gen_seconds": round(t_gen, 1),
        "total_seconds": round(dt, 1),
    }
    print(json.dumps({k: v for k, v in out.items() if k != "survivor_gcd_dist"}, indent=2))
    top = sorted(surv_gcd.items(), key=lambda x: -x[1])[:10]
    print(f"survivor gcd top-10: {top}  (strata: {len(surv_gcd)})")

    outdir = ROOT / "results/multi_n"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"full_scan_max{max_hyp}.json").write_text(json.dumps(out, indent=2))

    if agg["clos"]:
        print(f"\n*** {agg['clos']} CLOSURE HIT(S) — HARBORTH COUNTEREXAMPLE CANDIDATE(S) ***")
        for a, b, s in hits[:20]:
            print(f"    (A,B)=({a},{b}) gcd={gcd(a, b)} N={s}")
    else:
        print(f"\nNO closure up to max_hyp={max_hyp} (coprime + non-coprime), "
              f"{total} multi-N pairs decided.")


if __name__ == "__main__":
    main()
