from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_aa_bb_dyadic_relevant_subgroup_sanity import (
    BOUNDARY,
    audit_rank_zero_aa_bb_dyadic_relevant_subgroup_sanity,
    q2_squareclass,
    write_json,
)


def test_q2_squareclass_tracks_full_q2_classes() -> None:
    assert q2_squareclass(1) == "1"
    assert q2_squareclass(-1) == "-1"
    assert q2_squareclass(2) == "2"
    assert q2_squareclass(-2) == "-2"
    assert q2_squareclass(5) == "5"


def test_relevant_subgroup_sanity_keeps_full_q2_boundary() -> None:
    audit = audit_rank_zero_aa_bb_dyadic_relevant_subgroup_sanity(
        sample_pairs=[(1, 2), (1, 4), (3, 5), (5, 7)],
        numerator_bound=64,
        denominator_exp_bound=6,
    )

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["relevant_squareclass_subgroup"] == ["1", "-1", "2", "-2"]
    assert audit["target_intersection_squareclasses"] == ["1"]
    assert audit["observed_relevant_intersection_by_pair"] == {
        "1:2": ["1"],
        "1:4": ["1"],
        "3:5": ["1"],
        "5:7": ["1"],
    }
    assert audit["full_q2_singleton_counterexample"] == {
        "pair": "1:2",
        "class": "5",
        "meaning": (
            "full Q2 local image can contain a class outside "
            "{1,-1,2,-2}; the theorem target must stay subgroup-relative"
        ),
    }
    assert audit["finite_sanity_check_not_proof"] is True
    assert audit["dyadic_local_image_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["boundary"] == BOUNDARY


def test_relevant_subgroup_sanity_cli_writes_audit(tmp_path: Path) -> None:
    out = tmp_path / "sanity.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_aa_bb_dyadic_relevant_subgroup_sanity.py",
            "--sample-pair",
            "1:2",
            "--sample-pair",
            "1:4",
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "target_intersection_squareclasses=['1']" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["status"] == "ok"
    assert payload["full_q2_singleton_counterexample"]["class"] == "5"


def test_write_json_writes_sorted_relevant_subgroup_sanity(tmp_path: Path) -> None:
    out = tmp_path / "sanity.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
