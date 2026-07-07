#!/usr/bin/env python3
"""Audit intake packaging for external residual cover certificates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_CERTIFICATE_TYPE = "cover-no-rational-point-certificate"

BOUNDARY = (
    "This audits external certificate packaging only. It checks target matching, "
    "cover coverage, transcript presence, and required fields; it does not verify "
    "the external mathematics."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _target(payload: dict[str, Any]) -> dict[str, int | str]:
    nested = payload.get("target", {})
    source = nested if nested else payload
    return {
        "A": int(source.get("A", 0)),
        "B": int(source.get("B", 0)),
        "curve": str(source.get("curve", "")),
    }


def _cover_indices(handoff: dict[str, Any]) -> list[int]:
    return [int(cover["index"]) for cover in handoff.get("target_covers", [])]


def _resolve_path(root: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else root / path


def certificate_template(handoff: dict[str, Any]) -> dict[str, Any]:
    return {
        "target": _target(handoff),
        "source_tool": "magma-or-specialized-cover-descent",
        "transcript_path": "docs/external/replace-with-transcript.txt",
        "cover_certificates": [
            {
                "index": index,
                "certificate_type": REQUIRED_CERTIFICATE_TYPE,
                "result": "no-rational-points",
                "command_label": f"cover-{index}-certificate",
            }
            for index in _cover_indices(handoff)
        ],
        "boundary": BOUNDARY,
    }


def _certificate_rows(certificate: dict[str, Any]) -> dict[int, dict[str, Any]]:
    rows: dict[int, dict[str, Any]] = {}
    for row in certificate.get("cover_certificates", []):
        rows[int(row.get("index", 0))] = row
    return rows


def _certificate_violations(
    *,
    handoff: dict[str, Any],
    certificate: dict[str, Any],
    root: Path,
    required_cover_indices: list[int],
    certified_rows: dict[int, dict[str, Any]],
) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    if _target(certificate) != _target(handoff):
        violations.append(
            {
                "field": "target",
                "expected": _target(handoff),
                "actual": _target(certificate),
            }
        )

    transcript_path = str(certificate.get("transcript_path", ""))
    if not transcript_path or not _resolve_path(root, transcript_path).is_file():
        violations.append(
            {
                "field": "transcript_path",
                "expected": "existing transcript file",
                "actual": transcript_path,
            }
        )

    for index in required_cover_indices:
        row = certified_rows.get(index)
        if row is None:
            continue
        if row.get("certificate_type") != REQUIRED_CERTIFICATE_TYPE:
            violations.append(
                {
                    "field": f"cover_certificates[{index}].certificate_type",
                    "expected": REQUIRED_CERTIFICATE_TYPE,
                    "actual": row.get("certificate_type"),
                }
            )
        if row.get("result") != "no-rational-points":
            violations.append(
                {
                    "field": f"cover_certificates[{index}].result",
                    "expected": "no-rational-points",
                    "actual": row.get("result"),
                }
            )
        if not row.get("command_label"):
            violations.append(
                {
                    "field": f"cover_certificates[{index}].command_label",
                    "expected": "non-empty command label",
                    "actual": row.get("command_label", ""),
                }
            )
    return violations


def audit_certificate_intake(
    *,
    handoff: dict[str, Any],
    certificate: dict[str, Any] | None,
    root: Path,
) -> dict[str, Any]:
    required_cover_indices = _cover_indices(handoff)
    if certificate is None:
        return {
            "status": "ok",
            "ready": True,
            "target": _target(handoff),
            "cover_count": len(required_cover_indices),
            "required_cover_indices": required_cover_indices,
            "certified_cover_indices": [],
            "missing_cover_indices": required_cover_indices,
            "unexpected_cover_indices": [],
            "certificate_package_ready": False,
            "strict_promotion_ready": False,
            "strict_promotion_count": 0,
            "candidate_not_proof": True,
            "proof_status": "no-external-certificate-package-not-proof",
            "violations": [],
            "boundary": BOUNDARY,
        }

    rows = _certificate_rows(certificate)
    required_set = set(required_cover_indices)
    certified_indices = [
        index for index in required_cover_indices if index in rows
    ]
    missing_indices = [index for index in required_cover_indices if index not in rows]
    unexpected_indices = sorted(index for index in rows if index not in required_set)
    violations = _certificate_violations(
        handoff=handoff,
        certificate=certificate,
        root=root,
        required_cover_indices=required_cover_indices,
        certified_rows=rows,
    )
    if missing_indices:
        violations.append(
            {
                "field": "cover_certificates",
                "expected": f"certificates for covers {required_cover_indices}",
                "actual": f"missing covers {missing_indices}",
            }
        )
    if unexpected_indices:
        violations.append(
            {
                "field": "cover_certificates",
                "expected": f"only covers {required_cover_indices}",
                "actual": f"unexpected covers {unexpected_indices}",
            }
        )
    package_ready = not violations
    return {
        "status": "ok" if package_ready else "issues",
        "ready": package_ready,
        "target": _target(handoff),
        "cover_count": len(required_cover_indices),
        "required_cover_indices": required_cover_indices,
        "certified_cover_indices": certified_indices,
        "missing_cover_indices": missing_indices,
        "unexpected_cover_indices": unexpected_indices,
        "certificate_package_ready": package_ready,
        "strict_promotion_ready": False,
        "strict_promotion_count": 0,
        "candidate_not_proof": True,
        "proof_status": "certificate-package-ready-needs-math-review"
        if package_ready
        else "certificate-package-issues-not-proof",
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--template-out", type=Path)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    handoff = load_json(args.handoff)
    certificate = load_json(args.certificate) if args.certificate else None
    audit = audit_certificate_intake(
        handoff=handoff,
        certificate=certificate,
        root=args.root,
    )
    write_json(args.out, audit)
    if args.template_out:
        write_json(args.template_out, certificate_template(handoff))
    print(f"wrote external cover certificate intake audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"certificate_package_ready={audit['certificate_package_ready']}")
    print(f"strict_promotion_ready={audit['strict_promotion_ready']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
