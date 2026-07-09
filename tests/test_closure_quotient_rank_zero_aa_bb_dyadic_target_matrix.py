from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_dyadic_target_matrix import (
    BOUNDARY,
    audit_rank_zero_aa_bb_dyadic_target_matrix,
    write_json,
)


def _pattern_types() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "pattern_type_count": 5,
        "type_rows": [
            {
                "type_id": "all_trivial",
                "pattern_count": 1,
                "representative": {
                    "x_minus_p": "1",
                    "x_pos_2sqrt_q": "1",
                    "x_neg_2sqrt_q": "1",
                },
            },
            {
                "type_id": "minus_one_pair",
                "pattern_count": 3,
                "representative": {
                    "x_minus_p": "1",
                    "x_pos_2sqrt_q": "-1",
                    "x_neg_2sqrt_q": "-1",
                },
            },
            {
                "type_id": "two_pair",
                "pattern_count": 3,
                "representative": {
                    "x_minus_p": "1",
                    "x_pos_2sqrt_q": "2",
                    "x_neg_2sqrt_q": "2",
                },
            },
            {
                "type_id": "minus_two_pair",
                "pattern_count": 3,
                "representative": {
                    "x_minus_p": "1",
                    "x_pos_2sqrt_q": "-2",
                    "x_neg_2sqrt_q": "-2",
                },
            },
            {
                "type_id": "fully_mixed_nontrivial",
                "pattern_count": 6,
                "representative": {
                    "x_minus_p": "-1",
                    "x_pos_2sqrt_q": "2",
                    "x_neg_2sqrt_q": "-2",
                },
            },
        ],
    }


def test_dyadic_target_matrix_records_kernel_support_sets_per_type() -> None:
    audit = audit_rank_zero_aa_bb_dyadic_target_matrix(_pattern_types())

    assert audit["status"] == "ok"
    assert audit["pattern_type_count"] == 5
    assert audit["kernel_count"] == 3
    assert audit["dyadic_target_matrix_rows"] == [
        {
            "type_id": "all_trivial",
            "pattern_count": 1,
            "kernel_supports": {
                "x_minus_p": ["1"],
                "x_pos_2sqrt_q": ["1"],
                "x_neg_2sqrt_q": ["1"],
            },
            "dyadic_filter_hint": "To kill this type, some kernel must exclude class 1.",
        },
        {
            "type_id": "minus_one_pair",
            "pattern_count": 3,
            "kernel_supports": {
                "x_minus_p": ["-1", "1"],
                "x_pos_2sqrt_q": ["-1", "1"],
                "x_neg_2sqrt_q": ["-1", "1"],
            },
            "dyadic_filter_hint": (
                "To kill this type by one kernel alone, that kernel must exclude "
                "both 1 and -1 from its dyadic image."
            ),
        },
        {
            "type_id": "two_pair",
            "pattern_count": 3,
            "kernel_supports": {
                "x_minus_p": ["1", "2"],
                "x_pos_2sqrt_q": ["1", "2"],
                "x_neg_2sqrt_q": ["1", "2"],
            },
            "dyadic_filter_hint": (
                "To kill this type by one kernel alone, that kernel must exclude "
                "both 1 and 2 from its dyadic image."
            ),
        },
        {
            "type_id": "minus_two_pair",
            "pattern_count": 3,
            "kernel_supports": {
                "x_minus_p": ["-2", "1"],
                "x_pos_2sqrt_q": ["-2", "1"],
                "x_neg_2sqrt_q": ["-2", "1"],
            },
            "dyadic_filter_hint": (
                "To kill this type by one kernel alone, that kernel must exclude "
                "both 1 and -2 from its dyadic image."
            ),
        },
        {
            "type_id": "fully_mixed_nontrivial",
            "pattern_count": 6,
            "kernel_supports": {
                "x_minus_p": ["-1", "-2", "2"],
                "x_pos_2sqrt_q": ["-1", "-2", "2"],
                "x_neg_2sqrt_q": ["-1", "-2", "2"],
            },
            "dyadic_filter_hint": (
                "To kill this type by one kernel alone, that kernel must exclude "
                "all three classes {-1,2,-2}, or else use cross-kernel compatibility."
            ),
        },
    ]
    assert audit["next_target"] == (
        "Prove kernel-specific dyadic image restrictions strong enough to cut "
        "the listed support sets, or combine weaker dyadic images with "
        "cross-kernel/Selmer compatibility."
    )
    assert audit["boundary"] == BOUNDARY


def test_dyadic_target_matrix_requires_ready_pattern_types() -> None:
    payload = _pattern_types()
    payload["ready"] = False

    audit = audit_rank_zero_aa_bb_dyadic_target_matrix(payload)

    assert audit["status"] == "issues"
    assert audit["violations"] == ["pattern_types_not_ready"]


def test_dyadic_target_matrix_cli_writes_audit(tmp_path: Path) -> None:
    pattern_types = tmp_path / "pattern_types.json"
    out = tmp_path / "dyadic_target_matrix.json"
    pattern_types.write_text(json.dumps(_pattern_types()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_dyadic_target_matrix.py",
            "--pattern-types",
            str(pattern_types),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "pattern_type_count=5" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["kernel_count"] == 3


def test_write_json_writes_sorted_dyadic_target_matrix(tmp_path: Path) -> None:
    out = tmp_path / "dyadic_target_matrix.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
