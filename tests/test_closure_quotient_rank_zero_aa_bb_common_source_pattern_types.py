from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_common_source_pattern_types import (
    BOUNDARY,
    audit_rank_zero_aa_bb_common_source_pattern_types,
    write_json,
)


def _common_source_patterns() -> dict[str, object]:
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


def test_common_source_pattern_types_compress_16_patterns_to_5_types() -> None:
    audit = audit_rank_zero_aa_bb_common_source_pattern_types(
        _common_source_patterns()
    )

    assert audit["status"] == "ok"
    assert audit["raw_pattern_count"] == 16
    assert audit["pattern_type_count"] == 5
    assert audit["type_rows"] == [
        {
            "type_id": "all_trivial",
            "pattern_count": 1,
            "representative": {
                "x_minus_p": "1",
                "x_pos_2sqrt_q": "1",
                "x_neg_2sqrt_q": "1",
            },
            "description": "all three kernel classes trivial",
        },
        {
            "type_id": "minus_one_pair",
            "pattern_count": 3,
            "representative": {
                "x_minus_p": "1",
                "x_pos_2sqrt_q": "-1",
                "x_neg_2sqrt_q": "-1",
            },
            "description": "one trivial class and two -1 classes",
        },
        {
            "type_id": "two_pair",
            "pattern_count": 3,
            "representative": {
                "x_minus_p": "1",
                "x_pos_2sqrt_q": "2",
                "x_neg_2sqrt_q": "2",
            },
            "description": "one trivial class and two 2 classes",
        },
        {
            "type_id": "minus_two_pair",
            "pattern_count": 3,
            "representative": {
                "x_minus_p": "1",
                "x_pos_2sqrt_q": "-2",
                "x_neg_2sqrt_q": "-2",
            },
            "description": "one trivial class and two -2 classes",
        },
        {
            "type_id": "fully_mixed_nontrivial",
            "pattern_count": 6,
            "representative": {
                "x_minus_p": "-1",
                "x_pos_2sqrt_q": "2",
                "x_neg_2sqrt_q": "-2",
            },
            "description": "the three distinct nontrivial classes {-1,2,-2}",
        },
    ]
    assert audit["next_target"] == (
        "Check dyadic local-image and Selmer-lift compatibility by pattern type "
        "before descending to the 16 raw assignments."
    )
    assert audit["boundary"] == BOUNDARY


def test_common_source_pattern_types_require_ready_input() -> None:
    patterns = _common_source_patterns()
    patterns["ready"] = False

    audit = audit_rank_zero_aa_bb_common_source_pattern_types(patterns)

    assert audit["status"] == "issues"
    assert audit["violations"] == ["common_source_patterns_not_ready"]


def test_common_source_pattern_types_cli_writes_audit(tmp_path: Path) -> None:
    patterns = tmp_path / "patterns.json"
    out = tmp_path / "pattern_types.json"
    patterns.write_text(json.dumps(_common_source_patterns()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_common_source_pattern_types.py",
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

    assert "pattern_type_count=5" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["raw_pattern_count"] == 16


def test_write_json_writes_sorted_common_source_pattern_types(tmp_path: Path) -> None:
    out = tmp_path / "pattern_types.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
