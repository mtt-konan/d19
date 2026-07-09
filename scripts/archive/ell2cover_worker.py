#!/usr/bin/env python3
"""Single-pair worker for ell2cover scan.

For (A, B), compute:
- E = ellinit([0, A^2+B^2, 0, A^2*B^2, 0])
- ell2cover(E) -> list of [quartic, [u(x), v(x)]] pairs
- For each quartic g_i, run hyperellratpoints(g_i, h) to find rational
  points up to naive height h (default 10000).

Output one JSON line to stdout describing every cover:
- coeffs : the quartic [a4, a3, a2, a1, a0] (descending degree)
- lead, content, disc_factors
- num_pts : count of rational points found
- has_pt : true iff at least one rational point was found
- sample_pts : up to 5 sample (x, y) pairs as strings (for inspection)

A cover with `has_pt=false` is a candidate Sha[E][2] element (a 2-Selmer
class with no global rational point up to height h, while local
solubility is guaranteed by Sel construction).
"""
from __future__ import annotations

import json
import sys
import time

from cypari2 import Pari


def parse_quartic(quartic) -> list[int]:
    """Return [a4, a3, a2, a1, a0] as ints (descending-degree)."""
    coeffs = list(quartic.Vec())
    out: list[int] = []
    for c in coeffs:
        try:
            out.append(int(c))
        except (TypeError, ValueError):
            out.append(0)
    return out


def main() -> int:
    if len(sys.argv) < 3:
        print(json.dumps({"error": "usage: ell2cover_worker.py A B [h]"}))
        return 1
    A = int(sys.argv[1])
    B = int(sys.argv[2])
    h = int(sys.argv[3]) if len(sys.argv) > 3 else 10000

    pari = Pari()
    # NOTE: do NOT call pari.allocatemem(...); PARI prints a banner to stdout
    # that breaks JSON parsing in the driver. Default 8 MB stack is enough
    # for the (A, B) ranges we scan.
    a2 = A * A + B * B
    a4 = A * A * B * B

    t_start = time.perf_counter()
    try:
        E = pari(f"ellinit([0, {a2}, 0, {a4}, 0])")
        t0 = time.perf_counter()
        covers = pari(f"ell2cover({E})")
        t_cov = time.perf_counter() - t0

        cover_data: list[dict[str, object]] = []
        for i in range(len(covers)):
            entry = covers[i]
            quartic = entry[0]
            t1 = time.perf_counter()
            try:
                pts = pari(f"hyperellratpoints({quartic}, {h})")
                n_pts = len(pts)
                sample = []
                for j in range(min(n_pts, 5)):
                    sample.append(str(pts[j]))
                pts_err = None
            except Exception as exc:
                n_pts = -1
                sample = []
                pts_err = str(exc)
            t_pts = time.perf_counter() - t1

            try:
                disc = pari(f"poldisc({quartic})")
                lead = int(pari(f"pollead({quartic})"))
                content = int(pari(f"content({quartic})"))
                disc_factor_str = str(pari(f"factor({disc})"))
            except Exception:
                lead = 0
                content = 0
                disc_factor_str = ""

            cover_data.append({
                "i": i,
                "coeffs": parse_quartic(quartic),
                "lead": lead,
                "content": content,
                "disc_factors": disc_factor_str,
                "num_pts": n_pts,
                "has_pt": n_pts > 0,
                "sample_pts": sample,
                "time_pts_s": round(t_pts, 3),
                "pts_error": pts_err,
            })

        out = {
            "A": A, "B": B,
            "h": h,
            "n_covers": len(covers),
            "n_with_pt": sum(1 for c in cover_data if c["has_pt"]),
            "n_without_pt": sum(1 for c in cover_data
                                if not c["has_pt"] and c["num_pts"] != -1),
            "covers": cover_data,
            "time_cover_s": round(t_cov, 3),
            "time_total_s": round(time.perf_counter() - t_start, 3),
            "error": None,
        }
    except Exception as exc:
        out = {
            "A": A, "B": B, "h": h,
            "error": str(exc),
            "time_total_s": round(time.perf_counter() - t_start, 3),
        }

    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
