#!/usr/bin/env python3
"""Find concrete counterexamples to the IDEAS §2.4 hypothesis.

The hypothesis claims: for every Pythagorean hypotenuse h_i, all odd prime
factors are ≡ 1 (mod 4).  This is true for *primitive* triples, but FALSE
in general because scaled triples (kp, kq, kh) inherit any prime factor
from k.

Reads results/hyp_identity_*.jsonl and prints the smallest chains where
some h_i contains a prime ≡ 3 (mod 4).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from sympy import factorint  # type: ignore[import]
except ImportError as exc:
    raise SystemExit("sympy required: uv pip install sympy") from exc


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("jsonl", help="JSONL produced by analyze_hypotenuse_identity.py")
    ap.add_argument("--n", type=int, default=3,
                    help="Number of smallest counterexamples to display")
    args = ap.parse_args()

    rows = []
    with Path(args.jsonl).open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    violators = []
    for r in rows:
        bad_h = []
        for i, h in enumerate([r["h1"], r["h2"], r["h3"], r["h4"]], 1):
            f = factorint(h)
            bad_p = [p for p in f if p % 4 == 3]
            if bad_p:
                bad_h.append((i, h, dict(f), bad_p))
        if bad_h:
            mx = max(r["a"], r["b"], r["c"], r["d"])
            violators.append((mx, r, bad_h))

    violators.sort(key=lambda x: x[0])

    print(
        f"Total chains with at least one h_i containing a 3-mod-4 prime: "
        f"{len(violators)} / {len(rows)}"
    )
    print()
    print(f"Smallest {min(args.n, len(violators))} counterexamples to IDEAS §2.4 "
          f"hypothesis (\"h_i odd primes all ≡ 1 mod 4\"):")
    print()

    for mx, r, bad_h in violators[: args.n]:
        print(
            f"  (a,b,c,d)=({r['a']},{r['b']},{r['c']},{r['d']})  "
            f"hyp=({r['h1']},{r['h2']},{r['h3']},{r['h4']})"
        )
        for i, h, f, bad_p in bad_h:
            print(f"    h_{i}={h} = {f}  → contains 3 mod 4 primes: {bad_p}")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
