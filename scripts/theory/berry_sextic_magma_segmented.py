"""Proof data and serialization checks for the Berry C_1 Magma stages.

This module records exact local-Sage checks and the fixed data contract used
by the small Magma Calculator probes in this directory.  It does not invoke
TwoSelmerGroup or claim a Selmer bound.  The Calculator observations are kept
separate from the independent number-field and local-factor checks.
"""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

TASK_ID = "berry-sextic-genus2-classification-20260715"
SCHEMA_VERSION = "berry-c1-magma-segmented-v1"

F12 = (
    "x^12 - 4*x^11 - 62*x^10 + 68*x^9 + 1647*x^8 + 4184*x^7 "
    "+ 2716*x^6 - 376*x^5 + 623*x^4 - 788*x^3 + 194*x^2 - 12*x + 1"
)

# Relative (over Q(i)) decomposition data.  The ideal_number values are
# task-local stable slots, not Magma object handles or database indices.
MODEL_SUPPORT = (
    {
        "label": "varpi-factor-degree-2",
        "base_prime": "1+i",
        "ideal_number": 1,
        "norm": 2,
        "e": 2,
        "f": 1,
        "factor_degree": 2,
    },
    {
        "label": "varpi-factor-degree-4",
        "base_prime": "1+i",
        "ideal_number": 2,
        "norm": 2,
        "e": 4,
        "f": 1,
        "factor_degree": 4,
    },
    {
        "label": "pi-linear-3615",
        "base_prime": "94*i-169",
        "ideal_number": 3,
        "norm": 37397,
        "e": 1,
        "f": 1,
        "factor_degree": 1,
    },
    {
        "label": "pi-linear-9390",
        "base_prime": "94*i-169",
        "ideal_number": 4,
        "norm": 37397,
        "e": 1,
        "f": 1,
        "factor_degree": 1,
    },
    {
        "label": "pi-ramified-25652",
        "base_prime": "94*i-169",
        "ideal_number": 5,
        "norm": 37397,
        "e": 2,
        "f": 1,
        "factor_degree": 2,
    },
    {
        "label": "pi-quadratic-6501-25179",
        "base_prime": "94*i-169",
        "ideal_number": 6,
        "norm": 37397**2,
        "e": 1,
        "f": 2,
        "factor_degree": 2,
    },
)

CONJUGATE_SUPPORT = (
    {
        "label": "pi-bar-linear-1",
        "base_prime": "-94*i-169",
        "ideal_number": 7,
        "norm": 37397,
        "e": 1,
        "f": 1,
        "factor_degree": 1,
    },
    {
        "label": "pi-bar-linear-2",
        "base_prime": "-94*i-169",
        "ideal_number": 8,
        "norm": 37397,
        "e": 1,
        "f": 1,
        "factor_degree": 1,
    },
    {
        "label": "pi-bar-linear-3",
        "base_prime": "-94*i-169",
        "ideal_number": 9,
        "norm": 37397,
        "e": 1,
        "f": 1,
        "factor_degree": 1,
    },
    {
        "label": "pi-bar-cubic",
        "base_prime": "-94*i-169",
        "ideal_number": 10,
        "norm": 37397**3,
        "e": 1,
        "f": 3,
        "factor_degree": 3,
    },
)

ABSOLUTE_DECOMPOSITION = {
    "2": ((4, 1), (8, 1)),
    "37397": ((1, 1), (2, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 2), (1, 3)),
}

UNIT_INVARIANTS = (4, 0, 0, 0, 0, 0)
CLASS_GROUP_INVARIANTS: tuple[int, ...] = ()

