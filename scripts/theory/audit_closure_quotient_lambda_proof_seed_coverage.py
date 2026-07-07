#!/usr/bin/env python3
"""Audit coverage of lambda routes by proof-seed ledgers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This checks that lambda route classes are covered by proof-seed ledgers. "
    "It does not prove any lambda-family exclusion theorem."
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


def _family_exclusion_count(*payloads: dict[str, Any]) -> int:
    return sum(_int_value(payload, "family_exclusion_proved_count") for payload in payloads)


def _violation(
    *,
    field: str,
    route_partition: int,
    seed_ledger: int,
) -> dict[str, int | str]:
    return {
        "field": field,
        "route_partition": route_partition,
        "seed_ledger": seed_ledger,
    }


def audit_lambda_proof_seed_coverage(
    *,
    route_partition: dict[str, Any],
    rank_zero_seeds: dict[str, Any],
    root_number_seeds: dict[str, Any],
    two_cover_seeds: dict[str, Any],
) -> dict[str, Any]:
    route_class_counts = {
        "rank_zero": _int_value(route_partition, "rank_zero_class_count"),
        "root_number": _int_value(route_partition, "root_number_class_count"),
        "two_cover": _int_value(route_partition, "two_cover_class_count"),
    }
    seed_ledger_class_counts = {
        "rank_zero": _int_value(rank_zero_seeds, "candidate_class_count"),
        "root_number": _int_value(root_number_seeds, "target_class_count"),
        "two_cover": _int_value(two_cover_seeds, "target_class_count"),
    }
    seed_group_counts = {
        "rank_zero": _int_value(rank_zero_seeds, "seed_group_count"),
        "root_number": _int_value(root_number_seeds, "seed_group_count"),
        "two_cover": _int_value(two_cover_seeds, "seed_group_count"),
    }
    seed_ledger_class_count = sum(seed_ledger_class_counts.values())
    lambda_class_count = _int_value(route_partition, "lambda_class_count")
    covered_class_count = _int_value(route_partition, "covered_class_count")

    violations: list[dict[str, int | str]] = []
    for route, route_count in route_class_counts.items():
        seed_count = seed_ledger_class_counts[route]
        if route_count != seed_count:
            violations.append(
                _violation(
                    field=f"{route}_class_count",
                    route_partition=route_count,
                    seed_ledger=seed_count,
                )
            )
    if covered_class_count != seed_ledger_class_count:
        violations.append(
            _violation(
                field="seed_ledger_class_count",
                route_partition=covered_class_count,
                seed_ledger=seed_ledger_class_count,
            )
        )

    family_exclusion_proved_count = _family_exclusion_count(
        route_partition,
        rank_zero_seeds,
        root_number_seeds,
        two_cover_seeds,
    )
    if family_exclusion_proved_count:
        violations.append(
            _violation(
                field="family_exclusion_proved_count",
                route_partition=0,
                seed_ledger=family_exclusion_proved_count,
            )
        )
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "lambda_class_count": lambda_class_count,
        "covered_class_count": covered_class_count,
        "seed_ledger_class_count": seed_ledger_class_count,
        "route_class_counts": route_class_counts,
        "seed_ledger_class_counts": seed_ledger_class_counts,
        "seed_group_counts": seed_group_counts,
        "two_cover_candidate_cover_total": _int_value(
            two_cover_seeds,
            "candidate_cover_total",
        ),
        "all_routes_have_seed_ledgers": not violations,
        "family_exclusion_proved_count": family_exclusion_proved_count,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--route-partition", type=Path, required=True)
    parser.add_argument("--rank-zero-seeds", type=Path, required=True)
    parser.add_argument("--root-number-seeds", type=Path, required=True)
    parser.add_argument("--two-cover-seeds", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_lambda_proof_seed_coverage(
        route_partition=load_json(args.route_partition),
        rank_zero_seeds=load_json(args.rank_zero_seeds),
        root_number_seeds=load_json(args.root_number_seeds),
        two_cover_seeds=load_json(args.two_cover_seeds),
    )
    write_json(args.out, audit)
    print(f"wrote closure quotient lambda proof seed coverage audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"lambda_class_count={audit['lambda_class_count']}")
    print(f"seed_ledger_class_count={audit['seed_ledger_class_count']}")
    print(f"violations={audit['violations']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
