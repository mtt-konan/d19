from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_closure_quotient_paper_structure import (
    BOUNDARY,
    audit_paper_structure,
    write_json,
)


def _summary() -> dict[str, object]:
    return {
        "ready_for_partial_result": True,
        "strict_certificate": {
            "rank0_torsion_certificates": 275,
            "strict_excluded_pair_count": 220,
        },
        "residual_status": {
            "candidate_cover_total": 27,
            "proof_status": "candidate-not-proof",
        },
        "residual_open_frontier_status": {
            "open_frontier_cover_count": 23,
            "proof_status": "open-frontier-not-proof",
        },
        "frontier_strictification_status": {
            "target_count": 10,
            "cover_count": 23,
            "strict_certificate_ready_count": 0,
        },
        "external_certificate_frontier_status": {
            "target_count": 10,
            "cover_count": 23,
            "certificate_package_ready_count": 0,
            "strict_promotion_ready_count": 0,
            "proof_status": "frontier-external-certificates-missing-not-proof",
        },
    }


def _paper_text() -> str:
    return """
# Closure Quotient Partial Result

**Status:** draft note for a partial result. This document does not claim a proof of the
Harborth conjecture.

## 1. Claim Level

## 2. Main Lemma Draft

## 3. Certified Census

AA/BB rank-0 certificates = 275
strict excluded pairs = 220
certificate status = certified for all 216
certificate status = certified for all 59

### 3.4 Residual 2-cover candidates

candidate_cover_total = 27
proof_status = candidate-not-proof
open_frontier_cover_count = 23
proof_status = open-frontier-not-proof
frontier_strictification_status.target_count = 10
frontier_strictification_status.cover_count = 23
frontier_strictification_status.strict_certificate_ready_count = 0
external_certificate_frontier_status.target_count = 10
external_certificate_frontier_status.cover_count = 23
external_certificate_frontier_status.certificate_package_ready_count = 0
external_certificate_frontier_status.strict_promotion_ready_count = 0
external_certificate_frontier_status.proof_status = frontier-external-certificates-missing-not-proof
bounded search is not a proof
This is an intake gate, not a mathematical verifier.

## 7. Paper Path
"""


def test_paper_structure_audit_accepts_required_partial_result_shape() -> None:
    audit = audit_paper_structure(paper_text=_paper_text(), summary=_summary())

    assert audit == {
        "status": "ok",
        "ready": True,
        "required_section_count": 5,
        "matched_section_count": 5,
        "required_claim_count": 14,
        "matched_claim_count": 14,
        "missing_sections": [],
        "missing_claims": [],
        "boundary": BOUNDARY,
    }


def test_paper_structure_audit_reports_missing_open_boundary() -> None:
    text = _paper_text().replace("proof_status = candidate-not-proof", "")

    audit = audit_paper_structure(paper_text=text, summary=_summary())

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "residual candidate-not-proof status" in audit["missing_claims"]


def test_paper_structure_cli_strict_exits_nonzero_on_missing_claim(
    tmp_path: Path,
) -> None:
    paper = tmp_path / "paper.md"
    summary = tmp_path / "summary.json"
    out = tmp_path / "audit.json"
    paper.write_text("# Missing\n", encoding="utf-8")
    summary.write_text(json.dumps(_summary()) + "\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_closure_quotient_paper_structure.py",
            "--paper",
            str(paper),
            "--summary",
            str(summary),
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "status=issues" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["ready"] is False


def test_write_json_writes_sorted_paper_structure_audit(tmp_path: Path) -> None:
    out = tmp_path / "audit.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
