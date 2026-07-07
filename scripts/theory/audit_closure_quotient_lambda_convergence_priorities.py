#!/usr/bin/env python3
"""Audit the next lambda-family proof priorities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This turns the lambda proof-seed ledgers into a convergence priority "
    "audit. It does not prove any lambda-family exclusion theorem, and it does "
    "not count more search hits as progress."
)

RANK_ZERO_NEXT_ACTION = (
    "Prove the three rank-zero primitive lambda patterns as family theorems, "
    "using the coefficient identities, matched rank-zero invariants, and "
    "forced full rational 2-torsion as reviewable inputs."
)

ROOT_NUMBER_NEXT_ACTION = (
    "Use the root-number/rank patterns only as structural routing data; add a "
    "family rank, visibility, or descent argument before claiming no points."
)

TWO_COVER_NEXT_ACTION = (
    "Produce a family 2-cover/Selmer obstruction, or reviewable no-point "
    "certificates for every listed cover."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _int_value(payload: dict[str, Any], key: str) -> int:
    return int(payload.get(key, 0) or 0)


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _groups_keep_boundary(payload: dict[str, Any]) -> bool:
    return all(
        group.get("family_exclusion_proved") is False
        for group in payload.get("groups", [])
    )


def _two_cover_requires_strict_evidence(two_cover_seeds: dict[str, Any]) -> bool:
    groups = list(two_cover_seeds.get("groups", []))
    return bool(groups) and all(
        group.get("candidate_not_proof") is True
        and bool(group.get("required_strict_evidence"))
        and group.get("family_exclusion_proved") is False
        for group in groups
    )


def _family_exclusion_proved_count(*payloads: dict[str, Any]) -> int:
    return sum(_int_value(payload, "family_exclusion_proved_count") for payload in payloads)


def _rank_zero_support_ready(
    *,
    identity_audit: dict[str, Any],
    invariants: dict[str, Any],
    forced_torsion: dict[str, Any],
) -> bool:
    return (
        _ready(identity_audit)
        and _ready(invariants)
        and _ready(forced_torsion)
        and _int_value(identity_audit, "coefficient_identity_violation_count") == 0
        and invariants.get("all_matched_models_rank_zero") is True
        and invariants.get("all_matched_models_root_number_one") is True
        and invariants.get("all_matched_models_torsion_order_four") is True
        and _int_value(invariants, "missing_primitive_model_count") == 0
        and _int_value(forced_torsion, "forced_two_torsion_violation_count") == 0
        and _int_value(forced_torsion, "observed_extra_torsion_model_count") == 0
    )


def audit_lambda_convergence_priorities(
    *,
    proof_seed_coverage: dict[str, Any],
    rank_zero_seeds: dict[str, Any],
    rank_zero_identity_audit: dict[str, Any],
    rank_zero_invariants: dict[str, Any],
    rank_zero_forced_torsion: dict[str, Any],
    root_number_seeds: dict[str, Any],
    two_cover_seeds: dict[str, Any],
) -> dict[str, Any]:
    family_exclusion_count = _family_exclusion_proved_count(
        proof_seed_coverage,
        rank_zero_seeds,
        rank_zero_invariants,
        rank_zero_forced_torsion,
        root_number_seeds,
        two_cover_seeds,
    )
    checks = {
        "proof_seed_coverage_complete": (
            _ready(proof_seed_coverage)
            and proof_seed_coverage.get("all_routes_have_seed_ledgers") is True
            and proof_seed_coverage.get("search_count_used_as_progress") is False
        ),
        "rank_zero_support_ready": _rank_zero_support_ready(
            identity_audit=rank_zero_identity_audit,
            invariants=rank_zero_invariants,
            forced_torsion=rank_zero_forced_torsion,
        ),
        "rank_zero_boundary_retained": _groups_keep_boundary(rank_zero_seeds),
        "root_number_boundary_retained": _groups_keep_boundary(root_number_seeds),
        "two_cover_requires_strict_evidence": _two_cover_requires_strict_evidence(
            two_cover_seeds
        ),
        "family_exclusion_claim_count_zero": family_exclusion_count == 0,
        "search_count_rejected_as_progress": True,
    }
    violations = [
        name for name, passed in checks.items() if not passed
    ]

    routes = [
        {
            "route": "rank_zero",
            "priority": 1,
            "class_count": _int_value(rank_zero_seeds, "candidate_class_count"),
            "seed_group_count": _int_value(rank_zero_seeds, "seed_group_count"),
            "model_count": _int_value(rank_zero_seeds, "model_count"),
            "supporting_model_count": _int_value(
                rank_zero_identity_audit,
                "coefficient_identity_verified_count",
            ),
            "missing_theorem": "rank-zero primitive lambda family theorem",
            "next_action": RANK_ZERO_NEXT_ACTION,
            "family_exclusion_proved": False,
        },
        {
            "route": "root_number",
            "priority": 2,
            "class_count": _int_value(root_number_seeds, "target_class_count"),
            "seed_group_count": _int_value(root_number_seeds, "seed_group_count"),
            "target_pair_count": _int_value(root_number_seeds, "target_pair_count"),
            "missing_theorem": "family rank or descent argument beyond parity data",
            "next_action": ROOT_NUMBER_NEXT_ACTION,
            "family_exclusion_proved": False,
        },
        {
            "route": "two_cover",
            "priority": 3,
            "class_count": _int_value(two_cover_seeds, "target_class_count"),
            "seed_group_count": _int_value(two_cover_seeds, "seed_group_count"),
            "candidate_cover_total": _int_value(
                two_cover_seeds,
                "candidate_cover_total",
            ),
            "missing_theorem": "family 2-cover obstruction or cover-level no-point certificates",
            "next_action": TWO_COVER_NEXT_ACTION,
            "family_exclusion_proved": False,
        },
    ]
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "convergence_complete": False,
        "lambda_class_count": _int_value(proof_seed_coverage, "lambda_class_count"),
        "seed_ledger_class_count": _int_value(
            proof_seed_coverage,
            "seed_ledger_class_count",
        ),
        "total_seed_group_count": sum(route["seed_group_count"] for route in routes),
        "family_exclusion_proved_count": family_exclusion_count,
        "search_count_used_as_progress": False,
        "priority_order": [route["route"] for route in routes],
        "routes": routes,
        "checks": checks,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proof-seed-coverage", type=Path, required=True)
    parser.add_argument("--rank-zero-seeds", type=Path, required=True)
    parser.add_argument("--rank-zero-identity-audit", type=Path, required=True)
    parser.add_argument("--rank-zero-invariants", type=Path, required=True)
    parser.add_argument("--rank-zero-forced-torsion", type=Path, required=True)
    parser.add_argument("--root-number-seeds", type=Path, required=True)
    parser.add_argument("--two-cover-seeds", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_lambda_convergence_priorities(
        proof_seed_coverage=load_json(args.proof_seed_coverage),
        rank_zero_seeds=load_json(args.rank_zero_seeds),
        rank_zero_identity_audit=load_json(args.rank_zero_identity_audit),
        rank_zero_invariants=load_json(args.rank_zero_invariants),
        rank_zero_forced_torsion=load_json(args.rank_zero_forced_torsion),
        root_number_seeds=load_json(args.root_number_seeds),
        two_cover_seeds=load_json(args.two_cover_seeds),
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient lambda convergence priorities to {args.out}")
    print(f"status={audit['status']}")
    print(f"lambda_class_count={audit['lambda_class_count']}")
    print(f"priority_order={audit['priority_order']}")
    print(f"family_exclusion_proved_count={audit['family_exclusion_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
