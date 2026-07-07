#!/usr/bin/env python3
"""Audit residual frontier handoff packages without promoting them to proofs."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits frontier handoff package consistency. It does not prove that "
    "residual covers have no rational point."
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _int_list(values: Any) -> list[int]:
    return [int(value) for value in values or []]


def _target_dict(target: dict[str, Any]) -> dict[str, int | str]:
    return {
        "A": int(target.get("A", 0)),
        "B": int(target.get("B", 0)),
        "curve": str(target.get("curve", "")),
    }


def _priority_rows_by_number(priorities: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(row["priority"]): row for row in priorities.get("rows", [])}


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


def _expect_target_identity(
    violations: list[dict[str, Any]],
    *,
    name: str,
    prefix: str,
    payload: dict[str, Any],
    target: dict[str, int | str],
) -> None:
    _expect_equal(
        violations,
        name=name,
        field=f"{prefix}.A",
        actual=int(payload.get("A", 0)),
        expected=target["A"],
    )
    _expect_equal(
        violations,
        name=name,
        field=f"{prefix}.B",
        actual=int(payload.get("B", 0)),
        expected=target["B"],
    )
    _expect_equal(
        violations,
        name=name,
        field=f"{prefix}.curve",
        actual=str(payload.get("curve", "")),
        expected=target["curve"],
    )


def _missing_file(
    missing_files: list[dict[str, str]],
    *,
    name: str,
    kind: str,
    path: Path,
) -> None:
    missing_files.append({"name": name, "kind": kind, "path": str(path)})


def _cover_set(values: Any) -> list[int]:
    return sorted({int(value) for value in values or []})


def _cover_indices_from_rows(rows: list[dict[str, Any]]) -> list[int]:
    return [int(row["cover_index"]) for row in rows]


def _target_identity(target: dict[str, Any]) -> tuple[int, int, str]:
    return int(target.get("A", 0)), int(target.get("B", 0)), str(target.get("curve", ""))


def _spec_for_target(
    *,
    target: dict[str, Any],
    source: str,
    priority_rows: dict[int, dict[str, Any]],
    violations: list[dict[str, Any]],
) -> dict[str, Any]:
    priorities = _int_list(target.get("priorities", []))
    rows: list[dict[str, Any]] = []
    for priority in priorities:
        row = priority_rows.get(priority)
        if row is None:
            violations.append(
                {
                    "name": f"{source}:{_target_identity(target)}",
                    "field": "priorities",
                    "expected": f"priority row {priority}",
                    "actual": "missing",
                }
            )
        else:
            rows.append(row)

    expected_identity = _target_identity(target)
    for row in rows:
        row_identity = (int(row["A"]), int(row["B"]), str(row["curve"]))
        _expect_equal(
            violations,
            name=f"{source}:{expected_identity}",
            field=f"priority_{int(row['priority'])}.target",
            actual=row_identity,
            expected=expected_identity,
        )
        _expect_equal(
            violations,
            name=f"{source}:{expected_identity}",
            field=f"priority_{int(row['priority'])}.proof_status",
            actual=str(row.get("proof_status", "")),
            expected="candidate-not-proof",
        )

    if rows:
        cover_order = _cover_indices_from_rows(rows)
    else:
        cover_order = _int_list(target.get("cover_indices", []))
    a_value, b_value, curve = expected_identity
    first_priority = min(priorities) if priorities else 0
    covers = "_".join(str(index) for index in cover_order)
    name = f"priority_{first_priority:03d}_{a_value}_{b_value}_{curve}_covers_{covers}"
    frontier_type = str(
        target.get("frontier_type")
        or (
            "rank-zero-needs-rank-proof"
            if source == "rank-zero"
            else "non-rankzero-frontier"
        )
    )
    target_cover_set = _cover_set(target.get("cover_indices", []))
    priority_cover_set = _cover_set(cover_order)
    _expect_equal(
        violations,
        name=name,
        field="queue.cover_indices",
        actual=priority_cover_set,
        expected=target_cover_set,
    )
    _expect_equal(
        violations,
        name=name,
        field="queue.candidate_not_proof",
        actual=target.get("candidate_not_proof") is True,
        expected=True,
    )
    return {
        "name": name,
        "source": source,
        "target": _target_dict(target),
        "frontier_type": frontier_type,
        "priorities": priorities,
        "cover_order": cover_order,
        "cover_set": target_cover_set,
        "rank_bounds": _int_list(target.get("rank_bounds", [])),
        "expected_quartics": {
            int(row["cover_index"]): str(row.get("quartic", "")) for row in rows
        },
    }


def _frontier_specs(
    *,
    rank_zero_queue: dict[str, Any],
    non_rankzero_queue: dict[str, Any],
    priorities: dict[str, Any],
    violations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    _expect_equal(
        violations,
        name="rank-zero-queue",
        field="status",
        actual=str(rank_zero_queue.get("status", "")),
        expected="ok",
    )
    _expect_equal(
        violations,
        name="non-rankzero-queue",
        field="status",
        actual=str(non_rankzero_queue.get("status", "")),
        expected="ok",
    )
    priority_rows = _priority_rows_by_number(priorities)
    specs: list[dict[str, Any]] = []
    for target in rank_zero_queue.get("targets", []):
        specs.append(
            _spec_for_target(
                target=target,
                source="rank-zero",
                priority_rows=priority_rows,
                violations=violations,
            )
        )
    for target in non_rankzero_queue.get("targets", []):
        specs.append(
            _spec_for_target(
                target=target,
                source="non-rankzero",
                priority_rows=priority_rows,
                violations=violations,
            )
        )
    return specs


def _audit_handoff(
    *,
    spec: dict[str, Any],
    handoff: dict[str, Any],
    violations: list[dict[str, Any]],
) -> dict[str, Any]:
    name = str(spec["name"])
    target = spec["target"]
    _expect_target_identity(
        violations,
        name=name,
        prefix="handoff",
        payload=handoff,
        target=target,
    )
    strict_status = str(handoff.get("strict_proof_status", ""))
    _expect_equal(
        violations,
        name=name,
        field="strict_proof_status",
        actual=strict_status,
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
    target_cover_indices = _cover_set(handoff.get("target_cover_indices", []))
    _expect_equal(
        violations,
        name=name,
        field="handoff.target_cover_indices",
        actual=target_cover_indices,
        expected=spec["cover_set"],
    )
    covers = handoff.get("target_covers", [])
    cover_indices = _cover_set(cover.get("index") for cover in covers)
    _expect_equal(
        violations,
        name=name,
        field="handoff.target_covers.indices",
        actual=cover_indices,
        expected=spec["cover_set"],
    )
    actual_quartics = {
        int(cover.get("index", -1)): str(cover.get("quartic", "")) for cover in covers
    }
    _expect_equal(
        violations,
        name=name,
        field="handoff.target_covers.quartics",
        actual=actual_quartics,
        expected=spec["expected_quartics"],
    )
    point_counts = [int(cover.get("point_count", -1)) for cover in covers]
    _expect_equal(
        violations,
        name=name,
        field="handoff.target_covers.point_counts",
        actual=point_counts,
        expected=[0 for _cover in covers],
    )
    return {"strict_proof_status": strict_status}


def _audit_probe(
    *,
    spec: dict[str, Any],
    probe: dict[str, Any],
    violations: list[dict[str, Any]],
) -> dict[str, Any]:
    name = str(spec["name"])
    target = spec["target"]
    _expect_target_identity(
        violations,
        name=name,
        prefix="probe",
        payload=probe,
        target=target,
    )
    _expect_equal(
        violations,
        name=name,
        field="probe.status",
        actual=str(probe.get("status", "")),
        expected="ok",
    )
    sage = probe.get("sage", {})
    _expect_equal(
        violations,
        name=name,
        field="probe.rank_bounds",
        actual=_int_list(sage.get("rank_bounds", [])),
        expected=spec["rank_bounds"],
    )
    rank_proof_status = str(sage.get("rank_proof_status", ""))
    _expect_equal(
        violations,
        name=name,
        field="probe.rank_proof_status",
        actual=rank_proof_status,
        expected="runtime-error",
    )
    covers = sage.get("covers", [])
    cover_indices = _cover_set(row.get("index") for row in covers)
    _expect_equal(
        violations,
        name=name,
        field="probe.cover_indices",
        actual=cover_indices,
        expected=spec["cover_set"],
    )
    cover_point_counts = [int(row.get("rational_point_count", -1)) for row in covers]
    _expect_equal(
        violations,
        name=name,
        field="probe.cover_point_counts",
        actual=cover_point_counts,
        expected=[0 for _row in covers],
    )
    cover_statuses = [str(row.get("point_search_status", "")) for row in covers]
    _expect_equal(
        violations,
        name=name,
        field="probe.cover_point_search_statuses",
        actual=cover_statuses,
        expected=["ok" for _row in covers],
    )
    return {
        "rank_proof_status": rank_proof_status,
        "rank_bounds": _int_list(sage.get("rank_bounds", [])),
        "cover_point_counts": cover_point_counts,
    }


def _audit_map_verify(
    *,
    spec: dict[str, Any],
    map_verify: dict[str, Any],
    violations: list[dict[str, Any]],
) -> dict[str, Any]:
    name = str(spec["name"])
    target = spec["target"]
    _expect_target_identity(
        violations,
        name=name,
        prefix="map_verify",
        payload=map_verify,
        target=target,
    )
    _expect_equal(
        violations,
        name=name,
        field="map_verify.status",
        actual=str(map_verify.get("status", "")),
        expected="ok",
    )
    sage = map_verify.get("sage", {})
    all_verified = sage.get("all_verified") is True
    _expect_equal(
        violations,
        name=name,
        field="map_verify.all_verified",
        actual=all_verified,
        expected=True,
    )
    covers = sage.get("covers", [])
    cover_indices = _cover_set(row.get("index") for row in covers)
    _expect_equal(
        violations,
        name=name,
        field="map_verify.cover_indices",
        actual=cover_indices,
        expected=spec["cover_set"],
    )
    verified = [row.get("identity_verified") is True for row in covers]
    _expect_equal(
        violations,
        name=name,
        field="map_verify.cover_identity_verified",
        actual=verified,
        expected=[True for _row in covers],
    )
    return {"map_all_verified": all_verified}


def _audit_local_witnesses(
    *,
    spec: dict[str, Any],
    local_witnesses: dict[str, Any],
    violations: list[dict[str, Any]],
) -> dict[str, Any]:
    name = str(spec["name"])
    target = spec["target"]
    _expect_target_identity(
        violations,
        name=name,
        prefix="local_witnesses",
        payload=local_witnesses,
        target=target,
    )
    _expect_equal(
        violations,
        name=name,
        field="local_witnesses.status",
        actual=str(local_witnesses.get("status", "")),
        expected="ok",
    )
    sage = local_witnesses.get("sage", {})
    all_witnessed = sage.get("all_bad_primes_witnessed") is True
    _expect_equal(
        violations,
        name=name,
        field="local_witnesses.all_bad_primes_witnessed",
        actual=all_witnessed,
        expected=True,
    )
    covers = sage.get("covers", [])
    cover_indices = _cover_set(row.get("index") for row in covers)
    _expect_equal(
        violations,
        name=name,
        field="local_witnesses.cover_indices",
        actual=cover_indices,
        expected=spec["cover_set"],
    )
    cover_all_witnessed = [row.get("all_witnessed") is True for row in covers]
    _expect_equal(
        violations,
        name=name,
        field="local_witnesses.cover_all_witnessed",
        actual=cover_all_witnessed,
        expected=[True for _row in covers],
    )
    return {"local_all_bad_primes_witnessed": all_witnessed}


def audit_frontier_handoffs(
    *,
    rank_zero_queue: dict[str, Any],
    non_rankzero_queue: dict[str, Any],
    priorities: dict[str, Any],
    handoff_dir: Path,
) -> dict[str, Any]:
    missing_files: list[dict[str, str]] = []
    violations: list[dict[str, Any]] = []
    specs = _frontier_specs(
        rank_zero_queue=rank_zero_queue,
        non_rankzero_queue=non_rankzero_queue,
        priorities=priorities,
        violations=violations,
    )
    groups: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    strict_promotion_count = 0

    for spec in specs:
        name = str(spec["name"])
        group: dict[str, Any] = {
            "name": name,
            "source": spec["source"],
            "target": spec["target"],
            "frontier_type": spec["frontier_type"],
            "priorities": spec["priorities"],
            "cover_indices": spec["cover_set"],
            "handoff_cover_order": spec["cover_order"],
            "rank_bounds": spec["rank_bounds"],
            "proof_status": "handoff-not-proof",
        }

        for kind, suffix in (("json", ".json"), ("sage", ".sage"), ("magma", ".magma")):
            path = handoff_dir / f"{name}{suffix}"
            if not path.is_file():
                _missing_file(missing_files, name=name, kind=kind, path=path)

        handoff_path = handoff_dir / f"{name}.json"
        if handoff_path.is_file():
            handoff_summary = _audit_handoff(
                spec=spec,
                handoff=load_json(handoff_path),
                violations=violations,
            )
            group.update(handoff_summary)
            if handoff_summary["strict_proof_status"] != "open":
                strict_promotion_count += 1

        probe_path = handoff_dir / f"{name}_sage_probe.json"
        if not probe_path.is_file():
            _missing_file(missing_files, name=name, kind="sage_probe", path=probe_path)
        else:
            probe_summary = _audit_probe(
                spec=spec,
                probe=load_json(probe_path),
                violations=violations,
            )
            group.update(probe_summary)
            status_counts.update([f"probe:{probe_summary['rank_proof_status']}"])
            if probe_summary["rank_proof_status"] != "runtime-error":
                strict_promotion_count += 1

        map_verify_path = handoff_dir / f"{name}_map_verify.json"
        if not map_verify_path.is_file():
            _missing_file(missing_files, name=name, kind="map_verify", path=map_verify_path)
        else:
            map_summary = _audit_map_verify(
                spec=spec,
                map_verify=load_json(map_verify_path),
                violations=violations,
            )
            group.update(map_summary)
            status_counts.update(["map:ok" if map_summary["map_all_verified"] else "map:issue"])

        local_witness_path = handoff_dir / f"{name}_local_witnesses.json"
        if not local_witness_path.is_file():
            _missing_file(
                missing_files,
                name=name,
                kind="local_witnesses",
                path=local_witness_path,
            )
        else:
            local_summary = _audit_local_witnesses(
                spec=spec,
                local_witnesses=load_json(local_witness_path),
                violations=violations,
            )
            group.update(local_summary)
            status_counts.update(
                ["local:ok" if local_summary["local_all_bad_primes_witnessed"] else "local:issue"]
            )

        groups.append(group)

    rank_zero_group_count = sum(1 for group in groups if group["source"] == "rank-zero")
    non_rankzero_group_count = sum(
        1 for group in groups if group["source"] == "non-rankzero"
    )
    map_verified_group_count = sum(
        1 for group in groups if group.get("map_all_verified") is True
    )
    local_witnessed_group_count = sum(
        1 for group in groups if group.get("local_all_bad_primes_witnessed") is True
    )
    bounded_probe_group_count = sum(
        1
        for group in groups
        if group.get("rank_proof_status") == "runtime-error"
        and all(count == 0 for count in group.get("cover_point_counts", []))
    )
    status = (
        "ok"
        if not missing_files and not violations and strict_promotion_count == 0
        else "issues"
    )
    return {
        "status": status,
        "ready": status == "ok",
        "handoff_group_count": len(groups),
        "target_cover_count": sum(len(spec["cover_set"]) for spec in specs),
        "rank_zero_group_count": rank_zero_group_count,
        "non_rankzero_group_count": non_rankzero_group_count,
        "map_verified_group_count": map_verified_group_count,
        "local_witnessed_group_count": local_witnessed_group_count,
        "bounded_probe_group_count": bounded_probe_group_count,
        "strict_promotion_count": strict_promotion_count,
        "candidate_not_proof": strict_promotion_count == 0,
        "status_counts": dict(sorted(status_counts.items())),
        "missing_files": missing_files,
        "violations": violations,
        "groups": groups,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rank-zero-queue", type=Path, required=True)
    parser.add_argument("--non-rankzero-queue", type=Path, required=True)
    parser.add_argument("--priorities", type=Path, required=True)
    parser.add_argument("--handoff-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_frontier_handoffs(
        rank_zero_queue=load_json(args.rank_zero_queue),
        non_rankzero_queue=load_json(args.non_rankzero_queue),
        priorities=load_json(args.priorities),
        handoff_dir=args.handoff_dir,
    )
    write_json(args.out, audit)
    print(f"wrote mixed closure frontier handoff audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"handoff_group_count={audit['handoff_group_count']}")
    print(f"target_cover_count={audit['target_cover_count']}")
    print(f"strict_promotion_count={audit['strict_promotion_count']}")
    print(f"missing_files={audit['missing_files']}")
    print(f"violations={audit['violations']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
