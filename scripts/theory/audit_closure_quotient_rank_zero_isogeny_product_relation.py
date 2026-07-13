#!/usr/bin/env python3
"""Audit the common-source product relation among the three kernel coordinates."""

from __future__ import annotations

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits the common-source product relation among the three rank-zero "
    "2-isogeny target x-coordinates. It does not prove a local condition, "
    "prove a Selmer rank bound, prove rank zero, or prove any lambda-family "
    "exclusion."
)

ROOT_LABELS = {
    "kernel_minus_p": "-p",
    "kernel_pos_2sqrt_q": "2*sqrt_q",
    "kernel_neg_2sqrt_q": "-2*sqrt_q",
}

FORMULA_TEMPLATES = {
    "kernel_minus_p": {
        "denominator": "X-(-p)",
        "numerator": ["X-(2*sqrt_q)", "X-(-2*sqrt_q)"],
        "target_x_formula": "((X-(2*sqrt_q))*(X-(-2*sqrt_q)))/(X-(-p))",
        "exponents": {"-p": -1, "2*sqrt_q": 1, "-2*sqrt_q": 1},
    },
    "kernel_pos_2sqrt_q": {
        "denominator": "X-(2*sqrt_q)",
        "numerator": ["X-(-p)", "X-(-2*sqrt_q)"],
        "target_x_formula": "((X-(-p))*(X-(-2*sqrt_q)))/(X-(2*sqrt_q))",
        "exponents": {"-p": 1, "2*sqrt_q": -1, "-2*sqrt_q": 1},
    },
    "kernel_neg_2sqrt_q": {
        "denominator": "X-(-2*sqrt_q)",
        "numerator": ["X-(-p)", "X-(2*sqrt_q)"],
        "target_x_formula": "((X-(-p))*(X-(2*sqrt_q)))/(X-(-2*sqrt_q))",
        "exponents": {"-p": 1, "2*sqrt_q": 1, "-2*sqrt_q": -1},
    },
}


def _root_values(*, leg: int, total: int) -> dict[str, int]:
    p = 8 * leg * leg - 2 * total * total
    sqrt_q = total * total + 4 * leg * leg
    return {
        "-p": -p,
        "2*sqrt_q": 2 * sqrt_q,
        "-2*sqrt_q": -2 * sqrt_q,
    }


def _all_roots_once(exponents: dict[str, int]) -> bool:
    return all(int(exponents.get(label, 0)) == 1 for label in ("-p", "2*sqrt_q", "-2*sqrt_q"))


def audit_rank_zero_isogeny_product_relation(
    *,
    symbolic_inputs: dict[str, Any],
    source_shifts: dict[str, Any],
) -> dict[str, Any]:
    violations: list[dict[str, Any] | str] = []
    if (
        symbolic_inputs.get("status") != "ok"
        or symbolic_inputs.get("ready") is not True
        or int(symbolic_inputs.get("symbolic_formula_violation_count", 0) or 0) != 0
    ):
        violations.append("symbolic_inputs_not_ready")
    if (
        source_shifts.get("status") != "ok"
        or source_shifts.get("ready") is not True
        or int(source_shifts.get("source_shift_violation_count", 0) or 0) != 0
    ):
        violations.append("source_shifts_not_ready")

    models = list(symbolic_inputs.get("models", []))
    curve_counts: Counter[str] = Counter()
    product_relation_verified_count = 0

    summed_exponents = {"-p": 0, "2*sqrt_q": 0, "-2*sqrt_q": 0}
    for template in FORMULA_TEMPLATES.values():
        for label, exponent in template["exponents"].items():
            summed_exponents[label] += int(exponent)
    if not _all_roots_once(summed_exponents):
        violations.append(
            {
                "field": "product_exponents",
                "actual": summed_exponents,
                "expected": {"-p": 1, "2*sqrt_q": 1, "-2*sqrt_q": 1},
            }
        )

    sample_rows: list[dict[str, Any]] = []
    for model in models:
        curve = str(model.get("curve", ""))
        curve_counts[curve] += 1
        leg = int(model.get("leg", 0))
        total = int(model.get("total", 0))
        roots = _root_values(leg=leg, total=total)
        for kernel, template in FORMULA_TEMPLATES.items():
            denominator_label = ROOT_LABELS[kernel]
            numerator_labels = [
                label for label in ("-p", "2*sqrt_q", "-2*sqrt_q") if label != denominator_label
            ]
            if sample_rows.__len__() < 3:
                sample_rows.append(
                    {
                        "class": str(model.get("class", "")),
                        "curve": curve,
                        "kernel": kernel,
                        "denominator_root_value": roots[denominator_label],
                        "numerator_root_values": [roots[label] for label in numerator_labels],
                        "target_x_formula": template["target_x_formula"],
                    }
                )
        product_relation_verified_count += 1

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "primitive_model_count": len(models),
        "model_counts_by_curve": dict(sorted(curve_counts.items())),
        "kernel_count": len(FORMULA_TEMPLATES),
        "product_relation_verified_count": product_relation_verified_count,
        "common_source_relation": (
            "x_minus_p * x_pos_2sqrt_q * x_neg_2sqrt_q = "
            "(X-(-p))*(X-(2*sqrt_q))*(X-(-2*sqrt_q)) = Y^2"
        ),
        "product_exponents_by_kernel": {
            kernel: template["exponents"] for kernel, template in sorted(FORMULA_TEMPLATES.items())
        },
        "product_exponents_total": summed_exponents,
        "target_coordinate_formulas": FORMULA_TEMPLATES,
        "sample_rows": sample_rows,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbolic-inputs", type=Path, required=True)
    parser.add_argument("--source-shifts", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_isogeny_product_relation(
        symbolic_inputs=load_json(args.symbolic_inputs),
        source_shifts=load_json(args.source_shifts),
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient rank-zero isogeny product relation to {args.out}")
    print(f"status={audit['status']}")
    print(f"primitive_model_count={audit['primitive_model_count']}")
    print(f"product_relation_verified_count={audit['product_relation_verified_count']}")
    print(
        "selmer_rank_upper_bound_proved_count="
        f"{audit['selmer_rank_upper_bound_proved_count']}"
    )
    print(f"family_exclusion_proved_count={audit['family_exclusion_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
