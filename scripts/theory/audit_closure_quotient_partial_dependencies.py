#!/usr/bin/env python3
"""Audit dependency sources for closure-quotient partial-result summary fields."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This checks that partial-result summary fields have explicit upstream "
    "result-file dependencies. It does not verify the mathematics."
)

REQUIRED_DEPENDENCIES: list[dict[str, str]] = [
    {
        "summary_status": "strict_certificate",
        "path": "results/mixed_closure_rank_summary.json",
    },
    {
        "summary_status": "strict_certificate",
        "path": "results/mixed_closure_rank0_certificate_audit.json",
    },
    {
        "summary_status": "residual_status",
        "path": "results/mixed_closure_aabb_residual_cover_priorities.json",
    },
    {
        "summary_status": "residual_open_frontier_status",
        "path": "results/mixed_closure_residual_open_frontier_audit.json",
    },
    {
        "summary_status": "frontier_strictification_status",
        "path": "results/mixed_closure_frontier_strictification_queue.json",
    },
    {
        "summary_status": "external_certificate_frontier_status",
        "path": "results/mixed_closure_external_cover_certificate_frontier_intake.json",
    },
    {
        "summary_status": "paper_structure_status",
        "path": "results/closure_quotient_paper_structure_audit.json",
    },
    {
        "summary_status": "artifact_status",
        "path": "results/closure_quotient_partial_artifact_audit.json",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _artifact_paths(artifact_audit: dict[str, Any]) -> set[str]:
    return {
        str(row.get("path", ""))
        for row in artifact_audit.get("required_files", [])
        if row.get("category") == "result"
    }


def audit_dependencies(
    *,
    summary: dict[str, Any],
    artifact_audit: dict[str, Any],
    root: Path,
) -> dict[str, Any]:
    artifact_paths = _artifact_paths(artifact_audit)
    required_statuses = {
        dependency["summary_status"] for dependency in REQUIRED_DEPENDENCIES
    }
    missing_summary_statuses = sorted(
        status for status in required_statuses if status not in summary
    )
    missing_files = [
        dependency
        for dependency in REQUIRED_DEPENDENCIES
        if not (root / dependency["path"]).is_file()
    ]
    not_in_artifact_audit = [
        dependency
        for dependency in REQUIRED_DEPENDENCIES
        if dependency["path"] not in artifact_paths
    ]
    status = (
        "ok"
        if not missing_summary_statuses
        and not missing_files
        and not not_in_artifact_audit
        else "issues"
    )
    return {
        "status": status,
        "ready": status == "ok",
        "dependency_count": len(REQUIRED_DEPENDENCIES),
        "summary_status_count": len(required_statuses),
        "missing_summary_statuses": missing_summary_statuses,
        "missing_files": missing_files,
        "not_in_artifact_audit": not_in_artifact_audit,
        "dependencies": REQUIRED_DEPENDENCIES,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--artifact-audit", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_dependencies(
        summary=load_json(args.summary),
        artifact_audit=load_json(args.artifact_audit),
        root=args.root,
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient partial dependency audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"dependency_count={audit['dependency_count']}")
    print(f"missing_summary_statuses={len(audit['missing_summary_statuses'])}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
