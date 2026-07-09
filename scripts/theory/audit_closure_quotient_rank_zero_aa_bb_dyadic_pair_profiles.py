#!/usr/bin/env python3
"""Audit pair-profile compression behind AA+BB dyadic exclusion witnesses."""

from __future__ import annotations

import argparse
from collections import defaultdict
from itertools import combinations, product
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits pair-profile compression behind the AA+BB dyadic exclusion "
    "lower bound. It does not prove any actual dyadic local image, Selmer "
    "lift, Selmer rank bound, rank zero, or lambda-family exclusion."
)

KERNELS = ("x_minus_p", "x_pos_2sqrt_q", "x_neg_2sqrt_q")
CLASSES = ("1", "-1", "2", "-2")
CLASS_ORDER = {cls: idx for idx, cls in enumerate(CLASSES)}


def _atoms() -> list[tuple[str, str]]:
    return [(kernel, cls) for kernel in KERNELS for cls in CLASSES]


def _sort_classes(classes: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(classes, key=lambda cls: CLASS_ORDER[cls]))


def _hits(forbidden: tuple[tuple[str, str], ...], row: dict[str, Any]) -> bool:
    return any(str(row.get(kernel, "")) == cls for kernel, cls in forbidden)


def _kernel_projection(row: dict[str, Any]) -> dict[str, str]:
    return {kernel: str(row.get(kernel, "")) for kernel in KERNELS}


def _pair_family(pair: tuple[str, str]) -> str:
    pair_set = set(pair)
    if pair_set == {"1", "-1"} or pair_set == {"2", "-2"}:
        return "sign_family"
    if pair_set == {"1", "2"} or pair_set == {"-1", "-2"}:
        return "positive_two_family"
    if pair_set == {"1", "-2"} or pair_set == {"-1", "2"}:
        return "negative_two_family"
    return "unexpected"


def _trivial_retaining_shapes(
    rows: list[dict[str, Any]],
) -> tuple[int, int, list[dict[str, Any]]]:
    trivial_row = dict.fromkeys(KERNELS, "1")
    nontrivial_rows = [
        row for row in rows if _kernel_projection(row) != trivial_row
    ]
    allowed_options = [
        subset
        for size in range(1, len(CLASSES) + 1)
        for subset in combinations(CLASSES, size)
        if "1" in subset
    ]

    solutions: list[tuple[int, tuple[tuple[str, ...], ...]]] = []
    for profile in product(allowed_options, repeat=len(KERNELS)):
        if all(
            not all(row[kernel] in set(profile[idx]) for idx, kernel in enumerate(KERNELS))
            for row in nontrivial_rows
        ):
            forbidden_count = sum(len(CLASSES) - len(allowed) for allowed in profile)
            solutions.append((forbidden_count, profile))

    minimal_forbidden_count = min(count for count, _profile in solutions)
    minimal_profiles = [
        profile for count, profile in solutions if count == minimal_forbidden_count
    ]
    shape_groups: dict[tuple[tuple[str, ...], ...], int] = defaultdict(int)
    for profile in minimal_profiles:
        support_shape = tuple(
            sorted(
                (_sort_classes(tuple(allowed)) for allowed in profile),
                key=lambda allowed: (
                    len(allowed),
                    [CLASS_ORDER[cls] for cls in allowed],
                ),
            )
        )
        shape_groups[support_shape] += 1

    shape_rows = [
        {
            "support_shape_id": f"trivial_retaining_shape_{idx + 1}",
            "unordered_allowed_supports": [list(support) for support in shape],
            "realization_count": realization_count,
        }
        for idx, (shape, realization_count) in enumerate(
            sorted(
                shape_groups.items(),
                key=lambda item: (
                    [len(support) for support in item[0]],
                    [[CLASS_ORDER[cls] for cls in support] for support in item[0]],
                ),
            )
        )
    ]
    return minimal_forbidden_count, len(minimal_profiles), shape_rows


