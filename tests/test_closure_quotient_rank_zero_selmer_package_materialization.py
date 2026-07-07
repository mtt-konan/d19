from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.materialize_closure_quotient_rank_zero_selmer_packages import (
    BOUNDARY,
    REQUIRED_TRANSCRIPT_FIELDS,
    materialize_rank_zero_selmer_packages,
    write_json,
)


def _package_index() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 2,
        "open_package_count": 2,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "packages": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "family_pattern": "AA",
                "kernel": "kernel_minus_p",
                "candidate_class_count": 2,
                "model_count": 2,
                "kernel_root": "-p",
                "target_a2": "32*L^2 - 8*T^2",
                "target_a4": "16*(T^2 + 4*L^2)^2",
                "required_output": (
                    "reviewable transcript proving the uniform isogeny-Selmer "
                    "rank upper bound for this family/kernel"
                ),
                "status": "open",
                "selmer_rank_upper_bound_proved": False,
                "family_exclusion_proved": False,
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-pos-2sqrt-q",
                "family_pattern": "BB",
                "kernel": "kernel_pos_2sqrt_q",
                "candidate_class_count": 1,
                "model_count": 1,
                "kernel_root": "2*sqrt_q",
                "target_a2": "-8*(T^2 + 8*L^2)",
                "target_a4": "16*T^4",
                "required_output": (
                    "reviewable transcript proving the uniform isogeny-Selmer "
                    "rank upper bound for this family/kernel"
                ),
                "status": "open",
                "selmer_rank_upper_bound_proved": False,
                "family_exclusion_proved": False,
            },
        ],
    }


def test_materialize_rank_zero_selmer_packages_writes_json_and_markdown(
    tmp_path: Path,
) -> None:
    packages_dir = tmp_path / "packages"

    manifest = materialize_rank_zero_selmer_packages(
        package_index=_package_index(),
        packages_dir=packages_dir,
    )

    assert manifest["status"] == "ok"
    assert manifest["package_count"] == 2
    assert manifest["open_package_count"] == 2
    assert manifest["materialized_json_count"] == 2
    assert manifest["materialized_markdown_count"] == 2
    assert manifest["selmer_rank_upper_bound_proved_count"] == 0
    assert manifest["family_exclusion_proved_count"] == 0
    assert manifest["checks"] == {
        "package_index_ready": True,
        "package_count_matches_index": True,
        "all_packages_open": True,
        "selmer_rank_upper_bound_count_zero": True,
        "family_exclusion_claim_count_zero": True,
        "search_count_rejected_as_progress": True,
    }
    assert manifest["boundary"] == BOUNDARY

    json_path = packages_dir / "rank-zero-selmer-AA-kernel-minus-p.json"
    markdown_path = packages_dir / "rank-zero-selmer-AA-kernel-minus-p.md"
    assert json_path.is_file()
    assert markdown_path.is_file()

    package_payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert package_payload["package_id"] == "rank-zero-selmer-AA-kernel-minus-p"
    assert package_payload["status"] == "open"
    assert package_payload["transcript_status"] == "missing"
    assert package_payload["proof_claim"] == "none"
    assert package_payload["required_transcript_fields"] == REQUIRED_TRANSCRIPT_FIELDS
    assert package_payload["symbolic_model"] == {
        "T": "A+B",
        "L_role": "A for AA, B for BB; AA+BB requires both sides to close",
        "kernel_root": "-p",
        "target_a2": "32*L^2 - 8*T^2",
        "target_a4": "16*(T^2 + 4*L^2)^2",
    }

    markdown = markdown_path.read_text(encoding="utf-8")
    assert "# rank-zero-selmer-AA-kernel-minus-p" in markdown
    assert "Status: open" in markdown
    assert "target_a2 = 32*L^2 - 8*T^2" in markdown
    assert "transcript_status = missing" in markdown
    assert "No Selmer rank upper bound is proved by this file." in markdown


def test_materialize_rank_zero_selmer_packages_reports_bad_index(
    tmp_path: Path,
) -> None:
    package_index = _package_index()
    package_index["ready"] = False
    package_index["status"] = "issues"

    manifest = materialize_rank_zero_selmer_packages(
        package_index=package_index,
        packages_dir=tmp_path / "packages",
    )

    assert manifest["status"] == "issues"
    assert manifest["violations"] == ["package_index_ready"]


def test_materialize_rank_zero_selmer_packages_cli_writes_manifest(
    tmp_path: Path,
) -> None:
    package_index = tmp_path / "package_index.json"
    packages_dir = tmp_path / "packages"
    out = tmp_path / "manifest.json"
    package_index.write_text(json.dumps(_package_index()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/materialize_closure_quotient_rank_zero_selmer_packages.py",
            "--package-index",
            str(package_index),
            "--packages-dir",
            str(packages_dir),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "package_count=2" in result.stdout
    manifest = json.loads(out.read_text(encoding="utf-8"))
    assert manifest["materialized_json_count"] == 2
    assert manifest["materialized_markdown_count"] == 2


def test_write_json_writes_sorted_rank_zero_selmer_package_manifest(
    tmp_path: Path,
) -> None:
    out = tmp_path / "manifest.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
