#!/usr/bin/env python3
"""Verify stored rational maps for all residual mixed-closure no-point covers."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.sage_verify_mixed_closure_handoff_maps import verify_handoff_maps  # noqa: E402

Run = Callable[..., subprocess.CompletedProcess[str]]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _row_key(row: dict[str, Any]) -> tuple[int, int, str]:
    return int(row["A"]), int(row["B"]), str(row["curve"])


def build_residual_map_handoffs(
    *,
    cover_rows: list[dict[str, Any]],
    cover_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    cover_rows_by_key = {_row_key(row): row for row in cover_rows}
    handoffs: list[dict[str, Any]] = []

    for summary_row in cover_summary.get("no_point_cover_rows", []):
        cover_row = cover_rows_by_key[_row_key(summary_row)]
        covers_by_index = {
            int(cover["index"]): cover for cover in cover_row.get("covers", [])
        }
        target_indices = [
            int(index) for index in summary_row.get("no_point_cover_indices", [])
        ]
        target_covers = []
        for index in target_indices:
            cover = covers_by_index[index]
            target_covers.append(
                {
                    "index": index,
                    "quartic": str(cover["quartic"]),
                    "covering_map_to_elliptic": str(
                        cover.get("covering_map_to_elliptic", "")
                    ),
                }
            )
        handoffs.append(
            {
                "A": int(summary_row["A"]),
                "B": int(summary_row["B"]),
                "curve": str(summary_row["curve"]),
                "weierstrass_model": cover_row["model"],
                "target_cover_indices": target_indices,
                "target_covers": target_covers,
            }
        )

    return handoffs


def _group_summary(
    handoff: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    covers = list(result.get("sage", {}).get("covers", []))
    verified_cover_count = sum(
        1 for cover in covers if cover.get("identity_verified") is True
    )
    failed_cover_count = sum(
        1 for cover in covers if cover.get("identity_verified") is not True
    )
    return {
        "A": int(handoff["A"]),
        "B": int(handoff["B"]),
        "curve": str(handoff["curve"]),
        "target_cover_indices": [
            int(index) for index in handoff.get("target_cover_indices", [])
        ],
        "status": str(result.get("status", "missing")),
        "all_verified": bool(result.get("sage", {}).get("all_verified", False)),
        "verified_cover_count": verified_cover_count,
        "failed_cover_count": failed_cover_count,
    }


def verify_residual_cover_maps(
    *,
    cover_rows: list[dict[str, Any]],
    cover_summary: dict[str, Any],
    sage_executable: str,
    timeout_seconds: int,
    run: Run = subprocess.run,
    dot_sage: Path | None = None,
) -> dict[str, Any]:
    handoffs = build_residual_map_handoffs(
        cover_rows=cover_rows,
        cover_summary=cover_summary,
    )
    groups: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    target_cover_count = 0
    verified_cover_count = 0
    failed_cover_count = 0

    for handoff in handoffs:
        target_cover_count += len(handoff.get("target_covers", []))
        result = verify_handoff_maps(
            handoff,
            sage_executable=sage_executable,
            timeout_seconds=timeout_seconds,
            run=run,
            dot_sage=dot_sage,
        )
        group = _group_summary(handoff, result)
        groups.append(group)
        status_counts.update([group["status"]])
        verified_cover_count += int(group["verified_cover_count"])
        failed_cover_count += int(group["failed_cover_count"])

    all_verified = bool(
        groups
        and all(group["status"] == "ok" for group in groups)
        and all(group["all_verified"] for group in groups)
    )
    return {
        "status": "ok" if all_verified else "verification-failed",
        "all_verified": all_verified,
        "group_count": len(groups),
        "target_cover_count": target_cover_count,
        "verified_cover_count": verified_cover_count,
        "failed_cover_count": failed_cover_count,
        "status_counts": dict(sorted(status_counts.items())),
        "groups": groups,
        "boundary": (
            "This verifies stored rational maps for residual no-point covers. "
            "It does not prove that any residual cover has no rational point."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--covers", type=Path, required=True)
    parser.add_argument("--cover-summary", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sage", default="sage")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument(
        "--dot-sage",
        type=Path,
        default=Path("/private/tmp/d19-dot-sage"),
        help="Writable DOT_SAGE directory for sandboxed Sage runs.",
    )
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = verify_residual_cover_maps(
        cover_rows=load_jsonl(args.covers),
        cover_summary=load_json(args.cover_summary),
        sage_executable=args.sage,
        timeout_seconds=args.timeout,
        dot_sage=args.dot_sage,
    )
    write_json(args.out, result)
    print(f"wrote residual cover map verification to {args.out}")
    print(f"status={result['status']}")
    print(f"target_cover_count={result['target_cover_count']}")
    print(f"all_verified={result['all_verified']}")
    if args.strict and not result["all_verified"]:
        return 1
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
