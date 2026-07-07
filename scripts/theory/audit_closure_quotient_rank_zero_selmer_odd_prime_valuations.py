#!/usr/bin/env python3
"""Audit odd-prime valuation shapes for rank-zero Selmer local cases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits symbolic odd-prime valuation-shape candidates for future "
    "rank-zero isogeny-Selmer local checks. It does not compute local Selmer "
    "images, prove local conditions, prove a Selmer rank bound, or prove any "
    "lambda-family exclusion."
)

CASE_LABELS = (
    "odd-prime-divides-L",
    "odd-prime-divides-T",
    "odd-prime-divides-T2-plus-4L2",
)

KERNEL_TEMPLATES: dict[str, dict[str, str]] = {
    "kernel_minus_p": {
        "target_a2": "32*L^2 - 8*T^2",
        "target_a4": "16*(T^2 + 4*L^2)^2",
        "quadratic_discriminant": "-1024*L^2*T^2",
    },
    "kernel_pos_2sqrt_q": {
        "target_a2": "-8*(T^2 + 8*L^2)",
        "target_a4": "16*T^4",
        "quadratic_discriminant": "1024*L^2*(T^2 + 4*L^2)",
    },
    "kernel_neg_2sqrt_q": {
        "target_a2": "16*(T^2 + 2*L^2)",
        "target_a4": "256*L^4",
        "quadratic_discriminant": "256*T^2*(T^2 + 4*L^2)",
    },
}

KERNEL_VALUATION_SHAPES: dict[str, dict[str, dict[str, str]]] = {
    "kernel_minus_p": {
        "odd-prime-divides-L": {
            "a2_valuation_shape": "v_ell(a2)=0; a2 == -8*T^2 mod ell",
            "a4_valuation_shape": "v_ell(a4)=0",
            "quadratic_discriminant_valuation_shape": (
                "v_ell(discriminant)=2*v_ell(L)"
            ),
            "unit_reason": (
                "ell is odd, ell | L, and coprime support gives ell not "
                "dividing T or T^2 + 4*L^2"
            ),
        },
        "odd-prime-divides-T": {
            "a2_valuation_shape": "v_ell(a2)=0; a2 == 32*L^2 mod ell",
            "a4_valuation_shape": "v_ell(a4)=0",
            "quadratic_discriminant_valuation_shape": (
                "v_ell(discriminant)=2*v_ell(T)"
            ),
            "unit_reason": (
                "ell is odd, ell | T, and coprime support gives ell not "
                "dividing L or T^2 + 4*L^2"
            ),
        },
        "odd-prime-divides-T2-plus-4L2": {
            "a2_valuation_shape": "v_ell(a2)=0; a2 == -16*T^2 mod ell",
            "a4_valuation_shape": "v_ell(a4)=2*v_ell(T^2 + 4*L^2)",
            "quadratic_discriminant_valuation_shape": "v_ell(discriminant)=0",
            "unit_reason": (
                "ell is odd, ell | T^2 + 4*L^2, and coprime support gives "
                "ell not dividing L or T"
            ),
        },
    },
    "kernel_pos_2sqrt_q": {
        "odd-prime-divides-L": {
            "a2_valuation_shape": "v_ell(a2)=0; a2 == -8*T^2 mod ell",
            "a4_valuation_shape": "v_ell(a4)=0",
            "quadratic_discriminant_valuation_shape": (
                "v_ell(discriminant)=2*v_ell(L)"
            ),
            "unit_reason": (
                "ell is odd, ell | L, and coprime support gives ell not "
                "dividing T or T^2 + 4*L^2"
            ),
        },
        "odd-prime-divides-T": {
            "a2_valuation_shape": "v_ell(a2)=0; a2 == -64*L^2 mod ell",
            "a4_valuation_shape": "v_ell(a4)=4*v_ell(T)",
            "quadratic_discriminant_valuation_shape": "v_ell(discriminant)=0",
            "unit_reason": (
                "ell is odd, ell | T, and coprime support gives ell not "
                "dividing L or T^2 + 4*L^2"
            ),
        },
        "odd-prime-divides-T2-plus-4L2": {
            "a2_valuation_shape": "v_ell(a2)=0; a2 == -32*L^2 mod ell",
            "a4_valuation_shape": "v_ell(a4)=0",
            "quadratic_discriminant_valuation_shape": (
                "v_ell(discriminant)=v_ell(T^2 + 4*L^2)"
            ),
            "unit_reason": (
                "ell is odd, ell | T^2 + 4*L^2, and coprime support gives "
                "ell not dividing L or T"
            ),
        },
    },
    "kernel_neg_2sqrt_q": {
        "odd-prime-divides-L": {
            "a2_valuation_shape": "v_ell(a2)=0; a2 == 16*T^2 mod ell",
            "a4_valuation_shape": "v_ell(a4)=4*v_ell(L)",
            "quadratic_discriminant_valuation_shape": "v_ell(discriminant)=0",
            "unit_reason": (
                "ell is odd, ell | L, and coprime support gives ell not "
                "dividing T or T^2 + 4*L^2"
            ),
        },
        "odd-prime-divides-T": {
            "a2_valuation_shape": "v_ell(a2)=0; a2 == 32*L^2 mod ell",
            "a4_valuation_shape": "v_ell(a4)=0",
            "quadratic_discriminant_valuation_shape": (
                "v_ell(discriminant)=2*v_ell(T)"
            ),
            "unit_reason": (
                "ell is odd, ell | T, and coprime support gives ell not "
                "dividing L or T^2 + 4*L^2"
            ),
        },
        "odd-prime-divides-T2-plus-4L2": {
            "a2_valuation_shape": "v_ell(a2)=0; a2 == -32*L^2 mod ell",
            "a4_valuation_shape": "v_ell(a4)=0",
            "quadratic_discriminant_valuation_shape": (
                "v_ell(discriminant)=v_ell(T^2 + 4*L^2)"
            ),
            "unit_reason": (
                "ell is odd, ell | T^2 + 4*L^2, and coprime support gives "
                "ell not dividing L or T"
            ),
        },
    },
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _ready(odd_prime_cases: dict[str, Any]) -> bool:
    return (
        odd_prime_cases.get("status") == "ok"
        and odd_prime_cases.get("ready") is True
    )


def _valuation_entry(row: dict[str, Any]) -> dict[str, Any]:
    kernel = str(row.get("kernel", ""))
    case_label = str(row.get("case_label", ""))
    template = KERNEL_TEMPLATES[kernel]
    shape = KERNEL_VALUATION_SHAPES[kernel][case_label]
    return {
        "package_id": str(row.get("package_id", "")),
        "kernel": kernel,
        "case_label": case_label,
        "prime_condition": str(row.get("prime_condition", "")),
        **template,
        **shape,
        "valuation_shape_status": "candidate",
        "local_condition_proved": False,
    }


def audit_rank_zero_selmer_odd_prime_valuations(
    *,
    odd_prime_cases: dict[str, Any],
) -> dict[str, Any]:
    case_entries = list(odd_prime_cases.get("case_entries", []))
    violations: list[str] = []
    if not _ready(odd_prime_cases):
        violations.append("odd_prime_cases_not_ready")
    if odd_prime_cases.get("case_checklist_not_proof") is not True:
        violations.append("case_checklist_boundary_missing")
    if int(odd_prime_cases.get("local_condition_proved_count", 0) or 0) != 0:
        violations.append("local_condition_claim_count_nonzero")

    unknown_kernels = sorted(
        {
            str(row.get("kernel", ""))
            for row in case_entries
            if str(row.get("kernel", "")) not in KERNEL_VALUATION_SHAPES
        }
    )
    if unknown_kernels:
        violations.append(f"unknown_kernels={unknown_kernels}")

    unknown_cases = sorted(
        {
            str(row.get("case_label", ""))
            for row in case_entries
            if str(row.get("case_label", "")) not in CASE_LABELS
        }
    )
    if unknown_cases:
        violations.append(f"unknown_case_labels={unknown_cases}")

    valuation_entries = [
        _valuation_entry(row)
        for row in case_entries
        if str(row.get("kernel", "")) in KERNEL_VALUATION_SHAPES
        and str(row.get("case_label", "")) in CASE_LABELS
    ]
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "package_count": int(odd_prime_cases.get("package_count", 0) or 0),
        "odd_prime_case_count": int(
            odd_prime_cases.get("odd_prime_case_count", 0) or 0
        ),
        "odd_prime_valuation_case_count": len(valuation_entries),
        "valuation_shapes_not_conditions": True,
        "kernel_valuation_shapes": KERNEL_VALUATION_SHAPES,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "valuation_entries": valuation_entries,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--odd-prime-cases", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_odd_prime_valuations(
        odd_prime_cases=load_json(args.odd_prime_cases),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer odd-prime valuation audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"package_count={audit['package_count']}")
    print(f"odd_prime_valuation_case_count={audit['odd_prime_valuation_case_count']}")
    print(f"local_condition_proved_count={audit['local_condition_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
