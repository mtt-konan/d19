#!/usr/bin/env python3
"""Export strict-proof handoff files for mixed-closure residual 2-covers."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory.sage_recheck_mixed_closure_residuals import parse_curve_target  # noqa: E402


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _row_key(row: dict[str, Any]) -> tuple[int, int, str]:
    return int(row["A"]), int(row["B"]), str(row["curve"])


def _find_row(rows: list[dict[str, Any]], target: tuple[int, int, str]) -> dict[str, Any]:
    for row in rows:
        if _row_key(row) == target:
            return row
    raise ValueError(f"target row not found: {target[0]},{target[1]},{target[2]}")


def _bsd_row(
    rows: list[dict[str, Any]] | None,
    target: tuple[int, int, str],
) -> dict[str, Any] | None:
    if rows is None:
        return None
    try:
        return _find_row(rows, target)
    except ValueError:
        return None


def _select_covers(
    cover_row: dict[str, Any],
    target_indices: list[int],
) -> list[dict[str, Any]]:
    by_index = {int(cover["index"]): cover for cover in cover_row.get("covers", [])}
    selected: list[dict[str, Any]] = []
    for index in target_indices:
        if index not in by_index:
            raise ValueError(f"cover index {index} not found")
        cover = by_index[index]
        selected.append(
            {
                "index": int(cover["index"]),
                "quartic": str(cover["quartic"]),
                "covering_map_to_elliptic": str(cover.get("covering_map_to_elliptic", "")),
                "point_count": int(cover.get("point_count", 0)),
                "points": list(cover.get("points", [])),
            }
        )
    return selected


def _bsd_diagnostic(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    keys = (
        "status",
        "analytic_rank",
        "analytic_leading_value",
        "bsd_factor",
        "evidence_level",
    )
    return {key: row[key] for key in keys if key in row}


def build_handoff(
    *,
    cover_row: dict[str, Any],
    bsd_row: dict[str, Any] | None,
    target_indices: list[int],
) -> dict[str, Any]:
    return {
        "A": int(cover_row["A"]),
        "B": int(cover_row["B"]),
        "curve": str(cover_row["curve"]),
        "weierstrass_model": cover_row["model"],
        "input_rank": str(cover_row["input_rank"]),
        "ellrank": cover_row["ellrank"],
        "target_cover_indices": target_indices,
        "target_covers": _select_covers(cover_row, target_indices),
        "local_solubility_source": (
            "PARI ell2cover returns everywhere locally soluble 2-covers"
        ),
        "bounded_search_evidence": (
            "hyperellratpoints found no points on target covers in the input row"
        ),
        "bsd_conditional_diagnostic": _bsd_diagnostic(bsd_row),
        "strict_proof_status": "open",
        "proof_boundary": (
            "This handoff packages evidence and external-tool inputs. It does not "
            "prove that any cover has no rational point."
        ),
        "next_strict_tasks": [
            (
                "Prove each target cover has no rational point, or replace this "
                "with a strict rank/L-value certificate."
            ),
            (
                "If using Magma or a Mordell-Weil sieve, record a reproducible "
                "transcript before promoting the result."
            ),
        ],
    }


def _sage_quartic(quartic: str) -> str:
    return quartic.replace("^", "**")


def render_sage_handoff(handoff: dict[str, Any]) -> str:
    lines = [
        "# Sage handoff for mixed-closure residual 2-covers.",
        "# This file packages targets for further work; bounded search is not a proof.",
        "from sage.all import *",
        "R = PolynomialRing(QQ, names=('x',))",
        "x = R.gen()",
        "",
    ]
    for cover in handoff["target_covers"]:
        index = int(cover["index"])
        lines.extend(
            [
                f"f{index} = {_sage_quartic(str(cover['quartic']))}",
                f"C{index} = HyperellipticCurve(f{index}, R(0))",
                f"print('cover {index}:', C{index})",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_magma_handoff(handoff: dict[str, Any]) -> str:
    lines = [
        "// Magma handoff for mixed-closure residual 2-covers.",
        "// This Magma file is a handoff, not a certified transcript.",
        "Q := Rationals();",
        "P<x> := PolynomialRing(Q);",
        "",
    ]
    for cover in handoff["target_covers"]:
        index = int(cover["index"])
        lines.extend(
            [
                f"f{index} := {cover['quartic']};",
                f"C{index} := HyperellipticCurve(f{index});",
                f"print \"cover {index}\", C{index};",
                "",
            ]
        )
    lines.extend(
        [
            "// Suggested next steps in Magma, depending on available packages:",
            "//   Points(Ci : Bound := 100000);            // search only",
            "//   RankBounds(Jacobian(Ci));               // diagnostic, not enough alone",
            "//   Run a Mordell-Weil sieve / genus-one proof and save the transcript.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_handoff_files(out_dir: Path, name: str, handoff: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{name}.json").write_text(
        json.dumps(handoff, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out_dir / f"{name}.sage").write_text(render_sage_handoff(handoff), encoding="utf-8")
    (out_dir / f"{name}.magma").write_text(
        render_magma_handoff(handoff),
        encoding="utf-8",
    )


def priority_handoff_specs(priorities: dict[str, Any], *, top: int) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, int, str], dict[str, Any]] = {}
    for row in priorities.get("rows", [])[:top]:
        key = _row_key(row)
        if key not in grouped:
            grouped[key] = {
                "target": key,
                "cover_indices": [],
                "priorities": [],
            }
        grouped[key]["cover_indices"].append(int(row["cover_index"]))
        grouped[key]["priorities"].append(int(row["priority"]))

    specs: list[dict[str, Any]] = []
    for item in grouped.values():
        first_priority = min(item["priorities"])
        a_value, b_value, curve = item["target"]
        covers = "_".join(str(index) for index in item["cover_indices"])
        specs.append(
            {
                "name": (
                    f"priority_{first_priority:03d}_{a_value}_{b_value}_{curve}"
                    f"_covers_{covers}"
                ),
                "target": item["target"],
                "cover_indices": item["cover_indices"],
                "priorities": item["priorities"],
            }
        )
    return sorted(specs, key=lambda spec: min(spec["priorities"]))


def write_priority_handoff_files(
    *,
    cover_rows: list[dict[str, Any]],
    bsd_rows: list[dict[str, Any]] | None,
    priorities: dict[str, Any],
    top: int,
    out_dir: Path,
) -> list[dict[str, Any]]:
    written: list[dict[str, Any]] = []
    for spec in priority_handoff_specs(priorities, top=top):
        cover_row = _find_row(cover_rows, spec["target"])
        handoff = build_handoff(
            cover_row=cover_row,
            bsd_row=_bsd_row(bsd_rows, spec["target"]),
            target_indices=spec["cover_indices"],
        )
        handoff["priority_source"] = {
            "priorities": spec["priorities"],
            "name": spec["name"],
        }
        write_handoff_files(out_dir, spec["name"], handoff)
        written.append(
            {
                "name": spec["name"],
                "target": spec["target"],
                "cover_indices": spec["cover_indices"],
                "priorities": spec["priorities"],
            }
        )
    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--covers", type=Path, required=True)
    parser.add_argument("--bsd", type=Path, default=None)
    parser.add_argument("--target", type=parse_curve_target, default=None)
    parser.add_argument("--cover-index", type=int, action="append", default=[])
    parser.add_argument(
        "--priorities",
        type=Path,
        default=None,
        help="Priority JSON from prioritize_mixed_closure_residual_covers.py.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=None,
        help="When --priorities is set, export the first N priority rows grouped by target.",
    )
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--name", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cover_rows = load_jsonl(args.covers)
    bsd_rows = load_jsonl(args.bsd) if args.bsd else None
    if args.priorities is not None:
        if args.top is None or args.top <= 0:
            raise ValueError("--top must be a positive integer when --priorities is set")
        written = write_priority_handoff_files(
            cover_rows=cover_rows,
            bsd_rows=bsd_rows,
            priorities=load_json(args.priorities),
            top=args.top,
            out_dir=args.out_dir,
        )
        print(f"wrote {len(written)} priority handoff(s) to {args.out_dir}")
        for row in written:
            print(f"  {row['name']}: covers={row['cover_indices']}")
        return 0

    if args.target is None or not args.cover_index or args.name is None:
        raise ValueError("--target, --cover-index, and --name are required without --priorities")

    cover_row = _find_row(cover_rows, args.target)
    handoff = build_handoff(
        cover_row=cover_row,
        bsd_row=_bsd_row(bsd_rows, args.target),
        target_indices=args.cover_index,
    )
    write_handoff_files(args.out_dir, args.name, handoff)
    print(f"wrote handoff {args.name} to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
