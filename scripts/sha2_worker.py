#!/usr/bin/env python3
"""Single-pair worker for sha2 scan.

Reads (A, B) from argv, computes ``ellrank(E, effort)`` and prints
JSON to stdout. Designed to be invoked as a subprocess so the parent
can enforce a hard timeout via ``subprocess.run(timeout=...)``.
"""
from __future__ import annotations

import json
import sys
import time

from cypari2 import Pari


def main() -> int:
    if len(sys.argv) < 4:
        print(json.dumps({"error": "usage: sha2_worker.py A B effort"}))
        return 1
    A = int(sys.argv[1])
    B = int(sys.argv[2])
    effort = int(sys.argv[3])

    pari = Pari()
    a2 = A * A + B * B
    a4 = A * A * B * B

    t0 = time.perf_counter()
    try:
        E = pari(f"ellinit([0, {a2}, 0, {a4}, 0])")
        r = pari(f"ellrank({E}, {effort})")
        rank_lo = int(r[0])
        rank_hi = int(r[1])
        sha2_lo = int(r[2])
        out = {
            "A": A, "B": B,
            "rank_lower": rank_lo,
            "rank_upper": rank_hi,
            "sha2_lower": sha2_lo,
            "time_s": round(time.perf_counter() - t0, 3),
            "effort": effort,
            "error": None,
        }
    except Exception as exc:
        out = {
            "A": A, "B": B,
            "rank_lower": None, "rank_upper": None, "sha2_lower": None,
            "time_s": round(time.perf_counter() - t0, 3),
            "effort": effort,
            "error": str(exc),
        }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
