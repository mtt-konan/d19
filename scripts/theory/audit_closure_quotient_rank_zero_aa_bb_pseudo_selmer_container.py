#!/usr/bin/env python3
"""Audit a cheap pseudo-Selmer container for the AA+BB complete 2-descent route."""

from __future__ import annotations

try:
    from scripts.theory.json_io import load_json, load_jsonl, write_json
except ModuleNotFoundError:
    from json_io import load_json, load_jsonl, write_json

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits a pseudo-Selmer upper-bound container for the AA+BB "
    "complete 2-descent route. It does not prove rank zero, prove Sha[2]=0, "
    "or prove any family exclusion."
)

QUANTIFIER_AUDIT = [
    {
        "source": "wl457",
        "statement": "AA+BB kernel_neg_2sqrt_q has no odd-prime valuation support",
        "quantifier_kind": "mixed",
        "direct_transfer_to_sel2": False,
        "usable_in_pseudo_container": True,
        "reason": "uses local image rows plus AA/BB primitive common-source intersection",
    },
    {
        "source": "wl458",
        "statement": "AA+BB kernel_minus_p has no odd-prime valuation support",
        "quantifier_kind": "mixed",
        "direct_transfer_to_sel2": False,
        "usable_in_pseudo_container": True,
        "reason": "uses local image rows plus disjointness of D_A and D_B",
    },
    {
        "source": "wl459",
        "statement": "AA+BB kernel_pos_2sqrt_q has odd support only at ell | T, ell == 1 mod 4",
        "quantifier_kind": "mixed",
        "direct_transfer_to_sel2": False,
        "usable_in_pseudo_container": True,
        "reason": "uses local image rows and leaves the shared T tail",
    },
    {
        "source": "wl460",
        "statement": "opposite-mod-4 dyadic branch forces x_minus_p in {1}",
        "quantifier_kind": "local-point",
        "direct_transfer_to_sel2": True,
        "usable_in_pseudo_container": True,
        "reason": "Q_2 local image statement for one branch",
    },
    {
        "source": "wl461",
        "statement": "same-mod-4 dyadic branch has local x_minus_p class 2",
        "quantifier_kind": "local-point",
        "direct_transfer_to_sel2": True,
        "usable_in_pseudo_container": True,
        "reason": "Q_2 local image non-exclusion statement",
    },
    {
        "source": "wl462",
        "statement": (
            "same-mod-4 x_minus_p=2 is incompatible with the other two local "
            "kernel coordinates"
        ),
        "quantifier_kind": "local-common-source",
        "direct_transfer_to_sel2": True,
        "usable_in_pseudo_container": True,
        "reason": "the complete 2-descent local point carries all three root coordinates",
    },
    {
        "source": "wl463",
        "statement": "genuine AA+BB rational points collapse to (1,1,1)",
        "quantifier_kind": "global-point-summary",
        "direct_transfer_to_sel2": False,
        "usable_in_pseudo_container": False,
        "reason": "global rational-point conclusion, not a Sel_2 local membership row",
    },
]

PSEUDO_SELMER_CONTAINER = {
    "name": "S_tilde_AA_BB",
    "contained_object": "AA+BB common-source Selmer-candidate upper-bound container",
    "ambient_coordinates": ["d_minus_p", "d_pos_2sqrt_q", "d_neg_2sqrt_q"],
    "constraints": [
        "d_minus_p*d_pos_2sqrt_q*d_neg_2sqrt_q=1 in Q*/Q*2",
        "kernel_minus_p odd-prime support is trivial in the pseudo-container",
        "kernel_neg_2sqrt_q odd-prime support is trivial in the pseudo-container",
        (
            "kernel_pos_2sqrt_q odd-prime support is contained in primes "
            "ell | T with ell == 1 mod 4"
        ),
        (
            "wl460-wl463 dyadic rows collapse the rational 2-primary local "
            "common-source branch to (1,1,1)"
        ),
        "archimedean sign row is kept as a possible one-dimensional tail until checked",
    ],
    "common_source_candidate_subset_status": "proved-for-container-definition",
    "single_curve_full_sel2_subset_status": "not-claimed",
    "subset_reason": (
        "S~ is deliberately an upper-bound container for AA+BB common-source "
        "Selmer candidates: local-point rows are direct constraints, mixed "
        "odd-prime rows are used only as support bounds, and unresolved "
        "sign/T-tail classes are retained rather than cut."
    ),
}

