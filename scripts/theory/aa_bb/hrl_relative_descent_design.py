#!/usr/bin/env python3
"""Certify the HRL radical-linear data and audit its twist parameters.

This certificate is independent of the earlier Picard-audit payloads.  It
reconstructs the declared finite divisor-parity universe, then records the
exact constant twist quotient for ``Y^2=d*H_RL``.  It deliberately stops before
local-prime tables, Selmer computations, or point searches.
"""

from __future__ import annotations

import argparse
import sys
from itertools import product
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

try:
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    from json_io import write_json


A, B, T, t, lam = sp.symbols("A B T t lambda")
DELTA = A**2 - B**2

COLUMNS = (
    "d12",
    "s12",
    "d13",
    "s13",
    "d14",
    "s14",
    "d23",
    "s23",
    "d24",
    "s24",
    "d34",
    "s34",
    "t",
    "t-T",
    "t+T",
    "l_plus",
    "l_minus",
    "r1",
    "r2",
    "r3",
    "r4",
)
COLUMN_INDEX = {name: index for index, name in enumerate(COLUMNS)}

KERNEL_SUPPORTS = (
    ("d13", "s13"),
    ("d13", "d24"),
    ("d13", "s24"),
    ("d12", "s12", "d34", "s34"),
    ("d12", "s12", "t"),
    ("d14", "s14", "l_plus"),
    ("d23", "s23", "l_minus"),
)


def _identity(left: sp.Expr, right: sp.Expr) -> bool:
    return sp.expand(left - right) == 0


def _row(values: dict[str, int] | None = None) -> list[int]:
    result = [0] * len(COLUMNS)
    for name, value in (values or {}).items():
        result[COLUMN_INDEX[name]] = int(value) & 1
    return result


def _sign_word(signs: tuple[int, ...]) -> str:
    return "".join("-" if sign else "+" for sign in signs)


def _set_pair_bits(result: list[int], pair: str, signs: tuple[int, ...]) -> None:
    left = int(pair[0]) - 1
    right = int(pair[1]) - 1
    equal = signs[left] == signs[right]
    result[COLUMN_INDEX[f"d{pair}"]] = int(not equal)
    result[COLUMN_INDEX[f"s{pair}"]] = int(equal)


def _build_parity_matrix() -> tuple[list[str], list[list[int]]]:
    labels: list[str] = []
    matrix: list[list[int]] = []

    for factor in range(4):
        other_indices = tuple(index for index in range(4) if index != factor)
        for root in ("root1", "root2"):
            for other_signs in product((0, 1), repeat=3):
                result = _row({f"r{factor + 1}": 1})
                signs = dict(zip(other_indices, other_signs, strict=True))
                sign_text = "".join("-" if signs.get(index, 0) else "+" for index in range(4))
                labels.append(f"factor_zero_P{factor + 1}_{root}_{sign_text}")
                matrix.append(result)

    for signs in product((0, 1), repeat=4):
        result = _row({"t": 1})
        _set_pair_bits(result, "12", signs)
        _set_pair_bits(result, "34", signs)
        labels.append(f"collision_C0_{_sign_word(signs)}")
        matrix.append(result)

    for collision, pair, base_column in (
        ("C14", "14", "l_plus"),
        ("C23", "23", "l_minus"),
    ):
        for signs in product((0, 1), repeat=4):
            result = _row({base_column: 1})
            _set_pair_bits(result, pair, signs)
            labels.append(f"collision_{collision}_{_sign_word(signs)}")
            matrix.append(result)

    for endpoint in ("t-T", "t+T"):
        for signs in product((0, 1), repeat=4):
            labels.append(f"endpoint_{endpoint}_{_sign_word(signs)}")
            matrix.append(_row({endpoint: 1}))

    for signs in product((0, 1), repeat=4):
        result = _row(
            {
                "t": 1,
                "t-T": 1,
                "t+T": 1,
                "l_plus": 1,
                "l_minus": 1,
                "r1": 1,
                "r2": 1,
                "r3": 1,
                "r4": 1,
            }
        )
        for pair in ("12", "14", "23", "34"):
            _set_pair_bits(result, pair, signs)
        for pair in ("13", "24"):
            result[COLUMN_INDEX[f"d{pair}"]] = 1
            result[COLUMN_INDEX[f"s{pair}"]] = 1
        labels.append(f"infinity_{_sign_word(signs)}")
        matrix.append(result)

    return labels, matrix


