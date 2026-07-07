from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.audit_mixed_closure_frontier_strictification_attempts import (
    audit_attempts,
    parse_probe_arg,
    write_json,
)


def _queue() -> dict[str, object]:
    return {
        "status": "ok",
        "targets": [
            {
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "track": "rank-zero-rank-proof",
                "priorities": [5, 7],
                "cover_indices": [3, 4],
                "rank_bounds": [0, 2],
                "strict_certificate_ready": False,
                "candidate_not_proof": True,
            },
            {
                "A": 567,
                "B": 3757,
                "curve": "BB",
                "track": "rank-zero-rank-proof",
                "priorities": [6, 21],
                "cover_indices": [3, 4],
                "rank_bounds": [0, 2],
                "strict_certificate_ready": False,
                "candidate_not_proof": True,
            }
        ],
    }


def _timeout_probe() -> dict[str, object]:
    return {
        "A": 1625,
        "B": 5643,
        "curve": "AA",
        "status": "timeout",
        "timeout_seconds": 180,
        "boundary": "timeout is not a proof",
    }


def _rank_zero_probe() -> dict[str, object]:
    return {
        "A": 1625,
        "B": 5643,
        "curve": "AA",
        "status": "ok",
        "sage": {
            "rank_bounds": [0, 0],
            "rank_proof_status": "ok",
            "rank_proof": 0,
            "covers": [
                {"index": 3, "rational_point_count": 0},
                {"index": 4, "rational_point_count": 0},
            ],
        },
        "boundary": "rank proof transcript still needs downstream audit",
    }


def _rank_method_timeout_probe() -> dict[str, object]:
    return {
        "A": 1625,
        "B": 5643,
        "curve": "AA",
        "status": "ok",
        "method_status_counts": {
            "rank_bounds:ok": 1,
            "rank_proof:runtime-error": 1,
            "two_descent:timeout": 1,
        },
        "method_results": [
            {"method": "rank_bounds", "status": "ok", "rank_bounds": [0, 2]},
            {
                "method": "rank_proof",
                "status": "runtime-error",
                "error": "rank not provably correct",
            },
            {"method": "two_descent", "status": "timeout", "timeout_seconds": 90},
        ],
        "rank_zero_proof_candidate": False,
        "boundary": "rank method timeout is not a proof",
    }


def _rank_method_zero_probe() -> dict[str, object]:
    return {
        "A": 1625,
        "B": 5643,
        "curve": "AA",
        "status": "ok",
        "method_status_counts": {"rank_proof:ok": 1},
        "method_results": [{"method": "rank_proof", "status": "ok", "rank": 0}],
        "rank_zero_proof_candidate": True,
        "boundary": "rank proof candidate needs downstream audit",
    }


def _mwrank_open_probe() -> dict[str, object]:
    return {
        "status": "ok",
        "target": {"A": 1625, "B": 5643, "curve": "AA"},
        "rank_bounds": [0, 2],
        "rank_proved": False,
        "rank_zero_proof_candidate": False,
        "proof_status": "open-rank-bounds-not-proof",
        "boundary": "mwrank open rank bounds are not a proof",
    }


def _batch_rank_method_probe() -> dict[str, object]:
    return {
        "status": "ok",
        "target_count": 2,
        "method_status_counts": {
            "pari_ellrank:ok": 2,
            "rank_bounds:ok": 2,
            "selmer_rank:ok": 2,
        },
        "rank_zero_proof_candidate_count": 0,
        "targets": [
            {
                "name": "priority_005_1625_5643_AA_covers_4_3",
                "A": 1625,
                "B": 5643,
                "curve": "AA",
                "track": "rank-zero-rank-proof",
                "probe": {
                    "A": 1625,
                    "B": 5643,
                    "curve": "AA",
                    "status": "ok",
                    "method_status_counts": {
                        "pari_ellrank:ok": 1,
                        "rank_bounds:ok": 1,
                        "selmer_rank:ok": 1,
                    },
                    "method_results": [
                        {
                            "method": "rank_bounds",
                            "status": "ok",
                            "rank_bounds": [0, 2],
                        },
                        {"method": "selmer_rank", "status": "ok", "selmer_rank": 4},
                        {
                            "method": "pari_ellrank",
                            "status": "ok",
                            "rank_bounds": [0, 2],
                            "ellrank": ["0", "2", "0", "[]"],
                        },
                    ],
                    "rank_zero_proof_candidate": False,
                },
            },
            {
                "name": "priority_006_567_3757_BB_covers_4_3",
                "A": 567,
                "B": 3757,
                "curve": "BB",
                "track": "rank-zero-rank-proof",
                "probe": {
                    "A": 567,
                    "B": 3757,
                    "curve": "BB",
                    "status": "ok",
                    "method_status_counts": {
                        "pari_ellrank:ok": 1,
                        "rank_bounds:ok": 1,
                        "selmer_rank:ok": 1,
                    },
                    "method_results": [
                        {
                            "method": "rank_bounds",
                            "status": "ok",
                            "rank_bounds": [0, 2],
                        },
                        {"method": "selmer_rank", "status": "ok", "selmer_rank": 4},
                        {
                            "method": "pari_ellrank",
                            "status": "ok",
                            "rank_bounds": [0, 2],
                            "ellrank": ["0", "2", "0", "[]"],
                        },
                    ],
                    "rank_zero_proof_candidate": False,
                },
            },
        ],
        "boundary": "batch rank method probe is diagnostic only",
    }


