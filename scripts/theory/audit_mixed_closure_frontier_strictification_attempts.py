#!/usr/bin/env python3
"""Audit residual frontier strictification attempts."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This ledger records strictification attempts. It does not prove that "
    "residual covers have no rational point."
)

ATTEMPT_BOUNDARY = (
    "This records a strictification attempt. Timeout, runtime error, open rank "
    "bounds, and bounded point search are not proofs."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_probe_arg(raw: str) -> tuple[str, Path]:
    name, separator, path = raw.partition(":")
    if not separator or not name or not path:
        raise argparse.ArgumentTypeError("--probe must use NAME:/path/to/probe.json")
    return name, Path(path)


def _int_list(values: Any) -> list[int]:
    return [int(value) for value in values or []]


def _target(payload: dict[str, Any]) -> dict[str, int | str]:
    return {
        "A": int(payload.get("A", 0)),
        "B": int(payload.get("B", 0)),
        "curve": str(payload.get("curve", "")),
    }


def _target_key(payload: dict[str, Any]) -> tuple[int, int, str]:
    return int(payload.get("A", 0)), int(payload.get("B", 0)), str(payload.get("curve", ""))


def _queue_targets(
    strictification_queue: dict[str, Any],
) -> dict[tuple[int, int, str], dict[str, Any]]:
    return {
        _target_key(target): target
        for target in strictification_queue.get("targets", [])
    }


def _proof_status(probe: dict[str, Any]) -> str:
    if probe.get("status") == "timeout":
        return "timeout-not-proof"
    if probe.get("status") != "ok":
        return "attempt-error-not-proof"
    sage = probe.get("sage", {})
    rank_bounds = _int_list(sage.get("rank_bounds", []))
    if rank_bounds == [0, 0] and str(sage.get("rank_proof_status", "")) == "ok":
        return "rank-zero-proof-candidate"
    return "open-rank-bounds-not-proof"


def _attempt_summary(
    *,
    name: str,
    path: Path,
    probe: dict[str, Any],
    queue_target: dict[str, Any] | None,
) -> dict[str, Any]:
    sage = probe.get("sage", {})
    proof_status = _proof_status(probe)
    return {
        "name": name,
        "path": str(path),
        "target": _target(probe),
        "track": "" if queue_target is None else str(queue_target.get("track", "")),
        "status": str(probe.get("status", "")),
        "rank_bounds": _int_list(sage.get("rank_bounds", [])),
        "rank_proof_status": str(sage.get("rank_proof_status", "")),
        "two_descent_status": str(sage.get("two_descent", {}).get("status", ""))
        if isinstance(sage.get("two_descent"), dict)
        else "",
        "strict_certificate_ready": proof_status == "rank-zero-proof-candidate",
        "proof_status": proof_status,
        "boundary": ATTEMPT_BOUNDARY,
    }


def audit_attempts(
    *,
    strictification_queue: dict[str, Any],
    probes: list[tuple[str, Path]],
) -> dict[str, Any]:
    missing_files: list[dict[str, str]] = []
    violations: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    targets = _queue_targets(strictification_queue)

    if strictification_queue.get("status") != "ok":
        violations.append(
            {
                "name": "strictification_queue",
                "field": "status",
                "expected": "ok",
                "actual": strictification_queue.get("status"),
            }
        )

    for name, path in probes:
        if not path.is_file():
            missing_files.append({"name": name, "kind": "probe", "path": str(path)})
            continue
        probe = load_json(path)
        key = _target_key(probe)
        queue_target = targets.get(key)
        if queue_target is None:
            violations.append(
                {
                    "name": name,
                    "field": "target",
                    "expected": "target present in strictification queue",
                    "actual": _target(probe),
                }
            )
        attempts.append(
            _attempt_summary(
                name=name,
                path=path,
                probe=probe,
                queue_target=queue_target,
            )
        )

    ready_count = sum(
        1 for attempt in attempts if attempt.get("strict_certificate_ready") is True
    )
    attempted_targets = {
        (
            int(attempt["target"]["A"]),
            int(attempt["target"]["B"]),
            str(attempt["target"]["curve"]),
        )
        for attempt in attempts
    }
    status = "ok" if not missing_files and not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "attempt_count": len(attempts),
        "target_count_with_attempts": len(attempted_targets),
        "strict_certificate_ready_count": ready_count,
        "candidate_not_proof": ready_count == 0,
        "missing_files": missing_files,
        "violations": violations,
        "attempt_status_counts": dict(
            sorted(Counter(str(attempt["proof_status"]) for attempt in attempts).items())
        ),
        "attempts": attempts,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strictification-queue", type=Path, required=True)
    parser.add_argument(
        "--probe",
        action="append",
        type=parse_probe_arg,
        default=[],
        help="Strictification probe as NAME:/path/to/probe.json. Repeat as needed.",
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_attempts(
        strictification_queue=load_json(args.strictification_queue),
        probes=args.probe,
    )
    write_json(args.out, audit)
    print(f"wrote frontier strictification attempt audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"attempt_count={audit['attempt_count']}")
    print(f"strict_certificate_ready_count={audit['strict_certificate_ready_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
