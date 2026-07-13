#!/usr/bin/env python3
"""Audit source-root shifts behind the rank-zero 2-isogeny templates."""

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
    "This audits the source-root shift formulas behind the rank-zero 2-isogeny "
    "templates. It does not compute Selmer groups, prove a local condition, "
    "prove a Selmer rank bound, prove rank zero, or prove any lambda-family "
    "exclusion."
)

TEMPLATES = {
    "kernel_minus_p": {
        "kernel_root": "-p",
        "shifted_source_model": "y^2 = x*(x - 16*L^2)*(x + 4*T^2)",
        "relative_roots": ["16*L^2", "-4*T^2"],
        "source_a2": "4*T^2 - 16*L^2",
        "source_a4": "-64*L^2*T^2",
        "target_a2_relation": "-2*source_a2",
        "target_a4_relation": "source_a2^2 - 4*source_a4 = 16*(T^2 + 4*L^2)^2",
    },
    "kernel_pos_2sqrt_q": {
        "kernel_root": "2*sqrt_q",
        "shifted_source_model": "y^2 = x*(x + 16*L^2)*(x + 4*(T^2 + 4*L^2))",
        "relative_roots": ["-16*L^2", "-4*(T^2 + 4*L^2)"],
        "source_a2": "4*T^2 + 32*L^2",
        "source_a4": "64*L^2*(T^2 + 4*L^2)",
        "target_a2_relation": "-2*source_a2",
        "target_a4_relation": "source_a2^2 - 4*source_a4 = 16*T^4",
    },
    "kernel_neg_2sqrt_q": {
        "kernel_root": "-2*sqrt_q",
        "shifted_source_model": "y^2 = x*(x - 4*T^2)*(x - 4*(T^2 + 4*L^2))",
        "relative_roots": ["4*T^2", "4*(T^2 + 4*L^2)"],
        "source_a2": "-(8*T^2 + 16*L^2)",
        "source_a4": "16*T^2*(T^2 + 4*L^2)",
        "target_a2_relation": "-2*source_a2",
        "target_a4_relation": "source_a2^2 - 4*source_a4 = 256*L^4",
    },
}


def _root_values(*, leg: int, total: int) -> dict[str, int]:
    p = 8 * leg * leg - 2 * total * total
    sqrt_q = total * total + 4 * leg * leg
    return {
        "kernel_minus_p": -p,
        "kernel_pos_2sqrt_q": 2 * sqrt_q,
        "kernel_neg_2sqrt_q": -2 * sqrt_q,
    }


def _expected_shift_data(*, leg: int, total: int) -> dict[str, dict[str, int]]:
    roots = _root_values(leg=leg, total=total)
    kernel_order = [
        "kernel_minus_p",
        "kernel_pos_2sqrt_q",
        "kernel_neg_2sqrt_q",
    ]
    expected: dict[str, dict[str, int]] = {}
    for kernel in kernel_order:
        e = roots[kernel]
        others = [roots[name] for name in kernel_order if name != kernel]
        r1 = others[0] - e
        r2 = others[1] - e
        source_a2 = -(r1 + r2)
        source_a4 = r1 * r2
        target_a2 = -2 * source_a2
        target_a4 = source_a2 * source_a2 - 4 * source_a4
        expected[kernel] = {
            "relative_root_1": r1,
            "relative_root_2": r2,
            "source_a2": source_a2,
            "source_a4": source_a4,
            "target_a2": target_a2,
            "target_a4": target_a4,
        }
    return expected


def _symbolic_shift_data(*, leg: int, total: int) -> dict[str, dict[str, int]]:
    return {
        "kernel_minus_p": {
            "relative_root_1": 16 * leg * leg,
            "relative_root_2": -4 * total * total,
            "source_a2": 4 * total * total - 16 * leg * leg,
            "source_a4": -64 * leg * leg * total * total,
            "target_a2": 32 * leg * leg - 8 * total * total,
            "target_a4": 16 * (total * total + 4 * leg * leg) ** 2,
        },
        "kernel_pos_2sqrt_q": {
            "relative_root_1": -16 * leg * leg,
            "relative_root_2": -4 * (total * total + 4 * leg * leg),
            "source_a2": 4 * total * total + 32 * leg * leg,
            "source_a4": 64 * leg * leg * (total * total + 4 * leg * leg),
            "target_a2": -8 * (total * total + 8 * leg * leg),
            "target_a4": 16 * total**4,
        },
        "kernel_neg_2sqrt_q": {
            "relative_root_1": 4 * total * total,
            "relative_root_2": 4 * (total * total + 4 * leg * leg),
            "source_a2": -(8 * total * total + 16 * leg * leg),
            "source_a4": 16 * total * total * (total * total + 4 * leg * leg),
            "target_a2": 16 * (total * total + 2 * leg * leg),
            "target_a4": 256 * leg**4,
        },
    }


def audit_rank_zero_isogeny_source_shifts(
    symbolic_inputs: dict[str, Any],
) -> dict[str, Any]:
    models = list(symbolic_inputs.get("models", []))
    violations: list[dict[str, Any]] = []
    verified_by_kernel: Counter[str] = Counter()
    curve_counts: Counter[str] = Counter()

    for model in models:
        curve = str(model.get("curve", ""))
        curve_counts[curve] += 1
        leg = int(model.get("leg", 0))
        total = int(model.get("total", 0))
        expected = _expected_shift_data(leg=leg, total=total)
        symbolic = _symbolic_shift_data(leg=leg, total=total)
        for kernel, expected_row in expected.items():
            symbolic_row = symbolic[kernel]
            if expected_row != symbolic_row:
                violations.append(
                    {
                        "class": str(model.get("class", "")),
                        "curve": curve,
                        "kernel": kernel,
                        "expected": expected_row,
                        "symbolic": symbolic_row,
                    }
                )
            else:
                verified_by_kernel[kernel] += 1

    if (
        symbolic_inputs.get("status") != "ok"
        or symbolic_inputs.get("ready") is not True
        or int(symbolic_inputs.get("symbolic_formula_violation_count", 0) or 0) != 0
    ):
        violations.append(
            {
                "field": "symbolic_inputs",
                "status": symbolic_inputs.get("status"),
                "ready": symbolic_inputs.get("ready"),
                "symbolic_formula_violation_count": int(
                    symbolic_inputs.get("symbolic_formula_violation_count", 0) or 0
                ),
            }
        )

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "primitive_model_count": len(models),
        "kernel_count": len(TEMPLATES),
        "source_shift_check_count": len(models) * len(TEMPLATES),
        "source_shift_verified_count": sum(verified_by_kernel.values()),
        "source_shift_violation_count": len(violations),
        "verified_by_kernel": {
            kernel: int(verified_by_kernel.get(kernel, 0))
            for kernel in sorted(TEMPLATES)
        },
        "model_counts_by_curve": dict(sorted(curve_counts.items())),
        "global_relation_search_layer": (
            "source differences X-(-p), X-(2*sqrt_q), X-(-2*sqrt_q)"
        ),
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "symbolic_inputs_ready": status == "ok",
        "templates": TEMPLATES,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbolic-inputs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_isogeny_source_shifts(load_json(args.symbolic_inputs))
    write_json(args.out, audit)
    print(f"wrote closure quotient rank-zero isogeny source shifts to {args.out}")
    print(f"status={audit['status']}")
    print(f"primitive_model_count={audit['primitive_model_count']}")
    print(f"source_shift_verified_count={audit['source_shift_verified_count']}")
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
