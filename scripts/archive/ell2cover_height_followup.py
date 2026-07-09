#!/usr/bin/env python3
"""Re-run ell2cover_worker with a higher hyperellratpoints height bound on
the n_without_pt >= 4 outliers from results/ell2cover_sha2_cases.jsonl,
to check whether the extra "no rational point" covers are genuine Sha[2]
elements or just artifacts of the lower height bound.

For each case we compare h=10000 (original) with h=100000 (this script):
- if n_without_pt drops, the gap was a height-search artifact
- if n_without_pt stays the same, this is robust evidence for a higher
  Sha[E][2] dimension than ellrank effort=1 reports
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
WORKER = ROOT / "scripts" / "ell2cover_worker.py"


def main() -> int:
    in_path = ROOT / "results" / "ell2cover_sha2_cases.jsonl"
    out_path = ROOT / "results" / "ell2cover_outliers_h100k.jsonl"

    from typing import Any
    rows: list[dict[str, Any]] = []
    with open(in_path, encoding="utf-8") as fh:
        for line in fh:
            rows.append(json.loads(line))

    outliers = [r for r in rows if (r.get("n_without_pt") or 0) >= 4]
    print(f"Found {len(outliers)} outlier cases (n_without_pt >= 4 at h=10000)")
    print()

    h_new = 100000
    timeout = 120
    t_start = time.perf_counter()
    fh = open(out_path, "w", encoding="utf-8")
    try:
        for r in outliers:
            A, B = int(r["A"]), int(r["B"])
            old_no_pt = r["n_without_pt"]
            old_n_cov = r["n_covers"]
            cmd = ["uv", "run", "--quiet", "python", str(WORKER),
                   str(A), str(B), str(h_new)]
            t0 = time.perf_counter()
            try:
                proc = subprocess.run(
                    cmd, cwd=str(ROOT),
                    capture_output=True, text=True, timeout=timeout,
                )
                out = json.loads(proc.stdout.strip().splitlines()[-1])
                new_no_pt = out.get("n_without_pt")
                new_n_cov = out.get("n_covers")
            except subprocess.TimeoutExpired:
                new_no_pt = "TIMEOUT"
                new_n_cov = "TIMEOUT"
                out = {"error": "TIMEOUT"}
            dt = time.perf_counter() - t0

            verdict = "?"
            if isinstance(new_no_pt, int):
                if new_no_pt < old_no_pt:
                    verdict = f"DROP ({old_no_pt} -> {new_no_pt}) -- artifact"
                elif new_no_pt == old_no_pt:
                    verdict = f"STAY ({old_no_pt}) -- robust Sha[2] evidence"
                else:
                    verdict = f"RAISE ({old_no_pt} -> {new_no_pt}) -- ???"

            print(
                f"  ({A:>6}, {B:>6})  h=10k -> {old_n_cov}/{old_no_pt}  "
                f"h=100k -> {new_n_cov}/{new_no_pt}  ({dt:>5.2f}s)  {verdict}"
            )
            fh.write(json.dumps({
                "A": A, "B": B,
                "h_old": 10000, "n_covers_old": old_n_cov, "n_without_pt_old": old_no_pt,
                "h_new": h_new, "n_covers_new": new_n_cov, "n_without_pt_new": new_no_pt,
                "verdict": verdict,
                "time_s": round(dt, 3),
                "new_full_result": out,
            }) + "\n")
            fh.flush()
    finally:
        fh.close()

    elapsed = time.perf_counter() - t_start
    print()
    print(f"Done in {elapsed:.0f}s. Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
