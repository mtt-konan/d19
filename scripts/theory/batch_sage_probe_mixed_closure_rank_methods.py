#!/usr/bin/env python3
"""Batch Sage rank-method probes for mixed-closure frontier handoffs."""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.theory.sage_probe_mixed_closure_rank_methods import (  # noqa: E402
    load_json,
    probe_rank_methods,
    write_json,
)

Run = Callable[..., subprocess.CompletedProcess[str]]

DEFAULT_BATCH_METHODS = ("rank_bounds", "selmer_rank", "pari_ellrank")
DEFAULT_TRACKS = ("rank-zero-rank-proof",)

BOUNDARY = (
    "This batches Sage rank-method diagnostics over frontier handoffs. It does "
    "not prove residual covers have no rational point; open rank bounds, "
    "timeouts, runtime errors, and bounded method limits remain nonproof."
)


def _target_key(payload: dict[str, Any]) -> tuple[int, int, str]:
    return int(payload.get("A", 0)), int(payload.get("B", 0)), str(payload.get("curve", ""))


def _group_key(group: dict[str, Any]) -> tuple[int, int, str]:
    return _target_key(dict(group.get("target", {})))


def _handoff_groups(
    handoff_audit: dict[str, Any],
) -> dict[tuple[int, int, str], dict[str, Any]]:
    return {_group_key(group): group for group in handoff_audit.get("groups", [])}


def _selected_targets(
    *,
    strictification_queue: dict[str, Any],
    handoff_audit: dict[str, Any],
    handoff_dir: Path,
    tracks: list[str],
    limit: int | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    groups = _handoff_groups(handoff_audit)
    selected: list[dict[str, Any]] = []
    missing_files: list[dict[str, Any]] = []
    track_set = set(tracks)
    matched_count = 0

    for target in strictification_queue.get("targets", []):
        if str(target.get("track", "")) not in track_set:
            continue
        matched_count += 1
        group = groups.get(_target_key(target))
        if group is None:
            missing_files.append(
                {
                    "name": "",
                    "target": {
                        "A": int(target.get("A", 0)),
                        "B": int(target.get("B", 0)),
                        "curve": str(target.get("curve", "")),
                    },
                    "reason": "missing handoff audit group",
                }
            )
            if limit is not None and matched_count >= limit:
                break
            continue
        name = str(group["name"])
        path = handoff_dir / f"{name}.json"
        if not path.is_file():
            missing_files.append({"name": name, "path": str(path)})
            if limit is not None and matched_count >= limit:
                break
            continue
        selected.append(
            {
                "name": name,
                "path": path,
                "target": target,
            }
        )
        if limit is not None and matched_count >= limit:
            break

    return selected, missing_files


def _target_metadata(entry: dict[str, Any], probe: dict[str, Any]) -> dict[str, Any]:
    target = dict(entry["target"])
    return {
        "name": str(entry["name"]),
        "handoff": str(entry["path"]),
        "A": int(target["A"]),
        "B": int(target["B"]),
        "curve": str(target["curve"]),
        "track": str(target.get("track", "")),
        "priorities": [int(value) for value in target.get("priorities", [])],
        "cover_indices": [int(value) for value in target.get("cover_indices", [])],
        "probe": probe,
    }


def batch_probe_rank_methods(
    *,
    strictification_queue: dict[str, Any],
    handoff_audit: dict[str, Any],
    handoff_dir: Path,
    methods: list[str],
    tracks: list[str],
    limit: int | None,
    sage_executable: str,
    timeout_seconds: int,
    two_descent_second_limit: int | None,
    run: Run = subprocess.run,
    dot_sage: Path | None = None,
) -> dict[str, Any]:
    selected, missing_files = _selected_targets(
        strictification_queue=strictification_queue,
        handoff_audit=handoff_audit,
        handoff_dir=handoff_dir,
        tracks=tracks,
        limit=limit,
    )
    targets = [
        _target_metadata(
            entry,
            probe_rank_methods(
                load_json(entry["path"]),
                methods=methods,
                sage_executable=sage_executable,
                timeout_seconds=timeout_seconds,
                two_descent_second_limit=two_descent_second_limit,
                run=run,
                dot_sage=dot_sage,
            ),
        )
        for entry in selected
    ]
    violations: list[dict[str, Any]] = []
    if strictification_queue.get("status") != "ok":
        violations.append(
            {
                "name": "strictification_queue",
                "field": "status",
                "expected": "ok",
                "actual": strictification_queue.get("status"),
            }
        )
    if handoff_audit.get("status") != "ok":
        violations.append(
            {
                "name": "handoff_audit",
                "field": "status",
                "expected": "ok",
                "actual": handoff_audit.get("status"),
            }
        )

    status = "ok" if not missing_files and not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "tracks": list(tracks),
        "methods": list(methods),
        "timeout_seconds": int(timeout_seconds),
        "target_count": len(targets),
        "missing_files": missing_files,
        "violations": violations,
        "method_status_counts": dict(
            sorted(
                Counter(
                    key
                    for target in targets
                    for key, count in target["probe"]
                    .get("method_status_counts", {})
                    .items()
                    for _ in range(int(count))
                ).items()
            )
        ),
        "rank_zero_proof_candidate_count": sum(
            1
            for target in targets
            if target["probe"].get("rank_zero_proof_candidate") is True
        ),
        "targets": targets,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strictification-queue", type=Path, required=True)
    parser.add_argument("--handoff-audit", type=Path, required=True)
    parser.add_argument(
        "--handoff-dir",
        type=Path,
        default=Path("results/mixed_closure_residual_handoffs"),
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sage", default="sage")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--method", action="append", default=[])
    parser.add_argument("--track", action="append", default=[])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--two-descent-second-limit", type=int, default=None)
    parser.add_argument(
        "--dot-sage",
        type=Path,
        default=Path("/private/tmp/d19-dot-sage"),
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = batch_probe_rank_methods(
        strictification_queue=load_json(args.strictification_queue),
        handoff_audit=load_json(args.handoff_audit),
        handoff_dir=args.handoff_dir,
        methods=list(args.method or DEFAULT_BATCH_METHODS),
        tracks=list(args.track or DEFAULT_TRACKS),
        limit=args.limit,
        sage_executable=args.sage,
        timeout_seconds=args.timeout,
        two_descent_second_limit=args.two_descent_second_limit,
        dot_sage=args.dot_sage,
    )
    write_json(args.out, result)
    print(f"wrote batch Sage rank-method probe to {args.out}")
    print(f"status={result['status']}")
    print(f"target_count={result['target_count']}")
    print(f"method_status_counts={result['method_status_counts']}")
    print(
        "rank_zero_proof_candidate_count="
        f"{result['rank_zero_proof_candidate_count']}"
    )
    if args.strict and result["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
