#!/usr/bin/env python3
"""Analyze ell2cover_sha2_cases.jsonl produced by batch_ell2cover_v2.

For each (A, B) pair we have:
- n_covers: number of nontrivial 2-Selmer covers
- n_with_pt: number of covers with a rational point of height <= h
- n_without_pt: number of covers with NO rational point of height <= h

A cover with no rational point is a candidate Sha[E][2] element. The
distribution of n_without_pt across the 156 sha2>=2 hard_case pairs
gives a finer view of the Sha[2] structure than ellrank's sha2_lower.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent


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


def chi_compare_2x2(pos: int, neg: int, n_pos: int, n_neg: int) -> tuple[float, float]:
    a, b = pos, n_pos - pos
    c, d = neg, n_neg - neg
    n = a + b + c + d
    if n == 0:
        return 0.0, 1.0
    expected = [
        (a + b) * (a + c) / n, (a + b) * (b + d) / n,
        (c + d) * (a + c) / n, (c + d) * (b + d) / n,
    ]
    if any(e <= 0 for e in expected):
        return 0.0, 1.0
    chi2 = sum(
        (abs(o - e) - 0.5) ** 2 / e
        for o, e in zip([a, b, c, d], expected)
    )
    p = math.erfc(math.sqrt(chi2 / 2)) if chi2 >= 0 else 1.0
    return chi2, p


def main() -> int:
    path = ROOT / "results" / "ell2cover_sha2_cases.jsonl"
    rows: list[dict[str, Any]] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            rows.append(json.loads(line))
    print(f"Loaded {len(rows)} rows from {path}")
    print()

    # Joint distribution
    print("=" * 72)
    print("Joint distribution of (n_covers, n_without_pt)")
    print("=" * 72)
    joint = Counter((r.get("n_covers"), r.get("n_without_pt")) for r in rows)
    for (nc, nw), cnt in sorted(joint.items()):
        print(f"  n_covers={nc}  n_without_pt={nw}: {cnt:>4}")

    print()
    print("=" * 72)
    print("Outlier cases (n_without_pt >= 4)")
    print("=" * 72)
    outliers = [r for r in rows if (r.get("n_without_pt") or 0) >= 4]
    for r in sorted(outliers, key=lambda x: -(x.get("n_without_pt") or 0)):
        A, B = r["A"], r["B"]
        nc = r.get("n_covers")
        nw = r.get("n_without_pt")
        s_in = r.get("sha2_lower_input")
        pf_a, pf_b = prime_factors(A), prime_factors(B)
        print(f"  ({A:>5}, {B:>6}) n_covers={nc} n_without_pt={nw} "
              f"sha2_lower_in={s_in}")
        print(f"     A={dict(pf_a)}  B={dict(pf_b)}")

    # Stratify by n_without_pt
    print()
    print("=" * 72)
    print("Feature distribution by n_without_pt class")
    print("=" * 72)
    classes: dict[int, list[tuple[int, int]]] = {}
    for r in rows:
        nw = r.get("n_without_pt") or 0
        classes.setdefault(nw, []).append((r["A"], r["B"]))
    for nw in sorted(classes):
        pairs = classes[nw]
        n = len(pairs)
        a_sf = sum(1 for a, _ in pairs if is_squarefree(a))
        b_sf = sum(1 for _, b in pairs if is_squarefree(b))
        b_high = sum(1 for _, b in pairs if max_exp(b) >= 4)
        a_high = sum(1 for a, _ in pairs if max_exp(a) >= 3)
        print(
            f"  n_without_pt={nw}  n={n:>3}  "
            f"A_sf={a_sf/n:.0%}  B_sf={b_sf/n:.0%}  "
            f"max_exp(B)>=4: {b_high/n:.0%}  max_exp(A)>=3: {a_high/n:.0%}"
        )

    # Chi^2: n_without_pt >= 3 vs n_without_pt = 2 on max_exp(B) >= 4
    print()
    print("=" * 72)
    print("chi^2: n_without_pt >= 3 vs n_without_pt = 2")
    print("=" * 72)
    high = [r for r in rows if (r.get("n_without_pt") or 0) >= 3]
    base = [r for r in rows if (r.get("n_without_pt") or 0) == 2]
    n_h, n_b = len(high), len(base)
    for fname, fn in [
        ("max_exp(B) >= 4",
         lambda r: max_exp(r["B"]) >= 4),
        ("max_exp(B) >= 3",
         lambda r: max_exp(r["B"]) >= 3),
        ("A_sf",
         lambda r: is_squarefree(r["A"])),
        ("B_sf",
         lambda r: is_squarefree(r["B"])),
        ("max_exp(A) >= 3",
         lambda r: max_exp(r["A"]) >= 3),
        ("3 | A",
         lambda r: r["A"] % 3 == 0),
        ("3 | B",
         lambda r: r["B"] % 3 == 0),
    ]:
        c_h = sum(1 for r in high if fn(r))
        c_b = sum(1 for r in base if fn(r))
        chi2, p = chi_compare_2x2(c_h, c_b, n_h, n_b)
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(
            f"  {fname:<22}  high>=3: {c_h/n_h:.0%}  "
            f"base=2: {c_b/n_b:.0%}  "
            f"chi^2={chi2:>6.2f}  p={p:>9.2e}  {sig}"
        )

    # Sample first 10 obstructions
    print()
    print("=" * 72)
    print("First 5 sample (A, B) for each n_without_pt class, with cover obstruction signature")
    print("=" * 72)
    for nw in sorted(classes):
        print(f"\n--- n_without_pt = {nw} ---")
        sample = sorted(classes[nw], key=lambda x: max(x))[:5]
        for a_val, b_val in sample:
            r = next(
                rr for rr in rows if rr["A"] == a_val and rr["B"] == b_val
            )
            covers = r.get("covers", []) or []
            sig = "".join(
                "0" if c.get("has_pt") else "1" for c in covers  # type: ignore[union-attr]
            )
            print(f"  ({a_val:>5}, {b_val:>6})  cover signature: {sig}  "
                  f"(0=hasPt, 1=noPt, len={len(sig)})")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
