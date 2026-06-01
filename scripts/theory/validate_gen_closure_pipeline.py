"""wl094 validation: run the default proof-status pipeline over all primitive
(A, B) pairs and confirm the GEN-CLOSURE landing yields no hard_case / no
false solution_found.

Usage: python scripts/theory/validate_gen_closure_pipeline.py [max_hyp]
"""

from __future__ import annotations

import sys
import time
from collections import Counter

from rational_distance.concordant.pairs import generate_ab_pairs
from rational_distance.proof_status.workflow import compute_pair_status


def main() -> None:
    max_hyp = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    pairs = generate_ab_pairs(max_hyp)

    status_counts: Counter[str] = Counter()
    method_counts: Counter[str] = Counter()
    solution_pairs: list[tuple[int, int]] = []

    t0 = time.perf_counter()
    for a, b in pairs:
        res = compute_pair_status(a, b)
        status_counts[res.final_status] += 1
        method_counts[res.final_method or "?"] += 1
        if res.final_status == "solution_found":
            solution_pairs.append((a, b))
    elapsed = time.perf_counter() - t0

    print(f"max_hyp={max_hyp}  pairs={len(pairs)}  elapsed={elapsed:.1f}s")
    print(f"status: {dict(status_counts)}")
    print(f"deciding method: {dict(method_counts)}")
    print(
        f"hard_case={status_counts['hard_case']}  "
        f"solution_found={status_counts['solution_found']}"
    )
    if solution_pairs:
        print(f"!!! solution_found pairs (would refute Harborth): {solution_pairs[:20]}")


if __name__ == "__main__":
    main()
