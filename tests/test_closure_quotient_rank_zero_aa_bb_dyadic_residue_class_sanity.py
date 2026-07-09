from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_dyadic_residue_class_sanity import (
    BOUNDARY,
    audit_rank_zero_aa_bb_dyadic_residue_class_sanity,
    write_json,
)


def test_dyadic_residue_class_sanity_groups_by_primitive_mod8_class() -> None:
    audit = audit_rank_zero_aa_bb_dyadic_residue_class_sanity(
        modulus=8,
        numerator_bound=32,
        denominator_exp_bound=5,
        representative_search_bound=64,
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["residue_modulus"] == 8
    assert audit["primitive_residue_class_count"] == 48
    assert audit["relevant_squareclass_subgroup"] == ["1", "-1", "2", "-2"]
    assert audit["target_intersection_squareclasses"] == ["1"]
    assert audit["nontrivial_relevant_residue_class_count"] == 8
    assert audit["nontrivial_relevant_by_bucket"] == {
        "odd-even": 0,
        "even-odd": 0,
        "odd-odd": 8,
    }
    assert audit["full_q2_counterexample_residue_class_count"] > 0
    assert audit["parity_bucket_counts"] == {
        "odd-even": 16,
        "even-odd": 16,
        "odd-odd": 16,
    }
    assert audit["finite_sanity_check_not_proof"] is True
    assert audit["dyadic_local_image_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["boundary"] == BOUNDARY


def test_dyadic_residue_class_sanity_cli_writes_audit(tmp_path: Path) -> None:
    out = tmp_path / "residue_sanity.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_dyadic_residue_class_sanity.py",
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "primitive_residue_class_count=48" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["target_intersection_squareclasses"] == ["1"]
    assert payload["nontrivial_relevant_by_bucket"]["odd-odd"] == 8


def test_write_json_writes_sorted_dyadic_residue_class_sanity(tmp_path: Path) -> None:
    out = tmp_path / "residue_sanity.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
