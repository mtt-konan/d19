#!/usr/bin/env python3
"""Pattern hunt on hard_case (A, B) pairs.

Loads the proof_status DB, builds a feature matrix for every pair, then
compares the distribution between status=hard_case and status=no_solution.

Goals (in order of decreasing ambition):
1. Find a closed-form predicate `(A, B) -> bool` that is true on every
   hard_case but rarely on no_solution. If one exists, it gives us a
   no-effort obstruction candidate.
2. Find high-confidence statistical regularities: Mod-p residue
   imbalance, prime-divisor imbalance, etc.
3. Failing that, give a feature-importance ranking via random forest
   so we know which arithmetic invariants are at all predictive.

Outputs:
- ``results/pattern_hunt_summary.txt``  -- human-readable report
- ``results/pattern_hunt_features.parquet``  -- feature matrix (if pyarrow available, else CSV)
- ``results/pattern_hunt_chi2.jsonl``  -- per-feature chi-square / KS data
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import Counter
from math import gcd, isqrt, log
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))


def is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    s = isqrt(n)
    return s * s == n


def prime_factors(n: int) -> dict[int, int]:
    """Return {p: exponent} dict."""
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


def num_divisors(pf: dict[int, int]) -> int:
    n = 1
    for e in pf.values():
        n *= e + 1
    return n


def radical(pf: dict[int, int]) -> int:
    r = 1
    for p in pf:
        r *= p
    return r


def has_3mod4_prime(pf: dict[int, int]) -> int:
    """Return 1 if any prime factor is 3 mod 4 with odd exponent."""
    for p, e in pf.items():
        if p % 4 == 3 and e % 2 == 1:
            return 1
    return 0


def features_for_pair(A: int, B: int) -> dict[str, int | float]:
    """Build a numeric feature dict for one (A, B) pair."""
    pf_A = prime_factors(A)
    pf_B = prime_factors(B)
    g = gcd(A, B)
    AB = A * B
    s = A + B
    diff = B - A
    sq_sum = A * A + B * B
    pf_sq_sum = prime_factors(sq_sum)

    feats: dict[str, int | float] = {
        # raw magnitude
        "A": A,
        "B": B,
        "log_A": log(A),
        "log_B": log(B),
        "log_AB": log(AB),
        "log_A_plus_B": log(s),
        # gcd
        "gcd_AB": g,
        "is_coprime": int(g == 1),
        # parity / mod patterns of A
        "A_mod_2": A % 2,
        "A_mod_4": A % 4,
        "A_mod_8": A % 8,
        "A_mod_3": A % 3,
        "A_mod_5": A % 5,
        # parity / mod patterns of B
        "B_mod_2": B % 2,
        "B_mod_4": B % 4,
        "B_mod_8": B % 8,
        "B_mod_3": B % 3,
        "B_mod_5": B % 5,
        # joint mods
        "AplusB_mod_4": s % 4,
        "AplusB_mod_8": s % 8,
        "AplusB_mod_16": s % 16,
        "BminusA_mod_4": diff % 4,
        "BminusA_mod_8": diff % 8,
        "AB_mod_8": AB % 8,
        "AB_mod_24": AB % 24,
        # square-sum structure
        "A_sq_plus_B_sq": sq_sum,
        "log_sq_sum": log(sq_sum),
        "sq_sum_mod_4": sq_sum % 4,
        "sq_sum_mod_8": sq_sum % 8,
        "sq_sum_mod_16": sq_sum % 16,
        "sq_sum_has_3mod4_odd": has_3mod4_prime(pf_sq_sum),
        "sq_sum_n_distinct_primes": len(pf_sq_sum),
        # squarefree-ness
        "A_is_square": int(is_perfect_square(A)),
        "B_is_square": int(is_perfect_square(B)),
        "A_is_squarefree": int(all(e == 1 for e in pf_A.values())),
        "B_is_squarefree": int(all(e == 1 for e in pf_B.values())),
        # prime-divisor structure of A
        "A_omega": len(pf_A),
        "A_Omega": sum(pf_A.values()),
        "A_smallest_prime": min(pf_A) if pf_A else 0,
        "A_largest_prime": max(pf_A) if pf_A else 0,
        "A_n_divisors": num_divisors(pf_A),
        "A_has_3mod4_odd": has_3mod4_prime(pf_A),
        # prime-divisor structure of B
        "B_omega": len(pf_B),
        "B_Omega": sum(pf_B.values()),
        "B_smallest_prime": min(pf_B) if pf_B else 0,
        "B_largest_prime": max(pf_B) if pf_B else 0,
        "B_n_divisors": num_divisors(pf_B),
        "B_has_3mod4_odd": has_3mod4_prime(pf_B),
        # special chain patterns
        "A_eq_B_minus_A": int(A == diff),  # A = B - A i.e. B = 2A
        "B_div_A_int": int(A != 0 and B % A == 0),
        "ratio_B_over_A": B / A if A else 0.0,
    }
    return feats


def chi_square_test(
    counts_a: Counter, counts_b: Counter
) -> dict[str, object]:
    """Return chi-square statistic + p-value approximation for two
    Counters over the same key set."""
    keys = sorted(set(counts_a) | set(counts_b))
    n_a = sum(counts_a.values())
    n_b = sum(counts_b.values())
    n_total = n_a + n_b
    if n_total == 0:
        return {"chi2": 0.0, "df": 0, "p_value_upper_bound": 1.0}
    chi2 = 0.0
    for k in keys:
        oa = counts_a.get(k, 0)
        ob = counts_b.get(k, 0)
        row_total = oa + ob
        ea = row_total * n_a / n_total
        eb = row_total * n_b / n_total
        if ea > 0:
            chi2 += (oa - ea) ** 2 / ea
        if eb > 0:
            chi2 += (ob - eb) ** 2 / eb
    df = max(0, len(keys) - 1)
    # crude p-value upper bound via Markov
    p_upper = min(1.0, df / chi2) if chi2 > 0 else 1.0
    return {
        "chi2": chi2,
        "df": df,
        "p_value_upper_bound": p_upper,
        "n_classes": len(keys),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default="results/proof_status.db")
    ap.add_argument(
        "--summary-out", default="results/pattern_hunt_summary.txt"
    )
    ap.add_argument(
        "--chi2-out", default="results/pattern_hunt_chi2.jsonl"
    )
    ap.add_argument(
        "--features-out", default="results/pattern_hunt_features.csv"
    )
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT A, B, status, rank_lower, rank_upper, concordant_n_count, "
        "chain_compatible_count FROM pair_proof_status"
    ).fetchall()
    print(f"Loaded {len(rows)} pairs from {args.db}")

    by_status: dict[str, list[dict]] = {}
    for r in rows:
        by_status.setdefault(r["status"], []).append(dict(r))
    for k, v in by_status.items():
        print(f"  {k:18}: {len(v):>6}")

    if "hard_case" not in by_status or "no_solution" not in by_status:
        print("ERROR: need both 'hard_case' and 'no_solution' in db")
        return 1

    # Build feature matrices
    print("\nBuilding feature matrices...")
    feats_hard = [features_for_pair(r["A"], r["B"]) for r in by_status["hard_case"]]
    feats_easy = [features_for_pair(r["A"], r["B"]) for r in by_status["no_solution"]]

    n_hard = len(feats_hard)
    n_easy = len(feats_easy)
    print(f"  hard:        {n_hard}")
    print(f"  no_solution: {n_easy}")

    # Pick categorical/discrete features for chi-square
    discrete_feats = [
        k for k in feats_hard[0]
        if k.startswith("A_mod_") or k.startswith("B_mod_") or k.startswith("AplusB_mod_")
        or k.startswith("BminusA_mod_") or k.startswith("AB_mod_") or k.startswith("sq_sum_mod_")
        or k in {
            "is_coprime", "A_is_square", "B_is_square",
            "A_is_squarefree", "B_is_squarefree", "A_has_3mod4_odd", "B_has_3mod4_odd",
            "sq_sum_has_3mod4_odd", "A_omega", "B_omega", "A_Omega", "B_Omega",
            "B_div_A_int", "A_eq_B_minus_A", "gcd_AB",
        }
    ]

    chi2_results: list[dict] = []
    for fname in discrete_feats:
        ch = Counter(int(f[fname]) for f in feats_hard)
        ce = Counter(int(f[fname]) for f in feats_easy)
        result = chi_square_test(ch, ce)
        result["feature"] = fname
        result["dist_hard"] = {str(k): v / n_hard for k, v in sorted(ch.items())}
        result["dist_easy"] = {str(k): v / n_easy for k, v in sorted(ce.items())}
        chi2_results.append(result)

    chi2_results.sort(key=lambda r: -r["chi2"])

    # Save chi-square results
    Path(args.chi2_out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.chi2_out, "w") as fh:
        for r in chi2_results:
            fh.write(json.dumps(r) + "\n")

    # Quick summary report
    summary_lines: list[str] = []
    summary_lines.append("=" * 72)
    summary_lines.append(f"Pattern hunt on {args.db}")
    summary_lines.append(f"  hard_case   : {n_hard:>6}")
    summary_lines.append(f"  no_solution : {n_easy:>6}")
    summary_lines.append("=" * 72)
    summary_lines.append("")
    summary_lines.append("Top features by chi-square statistic")
    summary_lines.append("(higher chi2 = more difference between hard_case and no_solution)")
    summary_lines.append("")
    summary_lines.append(
        f"  {'feature':<30} {'chi2':>10} {'df':>4} "
        f"{'top_class_hard':>20} {'top_class_easy':>20}"
    )
    summary_lines.append("  " + "-" * 90)
    for r in chi2_results[:30]:
        top_h = max(r["dist_hard"].items(), key=lambda x: x[1]) if r["dist_hard"] else ("-", 0)
        top_e = max(r["dist_easy"].items(), key=lambda x: x[1]) if r["dist_easy"] else ("-", 0)
        summary_lines.append(
            f"  {r['feature']:<30} {r['chi2']:>10.2f} {r['df']:>4d} "
            f"{top_h[0]:>10}={top_h[1]:>6.1%} {top_e[0]:>10}={top_e[1]:>6.1%}"
        )

    summary_lines.append("")
    summary_lines.append("=" * 72)
    summary_lines.append("Detailed top-10 features")
    summary_lines.append("=" * 72)
    for r in chi2_results[:10]:
        summary_lines.append("")
        summary_lines.append(
            f"## {r['feature']}  (chi2={r['chi2']:.2f}, df={r['df']}, classes={r['n_classes']})"
        )
        summary_lines.append("")
        all_keys = sorted(
            set(r["dist_hard"]) | set(r["dist_easy"]),
            key=lambda k: -(r["dist_hard"].get(k, 0) - r["dist_easy"].get(k, 0)),
        )
        summary_lines.append(f"  {'class':>10} {'hard':>10} {'easy':>10} {'h-e':>10}")
        for k in all_keys:
            ph = r["dist_hard"].get(k, 0)
            pe = r["dist_easy"].get(k, 0)
            diff = ph - pe
            summary_lines.append(
                f"  {k:>10} {ph:>9.2%} {pe:>9.2%} {diff:>+9.2%}"
            )

    summary_text = "\n".join(summary_lines)
    Path(args.summary_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.summary_out).write_text(summary_text)
    print()
    print(summary_text)
    print()
    print(f"Wrote chi2 details to {args.chi2_out}")
    print(f"Wrote human-readable summary to {args.summary_out}")

    # Also save the feature matrix as CSV for downstream ML
    Path(args.features_out).parent.mkdir(parents=True, exist_ok=True)
    feat_keys = list(feats_hard[0].keys())
    with open(args.features_out, "w") as fh:
        fh.write("status," + ",".join(feat_keys) + "\n")
        for f in feats_hard:
            fh.write("hard_case," + ",".join(str(f[k]) for k in feat_keys) + "\n")
        for f in feats_easy:
            fh.write("no_solution," + ",".join(str(f[k]) for k in feat_keys) + "\n")
    print(f"Wrote feature matrix to {args.features_out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
