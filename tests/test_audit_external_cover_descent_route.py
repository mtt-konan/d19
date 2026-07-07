from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_external_cover_descent_route import (
    ACCEPTED_STRICT_ROUTES,
    BOUNDARY,
    REJECTED_PROMOTION_SIGNALS,
    audit_external_route,
    write_json,
)


def _handoff() -> dict[str, object]:
    return {
        "A": 1625,
        "B": 5643,
        "curve": "AA",
        "target_covers": [
            {"index": 4, "quartic": "2510769*x^4 + 3498741"},
            {"index": 3, "quartic": "444809*x^4 + 11120225"},
        ],
    }


def test_external_route_audit_records_missing_magma_as_open_gap() -> None:
    audit = audit_external_route(
        handoff=_handoff(),
        cover_capability_audit={"sage_direct_no_point_capable_count": 0},
        magma_command=None,
    )

    assert audit == {
        "status": "ok",
        "ready": True,
        "target": {"A": 1625, "B": 5643, "curve": "AA"},
        "cover_count": 2,
        "cover_indices": [4, 3],
        "local_magma_available": False,
        "magma_command": None,
        "sage_direct_no_point_capable_count": 0,
        "strict_certificate_ready_count": 0,
        "proof_status": "external-tool-gap-open",
        "recommended_next_action": (
            "obtain-magma-or-specialized-cover-descent-environment"
        ),
        "accepted_strict_routes": list(ACCEPTED_STRICT_ROUTES),
        "rejected_promotion_signals": list(REJECTED_PROMOTION_SIGNALS),
        "boundary": BOUNDARY,
    }


def test_external_route_audit_records_available_magma_as_transcript_needed() -> None:
    audit = audit_external_route(
        handoff=_handoff(),
        cover_capability_audit={"sage_direct_no_point_capable_count": 0},
        magma_command="/usr/local/bin/magma",
    )

    assert audit["local_magma_available"] is True
    assert audit["magma_command"] == "/usr/local/bin/magma"
    assert audit["proof_status"] == "external-transcript-required"
    assert audit["recommended_next_action"] == (
        "run-magma-or-specialized-cover-descent-transcript"
    )
    assert audit["strict_certificate_ready_count"] == 0


def test_external_route_cli_strict_exits_nonzero_on_missing_input(
    tmp_path: Path,
) -> None:
    out = tmp_path / "route.json"
    missing = tmp_path / "missing.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_external_cover_descent_route.py",
            "--handoff",
            str(missing),
            "--sage-cover-capability-audit",
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
    assert json.loads(out.read_text(encoding="utf-8"))["missing_inputs"] == [
        str(missing),
        str(missing),
    ]


def test_write_json_writes_sorted_external_route_audit(tmp_path: Path) -> None:
    out = tmp_path / "route.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
