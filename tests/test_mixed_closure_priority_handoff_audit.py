from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_mixed_closure_priority_handoffs import (
    audit_priority_handoffs,
    write_json,
)


def _priorities() -> dict[str, object]:
    return {
        "rows": [
            {
                "priority": 1,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 3,
                "quartic": "41*x^4 + 1025",
                "proof_status": "candidate-not-proof",
                "selmer_gap": 2,
            },
            {
                "priority": 2,
                "A": 115,
                "B": 297,
                "curve": "AA",
                "cover_index": 4,
                "quartic": "-19*x^4 - 5",
                "proof_status": "candidate-not-proof",
                "selmer_gap": 2,
            },
        ]
    }


def _write_complete_group(handoff_dir: Path) -> None:
    name = "priority_001_115_297_AA_covers_3_4"
    handoff = {
        "A": 115,
        "B": 297,
        "curve": "AA",
        "priority_source": {"name": name, "priorities": [1, 2]},
        "strict_proof_status": "open",
        "proof_boundary": "This handoff does not prove that any cover has no rational point.",
        "target_cover_indices": [3, 4],
        "target_covers": [
            {"index": 3, "quartic": "41*x^4 + 1025", "point_count": 0},
            {"index": 4, "quartic": "-19*x^4 - 5", "point_count": 0},
        ],
    }
    probe = {
        "A": 115,
        "B": 297,
        "curve": "AA",
        "status": "ok",
        "sage": {
            "rank_bounds": [0, 2],
            "rank_probable": 0,
            "rank_proof_status": "runtime-error",
            "selmer_rank": 4,
            "torsion_two_dimension": 2,
            "covers": [
                {
                    "index": 3,
                    "point_search_status": "ok",
                    "rational_point_count": 0,
                },
                {
                    "index": 4,
                    "point_search_status": "ok",
                    "rational_point_count": 0,
                },
            ],
        },
    }
    map_verify = {
        "A": 115,
        "B": 297,
        "curve": "AA",
        "status": "ok",
        "sage": {
            "all_verified": True,
            "covers": [
                {
                    "index": 3,
                    "map_parse_status": "ok",
                    "identity_verified": True,
                },
                {
                    "index": 4,
                    "map_parse_status": "ok",
                    "identity_verified": True,
                },
            ],
        },
    }
    local_witnesses = {
        "A": 115,
        "B": 297,
        "curve": "AA",
        "status": "ok",
        "sage": {
            "all_bad_primes_witnessed": True,
            "covers": [
                {
                    "index": 3,
                    "bad_primes": [2, 5],
                    "all_witnessed": True,
                    "witnesses": [
                        {"p": 2, "status": "ok", "kind": "infinity"},
                        {"p": 5, "status": "ok", "kind": "finite", "x": "1"},
                    ],
                },
                {
                    "index": 4,
                    "bad_primes": [2, 19],
                    "all_witnessed": True,
                    "witnesses": [
                        {"p": 2, "status": "ok", "kind": "finite", "x": "-1"},
                        {"p": 19, "status": "ok", "kind": "finite", "x": "0"},
                    ],
                },
            ],
        },
    }
    handoff_dir.mkdir(parents=True)
    (handoff_dir / f"{name}.json").write_text(
        json.dumps(handoff) + "\n",
        encoding="utf-8",
    )
    (handoff_dir / f"{name}.sage").write_text("sage handoff\n", encoding="utf-8")
    (handoff_dir / f"{name}.magma").write_text("magma handoff\n", encoding="utf-8")
    (handoff_dir / f"{name}_sage_probe.json").write_text(
        json.dumps(probe) + "\n",
        encoding="utf-8",
    )
    (handoff_dir / f"{name}_map_verify.json").write_text(
        json.dumps(map_verify) + "\n",
        encoding="utf-8",
    )
    (handoff_dir / f"{name}_local_witnesses.json").write_text(
        json.dumps(local_witnesses) + "\n",
        encoding="utf-8",
    )