DIMENSION_BOUND = {
    "torsion_baseline_dimension": 2,
    "symbolic_tail_terms": ["omega_{1 mod 4}(T)", "epsilon_sign"],
    "epsilon_sign_values": [0, 1],
    "upper_bound": "dim_F2 S~ <= 2 + omega_{1 mod 4}(T) + epsilon_sign",
    "forces_dim_2": False,
    "why_not_forced_dim_2": (
        "The current pseudo-container still allows a T-prime tail and an "
        "unresolved archimedean sign bit."
    ),
}

DIAGNOSTIC_OBJECT = {
    "measured_object": "single_curve_full_2_selmer",
    "source_tool": "Sage EllipticCurve(model).selmer_rank on the row's AA or BB curve",
    "not_measured": [
        "AA side only inside S_tilde_AA_BB",
        "BB side only inside S_tilde_AA_BB",
        "AA+BB common-source pseudo-container S_tilde_AA_BB",
        "complete C_d local matrix for S_tilde_AA_BB",
    ],
}


def _ready(payload: dict[str, Any]) -> bool:
    return payload.get("status") == "ok" and payload.get("ready") is True


def _prime_factors(n: int) -> list[int]:
    n = abs(n)
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            while n % divisor == 0:
                n //= divisor
        divisor += 1 if divisor == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


def _omega_one_mod_four(n: int) -> int:
    return sum(1 for prime in _prime_factors(n) if prime % 4 == 1)


def _selmer_rank(row: dict[str, Any]) -> int:
    if row.get("selmer_rank_mwrank") is not None:
        return int(row["selmer_rank_mwrank"])
    return int(row.get("selmer_rank_pari", 0) or 0)


def _rank_bounds(row: dict[str, Any]) -> list[int]:
    bounds = row.get("rank_bounds", [])
    if isinstance(bounds, list) and len(bounds) == 2:
        return [int(bounds[0]), int(bounds[1])]
    return []


def _diagnostic_summary(diagnostic_rows: list[dict[str, Any]]) -> dict[str, Any]:
    ok_rows = [row for row in diagnostic_rows if row.get("status") == "ok"]
    sample_rows: list[dict[str, Any]] = []
    t_tail_histogram: Counter[str] = Counter()
    eq_torsion_count = 0
    gt_torsion_count = 0
    proved_rank_zero_and_gt_torsion_count = 0
    frontier_gt_torsion_count = 0
    max_selmer_rank_minus_torsion = 0
    full_curve_rows_exceeding_capacity_count = 0
    omega_zero_full_curve_excess_rows = 0
    max_full_curve_excess_over_capacity = 0

    for row in ok_rows:
        a = int(row.get("A", 0) or 0)
        b = int(row.get("B", 0) or 0)
        total = a + b
        omega_tail = _omega_one_mod_four(total)
        symbolic_tail_capacity = omega_tail + max(DIMENSION_BOUND["epsilon_sign_values"])
        t_tail_histogram[str(omega_tail)] += 1
        selmer_rank = _selmer_rank(row)
        torsion_dim = int(row.get("torsion_two_dimension", 0) or 0)
        excess = selmer_rank - torsion_dim
        bounds = _rank_bounds(row)
        rank_zero_proved = bounds == [0, 0]

        if excess == 0:
            eq_torsion_count += 1
        if excess > 0:
            gt_torsion_count += 1
            if omega_tail == 0:
                omega_zero_full_curve_excess_rows += 1
            if rank_zero_proved:
                proved_rank_zero_and_gt_torsion_count += 1
            elif bounds and bounds[0] == 0:
                frontier_gt_torsion_count += 1
        max_selmer_rank_minus_torsion = max(max_selmer_rank_minus_torsion, excess)
        excess_over_capacity = excess - symbolic_tail_capacity
        if excess_over_capacity > 0:
            full_curve_rows_exceeding_capacity_count += 1
            max_full_curve_excess_over_capacity = max(
                max_full_curve_excess_over_capacity,
                excess_over_capacity,
            )

        if len(sample_rows) < 5:
            sample_rows.append(
                {
                    "A": a,
                    "B": b,
                    "curve": str(row.get("curve", "")),
                    "T": total,
                    "omega_1mod4_T": omega_tail,
                    "rank_bounds": bounds,
                    "selmer_rank": selmer_rank,
                    "torsion_two_dimension": torsion_dim,
                    "selmer_rank_minus_torsion": excess,
                    "rank_zero_proved": rank_zero_proved,
                    "diagnostic_object": DIAGNOSTIC_OBJECT["measured_object"],
                    "symbolic_container_tail_capacity": symbolic_tail_capacity,
                    "comparison_to_s_tilde_bound": "not_comparable_full_curve_diagnostic",
                }
            )

    return {
        "diagnostic_object": DIAGNOSTIC_OBJECT,
        "container_comparison": {
            "comparison_status": "not_comparable",
            "reason": (
                "The symbolic bound is for the AA+BB common-source pseudo-container S~, "
                "while diagnostics measure full 2-Selmer dimensions of individual AA/BB "
                "elliptic curves."
            ),
            "full_curve_rows_exceeding_symbolic_tail_capacity_count": (
                full_curve_rows_exceeding_capacity_count
            ),
            "omega_zero_full_curve_excess_rows": omega_zero_full_curve_excess_rows,
            "max_full_curve_excess_over_symbolic_tail_capacity": (
                max_full_curve_excess_over_capacity
            ),
        },
        "diagnostic_row_count": len(diagnostic_rows),
        "ok_row_count": len(ok_rows),
        "selmer_dim_eq_torsion_count": eq_torsion_count,
        "selmer_dim_gt_torsion_count": gt_torsion_count,
        "proved_rank_zero_and_selmer_gt_torsion_count": proved_rank_zero_and_gt_torsion_count,
        "rank_zero_frontier_selmer_gt_torsion_count": frontier_gt_torsion_count,
        "max_selmer_rank_minus_torsion": max_selmer_rank_minus_torsion,
        "t_tail_histogram": dict(sorted(t_tail_histogram.items())),
        "sample_rows": sample_rows,
    }


