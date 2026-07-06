from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_mixed_closure_residual_language import (
    audit_language,
    write_json,
)


def test_audit_language_accepts_explicit_candidate_boundaries(tmp_path: Path) -> None:
    doc = tmp_path / "safe.md"
    doc.write_text(
        "\n".join(
            [
                "Residual covers are explicit Sha[2] candidates.",
                "Every cover keeps proof_status = candidate-not-proof.",
                "A bounded search is not a proof that the cover has no rational point.",
                "BSD conditional rank zero is diagnostic evidence, not a strict rank certificate.",
            ]
        ),
        encoding="utf-8",
    )

    audit = audit_language([doc])

    assert audit == {
        "files": 1,
        "violations": [],
        "required_boundary_hits": {
            "bounded_search_not_proof": 1,
            "bsd_not_strict_certificate": 1,
            "candidate_not_proof": 1,
            "sha2_candidate": 1,
        },
        "boundary": (
            "This language audit checks residual-cover wording. It does not "
            "verify the mathematics; it only helps prevent numerical evidence "
            "from being written as a proof."
        ),
    }


def test_audit_language_flags_forbidden_overclaims(tmp_path: Path) -> None:
    doc = tmp_path / "bad.md"
    doc.write_text(
        "\n".join(
            [
                "The bounded search proves no rational point exists.",
                "BSD diagnostic is a strict rank certificate here.",
            ]
        ),
        encoding="utf-8",
    )

    audit = audit_language([doc])

    assert audit["violations"] == [
        {
            "path": str(doc),
            "line": 1,
            "kind": "bounded-search-proof-overclaim",
            "text": "The bounded search proves no rational point exists.",
        },
        {
            "path": str(doc),
            "line": 2,
            "kind": "bsd-strict-certificate-overclaim",
            "text": "BSD diagnostic is a strict rank certificate here.",
        },
    ]


def test_language_audit_cli_strict_exits_nonzero_on_violation(tmp_path: Path) -> None:
    doc = tmp_path / "bad.md"
    out = tmp_path / "audit.json"
    doc.write_text("hyperellratpoints proves cover has no rational point\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_mixed_closure_residual_language.py",
            "--path",
            str(doc),
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
    assert "violations=1" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["violations"][0]["kind"] == (
        "bounded-search-proof-overclaim"
    )


def test_write_json_writes_sorted_language_audit(tmp_path: Path) -> None:
    out = tmp_path / "language.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
