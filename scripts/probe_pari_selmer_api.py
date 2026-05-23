#!/usr/bin/env python3
"""Smoke test of cypari2's exposure of PARI 2-descent / Selmer / point machinery.

We need to understand what's available before building the Selmer-style
obstruction pipeline.  This script:

  1. Picks one moderate-sized chain candidate from results/dual_ec_probe.jsonl
  2. Builds E: Y^2 = X(X+A^2)(X+B^2) for the (a, c) and (b, d) diagonals
  3. Calls every potentially useful PARI ell* function and reports what
     each returns (type and shape).

This is exploratory; the output is meant to be read once.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

try:
    import cypari2
except ImportError as exc:
    raise SystemExit("cypari2 required") from exc


def describe(label: str, value, max_repr: int = 200) -> None:
    s = repr(value)
    if len(s) > max_repr:
        s = s[:max_repr] + " ... (truncated)"
    print(f"  {label:<28} {s}")


def main() -> int:
    # Pick a small but non-trivial chain candidate from dual_ec_probe
    jsonl_path = ROOT / "results" / "dual_ec_probe.jsonl"
    if not jsonl_path.exists():
        print(f"Missing {jsonl_path}; run probe_dual_ec.py first.")
        return 1
    with jsonl_path.open() as fh:
        rows = [json.loads(line) for line in fh]
    # Pick smallest by max(a, b, c, d)
    rows.sort(key=lambda r: max(r["a"], r["b"], r["c"], r["d"]))
    r = rows[0]
    a, b, c, d = r["a"], r["b"], r["c"], r["d"]
    print(f"Chain candidate: (a,b,c,d) = ({a}, {b}, {c}, {d})")
    print()

    pari = cypari2.Pari()
    pari.allocatemem(64 * 1024 * 1024)

    A, B = a, c  # main diagonal
    a2, b2 = A * A, B * B
    E = pari(f"ellinit([0, {a2 + b2}, 0, {a2 * b2}, 0])")
    print(f"E_(a,c): Y^2 = X(X+{a2})(X+{b2})  for (A,B)=({A},{B})")
    print()

    # 1. Standard rank
    print("--- ellrank(E, effort=2) ---")
    rr = pari.ellrank(E, 2)
    describe("return type", type(rr).__name__)
    describe("len(rr)", len(rr))
    for i, item in enumerate(rr):
        describe(f"  rr[{i}]", item, max_repr=300)
    print()

    # 2. Torsion subgroup
    print("--- elltors(E) ---")
    tors = pari.elltors(E)
    describe("return", tors, max_repr=400)
    print()

    # 3. ell2cover (if present)
    print("--- ell2cover(E) ---")
    try:
        cov = pari("ell2cover")(E)
        describe("return", cov, max_repr=600)
    except Exception as exc:
        print(f"  not available: {exc}")
    print()

    # 4. ellrankinit  (PARI 2.16+ API)
    print("--- ellrankinit(E, effort=2) ---")
    try:
        rinit = pari("ellrankinit")(E, 2)
        describe("return type", type(rinit).__name__)
        describe("repr (head)", rinit, max_repr=400)
    except Exception as exc:
        print(f"  not available: {exc}")
    print()

    # 5. Ratpoints up to small height
    print("--- ellratpoints(E, height=20) ---")
    try:
        pts = pari("ellratpoints")(E, 20)
        describe("return", pts, max_repr=600)
    except Exception as exc:
        print(f"  not available: {exc}")
    print()

    # 6. Decode ellrank's 4-tuple: [rank_lo, rank_hi, sha2_lo, gens]
    print("--- ellrank decode ---")
    if len(rr) >= 4:
        print(f"  rank lower bound : {int(rr[0])}")
        print(f"  rank upper bound : {int(rr[1])}")
        print(f"  Sha[2] lower(?)  : {rr[2]}  (PARI's third return; likely related to Sha)")
        gens_field = rr[3]
        # gens_field may be a vec t_VEC; iterate carefully
        try:
            gens_list = list(gens_field)
            print(f"  generators count : {len(gens_list)}")
            for i, g in enumerate(gens_list):
                describe(f"    gen[{i}]", g, max_repr=300)
        except TypeError:
            print(f"  gens_field not iterable (type={type(gens_field).__name__}, value={gens_field})")
    print()

    # 7. Check whether b^2 (the key chain rational point) is on the curve
    print("--- Is X = b^2 = {} a rational X on E? ---".format(b * b))
    try:
        # Y^2 = X(X+a^2)(X+c^2)
        X_target = b * b
        Y2 = pari(f"({X_target})*({X_target}+{a2})*({X_target}+{b2})")
        # Try issquare
        is_sq = pari(f"issquare({Y2})")
        describe("Y^2", Y2, max_repr=200)
        describe("issquare(Y^2)?", is_sq, max_repr=100)
    except Exception as exc:
        print(f"  Failed: {exc}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
