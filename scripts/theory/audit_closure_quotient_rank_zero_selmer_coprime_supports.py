#!/usr/bin/env python3
"""Audit coprime support partitions for rank-zero Selmer local checks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits symbolic coprime support partitions for future rank-zero "
    "isogeny-Selmer local checks. It does not compute local Selmer images, "
    "prove a Selmer rank bound, prove rank zero, or prove any lambda-family "
    "exclusion."
)

ODD_PRIME_PARTITION = [
    "odd primes dividing L",
    "odd primes dividing T",
    "odd primes dividing T^2 + 4*L^2",
]

SYMBOLIC_COPRIMALITY_FACTS = [
    {
        "statement": "gcd(L, T) = 1",
        "reason": "gcd(L, T)=gcd(L, A+B)=gcd(A, B) for primitive A:B",
    },
    {
        "statement": "gcd(L, T^2 + 4*L^2) = 1",
        "reason": "any common prime divides L and T^2, hence divides gcd(L,T)",
    },
    {
        "statement": "gcd(T, T^2 + 4*L^2) divides 4",
        "reason": (
            "any common prime divides T and 4*L^2; odd common primes divide "
            "gcd(T,L)"
        ),
    },
]

EXPECTED_SUPPORT_FACTORS = ["2", "L", "T", "T^2 + 4*L^2"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _ready(local_supports: dict[str, Any]) -> bool:
    return local_supports.get("status") == "ok" and local_supports.get("ready") is True


def _entry(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": str(row.get("package_id", "")),
        "kernel": str(row.get("kernel", "")),
        "odd_prime_partition_applies": True,
        "two_adic_check_required": True,
        "local_condition_proved": False,
    }


def audit_rank_zero_selmer_coprime_supports(
    *,
    local_supports: dict[str, Any],
) -> dict[str, Any]:
    support_entries = list(local_supports.get("support_entries", []))
    violations: list[str] = []
    if not _ready(local_supports):
        violations.append("local_supports_not_ready")
    if local_supports.get("support_factor_template") != EXPECTED_SUPPORT_FACTORS:
        violations.append("unexpected_support_factor_template")
    if local_supports.get("support_candidates_not_conditions") is not True:
        violations.append("support_candidates_promoted_to_conditions")
    if int(local_supports.get("local_condition_proved_count", 0) or 0) != 0:
        violations.append("local_condition_claim_count_nonzero")

    entries = [_entry(row) for row in support_entries]
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "package_count": int(local_supports.get("package_count", 0) or 0),
        "support_entry_count": int(local_supports.get("support_entry_count", 0) or 0),
        "coprime_support_entry_count": len(entries),
        "support_candidates_not_conditions": True,
        "two_adic_exception": True,
        "odd_prime_partition": ODD_PRIME_PARTITION,
        "symbolic_coprimality_facts": SYMBOLIC_COPRIMALITY_FACTS,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "entries": entries,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-supports", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_coprime_supports(
        local_supports=load_json(args.local_supports),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer coprime-support audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"package_count={audit['package_count']}")
    print(f"coprime_support_entry_count={audit['coprime_support_entry_count']}")
    print(f"local_condition_proved_count={audit['local_condition_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
