from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_lambda_proof_seed_coverage import (
    BOUNDARY,
    audit_lambda_proof_seed_coverage,
    write_json,
)


def _route_partition() -> dict[str, object]:
    return {
        "status": "ok",
        "lambda_class_count": 6,
        "covered_class_count": 6,
        "rank_zero_class_count": 3,
        "root_number_class_count": 2,
        "two_cover_class_count": 1,
        "family_exclusion_proved_count": 0,
        "missing_classes": [],
        "overlap_classes": [],
    }


def _rank_zero_seeds() -> dict[str, object]:
    return {
        "status": "ok",
        "seed_group_count": 2,
        "candidate_class_count": 3,
        "family_exclusion_proved_count": 0,
    }


def _root_number_seeds() -> dict[str, object]:
    return {
        "status": "ok",
        "seed_group_count": 2,
        "target_class_count": 2,
        "family_exclusion_proved_count": 0,
    }


def _two_cover_seeds() -> dict[str, object]:
    return {
        "status": "ok",
        "seed_group_count": 1,
        "target_class_count": 1,
        "candidate_cover_total": 2,
        "family_exclusion_proved_count": 0,
    }


def test_lambda_proof_seed_coverage_checks_all_routes_have_seed_ledgers() -> None:
    audit = audit_lambda_proof_seed_coverage(
        route_partition=_route_partition(),
        rank_zero_seeds=_rank_zero_seeds(),
        root_number_seeds=_root_number_seeds(),
        two_cover_seeds=_two_cover_seeds(),
    )

    assert audit == {
        "status": "ok",
        "ready": True,
        "lambda_class_count": 6,
        "covered_class_count": 6,
        "seed_ledger_class_count": 6,
        "route_class_counts": {
            "rank_zero": 3,
            "root_number": 2,
            "two_cover": 1,
        },
        "seed_ledger_class_counts": {
            "rank_zero": 3,
            "root_number": 2,
            "two_cover": 1,
        },
        "seed_group_counts": {
            "rank_zero": 2,
            "root_number": 2,
            "two_cover": 1,
        },
        "two_cover_candidate_cover_total": 2,
        "all_routes_have_seed_ledgers": True,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "violations": [],
        "boundary": BOUNDARY,
    }


def test_lambda_proof_seed_coverage_reports_route_mismatch() -> None:
    rank_zero = _rank_zero_seeds()
    rank_zero["candidate_class_count"] = 2

    audit = audit_lambda_proof_seed_coverage(
        route_partition=_route_partition(),
        rank_zero_seeds=rank_zero,
        root_number_seeds=_root_number_seeds(),
        two_cover_seeds=_two_cover_seeds(),
    )

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert audit["all_routes_have_seed_ledgers"] is False
    assert audit["violations"] == [
        {
            "field": "rank_zero_class_count",
            "route_partition": 3,
            "seed_ledger": 2,
        },
        {
            "field": "seed_ledger_class_count",
            "route_partition": 6,
            "seed_ledger": 5,
        },
    ]


def test_lambda_proof_seed_coverage_cli_writes_audit(tmp_path: Path) -> None:
    route = tmp_path / "route.json"
    rank_zero = tmp_path / "rank_zero.json"
    root_number = tmp_path / "root_number.json"
    two_cover = tmp_path / "two_cover.json"
    out = tmp_path / "coverage.json"
    route.write_text(json.dumps(_route_partition()), encoding="utf-8")
    rank_zero.write_text(json.dumps(_rank_zero_seeds()), encoding="utf-8")
    root_number.write_text(json.dumps(_root_number_seeds()), encoding="utf-8")
    two_cover.write_text(json.dumps(_two_cover_seeds()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_lambda_proof_seed_coverage.py",
            "--route-partition",
            str(route),
            "--rank-zero-seeds",
            str(rank_zero),
            "--root-number-seeds",
            str(root_number),
            "--two-cover-seeds",
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

    assert "seed_ledger_class_count=6" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "search_count_used_as_progress"
    ] is False


def test_write_json_writes_sorted_lambda_proof_seed_coverage(tmp_path: Path) -> None:
    out = tmp_path / "coverage.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
