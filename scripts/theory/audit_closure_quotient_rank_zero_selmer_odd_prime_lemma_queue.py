#!/usr/bin/env python3
"""Audit uniform odd-prime local lemma obligations for rank-zero Selmer cases."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This groups symbolic odd-prime valuation-shape candidates into uniform "
    "local lemma obligations. It does not prove local lemmas, compute local "
    "Selmer images, prove local conditions, prove a Selmer rank bound, or "
    "prove any lambda-family exclusion."
)

CASE_SUFFIXES = {
    "odd-prime-divides-L": "divides-L",
    "odd-prime-divides-T": "divides-T",
    "odd-prime-divides-T2-plus-4L2": "divides-T2-plus-4L2",
}

SIGNATURE_FIELDS = (
    "kernel",
    "case_label",
    "prime_condition",
    "target_a2",
    "target_a4",
    "quadratic_discriminant",
    "a2_valuation_shape",
    "a4_valuation_shape",
    "quadratic_discriminant_valuation_shape",
    "unit_reason",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _ready(odd_prime_valuations: dict[str, Any]) -> bool:
    return (
        odd_prime_valuations.get("status") == "ok"
        and odd_prime_valuations.get("ready") is True
    )


def _lemma_id(kernel: str, case_label: str) -> str:
    kernel_slug = kernel.replace("_", "-")
    case_suffix = CASE_SUFFIXES.get(case_label, case_label)
    return f"odd-prime-lemma-{kernel_slug}-{case_suffix}"


def _signature(row: dict[str, Any]) -> tuple[str, ...]:
    return tuple(str(row.get(field, "")) for field in SIGNATURE_FIELDS)


def _obligation(rows: list[dict[str, Any]]) -> dict[str, Any]:
    first = rows[0]
    kernel = str(first.get("kernel", ""))
    case_label = str(first.get("case_label", ""))
    package_ids = sorted({str(row.get("package_id", "")) for row in rows})
    return {
        "lemma_id": _lemma_id(kernel, case_label),
        "kernel": kernel,
        "case_label": case_label,
        "prime_condition": str(first.get("prime_condition", "")),
        "target_a2": str(first.get("target_a2", "")),
        "target_a4": str(first.get("target_a4", "")),
        "quadratic_discriminant": str(first.get("quadratic_discriminant", "")),
        "a2_valuation_shape": str(first.get("a2_valuation_shape", "")),
        "a4_valuation_shape": str(first.get("a4_valuation_shape", "")),
        "quadratic_discriminant_valuation_shape": str(
            first.get("quadratic_discriminant_valuation_shape", "")
        ),
        "unit_reason": str(first.get("unit_reason", "")),
        "covered_valuation_case_count": len(rows),
        "package_ids": package_ids,
        "uniform_over_packages": True,
        "required_transcript_section": "local_squareclass_conditions",
        "next_review_task": (
            "prove this valuation shape gives the required local squareclass "
            "condition for arbitrary primitive A:B"
        ),
        "proof_status": "open",
        "local_lemma_proved": False,
        "local_condition_proved": False,
    }


def audit_rank_zero_selmer_odd_prime_lemma_queue(
    *,
    odd_prime_valuations: dict[str, Any],
) -> dict[str, Any]:
    valuation_entries = list(odd_prime_valuations.get("valuation_entries", []))
    violations: list[str] = []
    if not _ready(odd_prime_valuations):
        violations.append("odd_prime_valuations_not_ready")
    if odd_prime_valuations.get("valuation_shapes_not_conditions") is not True:
        violations.append("valuation_boundary_missing")
    if int(odd_prime_valuations.get("local_condition_proved_count", 0) or 0) != 0:
        violations.append("local_condition_claim_count_nonzero")

    grouped: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in valuation_entries:
        grouped[_signature(row)].append(row)

    lemma_obligations = sorted(
        (_obligation(rows) for rows in grouped.values()),
        key=lambda row: (str(row["kernel"]), str(row["case_label"])),
    )
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "package_count": int(odd_prime_valuations.get("package_count", 0) or 0),
        "input_valuation_case_count": len(valuation_entries),
        "lemma_obligation_count": len(lemma_obligations),
        "lemma_queue_not_proof": True,
        "local_lemma_proved_count": 0,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "lemma_obligations": lemma_obligations,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--odd-prime-valuations", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_odd_prime_lemma_queue(
        odd_prime_valuations=load_json(args.odd_prime_valuations),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer odd-prime lemma queue audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"input_valuation_case_count={audit['input_valuation_case_count']}")
    print(f"lemma_obligation_count={audit['lemma_obligation_count']}")
    print(f"local_lemma_proved_count={audit['local_lemma_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
