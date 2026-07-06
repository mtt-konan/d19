from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_mixed_closure_even_model_identities import (
    audit_identities,
    write_json,
)


def test_audit_identities_verifies_even_model_and_birational_maps() -> None:
    audit = audit_identities()

    assert audit == {
        "identities": [
            {
                "name": "centered_even_quartic",
                "verified": True,
                "statement": (
                    "16*(N^2+L^2)*((S-N)^2+L^2) becomes "
                    "t^4 + p*t^2 + q under t=2*N-S"
                ),
            },
            {
                "name": "quartic_to_elliptic_map",
                "verified": True,
                "statement": (
                    "X=2*(z+t^2), V=2*t*(X+p) sends "
                    "z^2=t^4+p*t^2+q to V^2=X^3+p*X^2-4*q*X-4*p*q"
                ),
            },
            {
                "name": "elliptic_to_quartic_inverse",
                "verified": True,
                "statement": (
                    "t=V/(2*(X+p)), z=X/2-t^2 sends the elliptic equation "
                    "back to z^2=t^4+p*t^2+q when X+p is nonzero"
                ),
            },
        ],
        "all_verified": True,
        "proof_boundary": (
            "This is a symbolic algebra audit of the model identities. "
            "It does not certify ranks or rational points."
        ),
    }


def test_audit_cli_writes_json(tmp_path: Path) -> None:
    out = tmp_path / "identity.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_mixed_closure_even_model_identities.py",
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "all_verified=True" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["all_verified"] is True


def test_write_json_writes_sorted_identity_audit(tmp_path: Path) -> None:
    out = tmp_path / "identity.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