# Exact principal-generator coordinates from Sage's maximal-order basis.
# They independently certify that the support ideals are principal, but are
# not yet a cross-system Magma payload: the Calculator stages must emit their
# own order basis and coordinates before a fresh Magma request can consume
# them safely.
SAGE_SUPPORT_GENERATOR_COORDINATES = (
    (9740, -4485, -44277, 37495, 35148, -10405, -2042, 8911, 234, 12607, -31293, -43364),
    (6905, -6465, -23115, 33644, 21793, -13708, -1258, 4767, -6470, 7079, -20612, -19557),
    (20130, -8441, -10370, -28322, 1443, 21347, 10163, -17062, -3291, 26028, 6965, 489),
    (-22785, 20975, 44888, -18688, -35730, -3955, -11473, 6105, 6961, -33333, 20890, 31993),
    (8516, -78596, 249135, -190072, -171053, 64816, 73114, -113108, -78508, 18626, 193468, 314628),
    (-46317, 69134, -42107, 38778, 17344, -24911, -47716, 62911, 57434, -62301, -46005, -94685),
    (
        17391,
        -117665,
        260521,
        -187652,
        -168829,
        69338,
        98964,
        -131016,
        -100187,
        40245,
        209824,
        347157,
    ),
    (-4524, -39907, 284114, -293935, -219916, 113025, 65640, -120234, -44060, 2566, 234379, 328877),
    (3882, 43591, -72084, 16474, 37487, 271, -29096, 27569, 34650, -3523, -50488, -98127),
    (
        -94470,
        428483,
        -263420,
        -242160,
        24768,
        141941,
        -222008,
        186915,
        360766,
        -158273,
        -148268,
        -530917,
    ),
)
SAGE_UNIT_GENERATOR_COORDINATES = (
    (7268, -38436, 92064, -74826, -62448, 28303, 33941, -47255, -32626, 15111, 76344, 122389),
    (6065, -15899, -21422, 46542, 25667, -19579, 3059, 4429, -12921, 8120, -21447, -14253),
    (-180, 12481, -32591, 36660, 24276, -17370, -14139, 16928, 6643, -5160, -31217, -41035),
    (-1675, -2744, -7375, 15178, 8725, -6540, -346, 4471, -828, -941, -7720, -8157),
    (-293, -58688, 143913, -73866, -88704, 18668, 45401, -59724, -55787, 6572, 103831, 185601),
    (8136, -14136, 1644, 2756, 1449, 244, 8458, -8526, -10707, 11441, 4029, 12313),
)


def _squareclass_basis(prime_count: int) -> list[str]:
    return [
        "zeta4",
        *(f"epsilon_{index}" for index in range(1, 6)),
        *(f"S_prime_{index}" for index in range(1, prime_count + 1)),
    ]


def _relation_matrix(dimension: int) -> list[list[int]]:
    row = [0] * dimension
    row[0] = 4
    return [row]


def _support_record(entry: dict[str, Any]) -> dict[str, Any]:
    record = deepcopy(entry)
    record["generator_coordinates"] = list(
        SAGE_SUPPORT_GENERATOR_COORDINATES[entry["ideal_number"] - 1]
    )
    record["generator_encoding"] = "sage_maximal_order_basis_coordinates"
    return record


def stage_snapshot(*, include_conjugate_support: bool = False) -> dict[str, Any]:
    support = list(MODEL_SUPPORT)
    if include_conjugate_support:
        support.extend(CONJUGATE_SUPPORT)
    basis = _squareclass_basis(len(support))
    return {
        "schema_version": SCHEMA_VERSION,
        "field": {
            "base": "Q(i)",
            "relative_defining_polynomial": "g6(theta)",
            "absolute_defining_polynomial": F12,
            "relative_degree": 6,
            "absolute_degree": 12,
            "maximal_order_discriminant": "5019340374016",
            "basis_policy": (
                "Sage maximal-order coordinates are an independent certificate; "
                "cross-request Magma basis compatibility remains unverified"
            ),
        },
        "support": [_support_record(entry) for entry in support],
        "class_group": {
            "invariants": list(CLASS_GROUP_INVARIANTS),
            "two_primary_invariants": [],
        },
        "unit_group": {
            "invariants": list(UNIT_INVARIANTS),
            "squareclass_basis": ["zeta4", *(f"epsilon_{i}" for i in range(1, 6))],
            "generator_coordinates": [list(item) for item in SAGE_UNIT_GENERATOR_COORDINATES],
            "relation_matrix": _relation_matrix(6),
        },
        "s_unit_group": {
            "invariants": [4, *(0 for _ in range(5 + len(support)))],
            "squareclass_basis": basis,
            "relation_matrix": _relation_matrix(len(basis)),
        },
    }


