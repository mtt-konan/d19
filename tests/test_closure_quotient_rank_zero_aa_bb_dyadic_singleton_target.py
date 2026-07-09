from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_dyadic_singleton_target import (
    BOUNDARY,
    audit_rank_zero_aa_bb_dyadic_singleton_target,
    write_json,
)


def _pair_profiles() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "trivial_pattern_retained": True,
        "nontrivial_pattern_count": 15,
        "trivial_retaining_support_shape_count": 4,
        "trivial_retaining_support_shape_rows": [
            {
                "support_shape_id": "trivial_retaining_shape_1",
                "unordered_allowed_supports": [
                    ["1"],
                    ["1"],
                    ["1", "-1", "2", "-2"],
                ],
                "realization_count": 3,
            },
            {
                "support_shape_id": "trivial_retaining_shape_2",
                "unordered_allowed_supports": [
                    ["1"],
                    ["1", "-1"],
                    ["1", "2", "-2"],
                ],
                "realization_count": 6,
            },
            {
                "support_shape_id": "trivial_retaining_shape_3",
                "unordered_allowed_supports": [
                    ["1"],
                    ["1", "2"],
                    ["1", "-1", "-2"],
                ],
                "realization_count": 6,
            },
            {
                "support_shape_id": "trivial_retaining_shape_4",
                "unordered_allowed_supports": [
                    ["1"],
                    ["1", "-2"],
                    ["1", "-1", "2"],
                ],
                "realization_count": 6,
            },
        ],
    }


def test_dyadic_singleton_target_selects_x_minus_p() -> None:
    audit = audit_rank_zero_aa_bb_dyadic_singleton_target(_pair_profiles())

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["trivial_pattern_retained"] is True
    assert audit["nontrivial_pattern_count"] == 15
    assert audit["support_shape_count"] == 4
    assert audit["support_shape_forcing_singleton_count"] == 4
    assert audit["support_shape_with_two_singletons_count"] == 1
    assert audit["odd_collapsed_singleton_candidate_count"] == 2
    assert audit["primary_target_kernel"] == "x_minus_p"
    assert audit["primary_target_package"] == (
        "rank-zero-selmer-AA-BB-kernel-minus-p"
    )
    assert audit["alternate_target_kernels"] == ["x_neg_2sqrt_q"]
    assert audit["deferred_kernel"] == "x_pos_2sqrt_q"
    assert audit["relevant_squareclass_subgroup"] == ["1", "-1", "2", "-2"]
    assert audit["target_is_full_q2_singleton_claim"] is False
    assert audit["target_intersection_squareclasses"] == ["1"]
    assert audit["target_rows"] == [
        {
            "kernel": "x_minus_p",
            "package_id": "rank-zero-selmer-AA-BB-kernel-minus-p",
            "odd_support_status": "empty after AA+BB odd-support collapse",
            "priority": "primary",
        },
        {
            "kernel": "x_neg_2sqrt_q",
            "package_id": "rank-zero-selmer-AA-BB-kernel-neg-2sqrt-q",
            "odd_support_status": "empty after AA+BB odd-support collapse",
            "priority": "alternate",
        },
        {
            "kernel": "x_pos_2sqrt_q",
            "package_id": "rank-zero-selmer-AA-BB-kernel-pos-2sqrt-q",
            "odd_support_status": (
                "possible tail at odd primes ell | T, ell == 1 mod 4"
            ),
            "priority": "defer",
        },
    ]
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["violations"] == []
    assert audit["boundary"] == BOUNDARY


def test_dyadic_singleton_target_requires_ready_pair_profiles() -> None:
    payload = _pair_profiles()
    payload["trivial_pattern_retained"] = False

    audit = audit_rank_zero_aa_bb_dyadic_singleton_target(payload)

    assert audit["status"] == "issues"
    assert audit["violations"] == ["pair_profiles_not_ready"]


def test_dyadic_singleton_target_rejects_shapes_without_singleton() -> None:
    payload = _pair_profiles()
    payload["trivial_retaining_support_shape_rows"][0]["unordered_allowed_supports"] = [
        ["1", "-1"],
        ["1", "2"],
        ["1", "-2"],
    ]

    audit = audit_rank_zero_aa_bb_dyadic_singleton_target(payload)

    assert audit["status"] == "issues"
    assert audit["violations"] == ["not_every_shape_forces_singleton_kernel"]


def test_dyadic_singleton_target_cli_writes_audit(tmp_path: Path) -> None:
    pair_profiles = tmp_path / "pair_profiles.json"
    out = tmp_path / "singleton_target.json"
    pair_profiles.write_text(json.dumps(_pair_profiles()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_dyadic_singleton_target.py",
            "--pair-profiles",
            str(pair_profiles),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "primary_target_kernel=x_minus_p" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["primary_target_package"] == (
        "rank-zero-selmer-AA-BB-kernel-minus-p"
    )
    assert payload["target_is_full_q2_singleton_claim"] is False


def test_write_json_writes_sorted_dyadic_singleton_target(tmp_path: Path) -> None:
    out = tmp_path / "singleton_target.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
