#!/usr/bin/env python3
"""Audit the remaining odd-odd branch in the AA+BB x_minus_p dyadic sanity check."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BOUNDARY = (
    "This refines the finite AA+BB x_minus_p residue sanity check inside the "
    "odd-odd branch. It is not a proof of the dyadic local image, a Selmer "
    "lift, a Selmer rank bound, rank zero, or any lambda-family exclusion."
)


def _parse_residue_class(label: str) -> tuple[int, int]:
    ab, _mod, _modulus = label.split()
    a_raw, b_raw = ab.split(":", maxsplit=1)
    return int(a_raw), int(b_raw)


def audit_rank_zero_aa_bb_dyadic_odd_odd_split(
    residue_sanity: dict[str, Any],
) -> dict[str, Any]:
    violations: list[str] = []
    if (
        residue_sanity.get("status") != "ok"
        or residue_sanity.get("ready") is not True
        or int(residue_sanity.get("residue_modulus", 0) or 0) != 8
    ):
        violations.append("residue_sanity_not_ready")

    odd_odd_rows = [
        row
        for row in residue_sanity.get("sample_rows", [])
        if row.get("parity_bucket") == "odd-odd"
    ]
    same_mod4_rows = []
    opposite_mod4_rows = []
    for row in odd_odd_rows:
        a_residue, b_residue = _parse_residue_class(str(row.get("residue_class", "")))
        if (a_residue - b_residue) % 4 == 0:
            same_mod4_rows.append(row)
        else:
            opposite_mod4_rows.append(row)

    same_intersection = sorted(
        {
            cls
            for row in same_mod4_rows
            for cls in row.get("observed_relevant_intersection", [])
        },
        key=["1", "-1", "2", "-2"].index,
    )
    opposite_intersection = sorted(
        {
            cls
            for row in opposite_mod4_rows
            for cls in row.get("observed_relevant_intersection", [])
        },
        key=["1", "-1", "2", "-2"].index,
    )

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "odd_odd_residue_class_count": len(odd_odd_rows),
        "same_mod4_class_count": len(same_mod4_rows),
        "opposite_mod4_class_count": len(opposite_mod4_rows),
        "same_mod4_residue_classes": [
            str(row.get("residue_class", "")) for row in same_mod4_rows
        ],
        "opposite_mod4_residue_classes": [
            str(row.get("residue_class", "")) for row in opposite_mod4_rows
        ],
        "same_mod4_observed_intersection": same_intersection,
        "opposite_mod4_observed_intersection": opposite_intersection,
        "remaining_branch_description": (
            "Within odd-odd primitive residue classes mod 8, the currently observed "
            "extra class 2 survives only on the same-mod-4 branch."
        ),
        "next_target": (
            "Refine the AA+BB x_minus_p dyadic theorem only on the odd-odd "
            "same-mod-4 branch; the opposite-mod-4 branch already looks singleton "
            "at this finite residue level."
        ),
        "dyadic_local_image_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--residue-sanity", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_dyadic_odd_odd_split(
        load_json(args.residue_sanity)
    )
    write_json(args.out, audit)
    print(
        "wrote closure quotient rank-zero AA+BB dyadic odd-odd split audit to "
        f"{args.out}"
    )
    print(f"status={audit['status']}")
    print(f"same_mod4_class_count={audit['same_mod4_class_count']}")
    print(f"opposite_mod4_class_count={audit['opposite_mod4_class_count']}")
    print(f"dyadic_local_image_proved_count={audit['dyadic_local_image_proved_count']}")
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