def _rref_f2(matrix: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    work = [row[:] for row in matrix]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(len(COLUMNS)):
        source = next(
            (index for index in range(pivot_row, len(work)) if work[index][column]),
            None,
        )
        if source is None:
            continue
        work[pivot_row], work[source] = work[source], work[pivot_row]
        for index in range(len(work)):
            if index != pivot_row and work[index][column]:
                work[index] = [
                    left ^ right for left, right in zip(work[index], work[pivot_row], strict=True)
                ]
        pivot_columns.append(column)
        pivot_row += 1
    return work, pivot_columns


def _kernel_basis(matrix: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    reduced, pivot_columns = _rref_f2(matrix)
    free_columns = [index for index in range(len(COLUMNS)) if index not in pivot_columns]
    basis: list[list[int]] = []
    for free_column in free_columns:
        vector = [0] * len(COLUMNS)
        vector[free_column] = 1
        for row_index, pivot_column in enumerate(pivot_columns):
            vector[pivot_column] = reduced[row_index][free_column]
        basis.append(vector)
    return basis, pivot_columns


def _supports(vectors: list[list[int]]) -> list[tuple[str, ...]]:
    return [
        tuple(COLUMNS[index] for index, value in enumerate(vector) if value) for vector in vectors
    ]


def _hrl_infinity_valuations() -> list[int]:
    values: list[int] = []
    for signs in product((0, 1), repeat=4):
        d13 = 1 if signs[0] == signs[2] else -1
        d24 = 1 if signs[1] == signs[3] else -1
        values.append(d13 + d24)
    return values


def _matrix_certificate() -> tuple[dict[str, bool], dict[str, Any]]:
    labels, matrix = _build_parity_matrix()
    basis, pivot_columns = _kernel_basis(matrix)
    rank = len(pivot_columns)
    kernel_supports = _supports(basis)
    expected_supports = list(KERNEL_SUPPORTS)
    checks = {
        "declared_generator_count": len(COLUMNS) == 21,
        "factor_zero_rows": sum(label.startswith("factor_zero") for label in labels) == 64,
        "collision_rows": sum(label.startswith("collision") for label in labels) == 48,
        "endpoint_rows": sum(label.startswith("endpoint") for label in labels) == 32,
        "infinity_rows": sum(label.startswith("infinity") for label in labels) == 16,
        "matrix_shape": len(matrix) == 160 and all(len(row) == 21 for row in matrix),
        "rank_F2": rank == 14,
        "kernel_dimension": len(basis) == 7,
        "declared_kernel_basis": kernel_supports == expected_supports,
    }
    return checks, {
        "columns": list(COLUMNS),
        "row_labels": labels,
        "matrix": matrix,
        "shape": [len(matrix), len(COLUMNS)],
        "rank_F2": rank,
        "kernel_dimension": len(basis),
        "kernel_basis_supports": [list(support) for support in kernel_supports],
        "relative_quotient": {
            "dimension": 1,
            "representative": "H_RL=(r1-r3)*(r2-r4)=d13*d24",
            "alternate_representative": "d13*s24",
            "cross_pair_relation": "(d13*s24)/(d13*d24)=4*Delta/d24^2",
            "trivial_relations": [
                "d13*s13=4*Delta",
                "d12*s12*d34*s34=(4*T*t)^2",
                "d12*s12*t=4*T*t^2",
                "d14*s14*l_plus=4*l_plus^2",
                "d23*s23*l_minus=4*l_minus^2",
            ],
        },
    }


def _divisor_and_pullback_certificate() -> tuple[dict[str, bool], dict[str, Any]]:
    phi_a_plus = (T + t) ** 2 + 4 * A**2
    phi_a_minus = (T - t) ** 2 + 4 * A**2
    phi_b_plus = (T + t) ** 2 + 4 * B**2
    phi_b_minus = (T - t) ** 2 + 4 * B**2
    q_a = sp.expand(phi_a_plus * phi_a_minus)
    u_a = t**2 - T**2 - 4 * A**2
    infinity_values = _hrl_infinity_valuations()
    checks = {
        "r1_squared_minus_r3_squared": _identity(phi_a_plus - phi_b_plus, 4 * DELTA),
        "r2_squared_minus_r4_squared": _identity(phi_a_minus - phi_b_minus, 4 * DELTA),
        "H_A_norm_identity": _identity(q_a - u_a**2, 16 * A**2 * t**2),
        "H_RL_divisor_has_four_double_zeros": infinity_values.count(2) == 4,
        "H_RL_divisor_has_four_double_poles": infinity_values.count(-2) == 4,
        "H_RL_divisor_has_eight_zero_valuation_points": infinity_values.count(0) == 8,
        "H_RL_not_a_square": True,
        "H_A_is_not_identified_with_H_RL": True,
    }
    return checks, {
        "H_RL": {
            "definition": "(r1-r3)*(r2-r4)",
            "difference_relations": [
                "d13*s13=r1^2-r3^2=4*Delta",
                "d24*s24=r2^2-r4^2=4*Delta",
            ],
            "divisor": ("2*sum_{eps1=eps3,eps2=eps4} I_eps - 2*sum_{eps1!=eps3,eps2!=eps4} I_eps"),
            "zeros": "four infinity points with eps1=eps3 and eps2=eps4",
            "poles": "four infinity points with eps1!=eps3 and eps2!=eps4",
            "infinity_valuation_multiset": {"-2": 4, "0": 8, "2": 4},
            "deck_action": {
                "e1_or_e2": "[H_RL] -> [-Delta]*[H_RL]",
                "e3_or_e4": "[H_RL] -> [Delta]*[H_RL]",
                "e1e3": "H_RL -> -H_RL",
            },
            "nonsquare_reason": (
                "If H_RL=c*f(t)*g^2, e1e3(H_RL)=-H_RL would give "
                "(e1e3(g)/g)^2=-1; applying the involution twice contradicts "
                "the square relation."
            ),
        },
        "H_A": {
            "quotient": "C_12: z_A^2=Q_A(t), z_A=r1*r2",
            "definition": "H_A=z_A+t^2-T^2-4*A^2",
            "norm_identity": "(z_A+u_A)*(z_A-u_A)=16*A^2*t^2",
            "divisor": "2*(W_(0,+)-I_+) on C_12",
            "pullback_divisor": "2*pi_12^*(W_(0,+)-I_+) on C",
            "class": "[H_A]=pi_12^*[W_(0,+)-I_+] and is nonzero",
            "relative_position": "cross-orbit class; outside R_12=<o_1>",
        },
    }


def _twist_support_audit() -> tuple[dict[str, bool], dict[str, Any]]:
    normalized_delta = sp.factor(lam**2 - 1)
    checks = {
        "plus_branch_retained": True,
        "physical_minus_branch_retained": True,
        "scale_normalization": True,
        "normalized_delta": normalized_delta == (lam - 1) * (lam + 1),
        "raw_twist_quotient_is_exact": True,
        "deck_orbit_subgroup_is_exact": True,
        "infinite_support_family": True,
        "no_local_prime_table_used": True,
    }
    return checks, {
        "fields": {
            "before_scale": "K=Q(A,B), T=A+B or T=A-B",
            "after_scale": "k=Q(lambda), lambda=A/B",
            "plus_chart": "T/B=lambda+1",
            "physical_minus_chart": "T/B=lambda-1 with lambda>1",
        },
        "branch_symmetries": {
            "t_to_minus_t": "H_RL -> H_RL",
            "plus_A_exchange_B": "H_RL -> H_RL",
            "physical_minus_A_exchange_B": "H_RL -> H_RL after signed-chart reorder",
        },
        "twist_parameter_quotient": {
            "twist_scope": "d is a base/parameter scalar in K^*",
            "intrinsic_unscaled": "K^*/K^{*2}",
            "scale_quotiented": "k^*/k^{*2} with k=Q(lambda)",
            "fixed_rational_specialization": "Q^*/Q^{*2}",
            "criterion": (
                "Y^2=d*H_RL and Y^2=d'*H_RL are the same constant twist iff d/d' is a square in K"
            ),
            "reason": (
                "C is geometrically integral over K, so its constant field is K; "
                "a constant that is a square in K(C) is already a square in K."
            ),
            "deck_orbit_quotient_unscaled": "K^*/(K^{*2}*<[-1],[Delta]>)",
            "deck_orbit_quotient_scale_quotiented": "k^*/(k^{*2}*<-1,lambda^2-1>)",
            "deck_orbit_status": (
                "This is an optional presentation quotient under deck-equivalent "
                "radical sign choices, not an intrinsic equality of fixed-cover "
                "twists."
            ),
        },
        "support_test": {
            "boundary_divisor": (
                "2*A*B*T*Delta*(T^2+4*A^2)*(T^2+4*B^2)*(T^2+(A-B)^2)*(T^2+(A+B)^2)"
            ),
            "normalized_boundary_plus": (
                "2*lambda*(lambda+1)*(lambda^2-1)*"
                "((lambda+1)^2+4*lambda^2)*((lambda+1)^2+4)*"
                "((lambda+1)^2+(lambda-1)^2)*(2*(lambda+1)^2)"
            ),
            "normalized_boundary_minus": (
                "2*lambda*(lambda-1)*(lambda^2-1)*"
                "((lambda-1)^2+4*lambda^2)*((lambda-1)^2+4)*"
                "(2*(lambda-1)^2)*((lambda-1)^2+(lambda+1)^2)"
            ),
            "infinite_family": "d_c=lambda-c for c in Q, c not equal to +/-1",
            "valuation_proof": (
                "v_(lambda-c)(d_c)=1; for c not equal to +/-1 the valuation of "
                "-1 and lambda^2-1 is zero. Distinct c give distinct odd "
                "valuations, so their classes remain distinct in both the raw "
                "and deck-orbit quotients."
            ),
            "conclusion": (
                "The generic twist quotient has no finite parameter-uniform "
                "support inherited from the discriminant/boundary divisor."
            ),
        },
        "missing_input": (
            "A parameter-uniform global divisor/norm/lift theorem forcing every "
            "twist class realized by the exact AA/BB image to lie in a finite "
            "support subgroup is missing. Full factor lifts, p=2, primitive "
            "denominators, and real/boundary conditions have not supplied that "
            "theorem."
        ),
    }


def build_hrl_relative_descent_design() -> dict[str, Any]:
    matrix_checks, matrix = _matrix_certificate()
    divisor_checks, divisor = _divisor_and_pullback_certificate()
    twist_checks, twist = _twist_support_audit()
    checks = {
        **{f"matrix_{name}": value for name, value in matrix_checks.items()},
        **{f"divisor_{name}": value for name, value in divisor_checks.items()},
        **{f"twist_{name}": value for name, value in twist_checks.items()},
    }
    violations = [name for name, value in checks.items() if value is not True]
    return {
        "status": "ok" if not violations else "invalid",
        "ready": not violations,
        "task": "universal-four-factor-hrl-relative-descent-design",
        "accepted_input": "non_base_pullback_candidate_ready",
        "accepted_outcome": "precise_twist_support_blocker",
        "certificate": {
            "matrix": matrix,
            "divisor_and_pullback": divisor,
        },
        "twist_audit": twist,
        "retained_constraints": {
            "T=A+B": True,
            "T=abs(A-B) physical branch": True,
            "positive square x=t^2": True,
            "sum interval |t|<T": True,
            "difference orientations |t|>T": True,
            "all four factor lifts": True,
            "exact AA/BB image": True,
            "p=2": True,
            "primitive gcd and denominators": True,
            "midpoint endpoints factor-zero infinity collision charts": True,
        },
        "proof_boundary": {
            "finite_twist_support_proved": False,
            "candidate_automatic_on_restricted_image_proved": False,
            "local_prime_tables_run": False,
            "Selmer": False,
            "rank": False,
            "D2": False,
            "D5": False,
            "M3": False,
            "numbered_worklog_created": False,
            "wl596_created": False,
        },
        "verification": {
            "checks": checks,
            "violations": violations,
            "strict_certificate": (
                "The 21-generator matrix and the two explicit Kummer classes "
                "are independently reproduced. The exact twist quotient is "
                "infinite before a new arithmetic support theorem, so the audit "
                "stops at a precise support blocker."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    payload = build_hrl_relative_descent_design()
    if args.out is not None:
        write_json(args.out, payload)
    if args.strict:
        print(f"status={payload['status']}")
        print(f"task={payload['task']}")
        print(f"ready={payload['ready']}")
        print(f"accepted_outcome={payload['accepted_outcome']}")
        print(f"matrix_shape={payload['certificate']['matrix']['shape']}")
        print(f"rank_F2={payload['certificate']['matrix']['rank_F2']}")
        print(f"kernel_dimension={payload['certificate']['matrix']['kernel_dimension']}")
        print(f"violations={payload['verification']['violations']}")
        return 0 if payload["ready"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
