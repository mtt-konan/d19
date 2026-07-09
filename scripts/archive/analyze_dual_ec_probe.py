#!/usr/bin/env python3
"""Post-process the JSONL output of scripts/probe_dual_ec.py.

Splits "lower bound = 0" into two categories using the rank_*_bounds field:
    - CERTIFIED rank=0   (lower == upper == 0)
    - unproven rank=0    (lower == 0, upper > 0; PARI did not finish descent)

Usage:
    uv run python scripts/analyze_dual_ec_probe.py results/dual_ec_probe.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("jsonl", help="Probe JSONL produced by probe_dual_ec.py")
    args = ap.parse_args()

    path = Path(args.jsonl)
    rows: list[dict] = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    print(f"Loaded {len(rows)} probe rows from {path}")
    print()

    def fmt(row: dict, which: str) -> str:
        lo, hi = row[f"rank_{which}_bounds"]
        if lo == hi == 0:
            return f"CERTIFIED rank=0 (bounds=[0,0])"
        if lo == hi:
            return f"CERTIFIED rank={lo} (bounds=[{lo},{lo}])"
        return f"unproven rank in [{lo}, {hi}]"

    print("=" * 72)
    print("Samples with rank_bd LOWER bound = 0")
    print("-" * 72)
    bd_zero = [r for r in rows if r["rank_bd"] == 0]
    for r in bd_zero:
        print(
            f"  id={r['id']:>4}  "
            f"(a,b,c,d)=({r['a']},{r['b']},{r['c']},{r['d']})  "
            f"{fmt(r, 'bd')}"
        )
    print(f"  --> {len(bd_zero)} rows where rank_bd lower = 0")

    print()
    print("=" * 72)
    print("Samples with rank_ac LOWER bound = 0")
    print("-" * 72)
    ac_zero = [r for r in rows if r["rank_ac"] == 0]
    for r in ac_zero:
        print(
            f"  id={r['id']:>4}  "
            f"(a,b,c,d)=({r['a']},{r['b']},{r['c']},{r['d']})  "
            f"{fmt(r, 'ac')}"
        )
    print(f"  --> {len(ac_zero)} rows where rank_ac lower = 0")

    print()
    print("=" * 72)
    print("Certification status of rank bounds (both curves)")
    print("-" * 72)
    cc: Counter[tuple[bool, bool]] = Counter()
    for r in rows:
        ac_lo, ac_hi = r["rank_ac_bounds"]
        bd_lo, bd_hi = r["rank_bd_bounds"]
        cc[(ac_lo == ac_hi, bd_lo == bd_hi)] += 1
    print(f"  both ac and bd certified : {cc[(True, True)]}")
    print(f"  only ac certified        : {cc[(True, False)]}")
    print(f"  only bd certified        : {cc[(False, True)]}")
    print(f"  neither certified        : {cc[(False, False)]}")

    print()
    print("=" * 72)
    print("Real free obstructions: rank_bd CERTIFIED 0")
    print("-" * 72)
    certified_bd_zero = [
        r for r in rows if r["rank_bd_bounds"][0] == 0 and r["rank_bd_bounds"][1] == 0
    ]
    if not certified_bd_zero:
        print("  (none)")
    else:
        for r in certified_bd_zero:
            a, b, c, d = r["a"], r["b"], r["c"], r["d"]
            bd = b * d
            a2 = a * a
            tag = "  <-- a^2 == bd (cannot exclude)" if a2 == bd else "  (a^2 != bd)"
            print(
                f"  (a,b,c,d)=({a},{b},{c},{d})  "
                f"a^2={a2}  bd={bd}{tag}"
            )
    print(f"  --> {len(certified_bd_zero)} certified rank-0 dual obstructions")

    return 0


if __name__ == "__main__":
    sys.exit(main())
