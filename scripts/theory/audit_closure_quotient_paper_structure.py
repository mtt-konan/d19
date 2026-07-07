#!/usr/bin/env python3
"""Audit the paper-note structure for the closure-quotient partial result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This checks paper-note structure and claim-boundary text. It does not "
    "verify the mathematics or create new certificates."
)

REQUIRED_SECTIONS: tuple[tuple[str, str], ...] = (
    ("status boundary", "does not claim a proof of the"),
    ("claim level", "## 1. Claim Level"),
    ("main lemma draft", "## 2. Main Lemma Draft"),
    ("certified census", "## 3. Certified Census"),
    ("paper path", "## 7. Paper Path"),
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _int_value(payload: dict[str, Any], key: str) -> int:
    return int(payload.get(key, 0))


def _required_claims(summary: dict[str, Any]) -> tuple[tuple[str, str], ...]:
    strict = summary.get("strict_certificate", {})
    residual = summary.get("residual_status", {})
    open_frontier = summary.get("residual_open_frontier_status", {})
    strictification = summary.get("frontier_strictification_status", {})
    external = summary.get("external_certificate_frontier_status", {})
    return (
        (
            "rank-zero certificate count",
            f"AA/BB rank-0 certificates = {_int_value(strict, 'rank0_torsion_certificates')}",
        ),
        (
            "strict excluded pair count",
            f"strict excluded pairs = {_int_value(strict, 'strict_excluded_pair_count')}",
        ),
        (
            "residual candidate-cover count",
            f"candidate_cover_total = {_int_value(residual, 'candidate_cover_total')}",
        ),
        (
            "residual candidate-not-proof status",
            f"proof_status = {residual.get('proof_status', '')}",
        ),
        (
            "open frontier cover count",
            f"open_frontier_cover_count = {_int_value(open_frontier, 'open_frontier_cover_count')}",
        ),
        (
            "open frontier not-proof status",
            f"proof_status = {open_frontier.get('proof_status', '')}",
        ),
        (
            "frontier strictification target count",
            "frontier_strictification_status.target_count = "
            f"{_int_value(strictification, 'target_count')}",
        ),
        (
            "frontier strictification cover count",
            "frontier_strictification_status.cover_count = "
            f"{_int_value(strictification, 'cover_count')}",
        ),
        (
            "frontier strictification ready count",
            "frontier_strictification_status.strict_certificate_ready_count = "
            f"{_int_value(strictification, 'strict_certificate_ready_count')}",
        ),
        (
            "external certificate frontier target count",
            "external_certificate_frontier_status.target_count = "
            f"{_int_value(external, 'target_count')}",
        ),
        (
            "external certificate frontier cover count",
            "external_certificate_frontier_status.cover_count = "
            f"{_int_value(external, 'cover_count')}",
        ),
        (
            "external certificate frontier package count",
            "external_certificate_frontier_status.certificate_package_ready_count = "
            f"{_int_value(external, 'certificate_package_ready_count')}",
        ),
    )


def _summary_from_inputs(
    *,
    claim_audit: dict[str, Any],
    residual_open_frontier_audit: dict[str, Any],
    frontier_strictification_queue: dict[str, Any],
    external_certificate_frontier_audit: dict[str, Any],
) -> dict[str, Any]:
    claim_values = claim_audit.get("claim_values", {})
    return {
        "strict_certificate": {
            "rank0_torsion_certificates": _int_value(
                claim_values, "rank0_torsion_certificates"
            ),
            "strict_excluded_pair_count": _int_value(
                claim_values, "strict_excluded_pair_count"
            ),
        },
        "residual_status": {
            "candidate_cover_total": _int_value(
                claim_values, "residual_evidence_candidate_cover_total"
            ),
            "proof_status": "candidate-not-proof",
        },
        "residual_open_frontier_status": {
            "open_frontier_cover_count": _int_value(
                residual_open_frontier_audit, "open_frontier_cover_count"
            ),
            "proof_status": "open-frontier-not-proof",
        },
        "frontier_strictification_status": {
            "target_count": _int_value(frontier_strictification_queue, "target_count"),
            "cover_count": _int_value(frontier_strictification_queue, "cover_count"),
            "strict_certificate_ready_count": _int_value(
                frontier_strictification_queue, "strict_certificate_ready_count"
            ),
        },
        "external_certificate_frontier_status": {
            "target_count": _int_value(
                external_certificate_frontier_audit, "target_count"
            ),
            "cover_count": _int_value(
                external_certificate_frontier_audit, "cover_count"
            ),
            "certificate_package_ready_count": _int_value(
                external_certificate_frontier_audit,
                "certificate_package_ready_count",
            ),
        },
    }


def _missing(text: str, requirements: tuple[tuple[str, str], ...]) -> list[str]:
    return [name for name, needle in requirements if needle not in text]


def audit_paper_structure(*, paper_text: str, summary: dict[str, Any]) -> dict[str, Any]:
    boundary_claims = (
        ("bounded search boundary", "bounded search is not a proof"),
        ("external intake boundary", "not a mathematical verifier"),
    )
    required_claims = _required_claims(summary) + boundary_claims
    missing_sections = _missing(paper_text, REQUIRED_SECTIONS)
    missing_claims = _missing(paper_text, required_claims)
    status = "ok" if not missing_sections and not missing_claims else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "required_section_count": len(REQUIRED_SECTIONS),
        "matched_section_count": len(REQUIRED_SECTIONS) - len(missing_sections),
        "required_claim_count": len(required_claims),
        "matched_claim_count": len(required_claims) - len(missing_claims),
        "missing_sections": missing_sections,
        "missing_claims": missing_claims,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", type=Path, required=True)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--claim-audit", type=Path)
    parser.add_argument("--residual-open-frontier-audit", type=Path)
    parser.add_argument("--frontier-strictification-queue", type=Path)
    parser.add_argument("--external-certificate-frontier-audit", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.summary:
        summary = load_json(args.summary)
    else:
        required = (
            args.claim_audit,
            args.residual_open_frontier_audit,
            args.frontier_strictification_queue,
            args.external_certificate_frontier_audit,
        )
        if any(path is None for path in required):
            raise SystemExit(
                "--summary or all direct audit inputs are required"
            )
        summary = _summary_from_inputs(
            claim_audit=load_json(args.claim_audit),
            residual_open_frontier_audit=load_json(args.residual_open_frontier_audit),
            frontier_strictification_queue=load_json(
                args.frontier_strictification_queue
            ),
            external_certificate_frontier_audit=load_json(
                args.external_certificate_frontier_audit
            ),
        )
    audit = audit_paper_structure(
        paper_text=args.paper.read_text(encoding="utf-8"),
        summary=summary,
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient paper structure audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"matched_section_count={audit['matched_section_count']}")
    print(f"matched_claim_count={audit['matched_claim_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
