#!/usr/bin/env python3
"""Audit the external cover-descent route for an open residual target."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits the external cover-descent route. Tool availability, missing "
    "tools, local solubility, rank bounds, and bounded searches are not no-point "
    "proofs."
)

ACCEPTED_STRICT_ROUTES = (
    "cover-level no-rational-point certificate for every target cover",
    "strict rank proof closing the source elliptic rank bounds to [0,0], "
    "followed by torsion-preimage audit",
)

REJECTED_PROMOTION_SIGNALS = (
    "bounded point search with zero points",
    "rank bounds that remain [0,2]",
    "local solubility witnesses",
    "Sage interface availability or unavailability",
    "Magma transcript without reproducible no-point or rank certificate",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _target(handoff: dict[str, Any]) -> dict[str, int | str]:
    return {
        "A": int(handoff.get("A", 0)),
        "B": int(handoff.get("B", 0)),
        "curve": str(handoff.get("curve", "")),
    }


def _missing_input_audit(paths: list[Path]) -> dict[str, Any]:
    return {
        "status": "issues",
        "ready": False,
        "missing_inputs": [str(path) for path in paths if not path.is_file()],
        "target": {"A": 0, "B": 0, "curve": ""},
        "cover_count": 0,
        "cover_indices": [],
        "local_magma_available": False,
        "magma_command": None,
        "sage_direct_no_point_capable_count": 0,
        "strict_certificate_ready_count": 0,
        "proof_status": "input-missing-not-proof",
        "recommended_next_action": "restore-required-inputs",
        "accepted_strict_routes": list(ACCEPTED_STRICT_ROUTES),
        "rejected_promotion_signals": list(REJECTED_PROMOTION_SIGNALS),
        "boundary": BOUNDARY,
    }


def audit_external_route(
    *,
    handoff: dict[str, Any],
    cover_capability_audit: dict[str, Any],
    magma_command: str | None,
) -> dict[str, Any]:
    covers = handoff.get("target_covers", [])
    local_magma_available = bool(magma_command)
    proof_status = (
        "external-transcript-required"
        if local_magma_available
        else "external-tool-gap-open"
    )
    recommended_next_action = (
        "run-magma-or-specialized-cover-descent-transcript"
        if local_magma_available
        else "obtain-magma-or-specialized-cover-descent-environment"
    )
    return {
        "status": "ok",
        "ready": True,
        "target": _target(handoff),
        "cover_count": len(covers),
        "cover_indices": [int(cover["index"]) for cover in covers],
        "local_magma_available": local_magma_available,
        "magma_command": magma_command,
        "sage_direct_no_point_capable_count": int(
            cover_capability_audit.get("sage_direct_no_point_capable_count", 0)
        ),
        "strict_certificate_ready_count": 0,
        "proof_status": proof_status,
        "recommended_next_action": recommended_next_action,
        "accepted_strict_routes": list(ACCEPTED_STRICT_ROUTES),
        "rejected_promotion_signals": list(REJECTED_PROMOTION_SIGNALS),
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--sage-cover-capability-audit", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--magma", default="magma")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inputs = [args.handoff, args.sage_cover_capability_audit]
    missing_inputs = [path for path in inputs if not path.is_file()]
    if missing_inputs:
        audit = _missing_input_audit(inputs)
        write_json(args.out, audit)
        print(f"wrote external cover-descent route audit to {args.out}")
        print(f"status={audit['status']}")
        print(f"missing_inputs={len(audit['missing_inputs'])}")
        return 1 if args.strict else 0

    audit = audit_external_route(
        handoff=load_json(args.handoff),
        cover_capability_audit=load_json(args.sage_cover_capability_audit),
        magma_command=shutil.which(args.magma),
    )
    write_json(args.out, audit)
    print(f"wrote external cover-descent route audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"local_magma_available={audit['local_magma_available']}")
    print(f"proof_status={audit['proof_status']}")
    print(f"recommended_next_action={audit['recommended_next_action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