def test_audit_attempts_records_timeout_as_nonproof(tmp_path: Path) -> None:
    probe_path = tmp_path / "probe.json"
    probe_path.write_text(json.dumps(_timeout_probe()) + "\n", encoding="utf-8")

    audit = audit_attempts(
        strictification_queue=_queue(),
        probes=[("sage-twodescent20", probe_path)],
    )

    assert audit == {
        "status": "ok",
        "ready": True,
        "attempt_count": 1,
        "target_count_with_attempts": 1,
        "strict_certificate_ready_count": 0,
        "candidate_not_proof": True,
        "missing_files": [],
        "violations": [],
        "attempt_status_counts": {"timeout-not-proof": 1},
        "attempts": [
            {
                "name": "sage-twodescent20",
                "path": str(probe_path),
                "target": {"A": 1625, "B": 5643, "curve": "AA"},
                "track": "rank-zero-rank-proof",
                "status": "timeout",
                "rank_bounds": [],
                "rank_proof_status": "",
                "method_status_counts": {},
                "two_descent_status": "",
                "strict_certificate_ready": False,
                "proof_status": "timeout-not-proof",
                "boundary": (
                    "This records a strictification attempt. Timeout, runtime "
                    "error, open rank bounds, and bounded point search are not proofs."
                ),
            }
        ],
        "boundary": (
            "This ledger records strictification attempts. It does not prove "
            "that residual covers have no rational point."
        ),
    }


def test_audit_attempts_marks_rank_zero_probe_as_ready_candidate(tmp_path: Path) -> None:
    probe_path = tmp_path / "probe.json"
    probe_path.write_text(json.dumps(_rank_zero_probe()) + "\n", encoding="utf-8")

    audit = audit_attempts(
        strictification_queue=_queue(),
        probes=[("sage-rank-proof", probe_path)],
    )

    assert audit["status"] == "ok"
    assert audit["strict_certificate_ready_count"] == 1
    assert audit["candidate_not_proof"] is False
    assert audit["attempt_status_counts"] == {"rank-zero-proof-candidate": 1}
    assert audit["attempts"][0]["proof_status"] == "rank-zero-proof-candidate"
    assert audit["attempts"][0]["strict_certificate_ready"] is True


def test_audit_attempts_records_rank_method_timeout_as_nonproof(tmp_path: Path) -> None:
    probe_path = tmp_path / "rank_methods.json"
    probe_path.write_text(
        json.dumps(_rank_method_timeout_probe()) + "\n",
        encoding="utf-8",
    )

    audit = audit_attempts(
        strictification_queue=_queue(),
        probes=[("sage-rank-methods", probe_path)],
    )

    assert audit["status"] == "ok"
    assert audit["strict_certificate_ready_count"] == 0
    assert audit["candidate_not_proof"] is True
    assert audit["attempt_status_counts"] == {"rank-method-timeout-not-proof": 1}
    assert audit["attempts"][0]["proof_status"] == "rank-method-timeout-not-proof"
    assert audit["attempts"][0]["method_status_counts"] == {
        "rank_bounds:ok": 1,
        "rank_proof:runtime-error": 1,
        "two_descent:timeout": 1,
    }


def test_audit_attempts_records_mwrank_open_bounds_as_nonproof(tmp_path: Path) -> None:
    probe_path = tmp_path / "mwrank.json"
    probe_path.write_text(json.dumps(_mwrank_open_probe()) + "\n", encoding="utf-8")

    audit = audit_attempts(
        strictification_queue=_queue(),
        probes=[("mwrank-default", probe_path)],
    )

    assert audit["status"] == "ok"
    assert audit["target_count_with_attempts"] == 1
    assert audit["attempt_status_counts"] == {"open-rank-bounds-not-proof": 1}
    assert audit["attempts"][0]["target"] == {"A": 1625, "B": 5643, "curve": "AA"}
    assert audit["attempts"][0]["track"] == "rank-zero-rank-proof"
    assert audit["attempts"][0]["rank_bounds"] == [0, 2]
    assert audit["attempts"][0]["proof_status"] == "open-rank-bounds-not-proof"
    assert audit["attempts"][0]["strict_certificate_ready"] is False


