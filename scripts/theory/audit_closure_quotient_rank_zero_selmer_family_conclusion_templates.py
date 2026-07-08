#!/usr/bin/env python3
"""Audit family-level rank-zero conclusions from Selmer kernel-bound packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits how package-level isogeny-Selmer bound tasks aggregate into "
    "family-level rank-zero conclusion templates. It does not prove a Selmer "
    "rank bound, prove rank zero, or prove any lambda-family exclusion."
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


def _family_package_prefix(pattern: str) -> str:
    return pattern.replace("+", "-")


def _package_id(pattern: str, kernel: str) -> str:
    suffix = kernel.removeprefix("kernel_").replace("_", "-")
    return f"rank-zero-selmer-{_family_package_prefix(pattern)}-kernel-{suffix}"


def _bridge_rows_by_package(transcript_bridge: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("package_id", "")): row
        for row in transcript_bridge.get("bridge_rows", [])
    }


def audit_rank_zero_selmer_family_conclusion_templates(
    *,
    selmer_obligations: dict[str, Any],
    transcript_bridge: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(selmer_obligations):
        violations.append("selmer_obligations_not_ready")
    if not _ready(transcript_bridge):
        violations.append("transcript_bridge_not_ready")

    bridge_rows = _bridge_rows_by_package(transcript_bridge)
    templates: list[dict[str, Any]] = []
    kernel_bound_package_count = 0

    for family in selmer_obligations.get("families", []):
        pattern = str(family.get("pattern", ""))
        required_packages: list[dict[str, Any]] = []
        for kernel in family.get("required_kernel_obligations", []):
            kernel_name = str(kernel)
            package_id = _package_id(pattern, kernel_name)
            bridge_row = bridge_rows.get(package_id)
            if bridge_row is None:
                violations.append(f"missing_family_kernel_package={pattern}:{kernel_name}")
                continue
            required_packages.append(
                {
                    "kernel": kernel_name,
                    "package_id": package_id,
                    "transcript_package_ready": bool(
                        bridge_row.get("transcript_package_ready", False)
                    ),
                }
            )
            kernel_bound_package_count += 1

        conclusion_ready = bool(required_packages) and all(
            row["transcript_package_ready"] for row in required_packages
        )
        templates.append(
            {
                "family_pattern": pattern,
                "candidate_class_count": int(
                    family.get("candidate_class_count", 0) or 0
                ),
                "model_count": int(family.get("model_count", 0) or 0),
                "required_kernel_count": len(
                    list(family.get("required_kernel_obligations", []))
                ),
                "required_kernel_bound_packages": required_packages,
                "rank_zero_conclusion_ready": conclusion_ready,
                "rank_zero_conclusion_proved": False,
                "remaining_transcript_field": "rank_zero_conclusion",
            }
        )

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "family_conclusion_template_count": len(templates),
        "kernel_bound_package_count": kernel_bound_package_count,
        "open_family_conclusion_count": sum(
            1 for row in templates if not row["rank_zero_conclusion_ready"]
        ),
        "rank_zero_conclusion_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "family_conclusion_templates": templates,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selmer-obligations", type=Path, required=True)
    parser.add_argument("--transcript-bridge", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_family_conclusion_templates(
        selmer_obligations=load_json(args.selmer_obligations),
        transcript_bridge=load_json(args.transcript_bridge),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer family-conclusion template audit to {args.out}")
    print(f"status={audit['status']}")
    print(
        "family_conclusion_template_count="
        f"{audit['family_conclusion_template_count']}"
    )
    print(f"kernel_bound_package_count={audit['kernel_bound_package_count']}")
    print(f"open_family_conclusion_count={audit['open_family_conclusion_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
