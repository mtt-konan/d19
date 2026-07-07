#!/usr/bin/env python3
"""Audit external certificate intake coverage for all residual frontier groups."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

BOUNDARY = (
    "This audits external certificate package coverage for the residual "
    "frontier. It does not verify external mathematics or promote residual "
    "covers to strict theorems."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _group_target(group: dict[str, Any]) -> dict[str, int | str]:
    target = group.get("target", {})
    return {
        "A": int(target.get("A", 0)),
        "B": int(target.get("B", 0)),
        "curve": str(target.get("curve", "")),
    }


def _cover_indices(group: dict[str, Any]) -> list[int]:
    return [int(index) for index in group.get("cover_indices", [])]


def _certificate_path(certificate_dir: Path, name: str) -> Path:
    return certificate_dir / f"{name}_certificate.json"


def _proof_status(
    *,
    ready_count: int,
    target_count: int,
    strict_ready_count: int,
) -> str:
    if strict_ready_count:
        return "frontier-external-certificates-awaiting-promotion-review"
    if ready_count == 0:
        return "frontier-external-certificates-missing-not-proof"
    if ready_count < target_count:
        return "frontier-external-certificates-partial-not-proof"
    return "frontier-external-certificates-ready-needs-math-review"


def template_index(frontier_handoff_audit: dict[str, Any]) -> dict[str, Any]:
    templates = []
    cover_count = 0
    for group in frontier_handoff_audit.get("groups", []):
        name = str(group.get("name", ""))
        indices = _cover_indices(group)
        cover_count += len(indices)
        templates.append(
            {
                "name": name,
                "certificate_path": f"external_certificates/{name}_certificate.json",
                "cover_indices": indices,
            }
        )
    return {
        "target_count": len(templates),
        "cover_count": cover_count,
        "templates": templates,
        "boundary": BOUNDARY,
    }


def _group_summary(
    *,
    group: dict[str, Any],
    handoff_dir: Path,
    certificate_dir: Path,
    root: Path,
    missing_handoff_files: list[dict[str, str]],
    violations: list[dict[str, Any]],
) -> dict[str, Any] | None:
    from scripts.theory.audit_external_cover_certificate_intake import (
        audit_certificate_intake,
    )

    name = str(group.get("name", ""))
    handoff_path = handoff_dir / f"{name}.json"
    if not handoff_path.is_file():
        missing_handoff_files.append({"name": name, "path": str(handoff_path)})
        return None

    certificate_path = _certificate_path(certificate_dir, name)
    certificate = load_json(certificate_path) if certificate_path.is_file() else None
    intake = audit_certificate_intake(
        handoff=load_json(handoff_path),
        certificate=certificate,
        root=root,
    )
    for violation in intake.get("violations", []):
        violations.append({"name": name, **violation})
    return {
        "name": name,
        "target": _group_target(group),
        "cover_count": int(intake["cover_count"]),
        "certificate_package_ready": bool(intake["certificate_package_ready"]),
        "strict_promotion_ready": bool(intake["strict_promotion_ready"]),
        "proof_status": str(intake["proof_status"]),
    }


def audit_frontier_certificate_intake(
    *,
    frontier_handoff_audit: dict[str, Any],
    handoff_dir: Path,
    certificate_dir: Path,
    root: Path,
) -> dict[str, Any]:
    missing_handoff_files: list[dict[str, str]] = []
    violations: list[dict[str, Any]] = []
    if frontier_handoff_audit.get("status") != "ok":
        violations.append(
            {
                "field": "frontier_handoff_audit.status",
                "expected": "ok",
                "actual": frontier_handoff_audit.get("status"),
            }
        )

    groups = [
        summary
        for group in frontier_handoff_audit.get("groups", [])
        if (
            summary := _group_summary(
                group=group,
                handoff_dir=handoff_dir,
                certificate_dir=certificate_dir,
                root=root,
                missing_handoff_files=missing_handoff_files,
                violations=violations,
            )
        )
        is not None
    ]
    target_count = len(groups)
    cover_count = sum(int(group["cover_count"]) for group in groups)
    ready_count = sum(
        1 for group in groups if group["certificate_package_ready"] is True
    )
    strict_ready_count = sum(
        1 for group in groups if group["strict_promotion_ready"] is True
    )
    status = "ok" if not missing_handoff_files and not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "target_count": target_count,
        "cover_count": cover_count,
        "certificate_package_ready_count": ready_count,
        "missing_certificate_package_count": target_count - ready_count,
        "strict_promotion_ready_count": strict_ready_count,
        "strict_promotion_count": 0,
        "candidate_not_proof": strict_ready_count == 0,
        "missing_handoff_files": missing_handoff_files,
        "violations": violations,
        "proof_status": _proof_status(
            ready_count=ready_count,
            target_count=target_count,
            strict_ready_count=strict_ready_count,
        ),
        "groups": groups,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frontier-handoff-audit", type=Path, required=True)
    parser.add_argument("--handoff-dir", type=Path, required=True)
    parser.add_argument("--certificate-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--template-index-out", type=Path)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    frontier_handoff_audit = load_json(args.frontier_handoff_audit)
    audit = audit_frontier_certificate_intake(
        frontier_handoff_audit=frontier_handoff_audit,
        handoff_dir=args.handoff_dir,
        certificate_dir=args.certificate_dir,
        root=args.root,
    )
    write_json(args.out, audit)
    if args.template_index_out:
        write_json(args.template_index_out, template_index(frontier_handoff_audit))
    print(f"wrote external frontier certificate intake audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"target_count={audit['target_count']}")
    print(f"cover_count={audit['cover_count']}")
    print(
        "certificate_package_ready_count="
        f"{audit['certificate_package_ready_count']}"
    )
    print(f"strict_promotion_ready_count={audit['strict_promotion_ready_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
