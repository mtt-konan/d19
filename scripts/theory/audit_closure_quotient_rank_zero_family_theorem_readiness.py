#!/usr/bin/env python3
"""Audit readiness of rank-zero lambda-family theorem inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits the input chain for future rank-zero primitive lambda-family "
    "theorems. It does not prove local conditions, Selmer rank bounds, rank "
    "zero, no-point statements, or lambda-family exclusions."
)

ACCEPTABLE_NEXT_EVIDENCE = (
    "uniform isogeny-Selmer rank-bound transcript or external reviewable "
    "rank-zero theorem certificate"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _int(payload: dict[str, Any], key: str) -> int:
    return int(payload.get(key, 0) or 0)


def _sum_count(key: str, *payloads: dict[str, Any]) -> int:
    return sum(_int(payload, key) for payload in payloads)


def _readiness_rows(selmer_obligations: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for family in selmer_obligations.get("families", []):
        rows.append(
            {
                "pattern": str(family.get("pattern", "")),
                "candidate_class_count": _int(family, "candidate_class_count"),
                "model_count": _int(family, "model_count"),
                "required_kernel_obligations": list(
                    family.get("required_kernel_obligations", [])
                ),
                "acceptable_next_evidence": ACCEPTABLE_NEXT_EVIDENCE,
                "family_exclusion_proved": bool(
                    family.get("family_exclusion_proved", False)
                ),
            }
        )
    return rows


def _checks(
    *,
    lambda_handoff: dict[str, Any],
    family_obligations: dict[str, Any],
    symbolic_inputs: dict[str, Any],
    isogeny_templates: dict[str, Any],
    local_supports: dict[str, Any],
    selmer_obligations: dict[str, Any],
    transcript_intake: dict[str, Any],
) -> dict[str, bool]:
    primitive_model_count = _int(family_obligations, "primitive_model_count")
    selmer_obligation_count = _int(selmer_obligations, "selmer_obligation_count")
    package_count = _int(transcript_intake, "package_count")
    return {
        "lambda_rank_zero_route_ready": (
            _ready(lambda_handoff)
            and lambda_handoff.get("lambda_structural_handoff_ready") is True
            and lambda_handoff.get("closure_quotient_promoted_to_lambda_proof")
            is False
            and _int(
                lambda_handoff,
                "family_exclusion_proved_count",
            )
            == 0
        ),
        "family_obligations_ready": (
            _ready(family_obligations)
            and family_obligations.get("rank_zero_family_proof_complete") is False
            and _int(family_obligations, "open_obligation_count")
            == _int(family_obligations, "rank_zero_family_obligation_count")
        ),
        "symbolic_inputs_ready": (
            _ready(symbolic_inputs)
            and _int(symbolic_inputs, "primitive_model_count") == primitive_model_count
            and _int(symbolic_inputs, "symbolic_formula_violation_count") == 0
        ),
        "isogeny_templates_ready": (
            _ready(isogeny_templates)
            and _int(isogeny_templates, "primitive_model_count") == primitive_model_count
            and _int(isogeny_templates, "isogeny_template_violation_count") == 0
        ),
        "local_supports_remain_candidates": (
            _ready(local_supports)
            and local_supports.get("support_candidates_not_conditions") is True
            and _int(local_supports, "local_condition_proved_count") == 0
        ),
        "selmer_obligations_open": (
            _ready(selmer_obligations)
            and selmer_obligations.get("rank_zero_selmer_obligations_complete")
            is False
            and _int(selmer_obligations, "open_selmer_obligation_count")
            == selmer_obligation_count
        ),
        "transcripts_missing_not_proof": (
            _ready(transcript_intake)
            and transcript_intake.get("candidate_not_proof") is True
            and _int(transcript_intake, "open_package_count") == package_count
            and _int(transcript_intake, "missing_transcript_package_count")
            == package_count - _int(transcript_intake, "transcript_package_ready_count")
        ),
    }


def _violation_names(checks: dict[str, bool], *, local_supports: dict[str, Any]) -> list[str]:
    names = {
        "lambda_rank_zero_route_ready": "lambda_rank_zero_route_not_ready",
        "family_obligations_ready": "family_obligations_not_ready",
        "symbolic_inputs_ready": "symbolic_inputs_not_ready",
        "isogeny_templates_ready": "isogeny_templates_not_ready",
        "local_supports_remain_candidates": "local_supports_not_candidate_only",
        "selmer_obligations_open": "selmer_obligations_not_open",
        "transcripts_missing_not_proof": "transcript_intake_not_candidate_boundary",
    }
    violations = [names[name] for name, passed in checks.items() if not passed]
    if _int(local_supports, "local_condition_proved_count") != 0:
        violations = [
            "local_supports_promoted_to_conditions"
            if value == "local_supports_not_candidate_only"
            else value
            for value in violations
        ]
    return violations


def audit_rank_zero_family_theorem_readiness(
    *,
    lambda_handoff: dict[str, Any],
    family_obligations: dict[str, Any],
    symbolic_inputs: dict[str, Any],
    isogeny_templates: dict[str, Any],
    local_supports: dict[str, Any],
    selmer_obligations: dict[str, Any],
    transcript_intake: dict[str, Any],
) -> dict[str, Any]:
    checks = _checks(
        lambda_handoff=lambda_handoff,
        family_obligations=family_obligations,
        symbolic_inputs=symbolic_inputs,
        isogeny_templates=isogeny_templates,
        local_supports=local_supports,
        selmer_obligations=selmer_obligations,
        transcript_intake=transcript_intake,
    )
    boundary_counts = {
        "local_condition_proved_count": _sum_count(
            "local_condition_proved_count",
            local_supports,
        ),
        "selmer_rank_upper_bound_proved_count": _sum_count(
            "selmer_rank_upper_bound_proved_count",
            symbolic_inputs,
            isogeny_templates,
            local_supports,
            selmer_obligations,
            transcript_intake,
        ),
        "family_exclusion_proved_count": _sum_count(
            "family_exclusion_proved_count",
            lambda_handoff,
            family_obligations,
            symbolic_inputs,
            isogeny_templates,
            local_supports,
            selmer_obligations,
            transcript_intake,
        ),
    }
    boundary_ok = all(value == 0 for value in boundary_counts.values())
    violations = _violation_names(checks, local_supports=local_supports)
    if not boundary_ok and "local_supports_promoted_to_conditions" not in violations:
        violations.append("boundary_claim_count_nonzero")
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "rank_zero_input_chain_ready": status == "ok",
        "rank_zero_family_theorem_ready": False,
        "rank_zero_route_class_count": int(
            lambda_handoff.get("route_counts", {}).get(
                "rank-zero-family-generalization",
                0,
            )
            or 0
        ),
        "family_obligation_count": _int(
            family_obligations,
            "rank_zero_family_obligation_count",
        ),
        "primitive_model_count": _int(family_obligations, "primitive_model_count"),
        "selmer_obligation_count": _int(selmer_obligations, "selmer_obligation_count"),
        "open_selmer_obligation_count": _int(
            selmer_obligations,
            "open_selmer_obligation_count",
        ),
        "transcript_package_ready_count": _int(
            transcript_intake,
            "transcript_package_ready_count",
        ),
        "missing_transcript_package_count": _int(
            transcript_intake,
            "missing_transcript_package_count",
        ),
        "strict_promotion_ready_count": _int(
            transcript_intake,
            "strict_promotion_ready_count",
        ),
        **boundary_counts,
        "search_count_used_as_progress": False,
        "next_blocker": str(
            transcript_intake.get(
                "proof_status",
                "rank-zero-selmer-transcripts-missing-not-proof",
            )
        ),
        "readiness_rows": _readiness_rows(selmer_obligations),
        "checks": checks,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lambda-handoff", type=Path, required=True)
    parser.add_argument("--family-obligations", type=Path, required=True)
    parser.add_argument("--symbolic-inputs", type=Path, required=True)
    parser.add_argument("--isogeny-templates", type=Path, required=True)
    parser.add_argument("--local-supports", type=Path, required=True)
    parser.add_argument("--selmer-obligations", type=Path, required=True)
    parser.add_argument("--transcript-intake", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_family_theorem_readiness(
        lambda_handoff=load_json(args.lambda_handoff),
        family_obligations=load_json(args.family_obligations),
        symbolic_inputs=load_json(args.symbolic_inputs),
        isogeny_templates=load_json(args.isogeny_templates),
        local_supports=load_json(args.local_supports),
        selmer_obligations=load_json(args.selmer_obligations),
        transcript_intake=load_json(args.transcript_intake),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero family theorem readiness audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"rank_zero_input_chain_ready={audit['rank_zero_input_chain_ready']}")
    print(f"rank_zero_family_theorem_ready={audit['rank_zero_family_theorem_ready']}")
    print(f"missing_transcript_package_count={audit['missing_transcript_package_count']}")
    print(f"family_exclusion_proved_count={audit['family_exclusion_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
