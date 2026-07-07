from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_rank_zero_selmer_local_supports import (
    BOUNDARY,
    audit_rank_zero_selmer_local_supports,
    write_json,
)


def _package_index() -> dict[str, object]:
    return {
        "status": "ok",
        "ready": True,
        "package_count": 3,
        "open_package_count": 3,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "packages": [
            {
                "package_id": "rank-zero-selmer-AA-kernel-minus-p",
                "family_pattern": "AA",
                "kernel": "kernel_minus_p",
                "status": "open",
            },
            {
                "package_id": "rank-zero-selmer-AA-kernel-pos-2sqrt-q",
                "family_pattern": "AA",
                "kernel": "kernel_pos_2sqrt_q",
                "status": "open",
            },
            {
                "package_id": "rank-zero-selmer-BB-kernel-neg-2sqrt-q",
                "family_pattern": "BB",
                "kernel": "kernel_neg_2sqrt_q",
                "status": "open",
            },
        ],
    }


def test_rank_zero_selmer_local_supports_exports_symbolic_supports() -> None:
    audit = audit_rank_zero_selmer_local_supports(package_index=_package_index())

    assert audit["status"] == "ok"
    assert audit["package_count"] == 3
    assert audit["support_entry_count"] == 3
    assert audit["local_condition_proved_count"] == 0
    assert audit["selmer_rank_upper_bound_proved_count"] == 0
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["support_candidates_not_conditions"] is True
    assert audit["search_count_used_as_progress"] is False
    assert audit["boundary"] == BOUNDARY

    by_kernel = {entry["kernel"]: entry for entry in audit["support_entries"]}
    assert by_kernel["kernel_minus_p"]["quadratic_discriminant"] == (
        "-1024*L^2*T^2"
    )
    assert by_kernel["kernel_minus_p"]["quadratic_discriminant_squareclass"] == "-1"
    assert by_kernel["kernel_pos_2sqrt_q"]["quadratic_discriminant"] == (
        "1024*L^2*(T^2 + 4*L^2)"
    )
    assert by_kernel["kernel_pos_2sqrt_q"][
        "quadratic_discriminant_squareclass"
    ] == "T^2 + 4*L^2"
    assert by_kernel["kernel_neg_2sqrt_q"]["quadratic_discriminant"] == (
        "256*T^2*(T^2 + 4*L^2)"
    )
    assert by_kernel["kernel_neg_2sqrt_q"][
        "quadratic_discriminant_squareclass"
    ] == "T^2 + 4*L^2"
    assert by_kernel["kernel_minus_p"]["candidate_bad_factors"] == [
        "2",
        "L",
        "T",
        "T^2 + 4*L^2",
    ]


def test_rank_zero_selmer_local_supports_reports_bad_package_index() -> None:
    package_index = _package_index()
    package_index["status"] = "issues"
    package_index["ready"] = False

    audit = audit_rank_zero_selmer_local_supports(package_index=package_index)

    assert audit["status"] == "issues"
    assert audit["violations"] == ["package_index_not_ready"]


def test_rank_zero_selmer_local_supports_cli_writes_audit(tmp_path: Path) -> None:
    package_index = tmp_path / "package_index.json"
    out = tmp_path / "local_supports.json"
    package_index.write_text(json.dumps(_package_index()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_rank_zero_selmer_local_supports.py",
            "--package-index",
            str(package_index),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "support_entry_count=3" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))[
        "support_candidates_not_conditions"
    ] is True


def test_write_json_writes_sorted_rank_zero_selmer_local_supports(
    tmp_path: Path,
) -> None:
    out = tmp_path / "local_supports.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
