#!/usr/bin/env python3
"""Audit transcript intake for rank-zero isogeny-Selmer proof packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_TRANSCRIPT_TYPE = "uniform-isogeny-selmer-rank-bound-transcript"
REQUIRED_RESULT = "uniform-isogeny-selmer-rank-bound"

BOUNDARY = (
    "This audits transcript packaging for rank-zero isogeny-Selmer tasks. It "
    "checks package matching, transcript presence, and required field labels; "
    "it does not verify Selmer groups, prove rank zero, or promote any "
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


def _resolve_path(root: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else root / path


def _package_entries(materialization: dict[str, Any]) -> list[dict[str, Any]]:
    return list(materialization.get("packages", []))


def _package_payload(root: Path, package: dict[str, Any]) -> dict[str, Any]:
    json_path = _resolve_path(root, str(package.get("json_path", "")))
    return load_json(json_path)


def _transcript_rows(transcript_index: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if transcript_index is None:
        return {}
    return {
        str(row.get("package_id", "")): row
        for row in transcript_index.get("packages", [])
    }


def _missing_fields(
    *,
    required_fields: list[str],
    transcript_row: dict[str, Any] | None,
) -> list[str]:
    if transcript_row is None:
        return required_fields
    field_status = transcript_row.get("field_status", {})
    return [
        field
        for field in required_fields
        if str(field_status.get(field, "")) != "present"
    ]


def _package_violations(
    *,
    package_id: str,
    transcript_row: dict[str, Any] | None,
    missing_fields: list[str],
    root: Path,
) -> list[dict[str, Any]]:
    if transcript_row is None:
        return []
    violations: list[dict[str, Any]] = []
    transcript_path = str(transcript_row.get("transcript_path", ""))
    if not transcript_path or not _resolve_path(root, transcript_path).is_file():
        violations.append(
            {
                "package_id": package_id,
                "field": "transcript_path",
                "expected": "existing transcript file",
                "actual": transcript_path,
            }
        )
    if transcript_row.get("transcript_type") != REQUIRED_TRANSCRIPT_TYPE:
        violations.append(
            {
                "package_id": package_id,
                "field": "transcript_type",
                "expected": REQUIRED_TRANSCRIPT_TYPE,
                "actual": transcript_row.get("transcript_type"),
            }
        )
    if transcript_row.get("result") != REQUIRED_RESULT:
        violations.append(
            {
                "package_id": package_id,
                "field": "result",
                "expected": REQUIRED_RESULT,
                "actual": transcript_row.get("result"),
            }
        )
    if missing_fields:
        violations.append(
            {
                "package_id": package_id,
                "field": "field_status",
                "expected": "present for every required transcript field",
                "actual": f"missing fields {missing_fields}",
            }
        )
    return violations


def _overall_proof_status(*, ready_count: int, package_count: int) -> str:
    if ready_count == 0:
        return "rank-zero-selmer-transcripts-missing-not-proof"
    if ready_count < package_count:
        return "rank-zero-selmer-transcripts-partial-not-proof"
    return "rank-zero-selmer-transcripts-ready-needs-math-review"


def template_index(materialization: dict[str, Any]) -> dict[str, Any]:
    templates = []
    for package in _package_entries(materialization):
        package_id = str(package.get("package_id", ""))
        templates.append(
            {
                "package_id": package_id,
                "transcript_index_entry": {
                    "package_id": package_id,
                    "transcript_path": (
                        "docs/external/rank_zero_selmer/"
                        f"{package_id}-transcript.txt"
                    ),
                    "transcript_type": REQUIRED_TRANSCRIPT_TYPE,
                    "result": REQUIRED_RESULT,
                    "field_status": dict.fromkeys(
                        [
                            "statement",
                            "isogeny_setup",
                            "local_squareclass_conditions",
                            "selmer_bound_argument",
                            "rank_zero_conclusion",
                            "review_notes",
                        ],
                        "missing",
                    ),
                },
            }
        )
    return {
        "package_count": len(templates),
        "templates": templates,
        "boundary": BOUNDARY,
    }


def audit_rank_zero_selmer_transcript_intake(
    *,
    materialization: dict[str, Any],
    transcript_index: dict[str, Any] | None,
    root: Path,
) -> dict[str, Any]:
    package_entries = _package_entries(materialization)
    transcript_rows = _transcript_rows(transcript_index)
    package_ids = [str(package.get("package_id", "")) for package in package_entries]
    expected_ids = set(package_ids)
    unexpected_ids = sorted(
        package_id for package_id in transcript_rows if package_id not in expected_ids
    )
    packages: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []

    for package in package_entries:
        package_id = str(package.get("package_id", ""))
        package_payload = _package_payload(root, package)
        required_fields = [
            str(field)
            for field in package_payload.get("required_transcript_fields", [])
        ]
        transcript_row = transcript_rows.get(package_id)
        missing_fields = _missing_fields(
            required_fields=required_fields,
            transcript_row=transcript_row,
        )
        package_violations = _package_violations(
            package_id=package_id,
            transcript_row=transcript_row,
            missing_fields=missing_fields,
            root=root,
        )
        violations.extend(package_violations)
        package_ready = transcript_row is not None and not package_violations
        packages.append(
            {
                "package_id": package_id,
                "transcript_package_ready": package_ready,
                "strict_promotion_ready": False,
                "proof_status": (
                    "transcript-package-ready-needs-math-review"
                    if package_ready
                    else "no-transcript-package-not-proof"
                ),
                "missing_fields": missing_fields,
            }
        )

    for package_id in unexpected_ids:
        violations.append(
            {
                "package_id": package_id,
                "field": "package_id",
                "expected": f"one of {package_ids}",
                "actual": package_id,
            }
        )

    ready_count = sum(1 for package in packages if package["transcript_package_ready"])
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "package_count": len(packages),
        "open_package_count": int(materialization.get("open_package_count", 0) or 0),
        "transcript_package_ready_count": ready_count,
        "missing_transcript_package_count": len(packages) - ready_count,
        "strict_promotion_ready_count": 0,
        "strict_promotion_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "candidate_not_proof": True,
        "proof_status": _overall_proof_status(
            ready_count=ready_count,
            package_count=len(packages),
        ),
        "packages": packages,
        "unexpected_transcript_package_ids": unexpected_ids,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--materialization", type=Path, required=True)
    parser.add_argument("--transcript-index", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--template-index-out", type=Path)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    materialization = load_json(args.materialization)
    transcript_index = load_json(args.transcript_index) if args.transcript_index else None
    audit = audit_rank_zero_selmer_transcript_intake(
        materialization=materialization,
        transcript_index=transcript_index,
        root=args.root,
    )
    write_json(args.out, audit)
    if args.template_index_out:
        write_json(args.template_index_out, template_index(materialization))
    print(f"wrote rank-zero Selmer transcript intake audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"package_count={audit['package_count']}")
    print(f"transcript_package_ready_count={audit['transcript_package_ready_count']}")
    print(f"strict_promotion_ready_count={audit['strict_promotion_ready_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
