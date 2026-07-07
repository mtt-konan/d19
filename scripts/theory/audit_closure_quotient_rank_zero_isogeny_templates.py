#!/usr/bin/env python3
"""Audit 2-isogeny target templates for rank-zero primitive families."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits symbolic 2-isogeny target templates for the rank-zero "
    "primitive lambda families. It does not compute Selmer groups, prove a rank "
    "upper bound, or prove any lambda-family exclusion theorem."
)

TEMPLATES = {
    "kernel_minus_p": {
        "kernel_root": "-p",
        "target_model": "y^2 = x^3 + 4p*x^2 + 16*sqrt_q^2*x",
        "symbolic_a2": "32*L^2 - 8*T^2",
        "symbolic_a4": "16*(T^2 + 4*L^2)^2",
        "a4_square": "(4*(T^2 + 4*L^2))^2",
    },
    "kernel_pos_2sqrt_q": {
        "kernel_root": "2*sqrt_q",
        "target_model": "y^2 = x^3 + (-2p - 12*sqrt_q)*x^2 + (p - 2*sqrt_q)^2*x",
        "symbolic_a2": "-8*(T^2 + 8*L^2)",
        "symbolic_a4": "16*T^4",
        "a4_square": "(4*T^2)^2",
    },
    "kernel_neg_2sqrt_q": {
        "kernel_root": "-2*sqrt_q",
        "target_model": "y^2 = x^3 + (-2p + 12*sqrt_q)*x^2 + (p + 2*sqrt_q)^2*x",
        "symbolic_a2": "16*(T^2 + 2*L^2)",
        "symbolic_a4": "256*L^4",
        "a4_square": "(16*L^2)^2",
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


def _expected_targets(*, leg: int, total: int) -> dict[str, dict[str, int]]:
    p = 8 * leg * leg - 2 * total * total
    sqrt_q = total * total + 4 * leg * leg
    return {
        "kernel_minus_p": {
            "a2": 4 * p,
            "a4": 16 * sqrt_q * sqrt_q,
            "a4_square_root_abs": 4 * sqrt_q,
        },
        "kernel_pos_2sqrt_q": {
            "a2": -2 * p - 12 * sqrt_q,
            "a4": (p - 2 * sqrt_q) ** 2,
            "a4_square_root_abs": abs(p - 2 * sqrt_q),
        },
        "kernel_neg_2sqrt_q": {
            "a2": -2 * p + 12 * sqrt_q,
            "a4": (p + 2 * sqrt_q) ** 2,
            "a4_square_root_abs": abs(p + 2 * sqrt_q),
        },
    }


def _symbolic_targets(*, leg: int, total: int) -> dict[str, dict[str, int]]:
    return {
        "kernel_minus_p": {
            "a2": 32 * leg * leg - 8 * total * total,
            "a4": 16 * (total * total + 4 * leg * leg) ** 2,
            "a4_square_root_abs": 4 * (total * total + 4 * leg * leg),
        },
        "kernel_pos_2sqrt_q": {
            "a2": -8 * (total * total + 8 * leg * leg),
            "a4": 16 * total**4,
            "a4_square_root_abs": 4 * total * total,
        },
        "kernel_neg_2sqrt_q": {
            "a2": 16 * (total * total + 2 * leg * leg),
            "a4": 256 * leg**4,
            "a4_square_root_abs": 16 * leg * leg,
        },
    }


def audit_rank_zero_isogeny_templates(
    symbolic_inputs: dict[str, Any],
) -> dict[str, Any]:
    models = list(symbolic_inputs.get("models", []))
    violations: list[dict[str, Any]] = []
    curve_counts: Counter[str] = Counter()
    verified_by_kernel: Counter[str] = Counter()

    for model in models:
        curve = str(model.get("curve", ""))
        curve_counts[curve] += 1
        leg = int(model.get("leg", 0))
        total = int(model.get("total", 0))
        expected = _expected_targets(leg=leg, total=total)
        symbolic = _symbolic_targets(leg=leg, total=total)
        for kernel, expected_target in expected.items():
            symbolic_target = symbolic[kernel]
            if expected_target != symbolic_target:
                violations.append(
                    {
                        "class": str(model.get("class", "")),
                        "curve": curve,
                        "kernel": kernel,
                        "expected": expected_target,
                        "symbolic": symbolic_target,
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
    kernel_count = len(TEMPLATES)
    return {
        "status": status,
        "ready": status == "ok",
        "primitive_model_count": len(models),
        "kernel_count": kernel_count,
        "isogeny_template_check_count": len(models) * kernel_count,
        "isogeny_template_verified_count": sum(verified_by_kernel.values()),
        "isogeny_template_violation_count": len(violations),
        "verified_by_kernel": {
            kernel: int(verified_by_kernel.get(kernel, 0))
            for kernel in sorted(TEMPLATES)
        },
        "model_counts_by_curve": dict(sorted(curve_counts.items())),
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
    audit = audit_rank_zero_isogeny_templates(load_json(args.symbolic_inputs))
    write_json(args.out, audit)
    print(f"wrote closure quotient rank-zero isogeny templates to {args.out}")
    print(f"status={audit['status']}")
    print(f"primitive_model_count={audit['primitive_model_count']}")
    print(f"isogeny_template_verified_count={audit['isogeny_template_verified_count']}")
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