def audit_rank_zero_aa_bb_dyadic_pair_profiles(
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

    minimal_allowed_profiles: list[dict[str, tuple[str, str]]] = []
    for forbidden in combinations(atoms, 6):
        if not all(_hits(forbidden, row) for row in rows):
            continue
        allowed_profile: dict[str, tuple[str, str]] = {}
        ok = True
        for kernel in KERNELS:
            forbidden_here = {cls for kk, cls in forbidden if kk == kernel}
            allowed_here = tuple(sorted(all_classes - forbidden_here))
            if len(allowed_here) != 2:
                ok = False
                break
            allowed_profile[kernel] = allowed_here
        if ok:
            minimal_allowed_profiles.append(allowed_profile)

    if len(minimal_allowed_profiles) != 12:
        violations.append("minimal_allowed_profile_count_mismatch")

    profile_groups: dict[
        tuple[tuple[str, str], ...],
        list[dict[str, tuple[str, str]]],
    ] = defaultdict(list)
    family_groups: dict[tuple[str, str, str], list[dict[str, tuple[str, str]]]] = defaultdict(list)
    for profile in minimal_allowed_profiles:
        unordered_profile = tuple(sorted(profile.values()))
        profile_groups[unordered_profile].append(profile)
        family_signature = tuple(sorted(_pair_family(pair) for pair in profile.values()))
        family_groups[family_signature].append(profile)

    if len(profile_groups) != 6:
        violations.append("pair_profile_count_mismatch")
    if len(family_groups) != 3:
        violations.append("pair_family_count_mismatch")

    profile_rows = [
        {
            "pair_profile_id": f"profile_{idx+1}",
            "unordered_allowed_pairs": [list(pair) for pair in key],
            "realization_count": len(group),
            "description": (
                "all three kernels share the same allowed pair"
                if len(set(key)) == 1
                else "two kernels share one allowed pair and the third uses its complementary pair"
            ),
        }
        for idx, (key, group) in enumerate(sorted(profile_groups.items(), key=lambda item: item[0]))
    ]
    family_rows = [
        {
            "pair_family_signature": list(signature),
            "profile_count": len(
                {
                    tuple(sorted(profile.values()))
                    for profile in group
                }
            ),
            "realization_count": len(group),
        }
        for signature, group in sorted(family_groups.items(), key=lambda item: item[0])
    ]
    (
        trivial_retaining_minimal_forbidden_atom_count,
        trivial_retaining_minimal_profile_count,
        trivial_retaining_support_shape_rows,
    ) = _trivial_retaining_shapes(rows)

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "minimal_allowed_profile_count": len(minimal_allowed_profiles),
        "pair_profile_count": len(profile_rows),
        "pair_family_count": len(family_rows),
        "pair_profile_rows": profile_rows,
        "pair_family_rows": family_rows,
        "trivial_pattern_retained": True,
        "nontrivial_pattern_count": max(len(rows) - 1, 0),
        "trivial_retaining_minimal_forbidden_atom_count": (
            trivial_retaining_minimal_forbidden_atom_count
        ),
        "trivial_retaining_minimal_profile_count": (
            trivial_retaining_minimal_profile_count
        ),
        "trivial_retaining_support_shape_count": len(
            trivial_retaining_support_shape_rows
        ),
        "trivial_retaining_support_shape_rows": (
            trivial_retaining_support_shape_rows
        ),
        "next_target": (
            "For a Selmer-relevant independent dyadic route, retain the trivial "
            "pattern and focus on the four minimal support shapes that kill the "
            "15 nontrivial patterns."
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
    audit = audit_rank_zero_aa_bb_dyadic_pair_profiles(load_json(args.common_source_patterns))
    write_json(args.out, audit)
    print(
        "wrote closure quotient rank-zero AA+BB dyadic pair profiles to "
        f"{args.out}"
    )
    print(f"status={audit['status']}")
    print(f"minimal_allowed_profile_count={audit['minimal_allowed_profile_count']}")
    print(f"pair_profile_count={audit['pair_profile_count']}")
    print(f"pair_family_count={audit['pair_family_count']}")
    print(
        "trivial_retaining_support_shape_count="
        f"{audit['trivial_retaining_support_shape_count']}"
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
