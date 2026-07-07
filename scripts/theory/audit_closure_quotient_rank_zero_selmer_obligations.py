#!/usr/bin/env python3
"""Audit open isogeny-Selmer obligations for rank-zero lambda families."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits the open isogeny-Selmer rank-bound obligations after the "
    "rank-zero isogeny templates have been verified. It does not compute "
    "Selmer groups, prove rank zero, or prove any lambda-family exclusion."
)

MISSING_THEOREM = "uniform isogeny-Selmer rank upper bound for every listed kernel"


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


def _kernel_names(isogeny_templates: dict[str, Any]) -> list[str]:
    verified_by_kernel = isogeny_templates.get("verified_by_kernel", {})
    return sorted(str(kernel) for kernel in verified_by_kernel)


def _families(
    *,
    family_obligations: dict[str, Any],
    kernel_names: list[str],
) -> list[dict[str, Any]]:
    families: list[dict[str, Any]] = []
    for group in family_obligations.get("groups", []):
        families.append(
            {
                "pattern": str(group.get("pattern", "")),
                "candidate_class_count": _int_value(group, "candidate_class_count"),
                "model_count": _int_value(group, "model_count"),
                "required_kernel_obligations": kernel_names,
                "missing_theorem": MISSING_THEOREM,
                "selmer_rank_upper_bound_proved": False,
                "family_exclusion_proved": False,
            }
        )
    return families


def audit_rank_zero_selmer_obligations(
    *,
    family_obligations: dict[str, Any],
    isogeny_templates: dict[str, Any],
) -> dict[str, Any]:
    kernel_names = _kernel_names(isogeny_templates)
    families = _families(
        family_obligations=family_obligations,
        kernel_names=kernel_names,
    )
    selmer_rank_upper_bound_proved_count = _int_value(
        isogeny_templates,
        "selmer_rank_upper_bound_proved_count",
    )
    family_exclusion_proved_count = (
        _int_value(family_obligations, "family_exclusion_proved_count")
        + _int_value(isogeny_templates, "family_exclusion_proved_count")
    )
    checks = {
        "family_obligations_ready": (
            _ready(family_obligations)
            and _int_value(family_obligations, "open_obligation_count") == len(families)
            and all(
                group.get("family_exclusion_proved") is False
                for group in family_obligations.get("groups", [])
            )
        ),
        "isogeny_templates_ready": (
            _ready(isogeny_templates)
            and _int_value(isogeny_templates, "isogeny_template_violation_count") == 0
            and _int_value(isogeny_templates, "kernel_count") == len(kernel_names)
            and _int_value(isogeny_templates, "isogeny_template_verified_count")
            == _int_value(isogeny_templates, "primitive_model_count") * len(kernel_names)
        ),
        "selmer_rank_upper_bound_count_zero": (
            selmer_rank_upper_bound_proved_count == 0
        ),
        "family_exclusion_claim_count_zero": family_exclusion_proved_count == 0,
        "search_count_rejected_as_progress": True,
    }
    violations = [name for name, passed in checks.items() if not passed]
    status = "ok" if not violations else "issues"
    selmer_obligation_count = len(families) * len(kernel_names)
    return {
        "status": status,
        "ready": status == "ok",
        "rank_zero_selmer_obligations_complete": False,
        "family_obligation_count": len(families),
        "kernel_count": len(kernel_names),
        "selmer_obligation_count": selmer_obligation_count,
        "open_selmer_obligation_count": selmer_obligation_count,
        "primitive_model_count": _int_value(isogeny_templates, "primitive_model_count"),
        "isogeny_template_verified_count": _int_value(
            isogeny_templates,
            "isogeny_template_verified_count",
        ),
        "selmer_rank_upper_bound_proved_count": selmer_rank_upper_bound_proved_count,
        "family_exclusion_proved_count": family_exclusion_proved_count,
        "search_count_used_as_progress": False,
        "families": families,
        "checks": checks,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family-obligations", type=Path, required=True)
    parser.add_argument("--isogeny-templates", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_obligations(
        family_obligations=load_json(args.family_obligations),
        isogeny_templates=load_json(args.isogeny_templates),
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient rank-zero Selmer obligations to {args.out}")
    print(f"status={audit['status']}")
    print(f"family_obligation_count={audit['family_obligation_count']}")
    print(f"kernel_count={audit['kernel_count']}")
    print(f"selmer_obligation_count={audit['selmer_obligation_count']}")
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
