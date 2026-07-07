from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_lambda_route_partition import (
    BOUNDARY,
    audit_lambda_route_partition,
    write_json,
)


def _ray_ledger() -> dict[str, object]:
    return {
        "c_ratio_class_rows": [
            {"class": "3:5"},
            {"class": "7:11"},
            {"class": "13:17"},
        ]
    }


def test_lambda_route_partition_accepts_exact_disjoint_cover() -> None:
    audit = audit_lambda_route_partition(
        ray_ledger=_ray_ledger(),
        rank_zero_candidates={"candidates": [{"class": "3:5"}]},
        root_number_triage={"targets": [{"class": "7:11"}]},
        two_cover_frontier={"targets": [{"class": "13:17"}]},
    )

    assert audit == {
        "status": "ok",
        "ready": True,
        "lambda_class_count": 3,
        "rank_zero_class_count": 1,
        "root_number_class_count": 1,
        "two_cover_class_count": 1,
        "covered_class_count": 3,
        "missing_classes": [],
        "overlap_classes": [],
        "unexpected_classes": [],
        "route_counts": {
            "rank-zero-family-generalization": 1,
            "root-number-rank-structure-triage": 1,
            "two-cover-or-reviewable-no-point-certificate": 1,
        },
        "family_exclusion_proved_count": 0,
        "boundary": BOUNDARY,
    }


def test_lambda_route_partition_reports_missing_and_overlap() -> None:
    audit = audit_lambda_route_partition(
        ray_ledger=_ray_ledger(),
        rank_zero_candidates={"candidates": [{"class": "3:5"}, {"class": "7:11"}]},
        root_number_triage={"targets": [{"class": "7:11"}]},
        two_cover_frontier={"targets": [{"class": "19:23"}]},
    )

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert audit["missing_classes"] == ["13:17"]
    assert audit["overlap_classes"] == ["7:11"]
    assert audit["unexpected_classes"] == ["19:23"]


def test_lambda_route_partition_cli_writes_audit(tmp_path: Path) -> None:
    ray = tmp_path / "ray.json"
    rank_zero = tmp_path / "rank_zero.json"
    root = tmp_path / "root.json"
    two_cover = tmp_path / "two_cover.json"
    out = tmp_path / "partition.json"
    ray.write_text(json.dumps(_ray_ledger()), encoding="utf-8")
    rank_zero.write_text(
        json.dumps({"candidates": [{"class": "3:5"}]}),
        encoding="utf-8",
    )
    root.write_text(json.dumps({"targets": [{"class": "7:11"}]}), encoding="utf-8")
    two_cover.write_text(
        json.dumps({"targets": [{"class": "13:17"}]}),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_lambda_route_partition.py",
            "--ray-ledger",
            str(ray),
            "--rank-zero-candidates",
            str(rank_zero),
            "--root-number-triage",
            str(root),
            "--two-cover-frontier",
            str(two_cover),
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
    assert json.loads(out.read_text(encoding="utf-8"))["covered_class_count"] == 3


def test_write_json_writes_sorted_partition_audit(tmp_path: Path) -> None:
    out = tmp_path / "partition.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