def test_audit_priority_handoffs_marks_ready_when_handoffs_and_probes_align(
    tmp_path: Path,
) -> None:
    handoff_dir = tmp_path / "handoffs"
    _write_complete_group(handoff_dir)

    audit = audit_priority_handoffs(
        priorities=_priorities(),
        handoff_dir=handoff_dir,
        top=2,
        require_probes=True,
        require_map_verifications=True,
        require_local_witnesses=True,
    )

    assert audit == {
        "ready": True,
        "top": 2,
        "groups_checked": 1,
        "priority_rows_checked": 2,
        "target_cover_count": 2,
        "missing_files": [],
        "violations": [],
        "probe_status_counts": {"ok": 1},
        "map_verify_status_counts": {"ok": 1},
        "local_witness_status_counts": {"ok": 1},
        "groups": [
            {
                "name": "priority_001_115_297_AA_covers_3_4",
                "target": {"A": 115, "B": 297, "curve": "AA"},
                "priorities": [1, 2],
                "cover_indices": [3, 4],
                "max_selmer_gap": 2,
                "rank_bounds": [0, 2],
                "rank_probable": 0,
                "rank_proof_status": "runtime-error",
                "selmer_minus_torsion2": 2,
                "cover_point_counts": [0, 0],
                "map_all_verified": True,
                "map_verified_cover_count": 2,
                "local_all_bad_primes_witnessed": True,
                "local_bad_prime_count": 4,
            }
        ],
        "boundary": (
            "This audits priority handoff/probe alignment. It does not prove "
            "that residual covers have no rational point."
        ),
    }


def test_audit_priority_handoffs_reports_missing_required_probe(tmp_path: Path) -> None:
    handoff_dir = tmp_path / "handoffs"
    _write_complete_group(handoff_dir)
    (handoff_dir / "priority_001_115_297_AA_covers_3_4_sage_probe.json").unlink()

    audit = audit_priority_handoffs(
        priorities=_priorities(),
        handoff_dir=handoff_dir,
        top=2,
        require_probes=True,
        require_map_verifications=False,
        require_local_witnesses=False,
    )

    assert audit["ready"] is False
    assert audit["missing_files"] == [
        {
            "name": "priority_001_115_297_AA_covers_3_4",
            "kind": "sage_probe",
            "path": str(
                handoff_dir / "priority_001_115_297_AA_covers_3_4_sage_probe.json"
            ),
        }
    ]


def test_audit_priority_handoffs_reports_missing_required_map_verification(
    tmp_path: Path,
) -> None:
    handoff_dir = tmp_path / "handoffs"
    _write_complete_group(handoff_dir)
    (handoff_dir / "priority_001_115_297_AA_covers_3_4_map_verify.json").unlink()

    audit = audit_priority_handoffs(
        priorities=_priorities(),
        handoff_dir=handoff_dir,
        top=2,
        require_probes=True,
        require_map_verifications=True,
        require_local_witnesses=False,
    )

    assert audit["ready"] is False
    assert audit["missing_files"] == [
        {
            "name": "priority_001_115_297_AA_covers_3_4",
            "kind": "map_verify",
            "path": str(
                handoff_dir / "priority_001_115_297_AA_covers_3_4_map_verify.json"
            ),
        }
    ]


def test_audit_priority_handoffs_reports_missing_required_local_witnesses(
    tmp_path: Path,
) -> None:
    handoff_dir = tmp_path / "handoffs"
    _write_complete_group(handoff_dir)
    (handoff_dir / "priority_001_115_297_AA_covers_3_4_local_witnesses.json").unlink()

    audit = audit_priority_handoffs(
        priorities=_priorities(),
        handoff_dir=handoff_dir,
        top=2,
        require_probes=True,
        require_map_verifications=True,
        require_local_witnesses=True,
    )

    assert audit["ready"] is False
    assert audit["missing_files"] == [
        {
            "name": "priority_001_115_297_AA_covers_3_4",
            "kind": "local_witnesses",
            "path": str(
                handoff_dir
                / "priority_001_115_297_AA_covers_3_4_local_witnesses.json"
            ),
        }
    ]


def test_priority_handoff_audit_cli_strict_exits_nonzero_when_not_ready(
    tmp_path: Path,
) -> None:
    priorities = tmp_path / "priorities.json"
    out = tmp_path / "audit.json"
    handoff_dir = tmp_path / "handoffs"
    handoff_dir.mkdir()
    priorities.write_text(json.dumps(_priorities()) + "\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_mixed_closure_priority_handoffs.py",
            "--priorities",
            str(priorities),
            "--handoff-dir",
            str(handoff_dir),
            "--top",
            "2",
            "--require-probes",
            "--require-map-verifications",
            "--require-local-witnesses",
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
    assert "ready=False" in result.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["missing_files"]


def test_write_json_writes_sorted_priority_handoff_audit(tmp_path: Path) -> None:
    out = tmp_path / "audit.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
