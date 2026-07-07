from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_sage_cover_tool_capabilities import (
    audit_cover_capabilities,
    write_json,
)


def _handoff() -> dict[str, object]:
    return {
        "A": 1625,
        "B": 5643,
        "curve": "AA",
        "target_covers": [
            {
                "index": 4,
                "quartic": (
                    "2510769*x^4 - 4527908*x^3 - 7744107*x^2 "
                    "+ 3743936*x + 3498741"
                ),
            },
            {
                "index": 3,
                "quartic": (
                    "444809*x^4 + 3153444*x^3 - 2778939*x^2 "
                    "- 15767220*x + 11120225"
                ),
            },
        ],
    }


def test_audit_cover_capabilities_records_sage_interface_boundary() -> None:
    audit = audit_cover_capabilities(
        handoff=_handoff(),
        sage_probe={
            "status": "ok",
            "covers": [
                {
                    "index": 4,
                    "genus": 1,
                    "has_rational_points_method": True,
                    "has_local_points_method": False,
                    "has_is_locally_solvable_method": False,
                    "has_two_cover_descent_method": False,
                    "jacobian_has_rank_method": False,
                    "jacobian_has_gens_method": False,
                    "jacobian_has_elliptic_curve_method": False,
                },
                {
                    "index": 3,
                    "genus": 1,
                    "has_rational_points_method": True,
                    "has_local_points_method": False,
                    "has_is_locally_solvable_method": False,
                    "has_two_cover_descent_method": False,
                    "jacobian_has_rank_method": False,
                    "jacobian_has_gens_method": False,
                    "jacobian_has_elliptic_curve_method": False,
                },
            ],
        },
    )

    assert audit == {
        "status": "ok",
        "ready": True,
        "target": {"A": 1625, "B": 5643, "curve": "AA"},
        "cover_count": 2,
        "genus_one_cover_count": 2,
        "sage_direct_no_point_capable_count": 0,
        "strict_certificate_ready_count": 0,
        "recommended_next_tool": "magma-or-specialized-cover-descent",
        "covers": [
            {
                "index": 4,
                "genus": 1,
                "has_bounded_rational_points_method": True,
                "has_direct_local_solubility_method": False,
                "has_direct_two_cover_descent_method": False,
                "jacobian_has_rank_method": False,
                "jacobian_has_gens_method": False,
                "jacobian_has_elliptic_curve_method": False,
                "strict_certificate_ready": False,
                "proof_status": "sage-interface-not-proof",
            },
            {
                "index": 3,
                "genus": 1,
                "has_bounded_rational_points_method": True,
                "has_direct_local_solubility_method": False,
                "has_direct_two_cover_descent_method": False,
                "jacobian_has_rank_method": False,
                "jacobian_has_gens_method": False,
                "jacobian_has_elliptic_curve_method": False,
                "strict_certificate_ready": False,
                "proof_status": "sage-interface-not-proof",
            },
        ],
        "boundary": (
            "This audits Sage cover-level tool availability. Missing direct "
            "interfaces and bounded point searches are not no-point proofs."
        ),
    }


def test_cover_capability_cli_strict_exits_nonzero_on_missing_handoff(
    tmp_path: Path,
) -> None:
    out = tmp_path / "audit.json"
    missing = tmp_path / "missing.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_sage_cover_tool_capabilities.py",
            "--handoff",
            str(missing),
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


def test_write_json_writes_sorted_cover_capability_audit(tmp_path: Path) -> None:
    out = tmp_path / "audit.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
