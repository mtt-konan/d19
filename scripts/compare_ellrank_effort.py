#!/usr/bin/env python3
"""Compare PARI ellrank under effort = 0, 1, 2 on representative (A, B) cases.

Used in worklog 036 to decide the default `effort` value for the fixed
`compute_rank()`. Data are written to results/ellrank_effort_compare.json.

Cases covered:
- 7 chain near-misses where default effort gave fake rank=0 (from
  worklog 033's deep-rank recheck, results/dual_ec_deep.json)
- A handful of small (A, B) pairs from the proof_status pipeline,
  to confirm effort=2 is also cheap on small curves
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

import cypari2  # noqa: E402

# -----------------------------------------------------------------------------
# Test cases
# -----------------------------------------------------------------------------

# From results/dual_ec_deep.json: chain near-misses where default effort lied
HARD_CASES: list[tuple[int, int, str]] = [
    (240331, 66585, "wl033 #574 ac"),
    (262031, 39721, "wl033 #470 ac"),
    (331917, 61215, "wl033 #95 ac"),
    (22345, 678503, "wl033 #51 bd"),
    (713687, 683865, "wl033 #94 ac"),
    (1384320, 13232, "wl033 #94 bd"),
    (959180, 194040, "wl033 #382 ac"),
]

# Small curves from typical d19 hard_case range
SMALL_CASES: list[tuple[int, int, str]] = [
    (3, 4, "smallest non-trivial"),
    (7, 45, "wl035 chain (7,24,45,28) on E_{a,c}"),
    (264, 420, "test_concordant.py canonical (rank 2)"),
    (105, 480, "CURRENT_FINDINGS half-solution"),
]


def time_ellrank(pari, A: int, B: int, effort: int) -> dict:
    a2, b2 = A * A, B * B
    E = pari(f"ellinit([0, {a2 + b2}, 0, {a2 * b2}, 0])")
    started = time.perf_counter()
    try:
        if effort == 0:
            result = pari.ellrank(E)
        else:
            result = pari.ellrank(E, effort)
    except Exception as exc:
        return {
            "effort": effort,
            "error": str(exc),
            "time_s": time.perf_counter() - started,
        }
    elapsed = time.perf_counter() - started

    lower = int(result[0])
    upper = int(result[1])
    sha2 = int(result[2]) if len(result) > 2 else None
    n_gens = 0
    if len(result) > 3:
        try:
            n_gens = len(result[3])
        except Exception:
            n_gens = -1

    return {
        "effort": effort,
        "rank_lower": lower,
        "rank_upper": upper,
        "sha2_lower": sha2,
        "n_gens": n_gens,
        "time_s": round(elapsed, 4),
        "certified": lower == upper,
    }


def main() -> None:
    pari = cypari2.Pari()
    pari.allocatemem(64 * 1024 * 1024)

    output: list[dict] = []

    print(
        f"{'case':<55} {'A':>10} {'B':>10}  "
        f"{'eff0 (lo,hi,sha,t)':<25} {'eff1':<25} {'eff2':<25}  cert"
    )
    print("-" * 180)

    all_cases = [(*c, "hard") for c in HARD_CASES] + [(*c, "small") for c in SMALL_CASES]
    for A, B, label, kind in all_cases:
        row = {"A": A, "B": B, "label": label, "kind": kind, "results": {}}
        cert_changed = []
        for effort in (0, 1, 2):
            r = time_ellrank(pari, A, B, effort)
            row["results"][effort] = r
            if "error" in r:
                cert_changed.append(f"e{effort}=ERR")
                continue
            cert_changed.append(
                f"({r['rank_lower']},{r['rank_upper']},{r['sha2_lower']},{r['time_s']:.2f}s)"
            )
        # final certified status?
        final = row["results"].get(2, row["results"].get(1, row["results"][0]))
        certified = final.get("certified", False)
        print(
            f"{label:<55} {A:>10} {B:>10}  "
            f"{cert_changed[0]:<25} {cert_changed[1]:<25} {cert_changed[2]:<25}  "
            f"{'YES' if certified else 'NO'}"
        )
        output.append(row)

    out_path = ROOT / "results" / "ellrank_effort_compare.json"
    out_path.write_text(json.dumps(output, indent=2))
    print(f"\nWrote {out_path}")

    # Aggregate stats
    def agg(kind: str, effort: int) -> dict:
        rows = [r for r in output if r["kind"] == kind]
        certs = sum(1 for r in rows if r["results"][effort].get("certified", False))
        total_time = sum(r["results"][effort].get("time_s", 0.0) for r in rows)
        return {"n": len(rows), "n_certified": certs, "total_time_s": round(total_time, 3)}

    print("\nAggregate:")
    for kind in ("hard", "small"):
        for effort in (0, 1, 2):
            a = agg(kind, effort)
            print(
                f"  {kind:5} effort={effort}: "
                f"certified {a['n_certified']}/{a['n']}, "
                f"total time {a['total_time_s']}s"
            )


if __name__ == "__main__":
    main()
