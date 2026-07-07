#!/usr/bin/env python3
"""Audit algebraic identities behind rank-zero proof seeds."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits coefficient identities and forced p-signs for rank-zero proof "
    "seeds. It does not prove rank zero or a family exclusion theorem."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _expected_model(*, primitive_a: int, primitive_b: int, curve: str) -> dict[str, Any]:
    total = primitive_a + primitive_b
    leg = primitive_a if curve == "AA" else primitive_b
    sqrt_q = total * total + 4 * leg * leg
    p = 8 * leg * leg - 2 * total * total
    q = sqrt_q * sqrt_q
    return {
        "leg": leg,
        "total": total,
        "p": p,
        "q": q,
        "sqrt_q": sqrt_q,
        "weierstrass_model": [0, p, 0, -4 * q, -4 * p * q],
    }


def _observed_model(model: dict[str, Any]) -> dict[str, Any]:
    return {
        "leg": int(model.get("leg", 0)),
        "total": int(model.get("total", 0)),
        "p": int(model.get("p", 0)),
        "q": int(model.get("q", 0)),
        "sqrt_q": int(model.get("sqrt_q", 0)),
        "weierstrass_model": model.get("weierstrass_model", []),
    }


def _sign(value: int) -> str:
    if value < 0:
        return "negative"
    if value > 0:
        return "positive"
    return "zero"


def _primitive_ray(row: dict[str, Any], model: dict[str, Any]) -> tuple[int, int]:
    ray = row.get("unordered_primitive_ray", [])
    if len(ray) == 2:
        return int(ray[0]), int(ray[1])
    return int(model.get("primitive_A", 0)), int(model.get("primitive_B", 0))


def audit_rank_zero_seed_identities(
    primitive_models: dict[str, Any],
) -> dict[str, Any]:
    rows = list(primitive_models.get("primitive_model_rows", []))
    violations: list[dict[str, Any]] = []
    forced_p_sign_counts: dict[str, Counter[str]] = defaultdict(Counter)
    verified_count = 0
    model_count = 0

    for row in rows:
        for model in row.get("models", []):
            model_count += 1
            curve = str(model.get("curve", ""))
            primitive_a, primitive_b = _primitive_ray(row, model)
            expected = _expected_model(
                primitive_a=primitive_a,
                primitive_b=primitive_b,
                curve=curve,
            )
            observed = _observed_model(model)
            forced_p_sign_counts[curve][_sign(expected["p"])] += 1
            if observed == expected:
                verified_count += 1
            else:
                violations.append(
                    {
                        "class": str(row.get("class", "")),
                        "curve": curve,
                        "expected": expected,
                        "observed": observed,
                    }
                )

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "row_count": len(rows),
        "model_count": model_count,
        "coefficient_identity_verified_count": verified_count,
        "coefficient_identity_violation_count": len(violations),
        "forced_p_sign_counts_by_curve": {
            curve: dict(sorted(counts.items()))
            for curve, counts in sorted(forced_p_sign_counts.items())
        },
        "p_sign_novel_signal_count": 0,
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
    audit = audit_rank_zero_seed_identities(load_json(args.primitive_models))
    write_json(args.out, audit)
    print(f"wrote closure quotient rank-zero seed identity audit to {args.out}")
    print(f"status={audit['status']}")
    print(
        "coefficient_identity_verified_count="
        f"{audit['coefficient_identity_verified_count']}"
    )
    print(
        "coefficient_identity_violation_count="
        f"{audit['coefficient_identity_violation_count']}"
    )
    print(f"p_sign_novel_signal_count={audit['p_sign_novel_signal_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
