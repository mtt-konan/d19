from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_dyadic_pair_profiles import (
    BOUNDARY,
    audit_rank_zero_aa_bb_dyadic_pair_profiles,
    write_json,
)


def _patterns() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "common_source_kernel_triple_pattern_count": 16,
        "common_source_pattern_rows": [
            {"x_minus_p": "1", "x_pos_2sqrt_q": "1", "x_neg_2sqrt_q": "1"},
            {"x_minus_p": "1", "x_pos_2sqrt_q": "-1", "x_neg_2sqrt_q": "-1"},
            {"x_minus_p": "1", "x_pos_2sqrt_q": "2", "x_neg_2sqrt_q": "2"},
            {"x_minus_p": "1", "x_pos_2sqrt_q": "-2", "x_neg_2sqrt_q": "-2"},
            {"x_minus_p": "-1", "x_pos_2sqrt_q": "1", "x_neg_2sqrt_q": "-1"},
            {"x_minus_p": "-1", "x_pos_2sqrt_q": "-1", "x_neg_2sqrt_q": "1"},
            {"x_minus_p": "-1", "x_pos_2sqrt_q": "2", "x_neg_2sqrt_q": "-2"},
            {"x_minus_p": "-1", "x_pos_2sqrt_q": "-2", "x_neg_2sqrt_q": "2"},
            {"x_minus_p": "2", "x_pos_2sqrt_q": "1", "x_neg_2sqrt_q": "2"},
            {"x_minus_p": "2", "x_pos_2sqrt_q": "-1", "x_neg_2sqrt_q": "-2"},
            {"x_minus_p": "2", "x_pos_2sqrt_q": "2", "x_neg_2sqrt_q": "1"},
            {"x_minus_p": "2", "x_pos_2sqrt_q": "-2", "x_neg_2sqrt_q": "-1"},
            {"x_minus_p": "-2", "x_pos_2sqrt_q": "1", "x_neg_2sqrt_q": "-2"},
            {"x_minus_p": "-2", "x_pos_2sqrt_q": "-1", "x_neg_2sqrt_q": "2"},
            {"x_minus_p": "-2", "x_pos_2sqrt_q": "2", "x_neg_2sqrt_q": "-1"},
            {"x_minus_p": "-2", "x_pos_2sqrt_q": "-2", "x_neg_2sqrt_q": "1"},
        ],
    }


def test_dyadic_pair_profiles_compress_12_witnesses_to_6_profiles_and_3_families() -> None:
    audit = audit_rank_zero_aa_bb_dyadic_pair_profiles(_patterns())

    assert audit["status"] == "ok"
    assert audit["minimal_allowed_profile_count"] == 12
    assert audit["pair_profile_count"] == 6
    assert audit["pair_family_count"] == 3
    assert audit["pair_profile_rows"] == [
        {
            "pair_profile_id": "profile_1",
            "unordered_allowed_pairs": [["-1", "-2"], ["-1", "-2"], ["-1", "-2"]],
            "realization_count": 1,
            "description": "all three kernels share the same allowed pair",
        },
        {
            "pair_profile_id": "profile_2",
            "unordered_allowed_pairs": [["-1", "-2"], ["1", "2"], ["1", "2"]],
            "realization_count": 3,
            "description": "two kernels share one allowed pair and the third uses its complementary pair",
        },
        {
            "pair_profile_id": "profile_3",
            "unordered_allowed_pairs": [["-1", "1"], ["-1", "1"], ["-2", "2"]],
            "realization_count": 3,
            "description": "two kernels share one allowed pair and the third uses its complementary pair",
        },
        {
            "pair_profile_id": "profile_4",
            "unordered_allowed_pairs": [["-1", "2"], ["-1", "2"], ["-1", "2"]],
            "realization_count": 1,
            "description": "all three kernels share the same allowed pair",
        },
        {
            "pair_profile_id": "profile_5",
            "unordered_allowed_pairs": [["-1", "2"], ["-2", "1"], ["-2", "1"]],
            "realization_count": 3,
            "description": "two kernels share one allowed pair and the third uses its complementary pair",
        },
        {
            "pair_profile_id": "profile_6",
            "unordered_allowed_pairs": [["-2", "2"], ["-2", "2"], ["-2", "2"]],
            "realization_count": 1,
            "description": "all three kernels share the same allowed pair",
        },
    ]
    assert audit["pair_family_rows"] == [
        {
            "pair_family_signature": [
                "negative_two_family",
                "negative_two_family",
                "negative_two_family",
            ],
            "profile_count": 2,
            "realization_count": 4,
        },
        {
            "pair_family_signature": [
                "positive_two_family",
                "positive_two_family",
                "positive_two_family",
            ],
            "profile_count": 2,
            "realization_count": 4,
        },
        {
            "pair_family_signature": [
                "sign_family",
                "sign_family",
                "sign_family",
            ],
            "profile_count": 2,
            "realization_count": 4,
        },
    ]
    assert audit["trivial_pattern_retained"] is True
    assert audit["nontrivial_pattern_count"] == 15
    assert audit["trivial_retaining_minimal_forbidden_atom_count"] == 6
    assert audit["trivial_retaining_minimal_profile_count"] == 21
    assert audit["trivial_retaining_support_shape_count"] == 4
    assert audit["trivial_retaining_support_shape_rows"] == [
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
    ]
    assert audit["next_target"] == (
        "For a Selmer-relevant independent dyadic route, retain the trivial "
        "pattern and focus on the four minimal support shapes that kill the "
        "15 nontrivial patterns."
    )
    assert audit["boundary"] == BOUNDARY


def test_dyadic_pair_profiles_require_ready_patterns() -> None:
    payload = _patterns()
    payload["ready"] = False

    audit = audit_rank_zero_aa_bb_dyadic_pair_profiles(payload)

    assert audit["status"] == "issues"
    assert audit["violations"] == ["common_source_patterns_not_ready"]


def test_dyadic_pair_profiles_identifies_trivial_pattern_with_extra_row_fields() -> None:
    payload = _patterns()
    for row in payload["common_source_pattern_rows"]:
        row["product_squareclass"] = "1"

    audit = audit_rank_zero_aa_bb_dyadic_pair_profiles(payload)

    assert audit["status"] == "ok"
    assert audit["nontrivial_pattern_count"] == 15
    assert audit["trivial_retaining_support_shape_count"] == 4


def test_dyadic_pair_profiles_cli_writes_audit(tmp_path: Path) -> None:
    patterns = tmp_path / "patterns.json"
    out = tmp_path / "pair_profiles.json"
    patterns.write_text(json.dumps(_patterns()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_dyadic_pair_profiles.py",
            "--common-source-patterns",
            str(patterns),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "pair_profile_count=6" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["pair_family_count"] == 3
    assert payload["trivial_retaining_support_shape_count"] == 4


def test_write_json_writes_sorted_dyadic_pair_profiles(tmp_path: Path) -> None:
    out = tmp_path / "pair_profiles.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
