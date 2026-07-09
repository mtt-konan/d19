#!/usr/bin/env python3
"""Audit lower bounds for killing AA+BB common-source 2-primary patterns."""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits combinatorial lower bounds for killing the 16 AA+BB common-"
    "source 2-primary patterns by independent per-kernel dyadic class "
    "exclusions. It does not prove any actual dyadic local condition, Selmer "
    "lift, Selmer rank bound, rank zero, or lambda-family exclusion."
)

KERNELS = ("x_minus_p", "x_pos_2sqrt_q", "x_neg_2sqrt_q")
CLASSES = ("1", "-1", "2", "-2")


def _atoms() -> list[tuple[str, str]]:
    return [(kernel, cls) for kernel in KERNELS for cls in CLASSES]


def _hits(forbidden: tuple[tuple[str, str], ...], row: dict[str, Any]) -> bool:
    return any(str(row.get(kernel, "")) == cls for kernel, cls in forbidden)


def audit_rank_zero_aa_bb_dyadic_exclusion_lower_bound(
    common_source_patterns: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if (
        common_source_patterns.get("status") != "ok"
        or common_source_patterns.get("ready") is not True
        or int(common_source_patterns.get("common_source_kernel_triple_pattern_count", 0) or 0)
        != 16
    ):
        violations.append("common_source_patterns_not_ready")

    rows = list(common_source_patterns.get("common_source_pattern_rows", []))
    atoms = _atoms()
    all_classes = set(CLASSES)

    min_size = None
    witness_sets: list[list[list[str]]] = []
    witness_allowed_profiles: list[dict[str, list[str]]] = []

    for size in range(1, len(atoms) + 1):
        found_here = []
        for forbidden in combinations(atoms, size):
            if not all(_hits(forbidden, row) for row in rows):
                continue
            allowed_profile: dict[str, list[str]] = {}
            nonempty = True
            for kernel in KERNELS:
                forbidden_here = {cls for kk, cls in forbidden if kk == kernel}
                allowed_here = sorted(all_classes - forbidden_here)
                allowed_profile[kernel] = allowed_here
                if not allowed_here:
                    nonempty = False
            if not nonempty:
                continue
            found_here.append((forbidden, allowed_profile))
        if found_here:
            min_size = size
            for forbidden, allowed_profile in found_here[:12]:
                witness_sets.append([[kernel, cls] for kernel, cls in forbidden])
                witness_allowed_profiles.append(allowed_profile)
            solution_count = len(found_here)
            break

    if min_size is None:
        violations.append("no_nonempty_dyadic_exclusion_solution")
        min_size = 0
        solution_count = 0

    kernel_forbidden_counts = Counter[str]()
    if witness_sets:
        first = witness_sets[0]
        for kernel, _cls in first:
            kernel_forbidden_counts[str(kernel)] += 1

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "raw_pattern_count": len(rows),
        "kernel_count": len(KERNELS),
        "class_count_per_kernel": len(CLASSES),
        "minimal_nonempty_forbidden_atom_count": min_size,
        "minimal_nonempty_solution_count": solution_count,
        "first_witness_forbidden_atoms": witness_sets[0] if witness_sets else [],
        "first_witness_allowed_profile": witness_allowed_profiles[0]
        if witness_allowed_profiles
        else {},
        "first_witness_kernel_forbidden_counts": dict(sorted(kernel_forbidden_counts.items())),
        "next_target": (
            "Any AA+BB dyadic theorem that works by independent per-kernel class "
            "exclusions must remove at least two classes on each kernel, or else "
            "use cross-kernel/Selmer compatibility."
        ),
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--common-source-patterns", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_dyadic_exclusion_lower_bound(
        load_json(args.common_source_patterns)
    )
    write_json(args.out, audit)
    print(
        "wrote closure quotient rank-zero AA+BB dyadic exclusion lower bound to "
        f"{args.out}"
    )
    print(f"status={audit['status']}")
    print(
        "minimal_nonempty_forbidden_atom_count="
        f"{audit['minimal_nonempty_forbidden_atom_count']}"
    )
    print(
        "minimal_nonempty_solution_count="
        f"{audit['minimal_nonempty_solution_count']}"
    )
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
