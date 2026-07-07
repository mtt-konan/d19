#!/usr/bin/env python3
"""Audit proof obligations for the rank-zero lambda-family route."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits what remains before the rank-zero proof seeds can become "
    "lambda-family exclusion theorems. It does not prove rank zero, does not "
    "prove a no-point theorem, and does not count more individual samples as "
    "progress."
)

ACCEPTABLE_CLOSURE_ROUTES = [
    "uniform 2-isogeny or Selmer descent rank upper bound for the seed family",
    "or an external reviewable rank-zero theorem certificate for the seed family",
]

UNACCEPTABLE_PROGRESS = (
    "More individual scaled (A,B) rank rows are diagnostics only; they are not "
    "rank-zero family proof progress."
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


def _family_exclusion_count(*payloads: dict[str, Any]) -> int:
    return sum(_int_value(payload, "family_exclusion_proved_count") for payload in payloads)


def _rank_zero_priority_first(convergence_priorities: dict[str, Any]) -> bool:
    priority_order = list(convergence_priorities.get("priority_order", []))
    routes = list(convergence_priorities.get("routes", []))
    rank_zero_route = next(
        (route for route in routes if route.get("route") == "rank_zero"),
        {},
    )
    return (
        _ready(convergence_priorities)
        and priority_order[:1] == ["rank_zero"]
        and rank_zero_route.get("family_exclusion_proved") is False
        and rank_zero_route.get("missing_theorem")
        == "rank-zero primitive lambda family theorem"
    )


def _primitive_support_complete(
    *,
    primitive_models: dict[str, Any],
    identity_audit: dict[str, Any],
    invariants: dict[str, Any],
    forced_torsion: dict[str, Any],
) -> bool:
    model_count = _int_value(primitive_models, "model_count")
    return (
        _ready(primitive_models)
        and _ready(identity_audit)
        and _ready(invariants)
        and _ready(forced_torsion)
        and _int_value(identity_audit, "coefficient_identity_verified_count")
        == model_count
        and _int_value(identity_audit, "coefficient_identity_violation_count") == 0
        and _int_value(invariants, "primitive_model_count") == model_count
        and _int_value(invariants, "missing_primitive_model_count") == 0
        and invariants.get("all_matched_models_rank_zero") is True
        and invariants.get("all_matched_models_root_number_one") is True
        and invariants.get("all_matched_models_torsion_order_four") is True
        and _int_value(forced_torsion, "primitive_model_count") == model_count
        and _int_value(forced_torsion, "forced_full_two_torsion_count") == model_count
        and _int_value(forced_torsion, "forced_two_torsion_violation_count") == 0
        and _int_value(forced_torsion, "observed_extra_torsion_model_count") == 0
    )


def _groups(rank_zero_seeds: dict[str, Any]) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    for priority, group in enumerate(rank_zero_seeds.get("groups", []), start=1):
        groups.append(
            {
                "priority": priority,
                "pattern": str(group.get("pattern", "")),
                "candidate_class_count": _int_value(group, "candidate_class_count"),
                "model_count": _int_value(group, "model_count"),
                "model_counts_by_curve": group.get("model_counts_by_curve", {}),
                "already_checked_inputs": [
                    "coefficient identities",
                    "observed rank-zero invariant rows",
                    "forced full rational 2-torsion",
                ],
                "missing_theorem": "uniform rank-zero proof over the primitive lambda family",
                "acceptable_closure_routes": ACCEPTABLE_CLOSURE_ROUTES,
                "unacceptable_progress": UNACCEPTABLE_PROGRESS,
                "family_exclusion_proved": False,
            }
        )
    return groups


def audit_rank_zero_family_obligations(
    *,
    convergence_priorities: dict[str, Any],
    rank_zero_seeds: dict[str, Any],
    primitive_models: dict[str, Any],
    identity_audit: dict[str, Any],
    invariants: dict[str, Any],
    forced_torsion: dict[str, Any],
) -> dict[str, Any]:
    family_exclusion_proved_count = _family_exclusion_count(
        convergence_priorities,
        rank_zero_seeds,
        primitive_models,
        invariants,
        forced_torsion,
    )
    groups = _groups(rank_zero_seeds)
    checks = {
        "rank_zero_priority_first": _rank_zero_priority_first(convergence_priorities),
        "rank_zero_seed_groups_present": (
            _ready(rank_zero_seeds)
            and _int_value(rank_zero_seeds, "seed_group_count") == len(groups)
            and bool(groups)
        ),
        "primitive_support_complete": _primitive_support_complete(
            primitive_models=primitive_models,
            identity_audit=identity_audit,
            invariants=invariants,
            forced_torsion=forced_torsion,
        ),
        "group_boundaries_retained": all(
            group.get("family_exclusion_proved") is False
            for group in rank_zero_seeds.get("groups", [])
        ),
        "family_exclusion_claim_count_zero": family_exclusion_proved_count == 0,
        "sample_growth_rejected_as_progress": True,
    }
    violations = [name for name, passed in checks.items() if not passed]
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "rank_zero_family_proof_complete": False,
        "candidate_class_count": _int_value(rank_zero_seeds, "candidate_class_count"),
        "primitive_model_count": _int_value(primitive_models, "model_count"),
        "seed_group_count": len(groups),
        "rank_zero_family_obligation_count": len(groups),
        "open_obligation_count": len(groups),
        "family_exclusion_proved_count": family_exclusion_proved_count,
        "search_count_used_as_progress": False,
        "next_main_action": (
            "Prove a uniform rank-zero theorem for the AA, AA+BB, and BB "
            "primitive lambda seed groups."
        ),
        "groups": groups,
        "checks": checks,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--convergence-priorities", type=Path, required=True)
    parser.add_argument("--rank-zero-seeds", type=Path, required=True)
    parser.add_argument("--primitive-models", type=Path, required=True)
    parser.add_argument("--identity-audit", type=Path, required=True)
    parser.add_argument("--invariants", type=Path, required=True)
    parser.add_argument("--forced-torsion", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_family_obligations(
        convergence_priorities=load_json(args.convergence_priorities),
        rank_zero_seeds=load_json(args.rank_zero_seeds),
        primitive_models=load_json(args.primitive_models),
        identity_audit=load_json(args.identity_audit),
        invariants=load_json(args.invariants),
        forced_torsion=load_json(args.forced_torsion),
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient rank-zero family obligations to {args.out}")
    print(f"status={audit['status']}")
    print(f"rank_zero_family_proof_complete={audit['rank_zero_family_proof_complete']}")
    print(f"rank_zero_family_obligation_count={audit['rank_zero_family_obligation_count']}")
    print(f"family_exclusion_proved_count={audit['family_exclusion_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
