from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_mixed_closure_rank0_certificates import (
    audit_rows,
    write_json,
)


def _rank0_row(
    *,
    A: int,
    B: int,
    curve: str,
    certificate: dict[str, object] | None,
) -> dict[str, object]:
    row: dict[str, object] = {
        "A": A,
        "B": B,
        "curve": curve,
        "status": "ok",
        "rank_lower": 0,
        "rank_upper": 0,
    }
    if certificate is not None:
        row["rank0_torsion_certificate"] = certificate
    return row


def test_audit_rows_reports_rank0_aabb_certificate_violations() -> None:
    rows = [
        _rank0_row(
            A=9,
            B=35,
            curve="AA",
            certificate={
                "status": "certified",
                "affine_preimage_count": 2,
                "affine_preimage_classifications": [
                    {"is_midpoint": True, "is_full_closed_square": False},
                    {"is_midpoint": True, "is_full_closed_square": False},
                ],
                "certifies_no_full_closed_square": True,
                "all_affine_preimages_are_midpoints": True,
            },
        ),
        _rank0_row(
            A=11,
            B=39,
            curve="BB",
            certificate={
                "status": "certified",
                "affine_preimage_count": 2,
                "affine_preimage_classifications": [
                    {"is_midpoint": True, "is_full_closed_square": False},
                    {"is_midpoint": True, "is_full_closed_square": False},
                ],
                "certifies_no_full_closed_square": True,
                "all_affine_preimages_are_midpoints": False,
            },
        ),
        _rank0_row(
            A=13,
            B=41,
            curve="AA",
            certificate={
                "status": "certified",
                "affine_preimage_count": 3,
                "affine_preimage_classifications": [
                    {"is_midpoint": True, "is_full_closed_square": False},
                    {"is_midpoint": True, "is_full_closed_square": False},
                    {"is_midpoint": True, "is_full_closed_square": False},
                ],
                "certifies_no_full_closed_square": False,
                "all_affine_preimages_are_midpoints": True,
            },
        ),
        _rank0_row(
            A=14,
            B=42,
            curve="AA",
            certificate={
                "status": "certified",
                "affine_preimage_count": 2,
                "affine_preimage_classifications": [
                    {"is_midpoint": True, "is_full_closed_square": False},
                ],
                "certifies_no_full_closed_square": True,
                "all_affine_preimages_are_midpoints": True,
            },
        ),
        _rank0_row(
            A=15,
            B=43,
            curve="BB",
            certificate={
                "status": "certified",
                "affine_preimage_count": 2,
                "affine_preimage_classifications": [
                    {"is_midpoint": True, "is_full_closed_square": False},
                    {"is_midpoint": False, "is_full_closed_square": True},
                ],
                "certifies_no_full_closed_square": True,
                "all_affine_preimages_are_midpoints": True,
            },
        ),
        _rank0_row(A=16, B=44, curve="BB", certificate=None),
        {
            "A": 17,
            "B": 45,
            "curve": "AB",
            "status": "ok",
            "rank_lower": 0,
            "rank_upper": 0,
        },
        {
            "A": 19,
            "B": 47,
            "curve": "AA",
            "status": "ok",
            "rank_lower": 0,
            "rank_upper": 2,
        },
    ]

    audit = audit_rows(rows)

    assert audit == {
        "rows": 8,
        "rank0_aabb_rows": 6,
        "certified_rows": 5,
        "strict_no_full_closed_rows": 4,
        "only_midpoint_rows": 4,
        "classification_detail_rows": 5,
        "classification_detail_point_count": 10,
        "affine_preimage_counts": {"2": 4, "3": 1},
        "strict_excluded_pair_count": 4,
        "strict_excluded_pairs": [
            {"A": 9, "B": 35, "certifying_curves": ["AA"]},
            {"A": 11, "B": 39, "certifying_curves": ["BB"]},
            {"A": 14, "B": 42, "certifying_curves": ["AA"]},
            {"A": 15, "B": 43, "certifying_curves": ["BB"]},
        ],
        "violation_counts": {
            "missing-or-uncertified-certificate": 1,
            "not-only-midpoint": 1,
            "classification-count-mismatch": 1,
            "classification-not-midpoint": 1,
            "classification-full-closed-square": 1,
            "does-not-certify-no-full-closed-square": 1,
        },
        "violations": [
            {
                "A": 11,
                "B": 39,
                "curve": "BB",
                "reason": "not-only-midpoint",
            },
            {
                "A": 13,
                "B": 41,
                "curve": "AA",
                "reason": "does-not-certify-no-full-closed-square",
            },
            {
                "A": 14,
                "B": 42,
                "curve": "AA",
                "reason": "classification-count-mismatch",
            },
            {
                "A": 15,
                "B": 43,
                "curve": "BB",
                "reason": "classification-not-midpoint",
            },
            {
                "A": 15,
                "B": 43,
                "curve": "BB",
                "reason": "classification-full-closed-square",
            },
            {
                "A": 16,
                "B": 44,
                "curve": "BB",
                "reason": "missing-or-uncertified-certificate",
            },
        ],
        "certificate_scope": "AA/BB rows with exact rank 0/0 only",
        "proof_boundary": (
            "This audits stored torsion-pullback certificates; it does not "
            "certify rank by itself."
        ),
    }


def test_audit_cli_exits_nonzero_when_strict_flag_finds_violations(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "mixed.jsonl"
    out_path = tmp_path / "audit.json"
    input_path.write_text(
        json.dumps(
            _rank0_row(
                A=9,
                B=35,
                curve="AA",
                certificate={
                    "status": "certified",
                    "affine_preimage_count": 2,
                    "affine_preimage_classifications": [
                        {"is_midpoint": True, "is_full_closed_square": False},
                        {"is_midpoint": True, "is_full_closed_square": False},
                    ],
                    "certifies_no_full_closed_square": True,
                    "all_affine_preimages_are_midpoints": False,
                },
            )
        )
        + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_mixed_closure_rank0_certificates.py",
            "--input",
            str(input_path),
            "--out",
            str(out_path),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "violations=1" in result.stdout
    assert json.loads(out_path.read_text(encoding="utf-8"))["violation_counts"] == {
        "not-only-midpoint": 1
    }


def test_write_json_writes_sorted_audit(tmp_path: Path) -> None:
    out_path = tmp_path / "audit.json"

    write_json(out_path, {"b": 1, "a": 2})

    assert out_path.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
