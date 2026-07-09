from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_dyadic_odd_odd_split import (
    BOUNDARY,
    audit_rank_zero_aa_bb_dyadic_odd_odd_split,
    write_json,
)


def _residue_sanity() -> dict[str, object]:
    rows = []
    for a in (1, 3, 5, 7):
        for b in (1, 3, 5, 7):
            rows.append(
                {
                    "residue_class": f"{a}:{b} mod 8",
                    "representative_pair": f"{a}:{b}",
                    "parity_bucket": "odd-odd",
                    "observed_relevant_intersection": (
                        ["1", "2"] if (a - b) % 4 == 0 else ["1"]
                    ),
                    "observed_full_q2_classes_outside_relevant_subgroup": [],
                }
            )
    return {
        "status": "ok",
        "ready": True,
        "residue_modulus": 8,
        "primitive_residue_class_count": 48,
        "target_intersection_squareclasses": ["1"],
        "nontrivial_relevant_residue_class_count": 8,
        "nontrivial_relevant_by_bucket": {
            "odd-even": 0,
            "even-odd": 0,
            "odd-odd": 8,
        },
        "sample_rows": rows,
    }


def test_dyadic_odd_odd_split_is_same_mod4_vs_opposite_mod4() -> None:
    audit = audit_rank_zero_aa_bb_dyadic_odd_odd_split(_residue_sanity())

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["odd_odd_residue_class_count"] == 16
    assert audit["same_mod4_class_count"] == 8
    assert audit["opposite_mod4_class_count"] == 8
    assert audit["same_mod4_residue_classes"] == [
        "1:1 mod 8",
        "1:5 mod 8",
        "3:3 mod 8",
        "3:7 mod 8",
        "5:1 mod 8",
        "5:5 mod 8",
        "7:3 mod 8",
        "7:7 mod 8",
    ]
    assert audit["opposite_mod4_residue_classes"] == [
        "1:3 mod 8",
        "1:7 mod 8",
        "3:1 mod 8",
        "3:5 mod 8",
        "5:3 mod 8",
        "5:7 mod 8",
        "7:1 mod 8",
        "7:5 mod 8",
    ]
    assert audit["same_mod4_observed_intersection"] == ["1", "2"]
    assert audit["opposite_mod4_observed_intersection"] == ["1"]
    assert audit["remaining_branch_description"] == (
        "Within odd-odd primitive residue classes mod 8, the currently observed "
        "extra class 2 survives only on the same-mod-4 branch."
    )
    assert audit["next_target"] == (
        "Refine the AA+BB x_minus_p dyadic theorem only on the odd-odd "
        "same-mod-4 branch; the opposite-mod-4 branch already looks singleton "
        "at this finite residue level."
    )
    assert audit["dyadic_local_image_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["boundary"] == BOUNDARY


def test_dyadic_odd_odd_split_requires_ready_residue_sanity() -> None:
    payload = _residue_sanity()
    payload["ready"] = False

    audit = audit_rank_zero_aa_bb_dyadic_odd_odd_split(payload)

    assert audit["status"] == "issues"
    assert audit["violations"] == ["residue_sanity_not_ready"]


def test_dyadic_odd_odd_split_cli_writes_audit(tmp_path: Path) -> None:
    residue_sanity = tmp_path / "residue_sanity.json"
    out = tmp_path / "odd_odd_split.json"
    residue_sanity.write_text(json.dumps(_residue_sanity()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_dyadic_odd_odd_split.py",
            "--residue-sanity",
            str(residue_sanity),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "same_mod4_class_count=8" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["same_mod4_residue_classes"][0] == "1:1 mod 8"
    assert payload["same_mod4_observed_intersection"] == ["1", "2"]


def test_write_json_writes_sorted_dyadic_odd_odd_split(tmp_path: Path) -> None:
    out = tmp_path / "odd_odd_split.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
