"""wl099 — refined gcd-aware divisor D_g + sound gcd-aware closure sieve.

Verifies (on the 1,802 non-coprime multi-N pairs from wl056 and an independent
brute re-scan):
  1. SOUNDNESS: D_g = guaranteed_divisor(A,B) divides EVERY concordant N.
  2. KILLS: the O(1) D_g sieve (gcd_aware_kills) vs chain_closure mod-p^2,
     showing they are complementary (D_g catches pairs chain_closure misses).
  3. coprime g=1 reduces to D_g=12 (old safe_sieve).

Run: PYTHONPATH=src python scripts/multi_n/gcd_aware_sieve_audit.py
"""
from __future__ import annotations

import json
from collections import Counter
from math import gcd
from pathlib import Path

from rational_distance.concordant.chain_closure_sieve import find_killer_modulus
from rational_distance.concordant.fast_multi_n import exact_concordant_pair
from rational_distance.concordant.safe_pair_sieve import gcd_aware_kills, guaranteed_divisor

REPO = Path(__file__).resolve().parents[2]
JSONL = REPO / "results/multi_n/non_coprime_scan_max2000.jsonl"


def main() -> None:
    rows = [json.loads(line) for line in JSONL.read_text().splitlines() if line.strip()]
    print(f"loaded {len(rows)} non-coprime multi-N pairs (wl056, hyp<=2000)")

    # 1. soundness: D_g | every concordant N
    sviol = 0
    for r in rows:
        d = guaranteed_divisor(r["a"], r["b"])
        for n in exact_concordant_pair(r["a"], r["b"]):
            if n % d != 0:
                sviol += 1
    bviol = 0
    for a in range(2, 1200):
        for b in range(a + 1, 1200):
            if gcd(a, b) == 1:
                continue
            d = guaranteed_divisor(a, b)
            for n in exact_concordant_pair(a, b):
                if n % d != 0:
                    bviol += 1
    print(f"[soundness] D_g | N  file_violations={sviol}  brute_violations={bviol}")

    # 2. kills: D_g sieve vs chain_closure mod-p^2
    dg = chain = both = dg_only = chain_only = neither = 0
    by_d = Counter()
    for r in rows:
        a, b = r["a"], r["b"]
        dk = gcd_aware_kills(a, b)
        ck = find_killer_modulus(a, b, full_plane=True) is not None
        dg += dk
        chain += ck
        both += dk and ck
        dg_only += dk and not ck
        chain_only += ck and not dk
        neither += (not dk) and (not ck)
        if dk:
            by_d[guaranteed_divisor(a, b)] += 1
    print(f"[kills/{len(rows)}] D_g={dg}  chain={chain}  both={both}  "
          f"D_g_only={dg_only}  chain_only={chain_only}  survive_both={neither}")
    print(f"[D_g kills by divisor] {dict(sorted(by_d.items()))}")

    # 3. coprime reduction
    print(f"[coprime] D_g(3,4)={guaranteed_divisor(3,4)} D_g(7,17)={guaranteed_divisor(7,17)} "
          f"(expect 12);  D_g(gcd=2 pair 6,8)={guaranteed_divisor(6,8)} (expect 24)")


if __name__ == "__main__":
    main()
