#!/usr/bin/env python3
"""Export external cover-descent task packages for residual frontier targets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This exports external cover-descent inputs for the residual frontier. "
    "The generated Magma/Sage files are task inputs, not no-point certificates."
)

REQUIRED_STRICT_EVIDENCE = (
    "cover-level no-rational-point certificate for every listed cover",
    "or a strict source-curve rank proof plus downstream torsion-preimage audit",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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


def _magma_task_source(handoff: dict[str, Any]) -> str:
    target = _target(handoff)
    lines = [
        "/*",
        "External residual cover-descent task input.",
        "",
        f"Target: A={target['A']} B={target['B']} curve={target['curve']}",
        f"Boundary: {BOUNDARY}",
        "",
        "Required strict evidence:",
        "1. cover-level no-rational-point certificate for every listed cover;",
        "2. or a strict source-curve rank proof plus torsion-preimage audit.",
        "",
        "Bounded searches, local solubility, and open rank bounds are not proof.",
        "*/",
        "",
        "Q := Rationals();",
        "P<x> := PolynomialRing(Q);",
        "",
    ]
    for cover in handoff.get("target_covers", []):
        index = int(cover["index"])
        quartic = str(cover["quartic"])
        lines.extend(
            [
                f"// Cover {index}: y^2 = f{index}(x)",
                f"f{index} := P!({quartic});",
                f"C{index} := HyperellipticCurve(f{index});",
                f'print "cover {index} quartic";',
                f"print f{index};",
                f'print "cover {index} curve";',
                f"print C{index};",
                "",
            ]
        )
    lines.extend(
        [
            "/*",
            "Attach the final transcript to the matching external certificate JSON.",
            "Do not mark a cover as no-rational-points unless the transcript gives",
            "a reproducible strict no-point certificate for that cover.",
            "*/",
            "",
        ]
    )
    return "\n".join(lines)


def _sage_task_source(handoff: dict[str, Any]) -> str:
    target = _target(handoff)
    lines = [
        "# External residual cover task input for Sage inspection.",
        f"# Target: A={target['A']} B={target['B']} curve={target['curve']}",
        f"# Boundary: {BOUNDARY}",
        "# This file constructs the curves only; it is not a proof.",
        "",
        "R.<x> = PolynomialRing(QQ)",
        "",
    ]
    for cover in handoff.get("target_covers", []):
        index = int(cover["index"])
        quartic = str(cover["quartic"]).replace("^", "**")
        lines.extend(
            [
                f"f{index} = R({quartic})",
                f"C{index} = HyperellipticCurve(f{index})",
                f"print('cover {index} quartic')",
                f"print(f{index})",
                f"print('cover {index} curve')",
                f"print(C{index})",
                "",
            ]
        )
    return "\n".join(lines)


def _readme_source(handoff: dict[str, Any], name: str) -> str:
    target = _target(handoff)
    cover_indices = _cover_indices(handoff)
    return f"""# External Cover-Descent Task: {name}

Target: A={target["A"]}, B={target["B"]}, curve={target["curve"]}

Covers: {cover_indices}

This directory contains task inputs for an external cover-descent or
Mordell-Weil-sieve run. It does not contain a proof.

Strict promotion requires one of:

- cover-level no-rational-point certificate for every listed cover;
- or a strict source-curve rank proof plus downstream torsion-preimage audit.

Do not use a timeout, a bounded search with zero points, local solubility, or
open rank bounds as a no-point proof.
"""


def _input_payload(handoff: dict[str, Any], name: str) -> dict[str, Any]:
    return {
        "name": name,
        "target": _target(handoff),
        "cover_indices": _cover_indices(handoff),
        "target_covers": [
            {
                "index": int(cover["index"]),
                "quartic": str(cover["quartic"]),
                "covering_map_to_elliptic": str(
                    cover.get("covering_map_to_elliptic", "")
                ),
            }
            for cover in handoff.get("target_covers", [])
        ],
        "required_strict_evidence": list(REQUIRED_STRICT_EVIDENCE),
        "candidate_not_proof": True,
        "boundary": BOUNDARY,
    }


def _export_group(
    *,
    group: dict[str, Any],
    handoff_dir: Path,
    out_dir: Path,
    missing_handoff_files: list[dict[str, str]],
) -> dict[str, Any] | None:
    name = str(group.get("name", ""))
    handoff_path = handoff_dir / f"{name}.json"
    if not handoff_path.is_file():
        missing_handoff_files.append({"name": name, "path": str(handoff_path)})
        return None

    handoff = load_json(handoff_path)
    package_dir = out_dir / name
    input_path = package_dir / "cover_inputs.json"
    magma_path = package_dir / "magma_cover_descent_task.m"
    sage_path = package_dir / "sage_cover_task.sage"
    readme_path = package_dir / "README.md"

    write_json(input_path, _input_payload(handoff, name))
    write_text(magma_path, _magma_task_source(handoff))
    write_text(sage_path, _sage_task_source(handoff))
    write_text(readme_path, _readme_source(handoff, name))

    return {
        "name": name,
        "target": _target(handoff),
        "cover_count": len(_cover_indices(handoff)),
        "cover_indices": _cover_indices(handoff),
        "package_dir": str(package_dir),
        "input_path": str(input_path),
        "magma_task_path": str(magma_path),
        "sage_task_path": str(sage_path),
        "readme_path": str(readme_path),
        "candidate_not_proof": True,
    }


def export_packages(
    *,
    frontier_handoff_audit: dict[str, Any],
    handoff_dir: Path,
    out_dir: Path,
) -> dict[str, Any]:
    missing_handoff_files: list[dict[str, str]] = []
    groups = [
        package
        for group in frontier_handoff_audit.get("groups", [])
        if (
            package := _export_group(
                group=group,
                handoff_dir=handoff_dir,
                out_dir=out_dir,
                missing_handoff_files=missing_handoff_files,
            )
        )
        is not None
    ]
    status = "ok" if not missing_handoff_files else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "package_status": "external-task-inputs-ready-not-proof",
        "target_count": len(groups),
        "cover_count": sum(int(group["cover_count"]) for group in groups),
        "missing_handoff_files": missing_handoff_files,
        "strict_certificate_ready_count": 0,
        "candidate_not_proof": True,
        "packages": groups,
        "required_strict_evidence": list(REQUIRED_STRICT_EVIDENCE),
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frontier-handoff-audit", type=Path, required=True)
    parser.add_argument("--handoff-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = export_packages(
        frontier_handoff_audit=load_json(args.frontier_handoff_audit),
        handoff_dir=args.handoff_dir,
        out_dir=args.out_dir,
    )
    write_json(args.out, audit)
    print(f"wrote external cover-descent package index to {args.out}")
    print(f"status={audit['status']}")
    print(f"target_count={audit['target_count']}")
    print(f"cover_count={audit['cover_count']}")
    print(f"strict_certificate_ready_count={audit['strict_certificate_ready_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
