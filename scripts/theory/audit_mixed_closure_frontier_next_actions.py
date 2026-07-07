#!/usr/bin/env python3
"""Audit next actions for the mixed-closure residual frontier."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits next-action routing for residual frontier work. It does not "
    "prove that any residual cover has no rational point."
)

RANK_ZERO_REQUIRED_EVIDENCE = [
    "strict elliptic rank proof closing rank_bounds to [0,0]",
    "or a cover-level no-rational-point certificate for every listed cover",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _target_key(payload: dict[str, Any]) -> tuple[int, int, str]:
    return int(payload.get("A", 0)), int(payload.get("B", 0)), str(payload.get("curve", ""))


def _target_dict(payload: dict[str, Any]) -> dict[str, int | str]:
    return {
        "A": int(payload.get("A", 0)),
        "B": int(payload.get("B", 0)),
        "curve": str(payload.get("curve", "")),
    }


def _rank_zero_targets(strictification_queue: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        target
        for target in strictification_queue.get("targets", [])
        if str(target.get("track", "")) == "rank-zero-rank-proof"
    ]


def _batch_rank_zero_targets(batch_rank_methods: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        target
        for target in batch_rank_methods.get("targets", [])
        if str(target.get("track", "")) == "rank-zero-rank-proof"
    ]


def _batch_method_counts(batch_targets: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for target in batch_targets:
        counts.update(dict(target.get("probe", {}).get("method_status_counts", {})))
    return dict(sorted(counts.items()))


def _non_rankzero_next_action(target: dict[str, Any]) -> str:
    track = str(target.get("track", ""))
    if track == "rank-one-sha2-separation":
        return (
            "Find a visible rank-one generator and separate the residual "
            "Sha[2] class, or prove every listed cover has no rational point."
        )
    if track == "even-gap4-deeper-descent":
        return (
            "Use deeper descent or an independent Sha[2] obstruction, or prove "
            "every listed cover has no rational point."
        )
    return "Use the strict evidence required by the frontier queue."


def _long_two_descent_targets(
    rank_zero_targets: list[dict[str, Any]],
) -> list[dict[str, int | str]]:
    return [
        {
            **_target_dict(target),
            "timeout_seconds": int(target.get("max_timeout_seconds", 120)),
        }
        for target in rank_zero_targets
    ]


def audit_next_actions(
    *,
    strictification_queue: dict[str, Any],
    attempt_audit: dict[str, Any],
    batch_rank_methods: dict[str, Any],
) -> dict[str, Any]:
    violations: list[dict[str, Any]] = []
    for name, payload in (
        ("strictification_queue", strictification_queue),
        ("attempt_audit", attempt_audit),
        ("batch_rank_methods", batch_rank_methods),
    ):
        if payload.get("status") != "ok":
            violations.append(
                {
                    "name": name,
                    "field": "status",
                    "expected": "ok",
                    "actual": payload.get("status"),
                }
            )

    rank_zero_targets = _rank_zero_targets(strictification_queue)
    rank_zero_keys = {_target_key(target) for target in rank_zero_targets}
    batch_targets = _batch_rank_zero_targets(batch_rank_methods)
    batch_keys = {_target_key(target) for target in batch_targets}
    if batch_keys != rank_zero_keys:
        violations.append(
            {
                "name": "batch_rank_methods",
                "field": "rank_zero_target_coverage",
                "expected": len(rank_zero_keys),
                "actual": len(batch_keys & rank_zero_keys),
            }
        )

    method_counts = _batch_method_counts(batch_targets)
    expected_method_counts = {
        "pari_ellrank:ok": len(rank_zero_targets),
        "rank_bounds:ok": len(rank_zero_targets),
        "selmer_rank:ok": len(rank_zero_targets),
    }
    if batch_keys == rank_zero_keys and method_counts != expected_method_counts:
        violations.append(
            {
                "name": "batch_rank_methods",
                "field": "method_status_counts",
                "expected": expected_method_counts,
                "actual": method_counts,
            }
        )

    proof_candidate_count = int(
        batch_rank_methods.get("rank_zero_proof_candidate_count", 0)
    )
    if proof_candidate_count != 0:
        violations.append(
            {
                "name": "batch_rank_methods",
                "field": "rank_zero_proof_candidate_count",
                "expected": 0,
                "actual": proof_candidate_count,
            }
        )

    cheap_exhausted = (
        not violations
        and len(rank_zero_targets) > 0
        and int(attempt_audit.get("strict_certificate_ready_count", 0)) == 0
    )
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "rank_zero_target_count": len(rank_zero_targets),
        "rank_zero_batch_target_count": len(batch_keys & rank_zero_keys),
        "cheap_rank_method_target_hopping_exhausted": cheap_exhausted,
        "strict_certificate_ready_count": int(
            attempt_audit.get("strict_certificate_ready_count", 0)
        ),
        "recommended_mainline": "escalate-beyond-cheap-rank-methods"
        if cheap_exhausted
        else "complete-or-fix-frontier-diagnostics",
        "rank_zero_next_actions": {
            "long_two_descent_targets": _long_two_descent_targets(rank_zero_targets),
            "required_strict_evidence": RANK_ZERO_REQUIRED_EVIDENCE,
        },
        "non_rankzero_next_actions": [
            {
                **_target_dict(target),
                "track": str(target.get("track", "")),
                "next_action": _non_rankzero_next_action(target),
            }
            for target in strictification_queue.get("targets", [])
            if str(target.get("track", "")) != "rank-zero-rank-proof"
        ],
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strictification-queue", type=Path, required=True)
    parser.add_argument("--attempt-audit", type=Path, required=True)
    parser.add_argument("--batch-rank-methods", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_next_actions(
        strictification_queue=load_json(args.strictification_queue),
        attempt_audit=load_json(args.attempt_audit),
        batch_rank_methods=load_json(args.batch_rank_methods),
    )
    write_json(args.out, audit)
    print(f"wrote frontier next-action audit to {args.out}")
    print(f"status={audit['status']}")
    print(
        "cheap_rank_method_target_hopping_exhausted="
        f"{audit['cheap_rank_method_target_hopping_exhausted']}"
    )
    print(f"recommended_mainline={audit['recommended_mainline']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
