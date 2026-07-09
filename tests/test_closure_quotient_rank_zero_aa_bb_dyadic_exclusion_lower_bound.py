from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_dyadic_exclusion_lower_bound import (
    BOUNDARY,
    audit_rank_zero_aa_bb_dyadic_exclusion_lower_bound,
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


def test_dyadic_exclusion_lower_bound_requires_six_nonempty_forbidden_atoms() -> None:
    audit = audit_rank_zero_aa_bb_dyadic_exclusion_lower_bound(_patterns())

    assert audit["status"] == "ok"
    assert audit["raw_pattern_count"] == 16
    assert audit["minimal_nonempty_forbidden_atom_count"] == 6
    assert audit["minimal_nonempty_solution_count"] == 12
    assert audit["first_witness_forbidden_atoms"] == [
        ["x_minus_p", "1"],
        ["x_minus_p", "-1"],
        ["x_pos_2sqrt_q", "1"],
        ["x_pos_2sqrt_q", "-1"],
        ["x_neg_2sqrt_q", "1"],
        ["x_neg_2sqrt_q", "-1"],
    ]
    assert audit["first_witness_allowed_profile"] == {
        "x_minus_p": ["-2", "2"],
        "x_pos_2sqrt_q": ["-2", "2"],
        "x_neg_2sqrt_q": ["-2", "2"],
    }
    assert audit["first_witness_kernel_forbidden_counts"] == {
        "x_minus_p": 2,
        "x_neg_2sqrt_q": 2,
        "x_pos_2sqrt_q": 2,
    }
    assert audit["next_target"] == (
        "Any AA+BB dyadic theorem that works by independent per-kernel class "
        "exclusions must remove at least two classes on each kernel, or else "
        "use cross-kernel/Selmer compatibility."
    )
    assert audit["boundary"] == BOUNDARY


def test_dyadic_exclusion_lower_bound_requires_ready_patterns() -> None:
    payload = _patterns()
    payload["ready"] = False

    audit = audit_rank_zero_aa_bb_dyadic_exclusion_lower_bound(payload)

    assert audit["status"] == "issues"
    assert audit["violations"] == ["common_source_patterns_not_ready"]


def test_dyadic_exclusion_lower_bound_cli_writes_audit(tmp_path: Path) -> None:
    patterns = tmp_path / "patterns.json"
    out = tmp_path / "dyadic_lower_bound.json"
    patterns.write_text(json.dumps(_patterns()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_dyadic_exclusion_lower_bound.py",
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

    assert "minimal_nonempty_forbidden_atom_count=6" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["minimal_nonempty_solution_count"] == 12


def test_write_json_writes_sorted_dyadic_exclusion_lower_bound(tmp_path: Path) -> None:
    out = tmp_path / "dyadic_lower_bound.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
