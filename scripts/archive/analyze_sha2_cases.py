#!/usr/bin/env python3
"""Analyze the 156 sha2=2 hard_case pairs found in batch_sha2_scan_v2.

Compares feature distributions of sha2>=2 vs sha2=0 hard_case to
identify what makes Sha[E][2] non-trivial. Combines results with
the rank stratification and squarefree analysis from worklog 038.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


def prime_factors(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    if n <= 1:
        return out
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def is_squarefree(n: int) -> bool:
    return all(e == 1 for e in prime_factors(n).values())


def max_exp(n: int) -> int:
    pf = prime_factors(n)
    return max(pf.values()) if pf else 0


def num_distinct_primes(n: int) -> int:
    return len(prime_factors(n))


def feature_stats(rows: list[tuple[int, int]], name: str) -> dict[str, float]:
    n = len(rows)
    if n == 0:
        return {}
    print(f"\n--- {name} (n={n}) ---")

    # Squarefree
    a_sf = sum(1 for a, _ in rows if is_squarefree(a))
    b_sf = sum(1 for _, b in rows if is_squarefree(b))
    both_sf = sum(1 for a, b in rows if is_squarefree(a) and is_squarefree(b))
    neither = sum(
        1 for a, b in rows if not is_squarefree(a) and not is_squarefree(b)
    )

    # mod 8 (mod 3/4 are subsumed by mod 8 + mod 24 view, kept narrow)
    a_mod8 = Counter(a % 8 for a, _ in rows)
    b_mod8 = Counter(b % 8 for _, b in rows)

    # Max prime power exponent
    me_a = Counter(max_exp(a) for a, _ in rows)
    me_b = Counter(max_exp(b) for _, b in rows)

    # Number of distinct primes
    np_a = Counter(num_distinct_primes(a) for a, _ in rows)
    np_b = Counter(num_distinct_primes(b) for _, b in rows)

    # parity
    a_odd = sum(1 for a, _ in rows if a % 2 == 1)
    b_odd = sum(1 for _, b in rows if b % 2 == 1)

    # 3 | A, 3 | B
    a_3 = sum(1 for a, _ in rows if a % 3 == 0)
    b_3 = sum(1 for _, b in rows if b % 3 == 0)

    print(f"  A squarefree:        {a_sf:>4} ({a_sf/n:>6.2%})")
    print(f"  B squarefree:        {b_sf:>4} ({b_sf/n:>6.2%})")
    print(f"  both squarefree:     {both_sf:>4} ({both_sf/n:>6.2%})")
    print(f"  neither squarefree:  {neither:>4} ({neither/n:>6.2%})")
    print(f"  A odd:               {a_odd:>4} ({a_odd/n:>6.2%})")
    print(f"  B odd:               {b_odd:>4} ({b_odd/n:>6.2%})")
    print(f"  3|A:                 {a_3:>4} ({a_3/n:>6.2%})")
    print(f"  3|B:                 {b_3:>4} ({b_3/n:>6.2%})")

    print(f"  A mod 8: {dict(sorted(a_mod8.items()))}")
    print(f"  B mod 8: {dict(sorted(b_mod8.items()))}")
    print(f"  max-exp(A): {dict(sorted(me_a.items()))}")
    print(f"  max-exp(B): {dict(sorted(me_b.items()))}")
    print(f"  num-primes(A): {dict(sorted(np_a.items()))}")
    print(f"  num-primes(B): {dict(sorted(np_b.items()))}")

    return {
        "n": n,
        "a_sf_pct": a_sf / n,
        "b_sf_pct": b_sf / n,
        "both_sf_pct": both_sf / n,
        "neither_sf_pct": neither / n,
        "a_odd_pct": a_odd / n,
        "b_odd_pct": b_odd / n,
        "a3_pct": a_3 / n,
        "b3_pct": b_3 / n,
    }


def chi_compare_2x2(sha2_pos: int, sha2_neg: int,
                    n_pos: int, n_neg: int) -> tuple[float, float]:
    """Yates-corrected chi^2 for 2x2 contingency."""
    a, b = sha2_pos, n_pos - sha2_pos
    c, d = sha2_neg, n_neg - sha2_neg
    n = a + b + c + d
    if n == 0:
        return 0.0, 1.0
    expected = [
        (a + b) * (a + c) / n, (a + b) * (b + d) / n,
        (c + d) * (a + c) / n, (c + d) * (b + d) / n,
    ]
    obs = [a, b, c, d]
    if any(e <= 0 for e in expected):
        return 0.0, 1.0
    chi2 = sum((abs(o - e) - 0.5) ** 2 / e for o, e in zip(obs, expected))
    # Survival of chi^2 with df=1 via approximation
    # For df=1, p = erfc(sqrt(chi2/2))
    p = math.erfc(math.sqrt(chi2 / 2)) if chi2 >= 0 else 1.0
    return chi2, p


def main() -> int:
    jsonl_path = ROOT / "results" / "sha2_scan_hard_cases.jsonl"
    if not jsonl_path.exists():
        print(f"ERROR: {jsonl_path} not found.")
        return 1

    sha2_pos: list[tuple[int, int, int, int]] = []  # (A, B, rank_lo, sha2_lo)
    sha2_zero: list[tuple[int, int, int, int]] = []
    timeouts: list[tuple[int, int]] = []
    with open(jsonl_path, encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            A, B = row["A"], row["B"]
            if row.get("error") == "TIMEOUT":
                timeouts.append((A, B))
                continue
            if row.get("sha2_lower") is None:
                continue
            r_lo = row.get("rank_lower") or 0
            s_lo = row["sha2_lower"]
            entry = (A, B, r_lo, s_lo)
            if s_lo > 0:
                sha2_pos.append(entry)
            else:
                sha2_zero.append(entry)

    print("=" * 72)
    print(f"sha2_lower >= 2 cases: {len(sha2_pos)}")
    print(f"sha2_lower == 0 cases: {len(sha2_zero)}")
    print(f"TIMEOUT pairs: {len(timeouts)}")
    print("=" * 72)

    # Stratify by rank
    rank_pos = Counter(r for *_, r, _ in sha2_pos)
    rank_zero = Counter(r for *_, r, _ in sha2_zero)
    print("\n--- rank stratification ---")
    print(f"  sha2>=2 by rank: {dict(sorted(rank_pos.items()))}")
    print(f"  sha2==0 by rank: {dict(sorted(rank_zero.items()))}")

    # Feature stats
    pos_pairs = [(a, b) for a, b, *_ in sha2_pos]
    zero_pairs = [(a, b) for a, b, *_ in sha2_zero]
    _ = feature_stats(pos_pairs, "sha2>=2")
    _ = feature_stats(zero_pairs, "sha2==0")

    # 2x2 chi-square for each binary feature
    print("\n" + "=" * 72)
    print("Yates-corrected 2x2 chi^2 (sha2>=2 vs sha2==0)")
    print("=" * 72)
    n_pos, n_zero = len(pos_pairs), len(zero_pairs)
    binary_features = [
        ("A_squarefree", lambda a, b: is_squarefree(a)),
        ("B_squarefree", lambda a, b: is_squarefree(b)),
        ("both_squarefree", lambda a, b: is_squarefree(a) and is_squarefree(b)),
        ("neither_squarefree",
         lambda a, b: not is_squarefree(a) and not is_squarefree(b)),
        ("A_odd", lambda a, b: a % 2 == 1),
        ("B_odd", lambda a, b: b % 2 == 1),
        ("3_div_A", lambda a, b: a % 3 == 0),
        ("3_div_B", lambda a, b: b % 3 == 0),
        ("3_div_AB", lambda a, b: (a * b) % 3 == 0),
        ("A_mod_4_eq_3", lambda a, b: a % 4 == 3),
        ("B_mod_4_eq_3", lambda a, b: b % 4 == 3),
        ("A_mod_8_eq_1", lambda a, b: a % 8 == 1),
        ("max_exp_A_ge_2", lambda a, b: max_exp(a) >= 2),
        ("max_exp_B_ge_2", lambda a, b: max_exp(b) >= 2),
        ("max_exp_A_ge_3", lambda a, b: max_exp(a) >= 3),
        ("max_exp_B_ge_3", lambda a, b: max_exp(b) >= 3),
        ("max_exp_A_ge_4", lambda a, b: max_exp(a) >= 4),
        ("max_exp_B_ge_4", lambda a, b: max_exp(b) >= 4),
    ]
    print(
        f"{'feature':<25} {'pos%':>8} {'zero%':>8} "
        f"{'chi^2':>10} {'p':>10} {'sig':>5}"
    )
    print("-" * 72)
    rows_chi: list[tuple[str, float, float, float, float]] = []
    for fname, fn in binary_features:
        c_pos = sum(1 for a, b in pos_pairs if fn(a, b))
        c_zero = sum(1 for a, b in zero_pairs if fn(a, b))
        chi2, p = chi_compare_2x2(c_pos, c_zero, n_pos, n_zero)
        rows_chi.append(
            (fname, c_pos / max(n_pos, 1), c_zero / max(n_zero, 1), chi2, p)
        )

    # sort by chi^2
    rows_chi.sort(key=lambda r: -r[3])
    for fname, p_pos, p_zero, chi2, p in rows_chi:
        sig = (
            "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        )
        print(f"{fname:<25} {p_pos:>7.2%} {p_zero:>7.2%}  "
              f"{chi2:>9.2f} {p:>10.2e} {sig:>5}")

    print()
    print("=" * 72)
    print("Top sha2>=2 cases (sorted by max(A, B))")
    print("=" * 72)
    sha2_pos.sort(key=lambda x: max(x[0], x[1]))
    for a_val, b_val, r_lo, _s_lo in sha2_pos[:20]:
        pf_a = prime_factors(a_val)
        pf_b = prime_factors(b_val)
        print(f"  ({a_val:>6}, {b_val:>6})  rank_lo={r_lo}  "
              f"A={dict(pf_a)}  B={dict(pf_b)}")

    # TIMEOUT pairs
    print("\n" + "=" * 72)
    print(f"TIMEOUT pairs ({len(timeouts)})")
    print("=" * 72)
    for a_val, b_val in timeouts:
        pf_a = prime_factors(a_val)
        pf_b = prime_factors(b_val)
        print(f"  ({a_val:>6}, {b_val:>6})  A={dict(pf_a)}  B={dict(pf_b)}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
