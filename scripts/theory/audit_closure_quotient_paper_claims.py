#!/usr/bin/env python3
"""Audit stored closure-quotient outputs against paper-level numeric claims."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _int_value(payload: dict[str, Any], key: str) -> int:
    return int(payload.get(key, 0))


def _bsd_status_counts(rows: list[dict[str, Any]]) -> Counter[str]:
    return Counter(str(row.get("status", "missing")) for row in rows)


def _bsd_analytic_rank0_rows(rows: list[dict[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("status") == "ok" and row.get("analytic_rank") == 0)


def _mismatches(
    claim_values: dict[str, int],
    expected: dict[str, int],
) -> list[dict[str, int | str]]:
    rows: list[dict[str, int | str]] = []
    for field, expected_value in sorted(expected.items()):
        actual = claim_values.get(field)
        if actual != expected_value:
            rows.append(
                {
                    "field": field,
                    "expected": expected_value,
                    "actual": -1 if actual is None else actual,
                }
            )
    return rows


def audit_claims(
    *,
    rank_summary: dict[str, Any],
    rank0_audit: dict[str, Any],
    cover_summary: dict[str, Any],
    bsd_rows: list[dict[str, Any]],
    expected: dict[str, int],
) -> dict[str, Any]:
    bsd_counts = _bsd_status_counts(bsd_rows)
    claim_values = {
        "rank_summary_rows": _int_value(rank_summary, "rows"),
        "rank0_torsion_certificates": _int_value(
            rank_summary, "rank0_torsion_certificates"
        ),
        "certified_no_full_closed_square": _int_value(
            rank_summary, "certified_no_full_closed_square"
        ),
        "certified_all_midpoint": _int_value(rank_summary, "certified_all_midpoint"),
        "strict_excluded_pair_count": _int_value(
            rank_summary, "strict_excluded_pair_count"
        ),
        "uncertain_rank_rows": len(rank_summary.get("uncertain_rank_rows", [])),
        "rank0_aabb_rows": _int_value(rank0_audit, "rank0_aabb_rows"),
        "rank0_certified_rows": _int_value(rank0_audit, "certified_rows"),
        "rank0_strict_no_full_closed_rows": _int_value(
            rank0_audit, "strict_no_full_closed_rows"
        ),
        "rank0_only_midpoint_rows": _int_value(rank0_audit, "only_midpoint_rows"),
        "rank0_audit_violations": len(rank0_audit.get("violations", [])),
        "cover_rows": _int_value(cover_summary, "rows"),
        "cover_selmer_matches": int(
            cover_summary.get("selmer_gap_alignment_counts", {}).get("match", 0)
        ),
        "cover_bounded_candidates": int(
            cover_summary.get("evidence_level_counts", {}).get(
                "bounded-search-no-point-candidate", 0
            )
        ),
        "bsd_ok_rows": int(bsd_counts.get("ok", 0)),
        "bsd_analytic_rank0_rows": _bsd_analytic_rank0_rows(bsd_rows),
    }
    return {
        "claim_values": claim_values,
        "expected": dict(sorted(expected.items())),
        "mismatches": _mismatches(claim_values, expected),
        "boundary": (
            "This checks consistency of stored result files and paper-level "
            "claims. It does not create new mathematical certificates."
        ),
    }


def _parse_expect(values: list[str]) -> dict[str, int]:
    expected: dict[str, int] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"--expect must be field=value, got {value!r}")
        field, raw_int = value.split("=", 1)
        expected[field] = int(raw_int)
    return expected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rank-summary", type=Path, required=True)
    parser.add_argument("--rank0-audit", type=Path, required=True)
    parser.add_argument("--cover-summary", type=Path, required=True)
    parser.add_argument("--bsd", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--expect",
        action="append",
        default=[],
        help="Expected numeric claim, formatted as field=value. Repeat as needed.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_claims(
        rank_summary=load_json(args.rank_summary),
        rank0_audit=load_json(args.rank0_audit),
        cover_summary=load_json(args.cover_summary),
        bsd_rows=load_jsonl(args.bsd),
        expected=_parse_expect(args.expect),
    )
    write_json(args.out, audit)
    mismatch_count = len(audit["mismatches"])
    print(f"wrote closure quotient paper claim audit to {args.out}")
    print(f"mismatches={mismatch_count}")
    if args.strict and mismatch_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
