from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_ray_scale_invariance import (
    BOUNDARY,
    audit_scale_invariance,
    coefficient_scale_relations,
    write_json,
)


def _row(A: int, B: int, curve: str, lower: int, upper: int) -> dict[str, object]:
    return {
        "A": A,
        "B": B,
        "curve": curve,
        "status": "ok",
        "rank_lower": lower,
        "rank_upper": upper,
    }


def test_coefficient_scale_relations_verify_quartic_homogeneity() -> None:
    relations = coefficient_scale_relations(A=6, B=10, curve_name="AA")

    assert relations["primitive_A"] == 3
    assert relations["primitive_B"] == 5
    assert relations["scale"] == 2
    assert relations["curve"] == "AA"
    assert relations["all_coefficients_match"] is True
    assert [
        row["scale_power"]
        for row in relations["coefficient_relations"]
    ] == [4, 3, 2, 1, 0]


def test_scale_invariance_audit_groups_observed_rank_keys_by_ray() -> None:
    rows = []
    for curve in ["AA", "BB", "AB", "BA"]:
        rows.append(_row(3, 5, curve, 0, 0))
        rows.append(_row(6, 10, curve, 0, 0))
    rows.append(_row(10, 14, "AA", 0, 0))
    rows.append(_row(15, 21, "AA", 0, 2))

    audit = audit_scale_invariance(rows)

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert audit["observed_pair_count"] == 4
    assert audit["observed_ray_count"] == 2
    assert audit["multi_scale_ray_count"] == 2
    assert audit["coefficient_identity_verified_count"] == 10
    assert audit["rank_key_consistent_group_count"] == 4
    assert audit["rank_key_inconsistent_group_count"] == 1
    assert audit["violations"] == [
        {
            "primitive_A": 5,
            "primitive_B": 7,
            "curve": "AA",
            "reason": "rank-key-varies-across-observed-scales",
            "rank_keys": ["0/0", "0/2"],
            "scales": [2, 3],
        }
    ]
    assert audit["boundary"] == BOUNDARY


def test_scale_invariance_cli_writes_audit(tmp_path: Path) -> None:
    rank_jsonl = tmp_path / "rank.jsonl"
    out = tmp_path / "audit.json"
    rows = []
    for curve in ["AA", "BB", "AB", "BA"]:
        rows.append(_row(3, 5, curve, 0, 0))
        rows.append(_row(6, 10, curve, 0, 0))
    rank_jsonl.write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_ray_scale_invariance.py",
            "--rank-jsonl",
            str(rank_jsonl),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "status=ok" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["multi_scale_ray_count"] == 1


def test_write_json_writes_sorted_scale_audit(tmp_path: Path) -> None:
    out = tmp_path / "audit.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
