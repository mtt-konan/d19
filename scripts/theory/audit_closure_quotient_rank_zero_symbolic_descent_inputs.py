#!/usr/bin/env python3
"""Audit symbolic descent inputs for rank-zero primitive lambda families."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits uniform symbolic inputs for a future 2-isogeny/Selmer rank "
    "argument on the rank-zero primitive lambda families. It does not prove a "
    "Selmer bound, rank zero, or any lambda-family exclusion theorem."
)

FORMULA = {
    "variables": {
        "T": "primitive_A + primitive_B",
        "L": "primitive_A for AA, primitive_B for BB",
    },
    "p": "8*L^2 - 2*T^2",
    "sqrt_q": "T^2 + 4*L^2",
    "q": "sqrt_q^2",
    "two_torsion_roots": ["-2*sqrt_q", "-p", "2*sqrt_q"],
    "root_differences": {
        "(-p) - 2*sqrt_q": "-16*L^2",
        "(-p) - (-2*sqrt_q)": "4*T^2",
        "(2*sqrt_q) - (-2*sqrt_q)": "4*(T^2 + 4*L^2)",
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


def _leg(*, primitive_a: int, primitive_b: int, curve: str) -> int:
    return primitive_a if curve == "AA" else primitive_b


def _expected(*, primitive_a: int, primitive_b: int, curve: str) -> dict[str, Any]:
    total = primitive_a + primitive_b
    leg = _leg(primitive_a=primitive_a, primitive_b=primitive_b, curve=curve)
    sqrt_q = total * total + 4 * leg * leg
    p = 8 * leg * leg - 2 * total * total
    return {
        "leg": leg,
        "total": total,
        "p": p,
        "sqrt_q": sqrt_q,
        "q": sqrt_q * sqrt_q,
        "two_torsion_roots": sorted([-2 * sqrt_q, -p, 2 * sqrt_q]),
        "root_differences": {
            "minus_p_minus_pos_2sqrt_q": -p - 2 * sqrt_q,
            "minus_p_minus_neg_2sqrt_q": -p + 2 * sqrt_q,
            "pos_2sqrt_q_minus_neg_2sqrt_q": 4 * sqrt_q,
        },
        "expected_root_differences": {
            "minus_p_minus_pos_2sqrt_q": -16 * leg * leg,
            "minus_p_minus_neg_2sqrt_q": 4 * total * total,
            "pos_2sqrt_q_minus_neg_2sqrt_q": 4 * (total * total + 4 * leg * leg),
        },
        "squareclass_inputs": {
            "minus_p_minus_pos_2sqrt_q": "-1 times a square",
            "minus_p_minus_neg_2sqrt_q": "square",
            "pos_2sqrt_q_minus_neg_2sqrt_q": "4*(T^2 + 4*L^2)",
        },
    }


def audit_rank_zero_symbolic_descent_inputs(
    primitive_models: dict[str, Any],
) -> dict[str, Any]:
    rows = list(primitive_models.get("primitive_model_rows", []))
    violations: list[dict[str, Any]] = []
    curve_counts: Counter[str] = Counter()
    checked_models: list[dict[str, Any]] = []

    for row in rows:
        primitive_a, primitive_b = [
            int(value) for value in row.get("unordered_primitive_ray", [])
        ]
        for model in row.get("models", []):
            curve = str(model.get("curve", ""))
            curve_counts[curve] += 1
            expected = _expected(
                primitive_a=primitive_a,
                primitive_b=primitive_b,
                curve=curve,
            )
            observed = {
                "p": int(model.get("p", 0)),
                "sqrt_q": int(model.get("sqrt_q", 0)),
                "q": int(model.get("q", 0)),
                "two_torsion_roots": sorted(
                    [
                        -2 * int(model.get("sqrt_q", 0)),
                        -int(model.get("p", 0)),
                        2 * int(model.get("sqrt_q", 0)),
                    ]
                ),
            }
            expected_observed = {
                "p": expected["p"],
                "sqrt_q": expected["sqrt_q"],
                "q": expected["q"],
                "two_torsion_roots": expected["two_torsion_roots"],
            }
            root_differences_match = (
                expected["root_differences"]
                == expected["expected_root_differences"]
            )
            if observed != expected_observed or not root_differences_match:
                violations.append(
                    {
                        "class": str(row.get("class", "")),
                        "curve": curve,
                        "observed": observed,
                        "expected": expected_observed,
                        "root_differences": expected["root_differences"],
                        "expected_root_differences": expected[
                            "expected_root_differences"
                        ],
                    }
                )

            checked_models.append(
                {
                    "class": str(row.get("class", "")),
                    "curve": curve,
                    "leg": expected["leg"],
                    "total": expected["total"],
                    "root_differences": expected["root_differences"],
                    "squareclass_inputs": expected["squareclass_inputs"],
                    "selmer_rank_upper_bound_proved": False,
                    "family_exclusion_proved": False,
                }
            )

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "primitive_model_count": len(checked_models),
        "model_counts_by_curve": dict(sorted(curve_counts.items())),
        "symbolic_formula_verified_count": len(checked_models) - len(violations),
        "symbolic_formula_violation_count": len(violations),
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "formula": FORMULA,
        "models": checked_models,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primitive-models", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_symbolic_descent_inputs(
        load_json(args.primitive_models),
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient rank-zero symbolic descent inputs to {args.out}")
    print(f"status={audit['status']}")
    print(f"primitive_model_count={audit['primitive_model_count']}")
    print(f"symbolic_formula_verified_count={audit['symbolic_formula_verified_count']}")
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
