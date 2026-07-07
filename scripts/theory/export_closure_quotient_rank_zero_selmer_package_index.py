#!/usr/bin/env python3
"""Export rank-zero isogeny-Selmer proof package index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This exports reviewable task packages for the open rank-zero "
    "isogeny-Selmer obligations. It does not compute Selmer groups, prove rank "
    "zero, or prove any lambda-family exclusion."
)

REQUIRED_OUTPUT = (
    "reviewable transcript proving the uniform isogeny-Selmer rank upper bound "
    "for this family/kernel"
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


def _slug(value: str) -> str:
    return value.replace("+", "-").replace("_", "-")


def _packages(
    *,
    selmer_obligations: dict[str, Any],
    isogeny_templates: dict[str, Any],
) -> list[dict[str, Any]]:
    templates = dict(isogeny_templates.get("templates", {}))
    packages: list[dict[str, Any]] = []
    for family in selmer_obligations.get("families", []):
        family_pattern = str(family.get("pattern", ""))
        for kernel in family.get("required_kernel_obligations", []):
            kernel_name = str(kernel)
            template = templates.get(kernel_name, {})
            packages.append(
                {
                    "package_id": (
                        f"rank-zero-selmer-{_slug(family_pattern)}-"
                        f"{_slug(kernel_name)}"
                    ),
                    "family_pattern": family_pattern,
                    "kernel": kernel_name,
                    "candidate_class_count": int(
                        family.get("candidate_class_count", 0) or 0
                    ),
                    "model_count": int(family.get("model_count", 0) or 0),
                    "kernel_root": str(template.get("kernel_root", "")),
                    "target_a2": str(template.get("symbolic_a2", "")),
                    "target_a4": str(template.get("symbolic_a4", "")),
                    "required_output": REQUIRED_OUTPUT,
                    "status": "open",
                    "selmer_rank_upper_bound_proved": False,
                    "family_exclusion_proved": False,
                }
            )
    return packages


def export_rank_zero_selmer_package_index(
    *,
    selmer_obligations: dict[str, Any],
    isogeny_templates: dict[str, Any],
) -> dict[str, Any]:
    packages = _packages(
        selmer_obligations=selmer_obligations,
        isogeny_templates=isogeny_templates,
    )
    selmer_rank_upper_bound_proved_count = int(
        selmer_obligations.get("selmer_rank_upper_bound_proved_count", 0) or 0
    ) + int(isogeny_templates.get("selmer_rank_upper_bound_proved_count", 0) or 0)
    family_exclusion_proved_count = int(
        selmer_obligations.get("family_exclusion_proved_count", 0) or 0
    ) + int(isogeny_templates.get("family_exclusion_proved_count", 0) or 0)
    checks = {
        "selmer_obligations_ready": _ready(selmer_obligations),
        "isogeny_templates_ready": _ready(isogeny_templates),
        "package_count_matches_obligations": len(packages)
        == int(selmer_obligations.get("selmer_obligation_count", 0) or 0),
        "selmer_rank_upper_bound_count_zero": (
            selmer_rank_upper_bound_proved_count == 0
        ),
        "family_exclusion_claim_count_zero": family_exclusion_proved_count == 0,
        "search_count_rejected_as_progress": True,
    }
    violations = [name for name, passed in checks.items() if not passed]
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "package_count": len(packages),
        "open_package_count": sum(1 for package in packages if package["status"] == "open"),
        "selmer_rank_upper_bound_proved_count": selmer_rank_upper_bound_proved_count,
        "family_exclusion_proved_count": family_exclusion_proved_count,
        "search_count_used_as_progress": False,
        "packages": packages,
        "checks": checks,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selmer-obligations", type=Path, required=True)
    parser.add_argument("--isogeny-templates", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    index = export_rank_zero_selmer_package_index(
        selmer_obligations=load_json(args.selmer_obligations),
        isogeny_templates=load_json(args.isogeny_templates),
    )
    write_json(args.out, index)
    print(f"wrote rank-zero Selmer proof package index to {args.out}")
    print(f"status={index['status']}")
    print(f"package_count={index['package_count']}")
    print(f"open_package_count={index['open_package_count']}")
    print(
        "selmer_rank_upper_bound_proved_count="
        f"{index['selmer_rank_upper_bound_proved_count']}"
    )
    print(f"family_exclusion_proved_count={index['family_exclusion_proved_count']}")
    if args.strict and index["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
