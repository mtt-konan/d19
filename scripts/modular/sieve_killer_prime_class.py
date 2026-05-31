"""F.4 — killer-prime class analysis for the chain-closure mod-p² sieve.

Compares d19's chain-closure sieve to Peschmann (arXiv:2604.09328) §7(3)'s
"blocker prime" phenomenon.

Peschmann's blocker is a prime ``p`` where ``v_p(f1 f2)`` is *odd*, preventing
``f1 f2`` from being a perfect square. By Remark 6.5 (each ``f_i`` is a norm in
``Z[i]``), primes ``p ≡ 3 (mod 4)`` always divide ``f_i`` to an *even* power, so
they can **never** be blockers — empirically the blocker is always ``p = 2`` or
``p ≡ 1 (mod 4)``.

d19's chain-closure sieve is a different mechanism: for a reduced ``(A, B)`` it
kills the pair when ``T(A,B,M) ∩ ((A+B) − T(A,B,M)) = ∅`` (the apex closure
``b = A+B−N`` reflection), where
``T = {n : n²+A², n²+B² both squares mod M}``.

This script measures, over reduced pairs surviving ``safe_sieve``:
  * how many are killed, and the *reason* (pure ``T = ∅`` vs reflection-empty);
  * the residue class mod 4 of the *smallest* killer prime.

Result (max_hyp=2000): 100% of kills are reflection-empty (never pure ``T=∅``),
and ~90% use a prime ``p ≡ 3 (mod 4)`` (p=3 alone ~88%) — the exact opposite of
Peschmann's blocker, because the closure reflection is not a pure Gaussian-norm
square condition. See worklog 091.

Run:
    PYTHONPATH=src uv run python scripts/modular/sieve_killer_prime_class.py --max-hyp 2000
"""

from __future__ import annotations

import argparse
import json
from collections import Counter

from rational_distance.concordant.chain_closure_sieve import (
    EXTENDED_MODULI,
    allowed_n_mod,
)
from rational_distance.concordant.pairs import generate_ab_pairs
from rational_distance.concordant.safe_pair_sieve import allow_reduced_pair

# prime square modulus -> base prime
_MOD_PRIME = {
    p * p: p
    for p in (
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        47,
        53,
        59,
        61,
        67,
        71,
        73,
        79,
        83,
        89,
        97,
    )
}


def kill_reason(a: int, b: int, M: int) -> str | None:
    """Return why modulus ``M`` kills ``(a, b)``, or ``None`` if it doesn't.

    ``"T_empty"``           — no residue satisfies both concordant squares;
    ``"reflection_empty"``  — concordant residues exist but the apex closure
                              reflection ``T ∩ ((A+B) − T)`` is empty.
    """
    T = allowed_n_mod(a, b, M)
    if not T:
        return "T_empty"
    ab = (a + b) % M
    if not (T & frozenset((ab - n) % M for n in T)):
        return "reflection_empty"
    return None


def analyze(max_hyp: int) -> dict:
    pairs = [(a, b) for (a, b) in generate_ab_pairs(max_hyp) if allow_reduced_pair(a, b)]
    reason_total: Counter[str] = Counter()
    class_total: Counter[int] = Counter()
    prime_total: Counter[int] = Counter()
    survivors = 0
    for a, b in pairs:
        for M in EXTENDED_MODULI:  # primes 3..97
            r = kill_reason(a, b, M)
            if r is not None:
                p = _MOD_PRIME[M]
                reason_total[r] += 1
                class_total[p % 4] += 1
                prime_total[p] += 1
                break
        else:
            survivors += 1
    killed = sum(reason_total.values())
    p3 = sum(v for p, v in prime_total.items() if p % 4 == 3)
    return {
        "max_hyp": max_hyp,
        "reduced_pairs_after_safe_sieve": len(pairs),
        "killed": killed,
        "survivors": survivors,
        "kill_reason": dict(reason_total),
        "smallest_killer_prime_mod4": dict(sorted(class_total.items())),
        "smallest_killer_prime": dict(sorted(prime_total.items())),
        "killers_p_equiv_3_mod4": p3,
        "killers_p_equiv_3_mod4_frac": (p3 / killed) if killed else 0.0,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-hyp", type=int, default=2000)
    args = ap.parse_args()
    print(json.dumps(analyze(args.max_hyp), indent=2))


if __name__ == "__main__":
    main()