def test_audit_attempts_marks_rank_method_zero_probe_as_ready_candidate(
    tmp_path: Path,
) -> None:
    probe_path = tmp_path / "rank_methods.json"
    probe_path.write_text(
        json.dumps(_rank_method_zero_probe()) + "\n",
        encoding="utf-8",
    )

    audit = audit_attempts(
        strictification_queue=_queue(),
        probes=[("sage-rank-methods", probe_path)],
    )

    assert audit["strict_certificate_ready_count"] == 1
    assert audit["candidate_not_proof"] is False
    assert audit["attempt_status_counts"] == {"rank-zero-proof-candidate": 1}
    assert audit["attempts"][0]["proof_status"] == "rank-zero-proof-candidate"


def test_audit_attempts_expands_batch_rank_method_probe(tmp_path: Path) -> None:
    batch_path = tmp_path / "batch_rank_methods.json"
    batch_path.write_text(
        json.dumps(_batch_rank_method_probe()) + "\n",
        encoding="utf-8",
    )

    audit = audit_attempts(
        strictification_queue=_queue(),
        probes=[],
        batch_probes=[("rankzero-batch-t45", batch_path)],
    )

    assert audit["status"] == "ok"
    assert audit["attempt_count"] == 2
    assert audit["target_count_with_attempts"] == 2
    assert audit["strict_certificate_ready_count"] == 0
    assert audit["candidate_not_proof"] is True
    assert audit["attempt_status_counts"] == {"rank-method-open-not-proof": 2}
    assert [attempt["name"] for attempt in audit["attempts"]] == [
        "rankzero-batch-t45:priority_005_1625_5643_AA_covers_4_3",
        "rankzero-batch-t45:priority_006_567_3757_BB_covers_4_3",
    ]
    assert audit["attempts"][0]["method_status_counts"] == {
        "pari_ellrank:ok": 1,
        "rank_bounds:ok": 1,
        "selmer_rank:ok": 1,
    }


def test_audit_attempts_reports_probe_for_unknown_target(tmp_path: Path) -> None:
    probe = _timeout_probe()
    probe["B"] = 999
    probe_path = tmp_path / "probe.json"
    probe_path.write_text(json.dumps(probe) + "\n", encoding="utf-8")

    audit = audit_attempts(
        strictification_queue=_queue(),
        probes=[("bad-target", probe_path)],
    )

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert audit["violations"] == [
        {
            "name": "bad-target",
            "field": "target",
            "expected": "target present in strictification queue",
            "actual": {"A": 1625, "B": 999, "curve": "AA"},
        }
    ]


def test_attempt_ledger_cli_strict_exits_nonzero_when_not_ready(tmp_path: Path) -> None:
    queue_path = tmp_path / "queue.json"
    missing_probe = tmp_path / "missing.json"
    out = tmp_path / "audit.json"
    queue_path.write_text(json.dumps(_queue()) + "\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_mixed_closure_frontier_strictification_attempts.py",
            "--strictification-queue",
            str(queue_path),
            "--probe",
            f"missing:{missing_probe}",
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
    assert json.loads(out.read_text(encoding="utf-8"))["missing_files"] == [
        {"name": "missing", "kind": "probe", "path": str(missing_probe)}
    ]


def test_attempt_ledger_cli_accepts_batch_probe(tmp_path: Path) -> None:
    queue_path = tmp_path / "queue.json"
    batch_path = tmp_path / "batch.json"
    out = tmp_path / "audit.json"
    queue_path.write_text(json.dumps(_queue()) + "\n", encoding="utf-8")
    batch_path.write_text(
        json.dumps(_batch_rank_method_probe()) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/theory/audit_mixed_closure_frontier_strictification_attempts.py",
            "--strictification-queue",
            str(queue_path),
            "--batch-probe",
            f"rankzero-batch-t45:{batch_path}",
            "--out",
            str(out),
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert "attempt_count=2" in result.stdout
    assert payload["attempt_status_counts"] == {"rank-method-open-not-proof": 2}


def test_parse_probe_arg_requires_name_and_path() -> None:
    assert parse_probe_arg("one:/tmp/probe.json") == ("one", Path("/tmp/probe.json"))


def test_write_json_writes_sorted_attempt_ledger(tmp_path: Path) -> None:
    out = tmp_path / "ledger.json"

    write_json(out, {"b": 1, "a": 2})

    assert out.read_text(encoding="utf-8") == '{\n  "a": 2,\n  "b": 1\n}\n'
