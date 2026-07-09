#!/usr/bin/env python3
"""Empirical study of the four-hypotenuse identities (CHAIN_STRUCTURE_IDEAS §2).

Given complete rectangular 4-chains (a, b, c, d) with all four Pythagorean
edges closed (h_1, h_2, h_3, h_4 rational/integer), we test:

  Identity A (no condition):
      h_1^2 + h_3^2 == h_2^2 + h_4^2 == a^2 + b^2 + c^2 + d^2

  Identity B (square only, a+c == b+d):
      h_1^2 - h_2^2 == (a-c) S
      h_3^2 - h_4^2 == (c-a) S

  Identity C (no condition needed -- (a+c)(b+d) form):
      (h_1 h_3)^2 - (h_2 h_4)^2 == (d-b)(a-c)(a+c)(b+d)
      Equivalently:
          (h_1 h_3 - h_2 h_4)(h_1 h_3 + h_2 h_4) == (d-b)(a-c)(a+c)(b+d)

We then study the prime-factor distribution mod 4 of the LHS factors
vs. the RHS factors, looking for the blocker-prime phenomenon described
in IDEAS §2.4.

Usage:
    uv run python scripts/analyze_hypotenuse_identity.py --max-val 200
    uv run python scripts/analyze_hypotenuse_identity.py --max-val 500 --out results/hyp_identity.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rational_distance._legacy.search_chain import find_chains  # noqa: E402

try:
    from sympy import factorint  # type: ignore[import]
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "sympy is required.  Install via 'uv pip install sympy'."
    ) from exc


def mod4_class(p: int) -> str:
    """Classify a prime by its residue mod 4 (or '2' for the prime 2)."""
    if p == 2:
        return "2"
    if p % 4 == 1:
        return "1mod4"
    if p % 4 == 3:
        return "3mod4"
    return "other"


def factor_with_classes(n: int) -> tuple[dict[int, int], Counter]:
    """Factor an integer and return (factor map, mod-4 class counter).

    Multiplicities are summed when accumulating mod-4 classes.
    """
    if n == 0:
        return {}, Counter()
    n = abs(n)
    factors = factorint(n)
    classes: Counter = Counter()
    for p, mult in factors.items():
        classes[mod4_class(p)] += mult
    return factors, classes


def analyze_chain(r) -> dict:
    """Analyze a single ChainResult.  Returns a JSON-friendly dict."""
    a, b, c, d = r.a, r.b, r.c, r.d
    h1, h2, h3, h4 = r.x1, r.x2, r.x3, r.x4

    # --- Identity A ---------------------------------------------------------
    sum_sq = a * a + b * b + c * c + d * d
    A_ok = (h1 * h1 + h3 * h3 == sum_sq) and (h2 * h2 + h4 * h4 == sum_sq)

    # --- Identity B (square only) ------------------------------------------
    S = a + c if (a + c) == (b + d) else None
    if S is not None:
        B_ok = (h1 * h1 - h2 * h2 == (a - c) * S) and (
            h3 * h3 - h4 * h4 == (c - a) * S
        )
    else:
        B_ok = None  # not applicable

    # --- Identity C (general form, no square required) ---------------------
    lhs = h1 * h3 * h1 * h3 - h2 * h4 * h2 * h4
    rhs = (d - b) * (a - c) * (a + c) * (b + d)
    C_ok = lhs == rhs

    # --- Factor decomposition for blocker-prime analysis -------------------
    # Left factors: (h1 h3 - h2 h4), (h1 h3 + h2 h4)
    L_minus = h1 * h3 - h2 * h4
    L_plus = h1 * h3 + h2 * h4
    # Right factors: (d-b), (a-c), (a+c), (b+d)
    R_db = d - b
    R_ac = a - c
    R_apc = a + c
    R_bpd = b + d

    factors_left_minus, classes_left_minus = factor_with_classes(L_minus)
    factors_left_plus, classes_left_plus = factor_with_classes(L_plus)
    factors_R_db, classes_R_db = factor_with_classes(R_db)
    factors_R_ac, classes_R_ac = factor_with_classes(R_ac)
    factors_R_apc, classes_R_apc = factor_with_classes(R_apc)
    factors_R_bpd, classes_R_bpd = factor_with_classes(R_bpd)

    classes_left_total = classes_left_minus + classes_left_plus
    classes_right_total = (
        classes_R_db + classes_R_ac + classes_R_apc + classes_R_bpd
    )

    # Each h_i has only odd primes ≡ 1 (mod 4).  Verify.
    h_classes_check = Counter()
    for h in (h1, h2, h3, h4):
        _, hc = factor_with_classes(h)
        h_classes_check += hc
    h_violation = h_classes_check.get("3mod4", 0)

    return {
        "a": a, "b": b, "c": c, "d": d,
        "h1": h1, "h2": h2, "h3": h3, "h4": h4,
        "square_ok": r.square_ok,
        "S": S,
        "identity_A_ok": A_ok,
        "identity_B_ok": B_ok,
        "identity_C_ok": C_ok,
        "L_minus": L_minus,
        "L_plus": L_plus,
        "R_db": R_db, "R_ac": R_ac, "R_apc": R_apc, "R_bpd": R_bpd,
        "factors_left_minus": {str(k): v for k, v in factors_left_minus.items()},
        "factors_left_plus": {str(k): v for k, v in factors_left_plus.items()},
        "factors_R_db": {str(k): v for k, v in factors_R_db.items()},
        "factors_R_ac": {str(k): v for k, v in factors_R_ac.items()},
        "factors_R_apc": {str(k): v for k, v in factors_R_apc.items()},
        "factors_R_bpd": {str(k): v for k, v in factors_R_bpd.items()},
        "classes_left_total": dict(classes_left_total),
        "classes_right_total": dict(classes_right_total),
        "h_3mod4_violation": h_violation,
    }


def summarize(rows: list[dict]) -> None:
    """Print human-friendly aggregate statistics."""
    n = len(rows)
    if n == 0:
        print("No chains analyzed.")
        return

    # Identity verification
    A_pass = sum(1 for r in rows if r["identity_A_ok"])
    C_pass = sum(1 for r in rows if r["identity_C_ok"])
    B_applicable = [r for r in rows if r["identity_B_ok"] is not None]
    B_pass = sum(1 for r in B_applicable if r["identity_B_ok"])

    print()
    print("=" * 72)
    print(f"Chains analyzed: {n}")
    print(f"Identity A pass:  {A_pass}/{n}  ({100*A_pass/n:.1f}%)")
    print(f"Identity C pass:  {C_pass}/{n}  ({100*C_pass/n:.1f}%)")
    if B_applicable:
        print(
            f"Identity B pass:  {B_pass}/{len(B_applicable)} "
            f"(applicable when a+c=b+d, n={len(B_applicable)})"
        )
    else:
        print("Identity B: 0 chains satisfy a+c=b+d (no applicable rows)")

    # Sanity: every h_i should have only prime factors ≡ 1 (mod 4) (plus 2)
    h_violations = sum(1 for r in rows if r["h_3mod4_violation"] > 0)
    print(f"h_i prime-class sanity (no 3 mod 4): "
          f"{n - h_violations}/{n} clean")

    # Aggregate mod-4 classes
    L_total = Counter()
    R_total = Counter()
    for r in rows:
        L_total.update(r["classes_left_total"])
        R_total.update(r["classes_right_total"])

    print()
    print("=" * 72)
    print("Aggregate mod-4 prime-multiplicity counts (sum over all chains):")
    print("-" * 72)
    print(f"{'class':<8}  {'LHS (h1h3 - / + h2h4)':>22}  "
          f"{'RHS ((d-b)(a-c)(a+c)(b+d))':>30}")
    for cls in ("2", "1mod4", "3mod4"):
        L = L_total.get(cls, 0)
        R = R_total.get(cls, 0)
        print(f"{cls:<8}  {L:>22}  {R:>30}")

    # Per-factor distinct-prime counts (multiplicity-1)
    print()
    print("=" * 72)
    print("Per-RHS-factor distinct-prime mod-4 distribution:")
    print("(counts how many distinct primes of each class appear in each "
          "RHS factor, summed over chains)")
    print("-" * 72)
    print(f"{'factor':<10}  {'2':>6}  {'1mod4':>8}  {'3mod4':>8}")
    for key, label in (
        ("R_db", "(d-b)"), ("R_ac", "(a-c)"),
        ("R_apc", "(a+c)"), ("R_bpd", "(b+d)"),
    ):
        c2 = c1 = c3 = 0
        for r in rows:
            for p_str in r[f"factors_{key}"]:
                p = int(p_str)
                cls = mod4_class(p)
                if cls == "2":
                    c2 += 1
                elif cls == "1mod4":
                    c1 += 1
                elif cls == "3mod4":
                    c3 += 1
        print(f"{label:<10}  {c2:>6}  {c1:>8}  {c3:>8}")

    print()
    print("=" * 72)
    print("Per-LHS-factor distinct-prime mod-4 distribution:")
    print("-" * 72)
    print(f"{'factor':<14}  {'2':>6}  {'1mod4':>8}  {'3mod4':>8}")
    for key, label in (
        ("left_minus", "(h1h3 - h2h4)"),
        ("left_plus", "(h1h3 + h2h4)"),
    ):
        c2 = c1 = c3 = 0
        for r in rows:
            for p_str in r[f"factors_{key}"]:
                p = int(p_str)
                cls = mod4_class(p)
                if cls == "2":
                    c2 += 1
                elif cls == "1mod4":
                    c1 += 1
                elif cls == "3mod4":
                    c3 += 1
        print(f"{label:<14}  {c2:>6}  {c1:>8}  {c3:>8}")

    # Highlight: is the 3mod4 mass conserved between LHS and RHS?
    print()
    print("=" * 72)
    print("BLOCKER-PRIME CHECK")
    print("-" * 72)
    print(
        f"3-mod-4 prime multiplicity:  LHS = {L_total.get('3mod4', 0)},  "
        f"RHS = {R_total.get('3mod4', 0)}"
    )
    if L_total.get("3mod4", 0) == R_total.get("3mod4", 0):
        print("→ 3-mod-4 mass conserved (expected from identity C).")
    else:
        print("→ MISMATCH (would indicate identity C breaks somewhere).")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-val", type=int, default=200,
                    help="Upper bound for chain search (default: 200)")
    ap.add_argument("--out", default=None,
                    help="Optional JSONL output of per-chain analysis")
    ap.add_argument("--limit", type=int, default=0,
                    help="Limit number of chains analyzed (0 = no limit)")
    args = ap.parse_args()

    print(f"Searching for rectangular 4-chains, max_val={args.max_val} ...")
    t0 = time.perf_counter()
    chains = find_chains(max_val=args.max_val, require_square=False,
                         progress=False)
    t_search = time.perf_counter() - t0
    print(f"Found {len(chains)} chains in {t_search:.2f}s")

    if args.limit > 0:
        chains = chains[: args.limit]
        print(f"Limiting to first {len(chains)} chains.")

    print(f"Analyzing identities + factoring ...")
    t0 = time.perf_counter()
    rows = [analyze_chain(r) for r in chains]
    t_ana = time.perf_counter() - t0
    print(f"Analysis done in {t_ana:.2f}s")

    summarize(rows)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w") as fh:
            for row in rows:
                fh.write(json.dumps(row) + "\n")
        print()
        print(f"Saved {len(rows)} rows to {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
