"""Empirical verification of the gcd-aware mod-12 theorem (MATH §8.5.2 / wl098).

Law: for g = gcd(A, B) and any concordant N of (A, B),
    3 | N   whenever 3 ∤ g
    4 | N   whenever 4 ∤ g
(so 12 | N when gcd(A, B) is coprime to 12; g = 1 is the wl097 coprime case).

Also confirms the non-coprime deciders need no rewrite:
  - exact_concordant_pair reproduces the wl056 scan's complete sets (0 mismatch),
  - actual-pair GEN-CLOSURE on the complete concordant set: 0 closure hits,
  - chain_closure mod-p^2 (full_plane, sound) kills the bulk.

Run: PYTHONPATH=src python scripts/multi_n/gcd_aware_mod12_check.py
"""
from __future__ import annotations

import json
from math import gcd
from pathlib import Path

from rational_distance.concordant.chain_closure_sieve import find_killer_modulus
from rational_distance.concordant.fast_multi_n import exact_concordant_pair

REPO = Path(__file__).resolve().parents[2]
JSONL = REPO / "results/multi_n/non_coprime_scan_max2000.jsonl"


def law_holds(g: int, n: int) -> bool:
    if g % 3 != 0 and n % 3 != 0:
        return False
    return not (g % 4 != 0 and n % 4 != 0)


def main() -> None:
    rows = [json.loads(line) for line in JSONL.read_text().splitlines() if line.strip()]
    print(f"loaded {len(rows)} non-coprime multi-N pairs (wl056, hyp<=2000)")

    # (1) per-N assertion of the gcd-aware law on the scan file
    viol = nN = 0
    mismatch = 0
    gen_hits = 0
    chain_killed = 0
    for r in rows:
        a, b = r["a"], r["b"]
        g = gcd(a, b)
        S = exact_concordant_pair(a, b)
        if sorted(r["concordant_N"]) != S:
            mismatch += 1
        for n in S:
            nN += 1
            if not law_holds(g, n):
                viol += 1
        # actual GEN-CLOSURE on complete set
        targets = {a + b, abs(a - b)}
        hit = any(
            (S[i] + S[j]) in targets or abs(S[i] - S[j]) in targets
            for i in range(len(S))
            for j in range(i + 1, len(S))
        )
        gen_hits += hit
        if find_killer_modulus(a, b, full_plane=True) is not None:
            chain_killed += 1

    print(f"(1) wl056 file: {nN} N-values, gcd-aware law violations = {viol}")
    print(f"    exact_concordant vs scan mismatch = {mismatch}")
    print(f"    actual GEN-CLOSURE closure hits    = {gen_hits}")
    print(f"    chain_closure mod-p^2 sound-kills  = {chain_killed} / {len(rows)}")

    # (2) independent brute re-scan over ALL non-coprime (A,B), A<B<=BOUND
    bound = 1200
    viol2 = nN2 = npairs = 0
    for a in range(2, bound + 1):
        for b in range(a + 1, bound + 1):
            g = gcd(a, b)
            if g == 1:
                continue
            S = exact_concordant_pair(a, b)
            if not S:
                continue
            npairs += 1
            for n in S:
                nN2 += 1
                if not law_holds(g, n):
                    viol2 += 1
    print(
        f"(2) brute non-coprime A<B<={bound}: {npairs} pairs, "
        f"{nN2} N-values, violations = {viol2}"
    )
    print("LAW CONFIRMED" if viol == 0 and viol2 == 0 else "LAW VIOLATED")


if __name__ == "__main__":
    main()
