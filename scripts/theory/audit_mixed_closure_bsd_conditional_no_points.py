#!/usr/bin/env python3
"""Audit BSD-conditional no-point status for mixed-closure residual covers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _cover_key(row: dict[str, Any]) -> tuple[int, int, str, int]:
    return (
        int(row["A"]),
        int(row["B"]),
        str(row["curve"]),
        int(row["cover_index"]),
    )


def _torsion_preimage_index(
    torsion_preimage_audit: dict[str, Any],
) -> dict[tuple[int, int, str, int], bool]:
    return {
        _cover_key(row): row.get("no_torsion_preimage") is True
        for row in torsion_preimage_audit.get("sage", {}).get("covers", [])
    }


def audit_bsd_conditional_no_points(
    *,
    selmer_gap_ledger: dict[str, Any],
    torsion_preimage_audit: dict[str, Any],
) -> dict[str, Any]:
    no_torsion_by_key = _torsion_preimage_index(torsion_preimage_audit)
    rows: list[dict[str, Any]] = []

    for ledger_row in selmer_gap_ledger.get("rows", []):
        if ledger_row.get("gap_type") != "rank0-sha2-gap2":
            continue
        no_torsion_preimage = no_torsion_by_key.get(_cover_key(ledger_row), False)
        has_bsd_conditional_rank0 = (
            ledger_row.get("has_bsd_conditional_rank0") is True
        )
        conditional_status = (
            "bsd-conditional-no-point"
            if has_bsd_conditional_rank0 and no_torsion_preimage
            else "rank-zero-open"
        )
        rows.append(
            {
                "priority": int(ledger_row["priority"]),
                "A": int(ledger_row["A"]),
                "B": int(ledger_row["B"]),
                "curve": str(ledger_row["curve"]),
                "cover_index": int(ledger_row["cover_index"]),
                "gap_type": str(ledger_row["gap_type"]),
                "has_bsd_conditional_rank0": has_bsd_conditional_rank0,
                "no_torsion_preimage": no_torsion_preimage,
                "conditional_no_point_status": conditional_status,
            }
        )

    return {
        "status": "ok",
        "bsd_conditional_no_point_cover_count": sum(
            1
            for row in rows
            if row["conditional_no_point_status"] == "bsd-conditional-no-point"
        ),
        "rank0_sha2_gap2_cover_count": len(rows),
        "torsion_preimage_cover_count": len(no_torsion_by_key),
        "strict_no_point_cover_count": 0,
        "candidate_not_proof": True,
        "rows": rows,
        "boundary": (
            "This combines BSD-conditional rank-zero diagnostics with a torsion "
            "preimage audit. It is conditional evidence, not a strict no-point proof."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selmer-gap-ledger", type=Path, required=True)
    parser.add_argument("--rank0-torsion-preimage-audit", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_bsd_conditional_no_points(
        selmer_gap_ledger=load_json(args.selmer_gap_ledger),
        torsion_preimage_audit=load_json(args.rank0_torsion_preimage_audit),
    )
    write_json(args.out, audit)
    print(f"wrote BSD-conditional no-point audit to {args.out}")
    print(
        "bsd_conditional_no_point_cover_count="
        f"{audit['bsd_conditional_no_point_cover_count']}"
    )
    print(f"strict_no_point_cover_count={audit['strict_no_point_cover_count']}")
    if args.strict and audit["strict_no_point_cover_count"] != 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
