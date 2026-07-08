#!/usr/bin/env python3
"""Materialize rank-zero isogeny-Selmer proof packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This materializes reviewable task files for the open rank-zero "
    "isogeny-Selmer obligations. It does not compute Selmer groups, prove rank "
    "zero, or prove any lambda-family exclusion."
)

REQUIRED_TRANSCRIPT_FIELDS = [
    "statement",
    "isogeny_setup",
    "local_squareclass_conditions",
    "selmer_bound_argument",
    "rank_zero_conclusion",
    "review_notes",
]

L_ROLE = "A for AA, B for BB; AA+BB requires both sides to close"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _segment_rows(segment_index: dict[str, Any] | None) -> dict[str, list[dict[str, Any]]]:
    if segment_index is None:
        return {}
    rows: dict[str, list[dict[str, Any]]] = {}
    for row in segment_index.get("segments", []):
        package_id = str(row.get("package_id", ""))
        if not package_id:
            continue
        rows.setdefault(package_id, []).append(dict(row))
    return rows


def _reviewable_segments(package_id: str, segment_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    rows = segment_rows.get(package_id, [])
    segments: list[dict[str, str]] = []
    for row in rows:
        segments.append(
            {
                "required_field": str(row.get("required_field", "")),
                "proof_section": str(row.get("proof_section", "")),
                "segment_status": str(row.get("segment_status", "")),
                "proof_path": str(row.get("proof_path", "")),
                "segment_scope": str(row.get("segment_scope", "")),
                "summary": str(row.get("summary", "")),
            }
        )
    return segments


def _render_segment_block(reviewable_segments: list[dict[str, str]]) -> str:
    if not reviewable_segments:
        return ""
    segment_lines = []
    for segment in reviewable_segments:
        segment_lines.append(
            "- " f"`{segment['required_field']}` / `{segment['proof_section']}`"
        )
        segment_lines.append(f"  - status = {segment['segment_status']}")
        segment_lines.append(f"  - proof_path = {segment['proof_path']}")
        segment_lines.append(f"  - scope = {segment['segment_scope']}")
        segment_lines.append(f"  - summary = {segment['summary']}")
    return "## Partial Transcript Segments\n\n" + "\n".join(segment_lines) + "\n\n"


def _package_payload(package: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": str(package.get("package_id", "")),
        "family_pattern": str(package.get("family_pattern", "")),
        "kernel": str(package.get("kernel", "")),
        "candidate_class_count": int(package.get("candidate_class_count", 0) or 0),
        "model_count": int(package.get("model_count", 0) or 0),
        "required_output": str(package.get("required_output", "")),
        "status": "open",
        "transcript_status": "missing",
        "proof_claim": "none",
        "selmer_rank_upper_bound_proved": False,
        "family_exclusion_proved": False,
        "required_transcript_fields": REQUIRED_TRANSCRIPT_FIELDS,
        "symbolic_model": {
            "T": "A+B",
            "L_role": L_ROLE,
            "kernel_root": str(package.get("kernel_root", "")),
            "target_a2": str(package.get("target_a2", "")),
            "target_a4": str(package.get("target_a4", "")),
        },
        "boundary": BOUNDARY,
    }


def _package_payload_with_segments(
    package: dict[str, Any],
    segment_rows: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    payload = _package_payload(package)
    reviewable_segments = _reviewable_segments(payload["package_id"], segment_rows)
    if reviewable_segments:
        payload["transcript_status"] = "partial"
        payload["reviewable_segments"] = reviewable_segments
    return payload


def _render_markdown(payload: dict[str, Any]) -> str:
    symbolic_model = payload["symbolic_model"]
    fields = "\n".join(
        f"- {field}" for field in payload["required_transcript_fields"]
    )
    reviewable_segments = list(payload.get("reviewable_segments", []))
    segment_block = _render_segment_block(reviewable_segments)
    return (
        f"# {payload['package_id']}\n\n"
        f"Status: {payload['status']}\n\n"
        "## Scope\n\n"
        f"- family_pattern = {payload['family_pattern']}\n"
        f"- kernel = {payload['kernel']}\n"
        f"- candidate_class_count = {payload['candidate_class_count']}\n"
        f"- model_count = {payload['model_count']}\n\n"
        "## Symbolic Model\n\n"
        f"- T = {symbolic_model['T']}\n"
        f"- L role = {symbolic_model['L_role']}\n"
        f"- kernel_root = {symbolic_model['kernel_root']}\n"
        f"- target_a2 = {symbolic_model['target_a2']}\n"
        f"- target_a4 = {symbolic_model['target_a4']}\n\n"
        "## Required Transcript\n\n"
        f"{fields}\n\n"
        f"{segment_block}"
        "## Boundary\n\n"
        f"transcript_status = {payload['transcript_status']}\n\n"
        "No Selmer rank upper bound is proved by this file. No rank-zero theorem "
        "or lambda-family exclusion is claimed here.\n"
    )


def _sync_existing_markdown(existing: str, payload: dict[str, Any]) -> str:
    marker = "transcript_status = "
    updated = existing
    if marker in updated:
        lines = []
        for line in updated.splitlines():
            if line.startswith(marker):
                lines.append(f"{marker}{payload['transcript_status']}")
            else:
                lines.append(line)
        updated = "\n".join(lines)
        if existing.endswith("\n"):
            updated += "\n"
    segment_block = _render_segment_block(list(payload.get("reviewable_segments", [])))
    if segment_block:
        heading = "## Partial Transcript Segments\n\n"
        boundary_heading = "## Boundary"
        if heading in updated:
            start = updated.index(heading)
            end = updated.find(boundary_heading, start)
            if end == -1:
                updated = updated[:start] + segment_block
            else:
                updated = updated[:start] + segment_block + updated[end:]
        else:
            boundary_index = updated.find(boundary_heading)
            if boundary_index == -1:
                updated = updated.rstrip("\n") + "\n\n" + segment_block
            else:
                updated = (
                    updated[:boundary_index].rstrip("\n")
                    + "\n\n"
                    + segment_block
                    + updated[boundary_index:]
                )
    return updated


def _markdown_text(markdown_path: Path, payload: dict[str, Any]) -> str:
    if markdown_path.is_file():
        existing = markdown_path.read_text(encoding="utf-8")
        if "## Partial Transcript:" in existing:
            return _sync_existing_markdown(existing, payload)
    return _render_markdown(payload)


def materialize_rank_zero_selmer_packages(
    *,
    package_index: dict[str, Any],
    packages_dir: Path,
    segment_index: dict[str, Any] | None = None,
) -> dict[str, Any]:
    packages = list(package_index.get("packages", []))
    segment_rows = _segment_rows(segment_index)
    entries: list[dict[str, str]] = []
    for package in packages:
        payload = _package_payload_with_segments(package, segment_rows)
        package_id = payload["package_id"]
        json_path = packages_dir / f"{package_id}.json"
        markdown_path = packages_dir / f"{package_id}.md"
        write_json(json_path, payload)
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(
            _markdown_text(markdown_path, payload),
            encoding="utf-8",
        )
        entries.append(
            {
                "package_id": package_id,
                "json_path": str(json_path),
                "markdown_path": str(markdown_path),
                "status": payload["status"],
                "transcript_status": payload["transcript_status"],
            }
        )

    selmer_rank_upper_bound_proved_count = int(
        package_index.get("selmer_rank_upper_bound_proved_count", 0) or 0
    )
    family_exclusion_proved_count = int(
        package_index.get("family_exclusion_proved_count", 0) or 0
    )
    checks = {
        "package_index_ready": _ready(package_index),
        "package_count_matches_index": len(packages)
        == int(package_index.get("package_count", 0) or 0),
        "all_packages_open": all(
            str(package.get("status", "")) == "open" for package in packages
        ),
        "selmer_rank_upper_bound_count_zero": (
            selmer_rank_upper_bound_proved_count == 0
        ),
        "family_exclusion_claim_count_zero": family_exclusion_proved_count == 0,
        "search_count_rejected_as_progress": (
            package_index.get("search_count_used_as_progress") is False
        ),
    }
    violations = [name for name, passed in checks.items() if not passed]
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "package_count": len(packages),
        "open_package_count": sum(1 for package in packages if package["status"] == "open"),
        "materialized_json_count": len(entries),
        "materialized_markdown_count": len(entries),
        "selmer_rank_upper_bound_proved_count": selmer_rank_upper_bound_proved_count,
        "family_exclusion_proved_count": family_exclusion_proved_count,
        "packages_dir": str(packages_dir),
        "packages": entries,
        "checks": checks,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-index", type=Path, required=True)
    parser.add_argument("--packages-dir", type=Path, required=True)
    parser.add_argument("--segment-index", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = materialize_rank_zero_selmer_packages(
        package_index=load_json(args.package_index),
        packages_dir=args.packages_dir,
        segment_index=load_json(args.segment_index) if args.segment_index else None,
    )
    write_json(args.out, manifest)
    print(f"wrote rank-zero Selmer package materialization to {args.out}")
    print(f"status={manifest['status']}")
    print(f"package_count={manifest['package_count']}")
    print(f"open_package_count={manifest['open_package_count']}")
    print(f"materialized_json_count={manifest['materialized_json_count']}")
    print(f"materialized_markdown_count={manifest['materialized_markdown_count']}")
    print(
        "selmer_rank_upper_bound_proved_count="
        f"{manifest['selmer_rank_upper_bound_proved_count']}"
    )
    print(f"family_exclusion_proved_count={manifest['family_exclusion_proved_count']}")
    if args.strict and manifest["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
