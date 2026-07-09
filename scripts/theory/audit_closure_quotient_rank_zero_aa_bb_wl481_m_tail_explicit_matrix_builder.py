#!/usr/bin/env python3
"""Build explicit sampled M_tail matrices for the AA+BB complete d-route."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]

BOUNDARY = (
    "This audits only wl481 / M_tail_explicit_matrix_builder for the AA+BB "
    "complete d-coordinate route. It takes wl480 as input and makes the "
    "parameter-dependent F2 matrix M_tail explicit on deterministic primitive "
    "AA+BB samples. Odd rows use computable Legendre characters and dyadic "
    "rows use computable Q_2 squareclass characters from wl478. This is a "
    "finite sampled matrix diagnostic, not a proof of uniform full rank, not "
    "a complete Sel_2(E) upper bound, not dim Sel_2(E)=2, not rank zero, not "
    "Sha[2]=0, and not any family exclusion."
)

DEFAULT_SAMPLES = [
    ("AA", 3, 1),
    ("AA", 5, 1),
    ("AA", 1, 2),
    ("BB", 2, 1),
    ("BB", 5, 2),
]


def _v2(n: int) -> int:
    n = abs(n)
    if n == 0:
        raise ValueError("zero has no finite v2")
    out = 0
    while n % 2 == 0:
        out += 1
        n //= 2
    return out


def _prime_factors(n: int) -> list[int]:
    n = abs(n)
    factors: list[int] = []
    if n % 2 == 0:
        factors.append(2)
        while n % 2 == 0:
            n //= 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            while n % divisor == 0:
                n //= divisor
        divisor += 2
    if n > 1:
        factors.append(n)
    return factors


def _odd_prime_factors(n: int) -> list[int]:
    return [prime for prime in _prime_factors(n) if prime != 2]


def _legendre_bit(n: int, prime: int) -> int:
    residue = n % prime
    if residue == 0:
        return 0
    value = pow(residue, (prime - 1) // 2, prime)
    if value == 1:
        return 0
    if value == prime - 1:
        return 1
    raise ValueError(f"unexpected Legendre value {value} modulo {prime}")


def _q2_squareclass_bits(n: int) -> dict[str, int]:
    if n == 0:
        raise ValueError("zero has no Q_2 squareclass")
    valuation = _v2(n)
    unit = abs(n) >> valuation
    if n < 0:
        unit = -unit
    residue = unit % 8
    return {
        "sign": 1 if residue in {3, 7} else 0,
        "ramified_2": valuation % 2,
        "five": 1 if residue in {3, 5} else 0,
    }


def _generator(kind: str, prime: int) -> dict[str, Any]:
    if kind == "u":
        pattern = [prime, prime, 1]
        family = f"u_{prime}"
        source = "odd prime dividing L"
    elif kind == "v":
        pattern = [prime, 1, prime]
        family = f"v_{prime}"
        source = "odd prime dividing T"
    elif kind == "w":
        pattern = [1, prime, prime]
        family = f"w_{prime}"
        source = "odd prime dividing sqrt_q"
    elif kind == "w2":
        pattern = [1, 2, 2]
        family = "w_2"
        source = "balanced dyadic generator"
    else:
        raise ValueError(f"unknown generator kind {kind}")
    return {
        "id": family,
        "kind": kind,
        "prime": prime,
        "coordinate_pattern": pattern,
        "coordinate_order": COORDINATE_ORDER,
        "source": source,
    }


def _raw_generators(
    *, odd_L: list[int], odd_T: list[int], odd_sqrt_q: list[int], epsilon: int
) -> list[dict[str, Any]]:
    columns = [_generator("u", prime) for prime in odd_L]
    columns.extend(_generator("v", prime) for prime in odd_T)
    columns.extend(_generator("w", prime) for prime in odd_sqrt_q)
    if epsilon:
        columns.append(_generator("w2", 2))
    return columns


def _omitted_baseline_pivot(raw_columns: list[dict[str, Any]]) -> str | None:
    for column in raw_columns:
        if column["id"] == "w_2":
            return "w_2"
    sqrt_columns = [column["id"] for column in raw_columns if column["kind"] == "w"]
    if sqrt_columns:
        return sqrt_columns[-1]
    return None


def _odd_row_entry(row_kind: str, active_prime: int, column: dict[str, Any]) -> int:
    kind = column["kind"]
    prime = int(column["prime"])
    if row_kind == "L":
        if kind == "u":
            return 0
        return _legendre_bit(prime, active_prime)
    if row_kind == "T":
        if kind == "v":
            return 0
        return _legendre_bit(prime, active_prime)
    if row_kind == "sqrt_q":
        if kind in {"w", "w2"}:
            return 0
        return _legendre_bit(prime, active_prime)
    raise ValueError(f"unknown odd row kind {row_kind}")


def _odd_row(
    *,
    row_kind: str,
    active_prime: int,
    columns: list[dict[str, Any]],
) -> dict[str, Any]:
    if row_kind == "L":
        equation = "local class(d_minus_p)=local class(d_pos_2sqrt_q)"
        row_id = f"odd_L_{active_prime}_equal_d_minus_p_d_pos_2sqrt_q"
        source = "wl475 pure odd ell|L row"
    elif row_kind == "T":
        equation = "local class(d_minus_p)=local class(d_neg_2sqrt_q)"
        row_id = f"odd_T_{active_prime}_equal_d_minus_p_d_neg_2sqrt_q"
        source = "wl476 pure odd ell|T row"
    elif row_kind == "sqrt_q":
        equation = "local class(d_pos_2sqrt_q)=local class(d_neg_2sqrt_q)"
        row_id = f"odd_sqrt_q_{active_prime}_equal_d_pos_2sqrt_q_d_neg_2sqrt_q"
        source = "wl477 pure odd ell|sqrt_q row"
    else:
        raise ValueError(f"unknown odd row kind {row_kind}")
    return {
        "id": row_id,
        "source": source,
        "active_prime": active_prime,
        "equation": equation,
        "character_type": "computable Legendre character at an odd finite prime",
        "entries": [
            _odd_row_entry(row_kind, active_prime, column) for column in columns
        ],
    }


def _dyadic_rows(*, balanced: bool, columns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if balanced:
        return [
            {
                "id": "dyadic_balanced_d_minus_p_five_character",
                "source": "wl478 balanced odd-sqrt_q Q_2 row",
                "equation": "d_minus_p has no 5-character in Q_2*/Q_2*2",
                "character_type": "computable Q_2 squareclass character",
                "entries": [
                    _q2_squareclass_bits(column["coordinate_pattern"][0])["five"]
                    for column in columns
                ],
            },
            {
                "id": "dyadic_balanced_d_neg_2sqrt_q_sign_character",
                "source": "wl478 balanced odd-sqrt_q Q_2 row",
                "equation": "d_neg_2sqrt_q has no sign character in Q_2*/Q_2*2",
                "character_type": "computable Q_2 squareclass character",
                "entries": [
                    _q2_squareclass_bits(column["coordinate_pattern"][2])["sign"]
                    for column in columns
                ],
            },
        ]
    return [
        {
            "id": "dyadic_ordinary_d_neg_2sqrt_q_sign_character",
            "source": "wl478 ordinary even-sqrt_q Q_2 row",
            "equation": "d_neg_2sqrt_q lies in {1,5} in Q_2*/Q_2*2",
            "character_type": "computable Q_2 squareclass character",
            "entries": [
                _q2_squareclass_bits(column["coordinate_pattern"][2])["sign"]
                for column in columns
            ],
        }
    ]


def _f2_rank(matrix: list[list[int]], column_count: int) -> int:
    rows = [
        sum((entry & 1) << index for index, entry in enumerate(row))
        for row in matrix
    ]
    rank = 0
    pivot_bit = column_count - 1
    for bit in range(pivot_bit, -1, -1):
        pivot_index = next(
            (index for index, row in enumerate(rows[rank:], start=rank) if (row >> bit) & 1),
            None,
        )
        if pivot_index is None:
            continue
        rows[rank], rows[pivot_index] = rows[pivot_index], rows[rank]
        for index, row in enumerate(rows):
            if index != rank and ((row >> bit) & 1):
                rows[index] ^= rows[rank]
        rank += 1
    return rank


def _kernel_basis(matrix: list[list[int]], column_count: int) -> list[list[int]]:
    if column_count == 0:
        return []
    rows = [
        sum((entry & 1) << index for index, entry in enumerate(row))
        for row in matrix
        if any(entry & 1 for entry in row)
    ]
    pivot_columns: list[int] = []
    rank = 0
    for bit in range(column_count - 1, -1, -1):
        pivot_index = next(
            (index for index, row in enumerate(rows[rank:], start=rank) if (row >> bit) & 1),
            None,
        )
        if pivot_index is None:
            continue
        rows[rank], rows[pivot_index] = rows[pivot_index], rows[rank]
        for index, row in enumerate(rows):
            if index != rank and ((row >> bit) & 1):
                rows[index] ^= rows[rank]
        pivot_columns.append(bit)
        rank += 1
    pivot_set = set(pivot_columns)
    basis: list[list[int]] = []
    for free_column in range(column_count):
        if free_column in pivot_set:
            continue
        vector = 1 << free_column
        for row, pivot_column in zip(rows[:rank], pivot_columns, strict=True):
            if (row >> free_column) & 1:
                vector |= 1 << pivot_column
        basis.append([(vector >> index) & 1 for index in range(column_count)])
    return basis


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        payload.get("complete_selmer_upper_bound_proved") is True
        or payload.get("dim_sel2_eq_2_claimed") is True
        or payload.get("rank_zero_claimed") is True
        or payload.get("sha2_trivial_claimed") is True
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def build_sample_m_tail_matrix(*, side: str, A: int, B: int) -> dict[str, Any]:
    if side not in {"AA", "BB"}:
        raise ValueError("side must be AA or BB")
    primitive = math.gcd(A, B) == 1
    L = A if side == "AA" else B
    T = A + B
    sqrt_q = T * T + 4 * L * L
    odd_L = _odd_prime_factors(L)
    odd_T = _odd_prime_factors(T)
    odd_sqrt_q = _odd_prime_factors(sqrt_q)
    epsilon = 1 if _v2(T) == _v2(L) + 1 else 0

    raw_columns = _raw_generators(
        odd_L=odd_L,
        odd_T=odd_T,
        odd_sqrt_q=odd_sqrt_q,
        epsilon=epsilon,
    )
    omitted = _omitted_baseline_pivot(raw_columns)
    columns = [column for column in raw_columns if column["id"] != omitted]

    rows: list[dict[str, Any]] = []
    rows.extend(_odd_row(row_kind="L", active_prime=prime, columns=columns) for prime in odd_L)
    rows.extend(_odd_row(row_kind="T", active_prime=prime, columns=columns) for prime in odd_T)
    rows.extend(
        _odd_row(row_kind="sqrt_q", active_prime=prime, columns=columns)
        for prime in odd_sqrt_q
    )
    rows.extend(_dyadic_rows(balanced=bool(epsilon), columns=columns))

    matrix = [row["entries"] for row in rows]
    rank_needed = max(len(raw_columns) - 1, 0)
    computed_rank = _f2_rank(matrix, len(columns))
    kernel = _kernel_basis(matrix, len(columns))
    column_ids = [column["id"] for column in columns]
    kernel_supports = [
        [column_id for column_id, bit in zip(column_ids, vector, strict=True) if bit]
        for vector in kernel
    ]

    return {
        "sample": {
            "side": side,
            "A": A,
            "B": B,
            "L": L,
            "T": T,
            "sqrt_q": sqrt_q,
            "primitive": primitive,
        },
        "coordinate_order": COORDINATE_ORDER,
        "support_counts": {
            "omega_L": len(odd_L),
            "omega_T": len(odd_T),
            "omega_sqrt_q": len(odd_sqrt_q),
            "epsilon_balanced_2": epsilon,
        },
        "torsion_quotient": {
            "baseline_generator": (
                "tau_sqrt_q=product_{ell|sqrt_q} w_ell times w_2 when "
                "v2(sqrt_q) is odd"
            ),
            "omitted_baseline_pivot_column": omitted,
            "quotient_basis_rule": (
                "columns are row-ledger generators after omitting one "
                "tau_sqrt_q pivot; tau_minus is already removed"
            ),
        },
        "columns": columns,
        "rows": rows,
        "matrix": matrix,
        "rank_needed": rank_needed,
        "computed_rank": computed_rank,
        "computed_rank_status": (
            "full_for_this_finite_sample"
            if computed_rank >= rank_needed
            else "kernel_found_for_this_finite_sample"
        ),
        "symbolic_rank_status": "not_proved_uniformly_by_wl481",
        "kernel_diagnostics": {
            "kernel_dimension": len(columns) - computed_rank,
            "basis_vectors": kernel,
            "basis_supports": kernel_supports,
        },
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def _wl480_ready(wl480: dict[str, Any]) -> bool:
    return (
        wl480.get("status") == "ok"
        and wl480.get("ready") is True
        and wl480.get("lemma_id") == "D4_AA_BB_uniform_matrix_rank_bound_audit"
        and wl480.get("work_log") == "wl480"
        and wl480.get("complete_d_coordinate_order") == COORDINATE_ORDER
        and wl480.get("local_character_matrix", {}).get("id") == "M_tail"
        and wl480.get("old_package_x_coordinate_collapse_used") is False
        and not _claims_forbidden_bound(wl480)
    )


def build_wl481_m_tail_audit(
    *,
    wl480: dict[str, Any],
    samples: list[tuple[str, int, int]] | None = None,
) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl480_ready(wl480):
        violations.append("wl480_input_not_ready_or_not_scoped")

    sample_payloads = [
        build_sample_m_tail_matrix(side=side, A=A, B=B)
        for side, A, B in (samples or DEFAULT_SAMPLES)
    ]
    full_rank_count = sum(
        sample["computed_rank_status"] == "full_for_this_finite_sample"
        for sample in sample_payloads
    )
    kernel_count = len(sample_payloads) - full_rank_count
    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl480 plus solved rows wl475-wl479",
        "pattern": "AA+BB",
        "lemma_id": "WL481_M_tail_explicit_matrix_builder",
        "work_log": "wl481",
        "input_work_log": "wl480",
        "matrix_object": {
            "id": "M_tail",
            "object_scope": (
                "complete d-coordinate tail matrix for E_L: "
                "Y^2=(X+p)*(X^2-4*q)"
            ),
            "old_package_x_s_tilde_bridge_used": False,
            "entry_types": [
                "computable Legendre characters at odd finite primes",
                "computable Q_2 squareclass characters from wl478",
                "symbolic Legendre/Hilbert placeholders remain for the unsolved uniform theorem",
            ],
        },
        "column_definition": {
            "raw_generators": [
                "u_ell=(ell,ell,1) for odd ell|L",
                "v_ell=(ell,1,ell) for odd ell|T",
                "w_ell=(1,ell,ell) for odd ell|sqrt_q",
                "w_2=(1,2,2) in the balanced dyadic stratum",
            ],
            "tail_quotient": (
                "remove tau_minus and quotient by tau_sqrt_q by omitting one "
                "sqrt_q/dyadic pivot column"
            ),
        },
        "row_definition": {
            "odd_L": "entries are chi_ell(d_minus_p/d_pos_2sqrt_q)",
            "odd_T": "entries are chi_ell(d_minus_p/d_neg_2sqrt_q)",
            "odd_sqrt_q": "entries are chi_ell(d_pos_2sqrt_q/d_neg_2sqrt_q)",
            "dyadic": "entries are Q_2 squareclass characters cutting out the wl478 stratum row",
        },
        "sample_matrices": sample_payloads,
        "sample_summary": {
            "sample_count": len(sample_payloads),
            "full_rank_sample_count": full_rank_count,
            "kernel_sample_count": kernel_count,
            "sampled_computation_is_not_uniform_proof": True,
        },
        "symbolic_rank_status": "uniform_full_rank_not_proved",
        "computed_rank_status": "finite_samples_computed_only",
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "search_count_used_as_progress": False,
        "next_obstruction": "prove_uniform_full_rank_for_explicit_M_tail_or_classify_kernel",
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl480", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl481_m_tail_audit(wl480=load_json(args.wl480))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl481 M_tail explicit matrix audit to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"symbolic_rank_status={audit['symbolic_rank_status']}")
    print(
        "complete_selmer_upper_bound_proved="
        f"{audit['complete_selmer_upper_bound_proved']}"
    )
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
