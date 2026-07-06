#!/usr/bin/env python3
"""Audit priority residual handoffs and Sage probes."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.export_mixed_closure_residual_handoff import (  # noqa: E402
    priority_handoff_specs,
)

BOUNDARY = (
    "This audits priority handoff/probe alignment. It does not prove "
    "that residual covers have no rational point."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _target_dict(target: tuple[int, int, str]) -> dict[str, int | str]:
    return {"A": target[0], "B": target[1], "curve": target[2]}


def _priority_rows_by_number(priorities: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(row["priority"]): row for row in priorities.get("rows", [])}


def _expected_quartics(
    priority_rows: dict[int, dict[str, Any]],
    priority_numbers: list[int],
) -> dict[int, str]:
    return {
        int(priority_rows[number]["cover_index"]): str(priority_rows[number]["quartic"])
        for number in priority_numbers
    }


def _missing_file(
    missing_files: list[dict[str, str]],
    *,
    name: str,
    kind: str,
    path: Path,
) -> None:
    missing_files.append({"name": name, "kind": kind, "path": str(path)})


def _expect_equal(
    violations: list[dict[str, Any]],
    *,
    name: str,
    field: str,
    actual: Any,
    expected: Any,
) -> None:
    if actual != expected:
        violations.append(
            {
                "name": name,
                "field": field,
                "expected": expected,
                "actual": actual,
            }
        )


def _audit_handoff_json(
    *,
    name: str,
    handoff: dict[str, Any],
    target: tuple[int, int, str],
    priorities: list[int],
    cover_indices: list[int],
    expected_quartics: dict[int, str],
    violations: list[dict[str, Any]],
) -> None:
    _expect_equal(
        violations,
        name=name,
        field="A",
        actual=int(handoff.get("A", 0)),
        expected=target[0],
    )
    _expect_equal(
        violations,
        name=name,
        field="B",
        actual=int(handoff.get("B", 0)),
        expected=target[1],
    )
    _expect_equal(
        violations,
        name=name,
        field="curve",
        actual=str(handoff.get("curve", "")),
        expected=target[2],
    )
    _expect_equal(
        violations,
        name=name,
        field="priority_source.priorities",
        actual=list(handoff.get("priority_source", {}).get("priorities", [])),
        expected=priorities,
    )
    _expect_equal(
        violations,
        name=name,
        field="target_cover_indices",
        actual=[int(index) for index in handoff.get("target_cover_indices", [])],
        expected=cover_indices,
    )
    _expect_equal(
        violations,
        name=name,
        field="strict_proof_status",
        actual=str(handoff.get("strict_proof_status", "")),
        expected="open",
    )
    if "does not prove" not in str(handoff.get("proof_boundary", "")):
        violations.append(
            {
                "name": name,
                "field": "proof_boundary",
                "expected": "contains 'does not prove'",
                "actual": handoff.get("proof_boundary", ""),
            }
        )

    actual_quartics = {
        int(cover.get("index", -1)): str(cover.get("quartic", ""))
        for cover in handoff.get("target_covers", [])
    }
    _expect_equal(
        violations,
        name=name,
        field="target_covers.quartics",
        actual=actual_quartics,
        expected=expected_quartics,
    )


def _probe_summary(
    *,
    name: str,
    probe: dict[str, Any],
    target: tuple[int, int, str],
    cover_indices: list[int],
    max_selmer_gap: int,
    violations: list[dict[str, Any]],
) -> dict[str, Any]:
    _expect_equal(
        violations,
        name=name,
        field="probe.A",
        actual=int(probe.get("A", 0)),
        expected=target[0],
    )
    _expect_equal(
        violations,
        name=name,
        field="probe.B",
        actual=int(probe.get("B", 0)),
        expected=target[1],
    )
    _expect_equal(
        violations,
        name=name,
        field="probe.curve",
        actual=str(probe.get("curve", "")),
        expected=target[2],
    )
    _expect_equal(
        violations,
        name=name,
        field="probe.status",
        actual=str(probe.get("status", "")),
        expected="ok",
    )
    sage = probe.get("sage", {})
    covers = sage.get("covers", [])
    actual_cover_indices = [int(row.get("index", -1)) for row in covers]
    _expect_equal(
        violations,
        name=name,
        field="probe.cover_indices",
        actual=actual_cover_indices,
        expected=cover_indices,
    )
    cover_point_counts = [int(row.get("rational_point_count", -1)) for row in covers]
    _expect_equal(
        violations,
        name=name,
        field="probe.cover_point_counts",
        actual=cover_point_counts,
        expected=[0 for _index in cover_indices],
    )
    cover_statuses = [str(row.get("point_search_status", "")) for row in covers]
    _expect_equal(
        violations,
        name=name,
        field="probe.cover_point_search_statuses",
        actual=cover_statuses,
        expected=["ok" for _index in cover_indices],
    )

    selmer_rank = int(sage.get("selmer_rank", 0))
    torsion_two_dimension = int(sage.get("torsion_two_dimension", 0))
    selmer_minus_torsion2 = selmer_rank - torsion_two_dimension
    _expect_equal(
        violations,
        name=name,
        field="probe.selmer_minus_torsion2",
        actual=selmer_minus_torsion2,
        expected=max_selmer_gap,
    )
    return {
        "rank_bounds": [int(value) for value in sage.get("rank_bounds", [])],
        "rank_probable": int(sage.get("rank_probable", -1)),
        "rank_proof_status": str(sage.get("rank_proof_status", "")),
        "selmer_minus_torsion2": selmer_minus_torsion2,
        "cover_point_counts": cover_point_counts,
    }


def audit_priority_handoffs(
    *,
    priorities: dict[str, Any],
    handoff_dir: Path,
    top: int,
    require_probes: bool,
) -> dict[str, Any]:
    priority_rows = _priority_rows_by_number(priorities)
    specs = priority_handoff_specs(priorities, top=top)
    missing_files: list[dict[str, str]] = []
    violations: list[dict[str, Any]] = []
    groups: list[dict[str, Any]] = []
    probe_status_counts: Counter[str] = Counter()

    for spec in specs:
        name = str(spec["name"])
        target = spec["target"]
        priorities_for_group = [int(value) for value in spec["priorities"]]
        cover_indices = [int(value) for value in spec["cover_indices"]]
        max_selmer_gap = max(
            int(priority_rows[number].get("selmer_gap", 0))
            for number in priorities_for_group
        )
        group: dict[str, Any] = {
            "name": name,
            "target": _target_dict(target),
            "priorities": priorities_for_group,
            "cover_indices": cover_indices,
            "max_selmer_gap": max_selmer_gap,
        }

        for kind, suffix in (("json", ".json"), ("sage", ".sage"), ("magma", ".magma")):
            path = handoff_dir / f"{name}{suffix}"
            if not path.is_file():
                _missing_file(missing_files, name=name, kind=kind, path=path)

        handoff_path = handoff_dir / f"{name}.json"
        if handoff_path.is_file():
            _audit_handoff_json(
                name=name,
                handoff=load_json(handoff_path),
                target=target,
                priorities=priorities_for_group,
                cover_indices=cover_indices,
                expected_quartics=_expected_quartics(priority_rows, priorities_for_group),
                violations=violations,
            )

        probe_path = handoff_dir / f"{name}_sage_probe.json"
        if not probe_path.is_file():
            if require_probes:
                _missing_file(missing_files, name=name, kind="sage_probe", path=probe_path)
        else:
            probe = load_json(probe_path)
            probe_status_counts.update([str(probe.get("status", "missing"))])
            group.update(
                _probe_summary(
                    name=name,
                    probe=probe,
                    target=target,
                    cover_indices=cover_indices,
                    max_selmer_gap=max_selmer_gap,
                    violations=violations,
                )
            )
        groups.append(group)

    return {
        "ready": not missing_files and not violations,
        "top": top,
        "groups_checked": len(specs),
        "priority_rows_checked": min(top, len(priorities.get("rows", []))),
        "target_cover_count": sum(len(spec["cover_indices"]) for spec in specs),
        "missing_files": missing_files,
        "violations": violations,
        "probe_status_counts": dict(sorted(probe_status_counts.items())),
        "groups": groups,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--priorities", type=Path, required=True)
    parser.add_argument("--handoff-dir", type=Path, required=True)
    parser.add_argument("--top", type=int, required=True)
    parser.add_argument("--require-probes", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_priority_handoffs(
        priorities=load_json(args.priorities),
        handoff_dir=args.handoff_dir,
        top=args.top,
        require_probes=args.require_probes,
    )
    write_json(args.out, audit)
    print(f"wrote mixed closure priority handoff audit to {args.out}")
    print(f"ready={audit['ready']}")
    print(f"groups_checked={audit['groups_checked']}")
    print(f"missing_files={audit['missing_files']}")
    print(f"violations={audit['violations']}")
    if args.strict and not audit["ready"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