def _route_decision(diagnostic_summary: dict[str, Any]) -> dict[str, str]:
    if int(diagnostic_summary["proved_rank_zero_and_selmer_gt_torsion_count"]) > 0:
        return {
            "decision": "sha2_obstruction_candidate_after_rank_zero_confirmation",
            "reason": (
                "At least one diagnostic row has proved rank zero and Sel_2 dimension "
                "larger than the 2-torsion baseline, so extra Selmer classes cannot "
                "be removed by a rank bound alone."
            ),
            "next_action": (
                "separate Sha[2] via Cassels-Tate pairing, second descent, or L-value route"
            ),
        }
    return {
        "decision": "joint_local_condition_at_T_tail",
        "reason": (
            "S~ does not force dimension 2; full-curve diagnostics show extra "
            "Selmer dimension but no proved rank-zero Sha[2] witness."
        ),
        "next_action": (
            "kill or account for the ell | T, ell == 1 mod 4 tail and the "
            "archimedean sign bit"
        ),
    }


def audit_rank_zero_aa_bb_pseudo_selmer_container(
    *,
    complete_two_descent_recast: dict[str, Any],
    diagnostic_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    violations: list[str] = []
    if not _ready(complete_two_descent_recast):
        violations.append("complete_two_descent_recast_not_ready")

    diagnostic_summary = _diagnostic_summary(diagnostic_rows)
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl457-wl464",
        "pattern": "AA+BB",
        "quantifier_audit": QUANTIFIER_AUDIT,
        "pseudo_selmer_container": PSEUDO_SELMER_CONTAINER,
        "dimension_bound": DIMENSION_BOUND,
        "diagnostic_summary": diagnostic_summary,
        "route_decision": _route_decision(diagnostic_summary),
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--complete-two-descent-recast", type=Path, required=True)
    parser.add_argument("--diagnostics-jsonl", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_aa_bb_pseudo_selmer_container(
        complete_two_descent_recast=load_json(args.complete_two_descent_recast),
        diagnostic_rows=load_jsonl(args.diagnostics_jsonl),
    )
    write_json(args.out, audit)
    print(f"wrote AA+BB pseudo-Selmer container audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"forces_dim_2={audit['dimension_bound']['forces_dim_2']}")
    print(f"route_decision={audit['route_decision']['decision']}")
    print(
        "selmer_rank_upper_bound_proved_count="
        f"{audit['selmer_rank_upper_bound_proved_count']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
