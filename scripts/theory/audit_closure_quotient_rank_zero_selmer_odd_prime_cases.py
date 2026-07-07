#!/usr/bin/env python3
"""Audit odd-prime local case checklists for rank-zero Selmer packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits open odd-prime and 2-adic checklist cases for future "
    "rank-zero isogeny-Selmer transcripts. It does not compute local Selmer "
    "images, prove local conditions, prove a Selmer rank bound, or prove any "
    "lambda-family exclusion."
)

ODD_PRIME_CASES = [
    {
        "case_label": "odd-prime-divides-L",
        "prime_condition": "ell odd and ell | L",
    },
    {
        "case_label": "odd-prime-divides-T",
        "prime_condition": "ell odd and ell | T",
    },
    {
        "case_label": "odd-prime-divides-T2-plus-4L2",
        "prime_condition": "ell odd and ell | T^2 + 4*L^2",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _ready(coprime_supports: dict[str, Any]) -> bool:
    return (
        coprime_supports.get("status") == "ok"
        and coprime_supports.get("ready") is True
    )


def _case_entry(row: dict[str, Any], case: dict[str, str]) -> dict[str, Any]:
    return {
        "package_id": str(row.get("package_id", "")),
        "kernel": str(row.get("kernel", "")),
        "case_label": case["case_label"],
        "prime_condition": case["prime_condition"],
        "required_transcript_section": "local_squareclass_conditions",
        "case_status": "open",
        "local_condition_proved": False,
    }


def _two_adic_entry(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": str(row.get("package_id", "")),
        "kernel": str(row.get("kernel", "")),
        "case_label": "prime-2-adic",
        "prime_condition": "ell = 2",
        "required_transcript_section": "local_squareclass_conditions",
        "case_status": "open",
        "local_condition_proved": False,
    }


def audit_rank_zero_selmer_odd_prime_cases(
    *,
    coprime_supports: dict[str, Any],
) -> dict[str, Any]:
    entries = list(coprime_supports.get("entries", []))
    violations: list[str] = []
    if not _ready(coprime_supports):
        violations.append("coprime_supports_not_ready")
    if coprime_supports.get("two_adic_exception") is not True:
        violations.append("two_adic_exception_missing")
    if int(coprime_supports.get("local_condition_proved_count", 0) or 0) != 0:
        violations.append("local_condition_claim_count_nonzero")

    case_entries = [
        _case_entry(row, case)
        for row in entries
        for case in ODD_PRIME_CASES
    ]
    two_adic_entries = [_two_adic_entry(row) for row in entries]
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "package_count": int(coprime_supports.get("package_count", 0) or 0),
        "coprime_support_entry_count": int(
            coprime_supports.get("coprime_support_entry_count", 0) or 0
        ),
        "odd_prime_case_count": len(case_entries),
        "two_adic_case_count": len(two_adic_entries),
        "case_checklist_not_proof": True,
        "odd_prime_cases": ODD_PRIME_CASES,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "case_entries": case_entries,
        "two_adic_entries": two_adic_entries,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coprime-supports", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_odd_prime_cases(
        coprime_supports=load_json(args.coprime_supports),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer odd-prime case audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"package_count={audit['package_count']}")
    print(f"odd_prime_case_count={audit['odd_prime_case_count']}")
    print(f"two_adic_case_count={audit['two_adic_case_count']}")
    print(f"local_condition_proved_count={audit['local_condition_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