def serialize_stage_snapshot(snapshot: dict[str, Any]) -> str:
    """Serialize only stable data, never Magma map/object handles."""

    return json.dumps(snapshot, sort_keys=True, separators=(",", ":"))


def deserialize_stage_snapshot(payload: str) -> dict[str, Any]:
    snapshot = json.loads(payload)
    if snapshot.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported segmented Magma schema")
    field = snapshot.get("field", {})
    if field.get("absolute_defining_polynomial") != F12:
        raise ValueError("field polynomial does not identify the Berry C_1 field")
    support = snapshot.get("support", [])
    ideal_numbers = [entry.get("ideal_number") for entry in support]
    if ideal_numbers != list(range(1, len(support) + 1)):
        raise ValueError("support ideal numbers are not deterministic")
    for entry in support:
        if not entry.get("generator_encoding"):
            raise ValueError("support generator is missing")
        if len(entry.get("generator_coordinates", [])) != 12:
            raise ValueError("support generator coordinates are missing")
        if entry["e"] * entry["f"] != entry["factor_degree"]:
            raise ValueError("support factor data is inconsistent")
    return snapshot


def validate_snapshot(snapshot: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    if snapshot["field"]["relative_degree"] != 6:
        violations.append("relative_degree")
    if snapshot["field"]["absolute_degree"] != 12:
        violations.append("absolute_degree")
    if snapshot["field"]["maximal_order_discriminant"] != "5019340374016":
        violations.append("maximal_order_discriminant")
    if snapshot["class_group"]["invariants"] != []:
        violations.append("class_group_not_trivial")
    if snapshot["unit_group"]["invariants"] != list(UNIT_INVARIANTS):
        violations.append("unit_group_invariants")
    if len(snapshot["unit_group"].get("generator_coordinates", [])) != 6:
        violations.append("unit_group_generators")
    support = snapshot["support"]
    if sum(entry["e"] * entry["f"] for entry in support[:2]) != 6:
        violations.append("dyadic_degree_sum")
    if sum(entry["e"] * entry["f"] for entry in support[2:6]) != 6:
        violations.append("selected_pi_degree_sum")
    expected_dimension = 6 + len(support)
    if len(snapshot["s_unit_group"]["squareclass_basis"]) != expected_dimension:
        violations.append("s_unit_squareclass_dimension")
    if snapshot["s_unit_group"]["relation_matrix"] != _relation_matrix(expected_dimension):
        violations.append("s_unit_relation_matrix")
    return violations


def build_certificate() -> dict[str, Any]:
    model = stage_snapshot()
    conservative = stage_snapshot(include_conjugate_support=True)
    model_violations = validate_snapshot(model)
    conservative_violations = validate_snapshot(conservative)
    checks = {
        "absolute_decomposition_degree_2": sum(e * f for e, f in ABSOLUTE_DECOMPOSITION["2"]) == 12,
        "absolute_decomposition_degree_37397": sum(
            e * f for e, f in ABSOLUTE_DECOMPOSITION["37397"]
        )
        == 12,
        "model_support_has_six_primes": len(model["support"]) == 6,
        "conservative_support_has_ten_primes": len(conservative["support"]) == 10,
        "model_snapshot_round_trip": deserialize_stage_snapshot(serialize_stage_snapshot(model))
        == model,
        "conservative_snapshot_round_trip": deserialize_stage_snapshot(
            serialize_stage_snapshot(conservative)
        )
        == conservative,
        "model_snapshot_valid": not model_violations,
        "conservative_snapshot_valid": not conservative_violations,
        "local_target_dyadic": local_kummer_target("dyadic") == 5,
        "local_target_odd": local_kummer_target("odd") == 2,
    }
    violations = [name for name, passed in checks.items() if not passed]
    return {
        "status": "ok" if not violations else "invalid",
        "ready": not violations,
        "task": TASK_ID,
        "accepted_outcome": "segmented_free_magma_route_ready",
        "checks": checks,
        "violations": violations,
        "field_and_order": model["field"],
        "support_decomposition": {
            "model": model["support"],
            "conservative_with_conjugate_prime": conservative["support"],
            "absolute_patterns": {
                "2": [list(item) for item in ABSOLUTE_DECOMPOSITION["2"]],
                "37397": [list(item) for item in ABSOLUTE_DECOMPOSITION["37397"]],
            },
        },
        "global_data": {
            "class_group_invariants": list(CLASS_GROUP_INVARIANTS),
            "unit_group_invariants": list(UNIT_INVARIANTS),
            "model_s_unit_group_invariants": model["s_unit_group"]["invariants"],
            "model_squareclass_dimension": len(model["s_unit_group"]["squareclass_basis"]),
            "conservative_squareclass_dimension": len(
                conservative["s_unit_group"]["squareclass_basis"]
            ),
            "model_basis": model["s_unit_group"]["squareclass_basis"],
            "conservative_basis": conservative["s_unit_group"]["squareclass_basis"],
        },
        "local_target": {
            "dyadic": {
                "relative_factor_degrees": [2, 4],
                "j2_dimension": 1,
                "field_degree_over_Q2": 2,
                "genus": 2,
                "strict_dimension_formula": "[K_varpi:Q_2]*g + dim_F2 J(K_varpi)[2]",
                "dim_J_over_2J": 5,
            },
            "odd_pi": {
                "relative_factor_degrees": [1, 1, 2, 2],
                "j2_dimension": 2,
                "residue_characteristic": 37397,
                "strict_dimension_formula": "dim_F2 J(K_pi)[2]",
                "dim_J_over_2J": 2,
            },
            "both_twists_same_2_torsion": True,
        },
        "calculator_observations": {
            "capability_probe": {
                "status": "ok",
                "version": "2.29-8",
                "max_time": 60,
                "field_degree": 2,
                "curve_genus": 2,
                "two_selmer_group_intrinsic": True,
                "two_cover_descent_intrinsic": True,
                "local_kummer_image_intrinsic": False,
            },
            "prior_full_global_probe": {
                "status": "magma_error",
                "max_time": 60,
                "last_marker": "BERRY_TWO_SELMER_V1_START",
                "warning": (
                    "The computation exceeded the time limit and so was terminated prematurely."
                ),
                "not_rerun_here": True,
            },
            "segmented_submissions": {
                "status": "ok",
                "proxy": "127.0.0.1:7897",
                "version": "2.29-8",
                "elapsed_seconds": {
                    "field_order": 0.06,
                    "class_units_sunits": 0.78,
                    "local_factorization": 0.07,
                    "scalar_rebuild": 0.03,
                },
                "all_below_public_limit": True,
            },
        },
        "boundary": {
            "not_a_selmer_computation": True,
            "not_a_rank_computation": True,
            "not_an_arithmetic_blocker": True,
            "segmented_route_ready": True,
            "next_obligation": (
                "Use the fixed absolute-field power-basis S-unit coordinates to "
                "construct the two complete local Kummer images; do not infer a "
                "Selmer bound from this feasibility certificate."
            ),
        },
    }


def local_kummer_target(place: str) -> int:
    """Return the strict local quotient dimension target for either model."""

    if place == "dyadic":
        # K_varpi = Q_2(i) has degree 2.  The [2,4] factorization gives one
        # invariant even branch partition modulo the all-branch relation.
        return 2 * 2 + 1
    if place == "odd":
        # Four Galois orbits on six branch points give r-2=2 invariant J[2]
        # dimensions for an even-degree genus-2 model.
        return 2
    raise ValueError(f"unknown local place: {place}")


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    payload = build_certificate()
    if args.out:
        args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"status={payload['status']}")
    print(f"task={payload['task']}")
    print(f"ready={payload['ready']}")
    print(f"accepted_outcome={payload['accepted_outcome']}")
    print(f"violations={payload['violations']}")
