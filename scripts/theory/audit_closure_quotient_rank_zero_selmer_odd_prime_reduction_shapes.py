#!/usr/bin/env python3
"""Audit odd-prime reduced cubic shapes for rank-zero Selmer local lemmas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BOUNDARY = (
    "This audits symbolic mod-ell reduction shapes for the odd-prime "
    "rank-zero Selmer local lemma queue. It proves only the displayed reduced "
    "cubic factorization shapes; it does not compute local Selmer images, "
    "prove local conditions, prove a Selmer rank bound, or prove any "
    "lambda-family exclusion."
)

NEXT_LOCAL_GAP = (
    "derive the required isogeny-Selmer local squareclass image from this "
    "nodal reduction shape"
)

REDUCTION_SHAPES: dict[tuple[str, str], dict[str, Any]] = {
    ("kernel_minus_p", "odd-prime-divides-L"): {
        "mod_relation": "L == 0 mod ell",
        "reduced_a2": "-8*T^2",
        "reduced_a4": "16*T^4",
        "reduced_cubic_factorization": "x*(x - 4*T^2)^2",
        "double_root": "4*T^2",
        "simple_root": "0",
        "double_root_unit": True,
        "simple_root_unit": False,
        "nodal_reduction_shape": "split-nodal-cubic-with-nonzero-double-root",
    },
    ("kernel_minus_p", "odd-prime-divides-T"): {
        "mod_relation": "T == 0 mod ell",
        "reduced_a2": "32*L^2",
        "reduced_a4": "256*L^4",
        "reduced_cubic_factorization": "x*(x + 16*L^2)^2",
        "double_root": "-16*L^2",
        "simple_root": "0",
        "double_root_unit": True,
        "simple_root_unit": False,
        "nodal_reduction_shape": "split-nodal-cubic-with-nonzero-double-root",
    },
    ("kernel_minus_p", "odd-prime-divides-T2-plus-4L2"): {
        "mod_relation": "T^2 + 4*L^2 == 0 mod ell",
        "reduced_a2": "64*L^2",
        "reduced_a4": "0",
        "reduced_cubic_factorization": "x^2*(x + 64*L^2)",
        "double_root": "0",
        "simple_root": "-64*L^2",
        "double_root_unit": False,
        "simple_root_unit": True,
        "nodal_reduction_shape": "split-nodal-cubic-with-zero-double-root",
    },
    ("kernel_pos_2sqrt_q", "odd-prime-divides-L"): {
        "mod_relation": "L == 0 mod ell",
        "reduced_a2": "-8*T^2",
        "reduced_a4": "16*T^4",
        "reduced_cubic_factorization": "x*(x - 4*T^2)^2",
        "double_root": "4*T^2",
        "simple_root": "0",
        "double_root_unit": True,
        "simple_root_unit": False,
        "nodal_reduction_shape": "split-nodal-cubic-with-nonzero-double-root",
    },
    ("kernel_pos_2sqrt_q", "odd-prime-divides-T"): {
        "mod_relation": "T == 0 mod ell",
        "reduced_a2": "-64*L^2",
        "reduced_a4": "0",
        "reduced_cubic_factorization": "x^2*(x - 64*L^2)",
        "double_root": "0",
        "simple_root": "64*L^2",
        "double_root_unit": False,
        "simple_root_unit": True,
        "nodal_reduction_shape": "split-nodal-cubic-with-zero-double-root",
    },
    ("kernel_pos_2sqrt_q", "odd-prime-divides-T2-plus-4L2"): {
        "mod_relation": "T^2 + 4*L^2 == 0 mod ell",
        "reduced_a2": "-32*L^2",
        "reduced_a4": "256*L^4",
        "reduced_cubic_factorization": "x*(x - 16*L^2)^2",
        "double_root": "16*L^2",
        "simple_root": "0",
        "double_root_unit": True,
        "simple_root_unit": False,
        "nodal_reduction_shape": "split-nodal-cubic-with-nonzero-double-root",
    },
    ("kernel_neg_2sqrt_q", "odd-prime-divides-L"): {
        "mod_relation": "L == 0 mod ell",
        "reduced_a2": "16*T^2",
        "reduced_a4": "0",
        "reduced_cubic_factorization": "x^2*(x + 16*T^2)",
        "double_root": "0",
        "simple_root": "-16*T^2",
        "double_root_unit": False,
        "simple_root_unit": True,
        "nodal_reduction_shape": "split-nodal-cubic-with-zero-double-root",
    },
    ("kernel_neg_2sqrt_q", "odd-prime-divides-T"): {
        "mod_relation": "T == 0 mod ell",
        "reduced_a2": "32*L^2",
        "reduced_a4": "256*L^4",
        "reduced_cubic_factorization": "x*(x + 16*L^2)^2",
        "double_root": "-16*L^2",
        "simple_root": "0",
        "double_root_unit": True,
        "simple_root_unit": False,
        "nodal_reduction_shape": "split-nodal-cubic-with-nonzero-double-root",
    },
    ("kernel_neg_2sqrt_q", "odd-prime-divides-T2-plus-4L2"): {
        "mod_relation": "T^2 + 4*L^2 == 0 mod ell",
        "reduced_a2": "-32*L^2",
        "reduced_a4": "256*L^4",
        "reduced_cubic_factorization": "x*(x - 16*L^2)^2",
        "double_root": "16*L^2",
        "simple_root": "0",
        "double_root_unit": True,
        "simple_root_unit": False,
        "nodal_reduction_shape": "split-nodal-cubic-with-nonzero-double-root",
    },
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _ready(lemma_queue: dict[str, Any]) -> bool:
    return lemma_queue.get("status") == "ok" and lemma_queue.get("ready") is True


def _entry(row: dict[str, Any]) -> dict[str, Any]:
    kernel = str(row.get("kernel", ""))
    case_label = str(row.get("case_label", ""))
    shape = REDUCTION_SHAPES[(kernel, case_label)]
    return {
        "lemma_id": str(row.get("lemma_id", "")),
        "kernel": kernel,
        "case_label": case_label,
        "prime_condition": str(row.get("prime_condition", "")),
        **shape,
        "reduction_shape_proved": True,
        "local_condition_proved": False,
        "next_local_gap": NEXT_LOCAL_GAP,
    }


def audit_rank_zero_selmer_odd_prime_reduction_shapes(
    *,
    odd_prime_lemma_queue: dict[str, Any],
) -> dict[str, Any]:
    lemma_obligations = list(odd_prime_lemma_queue.get("lemma_obligations", []))
    violations: list[str] = []
    if not _ready(odd_prime_lemma_queue):
        violations.append("odd_prime_lemma_queue_not_ready")
    if odd_prime_lemma_queue.get("lemma_queue_not_proof") is not True:
        violations.append("lemma_queue_boundary_missing")
    if int(odd_prime_lemma_queue.get("local_condition_proved_count", 0) or 0) != 0:
        violations.append("local_condition_claim_count_nonzero")

    unknown_shapes = sorted(
        {
            (str(row.get("kernel", "")), str(row.get("case_label", "")))
            for row in lemma_obligations
            if (str(row.get("kernel", "")), str(row.get("case_label", "")))
            not in REDUCTION_SHAPES
        }
    )
    if unknown_shapes:
        violations.append(f"unknown_reduction_shapes={unknown_shapes}")

    reduction_entries = [
        _entry(row)
        for row in lemma_obligations
        if (str(row.get("kernel", "")), str(row.get("case_label", "")))
        in REDUCTION_SHAPES
    ]
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "input_lemma_obligation_count": len(lemma_obligations),
        "reduction_shape_count": len(reduction_entries),
        "reduction_shape_proved_count": len(reduction_entries),
        "reduction_shapes_not_local_conditions": True,
        "local_condition_proved_count": 0,
        "selmer_rank_upper_bound_proved_count": 0,
        "family_exclusion_proved_count": 0,
        "search_count_used_as_progress": False,
        "reduction_entries": reduction_entries,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--odd-prime-lemma-queue", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_rank_zero_selmer_odd_prime_reduction_shapes(
        odd_prime_lemma_queue=load_json(args.odd_prime_lemma_queue),
    )
    write_json(args.out, audit)
    print(f"wrote rank-zero Selmer odd-prime reduction-shape audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"input_lemma_obligation_count={audit['input_lemma_obligation_count']}")
    print(f"reduction_shape_count={audit['reduction_shape_count']}")
    print(f"reduction_shape_proved_count={audit['reduction_shape_proved_count']}")
    print(f"local_condition_proved_count={audit['local_condition_proved_count']}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
