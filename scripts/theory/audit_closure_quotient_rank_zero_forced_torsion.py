#!/usr/bin/env python3
"""Audit forced rational 2-torsion in rank-zero primitive models."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits the rational 2-torsion forced by q being a square in the "
    "rank-zero primitive models. It does not prove rank zero or a lambda-family "
    "exclusion theorem."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _invariant_torsion_orders(
    certifying_invariants: dict[str, Any],
) -> dict[tuple[str, str], list[int]]:
    return {
        (str(row.get("class", "")), str(row.get("curve", ""))): [
            int(value) for value in row.get("torsion_orders", [])
        ]
        for row in certifying_invariants.get("models", [])
    }


def _forced_model(*, p: int, q: int) -> list[int]:
    return [0, p, 0, -4 * q, -4 * p * q]


def audit_forced_torsion(
    *,
    primitive_models: dict[str, Any],
    certifying_invariants: dict[str, Any],
) -> dict[str, Any]:
    torsion_orders_by_model = _invariant_torsion_orders(certifying_invariants)
    models: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []

    for row in primitive_models.get("primitive_model_rows", []):
        class_name = str(row.get("class", ""))
        for model in row.get("models", []):
            curve = str(model.get("curve", ""))
            p = int(model.get("p", 0))
            q = int(model.get("q", 0))
            sqrt_q = int(model.get("sqrt_q", 0))
            expected_model = _forced_model(p=p, q=q)
            observed_model = model.get("weierstrass_model", [])
            if observed_model != expected_model:
                violations.append(
                    {
                        "class": class_name,
                        "curve": curve,
                        "expected_model": expected_model,
                        "observed_model": observed_model,
                    }
                )

            observed_torsion_orders = torsion_orders_by_model.get(
                (class_name, curve),
                [],
            )
            observed_extra_torsion = any(order != 4 for order in observed_torsion_orders)
            models.append(
                {
                    "class": class_name,
                    "curve": curve,
                    "p": p,
                    "sqrt_q": sqrt_q,
                    "two_torsion_x_roots": sorted([-2 * sqrt_q, -p, 2 * sqrt_q]),
                    "forced_two_torsion_status": (
                        "full-rational-2-torsion-forced"
                        if sqrt_q * sqrt_q == q and observed_model == expected_model
                        else "forced-two-torsion-identity-issue"
                    ),
                    "observed_torsion_orders": observed_torsion_orders,
                    "observed_extra_torsion": observed_extra_torsion,
                    "family_exclusion_proved": False,
                }
            )

    forced_count = sum(
        1
        for model in models
        if model["forced_two_torsion_status"] == "full-rational-2-torsion-forced"
    )
    exact_order_four_count = sum(
        1 for model in models if model["observed_torsion_orders"] == [4]
    )
    extra_torsion_count = sum(1 for model in models if model["observed_extra_torsion"])
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "primitive_model_count": len(models),
        "forced_full_two_torsion_count": forced_count,
        "forced_two_torsion_violation_count": len(violations),
        "observed_exact_torsion_order_four_count": exact_order_four_count,
        "observed_extra_torsion_model_count": extra_torsion_count,
        "family_exclusion_proved_count": 0,
        "models": models,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primitive-models", type=Path, required=True)
    parser.add_argument("--certifying-invariants", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_forced_torsion(
        primitive_models=load_json(args.primitive_models),
        certifying_invariants=load_json(args.certifying_invariants),
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient rank-zero forced torsion audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"primitive_model_count={audit['primitive_model_count']}")
    print(f"forced_full_two_torsion_count={audit['forced_full_two_torsion_count']}")
    print(
        "observed_exact_torsion_order_four_count="
        f"{audit['observed_exact_torsion_order_four_count']}"
    )
    print(f"family_exclusion_proved_count={audit['family_exclusion_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
