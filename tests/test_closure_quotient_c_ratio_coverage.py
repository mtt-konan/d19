from __future__ import annotations

import importlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

MODULE_NAME = "scripts.theory.audit_closure_quotient_c_ratio_coverage"


def _coverage_module() -> ModuleType:
    assert importlib.util.find_spec(MODULE_NAME) is not None
    return importlib.import_module(MODULE_NAME)


def _ray_ledger() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "pair_count": 5,
        "primitive_ray_count": 4,
        "c_ratio_class_count": 3,
        "strict_c_ratio_class_count": 1,
        "c_minus_zero_pair_count": 1,
        "search_count_used_as_progress": False,
        "c_ratio_class_rows": [
            {
                "class": "3:5",
                "unordered_primitive_ray": [3, 5],
                "possible_oriented_rays": [[3, 5], [5, 3]],
                "observed_oriented_rays": [[3, 5], [5, 3]],
                "orientation_lost_by_c_ratio": True,
                "c_ratio": "4",
                "pair_count": 3,
                "status_counts": {
                    "strict-local-tool-excludes-observed-pair": 2,
                    "residual-candidate-not-proof": 1,
                },
                "coverage_status": "some-observed-pairs-strict",
            },
            {
                "class": "2:7",
                "unordered_primitive_ray": [2, 7],
                "possible_oriented_rays": [[2, 7], [7, 2]],
                "observed_oriented_rays": [[2, 7]],
                "orientation_lost_by_c_ratio": True,
                "c_ratio": "9/5",
                "pair_count": 1,
                "status_counts": {
                    "observed-not-closed-by-local-tool": 1,
                },
                "coverage_status": "observed-open",
            },
            {
                "class": "1:1",
                "unordered_primitive_ray": [1, 1],
                "possible_oriented_rays": [[1, 1]],
                "observed_oriented_rays": [[1, 1]],
                "orientation_lost_by_c_ratio": False,
                "c_ratio": "undefined",
                "pair_count": 1,
                "status_counts": {
                    "strict-local-tool-excludes-observed-pair": 1,
                },
                "coverage_status": "all-observed-pairs-strict",
            },
        ],
        "boundary": "ray ledger boundary",
    }


def test_c_ratio_coverage_separates_unordered_classes_from_lambda_orientations() -> None:
    coverage = _coverage_module()

    audit = coverage.audit_c_ratio_coverage(ray_ledger=_ray_ledger())

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["input_c_ratio_class_count"] == 3
    assert audit["defined_c_ratio_class_count"] == 2
    assert audit["undefined_c_ratio_class_count"] == 1
    assert audit["orientation_lost_class_count"] == 2
    assert audit["both_orientations_observed_class_count"] == 1
    assert audit["single_orientation_observed_class_count"] == 1
    assert audit["lambda_orientation_gap_class_count"] == 1
    assert audit["strict_unordered_class_count"] == 1
    assert audit["residual_unordered_class_count"] == 1
    assert audit["open_unordered_class_count"] == 1
    assert audit["lambda_family_exclusion_proved_count"] == 0
    assert audit["search_count_used_as_progress"] is False
    assert audit["coverage_rows"] == [
        {
            "class": "2:7",
            "c_ratio": "9/5",
            "unordered_primitive_ray": [2, 7],
            "possible_oriented_rays": [[2, 7], [7, 2]],
            "observed_oriented_rays": [[2, 7]],
            "missing_oriented_rays": [[7, 2]],
            "covers_unordered_ratio_class": True,
            "covers_all_lambda_orientations": False,
            "coverage_status": "observed-open",
            "lambda_mainline_status": "needs-lambda-family-proof-or-certificate",
        },
        {
            "class": "3:5",
            "c_ratio": "4",
            "unordered_primitive_ray": [3, 5],
            "possible_oriented_rays": [[3, 5], [5, 3]],
            "observed_oriented_rays": [[3, 5], [5, 3]],
            "missing_oriented_rays": [],
            "covers_unordered_ratio_class": True,
            "covers_all_lambda_orientations": True,
            "coverage_status": "some-observed-pairs-strict",
            "lambda_mainline_status": "observed-class-mixed-not-family-proof",
        },
        {
            "class": "1:1",
            "c_ratio": "undefined",
            "unordered_primitive_ray": [1, 1],
            "possible_oriented_rays": [[1, 1]],
            "observed_oriented_rays": [[1, 1]],
            "missing_oriented_rays": [],
            "covers_unordered_ratio_class": False,
            "covers_all_lambda_orientations": True,
            "coverage_status": "all-observed-pairs-strict",
            "lambda_mainline_status": "c-minus-zero-not-a-c-ratio-class",
        },
    ]
    assert audit["c_ratio_coverage_not_lambda_family_proof"] is True


def test_c_ratio_coverage_rejects_unready_ray_ledger() -> None:
    coverage = _coverage_module()
    ledger = _ray_ledger()
    ledger["ready"] = False
    ledger["status"] = "issues"

    audit = coverage.audit_c_ratio_coverage(ray_ledger=ledger)

    assert audit["status"] == "issues"
    assert audit["violations"] == ["ray_ledger_not_ready"]


def test_c_ratio_coverage_cli_writes_audit(tmp_path: Path) -> None:
    ledger = tmp_path / "ray_ledger.json"
    out = tmp_path / "c_ratio_coverage.json"
    ledger.write_text(json.dumps(_ray_ledger()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_c_ratio_coverage.py",
            "--ray-ledger",
            str(ledger),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "defined_c_ratio_class_count=2" in result.stdout
    assert "lambda_family_exclusion_proved_count=0" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["c_ratio_coverage_not_lambda_family_proof"] is True


def test_write_json_writes_sorted_c_ratio_coverage(tmp_path: Path) -> None:
    coverage = _coverage_module()
    out = tmp_path / "coverage.json"

    coverage.write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
