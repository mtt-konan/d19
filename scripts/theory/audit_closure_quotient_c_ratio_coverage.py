#!/usr/bin/env python3
"""Audit what c_+/c_- classes cover in the closure-quotient ray ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits c_+/c_- coverage in the existing primitive-ray ledger. It "
    "identifies unordered primitive ratio classes and missing lambda "
    "orientations; it does not add no-point certificates or prove any "
    "lambda-family exclusion."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _orientation_key(row: dict[str, Any]) -> tuple[int, int, str]:
    primitive = list(row.get("unordered_primitive_ray", []))
    c_ratio = str(row.get("c_ratio", ""))
    if c_ratio == "undefined":
        return (10**18, 10**18, str(row.get("class", "")))
    if len(primitive) == 2:
        return (int(primitive[0]), int(primitive[1]), str(row.get("class", "")))
    return (10**12, 10**12, str(row.get("class", "")))


def _lambda_mainline_status(row: dict[str, Any], *, missing_count: int) -> str:
    if str(row.get("c_ratio", "")) == "undefined":
        return "c-minus-zero-not-a-c-ratio-class"
    if missing_count:
        return "needs-lambda-family-proof-or-certificate"
    coverage_status = str(row.get("coverage_status", ""))
    if coverage_status == "all-observed-pairs-strict":
        return "observed-class-strict-not-family-proof"
    if coverage_status == "some-observed-pairs-strict":
        return "observed-class-mixed-not-family-proof"
    return "needs-lambda-family-proof-or-certificate"


def _coverage_row(row: dict[str, Any]) -> dict[str, Any]:
    possible = [list(ray) for ray in row.get("possible_oriented_rays", [])]
    observed = [list(ray) for ray in row.get("observed_oriented_rays", [])]
    observed_set = {tuple(ray) for ray in observed}
    missing = [ray for ray in possible if tuple(ray) not in observed_set]
    c_ratio = str(row.get("c_ratio", ""))
    return {
        "class": str(row.get("class", "")),
        "c_ratio": c_ratio,
        "unordered_primitive_ray": list(row.get("unordered_primitive_ray", [])),
        "possible_oriented_rays": possible,
        "observed_oriented_rays": observed,
        "missing_oriented_rays": missing,
        "covers_unordered_ratio_class": c_ratio != "undefined",
        "covers_all_lambda_orientations": not missing,
        "coverage_status": str(row.get("coverage_status", "")),
        "lambda_mainline_status": _lambda_mainline_status(
            row,
            missing_count=len(missing),
        ),
    }


def audit_c_ratio_coverage(*, ray_ledger: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(ray_ledger):
        violations.append("ray_ledger_not_ready")
    if ray_ledger.get("search_count_used_as_progress") is True:
        violations.append("ray_ledger_uses_search_count_as_progress")

    source_rows = sorted(
        [dict(row) for row in ray_ledger.get("c_ratio_class_rows", [])],
        key=_orientation_key,
    )
    rows = [_coverage_row(row) for row in source_rows]
    defined_rows = [row for row in rows if row["covers_unordered_ratio_class"] is True]
    undefined_rows = [
        row for row in rows if row["covers_unordered_ratio_class"] is False
    ]
    orientation_lost_rows = [
        row
        for row in defined_rows
        if len(row["possible_oriented_rays"]) > 1
    ]
    both_orientations_observed_rows = [
        row
        for row in defined_rows
        if row["covers_all_lambda_orientations"] is True
        and len(row["possible_oriented_rays"]) > 1
    ]
    single_orientation_observed_rows = [
        row
        for row in defined_rows
        if row["covers_all_lambda_orientations"] is False
    ]
    strict_rows = [
        row
        for row in defined_rows
        if row["coverage_status"]
        in {"all-observed-pairs-strict", "some-observed-pairs-strict"}
    ]
    residual_rows = [
        row
        for row in source_rows
        if row.get("c_ratio") != "undefined"
        and int(row.get("status_counts", {}).get("residual-candidate-not-proof", 0))
        > 0
    ]
    open_rows = [
        row
        for row in defined_rows
        if row["coverage_status"] in {"observed-open", "residual-candidate-open"}
    ]

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "input_c_ratio_class_count": int(
            ray_ledger.get("c_ratio_class_count", len(source_rows)) or 0
        ),
        "defined_c_ratio_class_count": len(defined_rows),
        "undefined_c_ratio_class_count": len(undefined_rows),
        "orientation_lost_class_count": len(orientation_lost_rows),
        "both_orientations_observed_class_count": len(
            both_orientations_observed_rows
        ),
        "single_orientation_observed_class_count": len(
            single_orientation_observed_rows
        ),
        "lambda_orientation_gap_class_count": len(single_orientation_observed_rows),
        "strict_unordered_class_count": len(strict_rows),
        "residual_unordered_class_count": len(residual_rows),
        "open_unordered_class_count": len(open_rows),
        "lambda_family_exclusion_proved_count": 0,
        "no_point_certificate_added_count": 0,
        "search_count_used_as_progress": False,
        "c_ratio_coverage_not_lambda_family_proof": True,
        "coverage_interpretation": (
            "c_+/c_- covers unordered primitive ratio classes {A:B, B:A}. "
            "A defined class still needs lambda-oriented family proof or a "
            "reviewable no-point certificate before it can be promoted."
        ),
        "coverage_rows": rows,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ray-ledger", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_c_ratio_coverage(ray_ledger=load_json(args.ray_ledger))
    write_json(args.out, audit)
    print(f"wrote closure quotient c-ratio coverage audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"defined_c_ratio_class_count={audit['defined_c_ratio_class_count']}")
    print(
        "lambda_orientation_gap_class_count="
        f"{audit['lambda_orientation_gap_class_count']}"
    )
    print(
        "lambda_family_exclusion_proved_count="
        f"{audit['lambda_family_exclusion_proved_count']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
