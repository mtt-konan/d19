#!/usr/bin/env python3
"""Path A direction 2a: empirically check the height-bound hypothesis.

Hypothesis (HB):
    For every k=2 multi-N pair (A, B) with concordant_N = {N_1, N_2},
        min(ĥ(P_{N_1}), ĥ(P_{N_2})) > C(A, B)
    where C(A, B) is some explicit upper bound on ĥ(P_N) when N ≤ A + B.

Closure requires N_1 + N_2 = A + B, hence max N_i ≤ A + B, hence both N_i ≤ S.
By the standard Néron–Tate / Weil-height comparison
    ĥ(P_N) = (1/2) log H(N²) + O_E(1)
the hypothesis would imply ĥ exceeds the closure-bound, ruling closure out.

This script reads ``results/k2_closure_fiber_max1m.jsonl`` (1879 k=2 pairs
already analysed via PARI in wl074) and computes:

  log_S    := log(A + B)
  log_N_1  := log(N_1)
  h1       := ĥ(P_{N_1})  (PARI canonical height, already in jsonl)
  ratio    := h1 / log_S      — how many times larger ĥ is vs log_S
  margin   := h1 - 2*log_S    — height gap (positive = HB holds)

If margin > 0 universally, height-bound hypothesis is empirically validated.
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "results/k2_closure_fiber_max1m.jsonl")
    rows = [json.loads(line) for line in path.open()]
    print(f"loaded {len(rows)} k=2 rows from {path}")

    margin_signs: Counter[str] = Counter()
    margins: list[float] = []
    fails: list[dict[str, float | int]] = []

    for r in rows:
        S = r["S"]
        h1 = r["h1"]
        h2 = r["h2"]
        if h1 is None or h2 is None:
            continue
        log_S = math.log(S)
        log_N1 = math.log(r["N_1"])
        log_N2 = math.log(r["N_2"])
        h_min = min(h1, h2)
        margin = h_min - 2 * log_S  # positive ⟹ HB holds
        margins.append(margin)
        margin_signs["positive" if margin > 0 else "non-positive"] += 1
        if margin <= 0:
            fails.append(
                {
                    "A": r["A"],
                    "B": r["B"],
                    "N_1": r["N_1"],
                    "N_2": r["N_2"],
                    "h1": h1,
                    "h2": h2,
                    "log_S": log_S,
                    "log_N1": log_N1,
                    "log_N2": log_N2,
                    "margin": margin,
                }
            )

    print(f"margin sign distribution: {dict(margin_signs)}")
    if margins:
        margins_sorted = sorted(margins)
        print(
            f"margin: min={margins_sorted[0]:.3f} "
            f"q1={margins_sorted[len(margins) // 4]:.3f} "
            f"median={margins_sorted[len(margins) // 2]:.3f} "
            f"q3={margins_sorted[3 * len(margins) // 4]:.3f} "
            f"max={margins_sorted[-1]:.3f}"
        )
    print(f"HB violations (margin <= 0): {len(fails)}")
    for r in fails[:10]:
        print(
            f"  (A={r['A']}, B={r['B']}) N=[{r['N_1']}, {r['N_2']}]  "
            f"h_min vs 2*log(S): margin={r['margin']:.3f}  "
            f"(h1={r['h1']:.3f}, h2={r['h2']:.3f}, log_S={r['log_S']:.3f})"
        )

    # Side observation: ratio ĥ / log(N) — how the canonical height
    # compares to the naive log of the integer.
    ratios: list[float] = []
    for r in rows:
        if r["h1"] is None:
            continue
        log_N1 = math.log(r["N_1"])
        if log_N1 > 0:
            ratios.append(r["h1"] / log_N1)
    if ratios:
        ratios_sorted = sorted(ratios)
        print(
            f"\nratio ĥ(P_1)/log(N_1):  min={ratios_sorted[0]:.3f} "
            f"median={ratios_sorted[len(ratios) // 2]:.3f} "
            f"max={ratios_sorted[-1]:.3f}"
        )


if __name__ == "__main__":
    main()
