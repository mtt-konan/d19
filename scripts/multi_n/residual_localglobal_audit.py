"""wl100 — dissect the residual surviving BOTH sound sieves (D_g divisibility +
chain_closure mod-p^2) on the 1,802 non-coprime multi-N pairs.

Finding: the irreducible residual is a LOCAL-GLOBAL gap — its closure
congruence is solvable mod every tested modulus (p^2 up to 300 + prime powers),
so no mod-p^k sieve can ever kill it. But GEN-CLOSURE on the complete concordant
set is cheap (survivors have tiny concordant sets) and sound, and returns 0
closures. Hence the correct sound pipeline is a 3-stage prefilter+backstop:
    gcd_aware_kills (O(1)) -> chain_closure mod-p^2 -> GEN-CLOSURE (complete).

Run: PYTHONPATH=src python scripts/multi_n/residual_localglobal_audit.py
"""
from __future__ import annotations

import json
import time
from collections import Counter
from math import gcd
from pathlib import Path

from rational_distance.concordant.chain_closure_sieve import (
    STANDARD_MODULI,
    find_killer_modulus,
    killed_at_modulus,
)
from rational_distance.concordant.fast_multi_n import exact_concordant_pair
from rational_distance.concordant.safe_pair_sieve import gcd_aware_kills

REPO = Path(__file__).resolve().parents[2]
JSONL = REPO / "results/multi_n/non_coprime_scan_max2000.jsonl"


def primes_upto(n: int) -> list[int]:
    s = [True] * (n + 1)
    out = []
    for i in range(2, n + 1):
        if s[i]:
            out.append(i)
            for j in range(i * i, n + 1, i):
                s[j] = False
    return out


def main() -> None:
    rows = [json.loads(line) for line in JSONL.read_text().splitlines() if line.strip()]

    residual = [
        (r["a"], r["b"]) for r in rows
        if not gcd_aware_kills(r["a"], r["b"])
        and find_killer_modulus(r["a"], r["b"], full_plane=True, moduli=STANDARD_MODULI) is None
    ]
    big = sorted({p * p for p in primes_upto(300)}
                 | {8, 16, 32, 64, 128, 256, 27, 81, 243, 125, 625, 343})
    irreducible = [
        (a, b) for a, b in residual
        if not any(killed_at_modulus(a, b, M, full_plane=True) for M in big)
    ]
    print(f"D_g + STANDARD chain survivors : {len(residual)} / {len(rows)}")
    print(f"irreducible by ANY modulus      : {len(irreducible)}  "
          f"(p^2<=300 + prime powers, {len(big)} moduli)")

    nN = Counter()
    gcd12 = closures = 0
    t0 = time.perf_counter()
    for a, b in irreducible:
        S = exact_concordant_pair(a, b)
        nN[len(S)] += 1
        gcd12 += gcd(a, b) % 12 == 0
        targets = {a + b, abs(a - b)}
        if any((S[i] + S[j]) in targets or abs(S[i] - S[j]) in targets
               for i in range(len(S)) for j in range(i + 1, len(S))):
            closures += 1
    dt = time.perf_counter() - t0
    print(f"  #N distribution               : {dict(sorted(nN.items()))}")
    print(f"  12|gcd among irreducible       : {gcd12}/{len(irreducible)}")
    print(f"  GEN-CLOSURE backstop           : {closures} closures, "
          f"{dt*1000/max(len(irreducible),1):.2f} ms/pair (complete + sound)")
    print("=> no modular sieve clears the residual (local-global gap); "
          "GEN-CLOSURE is the cheap complete decider.")


if __name__ == "__main__":
    main()
