#!/usr/bin/env python3
"""Audit symbolic local-support candidates for rank-zero Selmer packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits symbolic support candidates for future rank-zero "
    "isogeny-Selmer local conditions. It does not compute local Selmer images, "
    "prove a Selmer rank bound, prove rank zero, or prove any lambda-family "
    "exclusion."
)

CANDIDATE_BAD_FACTORS = ["2", "L", "T", "T^2 + 4*L^2"]

SUPPORT_TEMPLATES: dict[str, dict[str, str | list[str]]] = {
    "kernel_minus_p": {
        "target_a2": "32*L^2 - 8*T^2",
        "target_a4": "16*(T^2 + 4*L^2)^2",
        "a4_square_root": "4*(T^2 + 4*L^2)",
        "quadratic_discriminant": "-1024*L^2*T^2",
        "quadratic_discriminant_squareclass": "-1",
        "candidate_bad_factors": CANDIDATE_BAD_FACTORS,
    },
    "kernel_pos_2sqrt_q": {
        "target_a2": "-8*(T^2 + 8*L^2)",
        "target_a4": "16*T^4",
        "a4_square_root": "4*T^2",
        "quadratic_discriminant": "1024*L^2*(T^2 + 4*L^2)",
        "quadratic_discriminant_squareclass": "T^2 + 4*L^2",
        "candidate_bad_factors": CANDIDATE_BAD_FACTORS,
    },
    "kernel_neg_2sqrt_q": {
        "target_a2": "16*(T^2 + 2*L^2)",
        "target_a4": "256*L^4",
        "a4_square_root": "16*L^2",
        "quadratic_discriminant": "256*T^2*(T^2 + 4*L^2)",
        "quadratic_discriminant_squareclass": "T^2 + 4*L^2",
        "candidate_bad_factors": CANDIDATE_BAD_FACTORS,
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


def _package_index_ready(package_index: dict[str, Any]) -> bool:
    return package_index.get("status") == "ok" and package_index.get("ready") is True


def _support_entry(package: dict[str, Any]) -> dict[str, Any]:
    kernel = str(package.get("kernel", ""))
    template = dict(SUPPORT_TEMPLATES[kernel])
    return {
        "package_id": str(package.get("package_id", "")),
        "family_pattern": str(package.get("family_pattern", "")),
        "kernel": kernel,
        "status": str(package.get("status", "")),
        **template,
        "support_candidates_not_conditions": True,
        "local_condition_proved": False,
        "selmer_rank_upper_bound_proved": False,
        "family_exclusion_proved": False,
    }


def audit_rank_zero_selmer_local_supports(
    *,
    package_index: dict[str, Any],
) -> dict[str, Any]:
    packages = list(package_index.get("packages", []))
    violations: list[str] = []
    if not _package_index_ready(package_index):
        violations.append("package_index_not_ready")
    unknown_kernels = sorted(
        {
            str(package.get("kernel", ""))
            for package in packages
            if str(package.get("kernel", "")) not in SUPPORT_TEMPLATES
        }
    )
    if unknown_kernels:
        violations.append(f"unknown_kernels={unknown_kernels}")

    support_entries = [
        _support_entry(package)
        for package in packages
        if str(package.get("kernel", "")) in SUPPORT_TEMPLATES
    ]
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "package_count": len(packages),
        "support_entry_count": len(support_entries),
        "kernel_count": len(SUPPORT_TEMPLATES),
        "support_factor_template": CANDIDATE_BAD_FACTORS,
        "support_candidates_not_conditions": True,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "support_entries": support_entries,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-index", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_local_supports(
        package_index=load_json(args.package_index),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer local-support audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"package_count={audit['package_count']}")
    print(f"support_entry_count={audit['support_entry_count']}")
    print(f"local_condition_proved_count={audit['local_condition_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
