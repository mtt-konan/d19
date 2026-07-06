#!/usr/bin/env python3
"""Audit stored AA/BB rank-zero torsion-pullback certificates."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


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


def _is_rank0_aabb(row: dict[str, Any]) -> bool:
    return (
        row.get("status") == "ok"
        and row.get("curve") in {"AA", "BB"}
        and int(row.get("rank_lower", -1)) == 0
        and int(row.get("rank_upper", -1)) == 0
    )


def _violation(row: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "A": int(row["A"]),
        "B": int(row["B"]),
        "curve": str(row["curve"]),
        "reason": reason,
    }


def _counter_dict(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items()))


def _audit_classifications(
    row: dict[str, Any],
    certificate: dict[str, Any],
) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    classifications = certificate.get("affine_preimage_classifications", [])
    expected_count = int(certificate["affine_preimage_count"])
    if len(classifications) != expected_count:
        violations.append(_violation(row, "classification-count-mismatch"))

    for classification in classifications:
        if not classification.get("is_midpoint"):
            violations.append(_violation(row, "classification-not-midpoint"))
        if classification.get("is_full_closed_square"):
            violations.append(_violation(row, "classification-full-closed-square"))
    return violations


def audit_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    rank0_aabb_rows = 0
    certified_rows = 0
    strict_no_full_closed_rows = 0
    only_midpoint_rows = 0
    classification_detail_rows = 0
    classification_detail_point_count = 0
    affine_preimage_counts: Counter[str] = Counter()
    strict_excluded_pairs: dict[tuple[int, int], set[str]] = defaultdict(set)
    violations: list[dict[str, Any]] = []

    for row in rows:
        if not _is_rank0_aabb(row):
            continue

        rank0_aabb_rows += 1
        certificate = row.get("rank0_torsion_certificate")
        if not isinstance(certificate, dict) or certificate.get("status") != "certified":
            violations.append(_violation(row, "missing-or-uncertified-certificate"))
            continue

        certified_rows += 1
        affine_preimage_counts[str(certificate["affine_preimage_count"])] += 1
        classifications = certificate.get("affine_preimage_classifications", [])
        if isinstance(classifications, list):
            classification_detail_rows += 1
            classification_detail_point_count += len(classifications)
            violations.extend(_audit_classifications(row, certificate))

        if certificate.get("certifies_no_full_closed_square"):
            strict_no_full_closed_rows += 1
            strict_excluded_pairs[(int(row["A"]), int(row["B"]))].add(str(row["curve"]))
        else:
            violations.append(_violation(row, "does-not-certify-no-full-closed-square"))

        if certificate.get("all_affine_preimages_are_midpoints"):
            only_midpoint_rows += 1
        else:
            violations.append(_violation(row, "not-only-midpoint"))

    strict_excluded_pair_rows = [
        {
            "A": pair[0],
            "B": pair[1],
            "certifying_curves": sorted(curves),
        }
        for pair, curves in sorted(strict_excluded_pairs.items())
    ]
    violation_counts = Counter(str(violation["reason"]) for violation in violations)

    return {
        "rows": len(rows),
        "rank0_aabb_rows": rank0_aabb_rows,
        "certified_rows": certified_rows,
        "strict_no_full_closed_rows": strict_no_full_closed_rows,
        "only_midpoint_rows": only_midpoint_rows,
        "classification_detail_rows": classification_detail_rows,
        "classification_detail_point_count": classification_detail_point_count,
        "affine_preimage_counts": _counter_dict(affine_preimage_counts),
        "strict_excluded_pair_count": len(strict_excluded_pair_rows),
        "strict_excluded_pairs": strict_excluded_pair_rows,
        "violation_counts": _counter_dict(violation_counts),
        "violations": violations,
        "certificate_scope": "AA/BB rows with exact rank 0/0 only",
        "proof_boundary": (
            "This audits stored torsion-pullback certificates; it does not "
            "certify rank by itself."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        action="append",
        required=True,
        help="Mixed closure rank/certificate JSONL file. Repeat to merge datasets.",
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any certificate violation is found.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows: list[dict[str, Any]] = []
    for path in args.input:
        rows.extend(load_jsonl(path))

    audit = audit_rows(rows)
    write_json(args.out, audit)
    violation_total = len(audit["violations"])
    print(f"wrote rank0 certificate audit for {audit['rows']} rows to {args.out}")
    print(
        f"rank0_aabb_rows={audit['rank0_aabb_rows']} "
        f"certified_rows={audit['certified_rows']} "
        f"strict_no_full_closed_rows={audit['strict_no_full_closed_rows']} "
        f"only_midpoint_rows={audit['only_midpoint_rows']} "
        f"violations={violation_total}"
    )
    if args.strict and violation_total:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
