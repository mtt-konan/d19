#!/usr/bin/env python3
"""Check the wl486 local-solubility gate for the explicit u_3 C_d cover."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.theory.json_io import load_json, write_json
except ModuleNotFoundError:
    from json_io import load_json, write_json

BOUNDARY = (
    "This audits only wl486 / local_solubility_gate for the AA+BB complete "
    "d-coordinate route. It takes wl485 as input and checks local solubility "
    "of the explicit d=(3,3,1) C_d cover only at infinity, 2, 3, and 13. It "
    "records local certificates. The local certificate found here is an exact "
    "integral point, so this audit also records global solubility of this "
    "single C_d cover. It does not run broad rank or Selmer diagnostics, does "
    "not prove an obstruction, does not prove a complete Sel_2(E) upper "
    "bound, and does not claim dim Sel_2(E)=2, rank zero, Sha[2]=0, or any "
    "family exclusion."
)

COORDINATE_ORDER = [
    "d_minus_p",
    "d_pos_2sqrt_q",
    "d_neg_2sqrt_q",
]
RELEVANT_PLACES = ["infinity", "2", "3", "13"]
TARGET_CANDIDATE_ID = "AA_A3_B1_u_3_complete_d_candidate"
FORBIDDEN_FLAGS = [
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
]
LOCAL_POINT = {
    "X": 152,
    "u_minus_p": 8,
    "u_pos_2sqrt_q": 4,
    "u_neg_2sqrt_q": 16,
}
ELLIPTIC_POINT = {"X": 152, "Y": 1536}
NORMALIZED_EQUATIONS = [
    "u_minus_p^2 - u_pos_2sqrt_q^2 - 48",
    "3*u_minus_p^2 - u_neg_2sqrt_q^2 + 64",
]


def _claims_forbidden_bound(payload: dict[str, Any]) -> bool:
    return (
        any(payload.get(flag) is True for flag in FORBIDDEN_FLAGS)
        or payload.get("family_exclusion_proved_count", 0) != 0
    )


def _wl485_ready(wl485: dict[str, Any]) -> bool:
    cover = wl485.get("explicit_c_d_cover", {})
    return (
        wl485.get("status") == "ok"
        and wl485.get("ready") is True
        and wl485.get("lemma_id") == "WL485_explicit_C_d_cover_equation_instantiation"
        and wl485.get("work_log") == "wl485"
        and wl485.get("input_work_log") == "wl484"
        and cover.get("candidate_id") == TARGET_CANDIDATE_ID
        and cover.get("coordinate_order") == COORDINATE_ORDER
        and cover.get("d_vector")
        == {
            "d_minus_p": 3,
            "d_pos_2sqrt_q": 3,
            "d_neg_2sqrt_q": 1,
        }
        and cover.get("two_independent_equations")
        == [
            "3*u_minus_p^2 - 3*u_pos_2sqrt_q^2 = 144",
            "3*u_minus_p^2 - u_neg_2sqrt_q^2 = -64",
        ]
        and wl485.get("relevant_places") == RELEVANT_PLACES
        and wl485.get("equation_instantiation_only") is True
        and wl485.get("local_solubility_decided_here") is False
        and wl485.get("global_solubility_decided_here") is False
        and wl485.get("old_package_x_coordinate_collapse_used") is False
        and not _claims_forbidden_bound(wl485)
    )


def _real_certificate() -> dict[str, Any]:
    return {
        "place": "infinity",
        "field": "R",
        "status": "locally_soluble",
        "certificate_type": "explicit_real_point",
        "point": dict(LOCAL_POINT),
        "equation_checks": [
            "152 + 40 = 3*8^2 = 192",
            "152 - 104 = 3*4^2 = 48",
            "152 + 104 = 16^2 = 256",
        ],
    }


def _dyadic_certificate() -> dict[str, Any]:
    return {
        "place": "2",
        "field": "Q_2",
        "status": "locally_soluble",
        "certificate_type": "exact_integral_2_adic_point",
        "point": dict(LOCAL_POINT),
        "modular_lift_certificate": {
            "method": "exact_zero_over_Z_embeds_in_Q_2",
            "verified_moduli": [2, 4, 8, 16, 32],
            "hensel_regular_minor_required": False,
            "reason": (
                "The displayed integer tuple satisfies the three C_d square "
                "relations exactly, so its reductions are compatible modulo "
                "2^n for every n. This same tuple is also a global integral "
                "point, recorded separately below."
            ),
        },
    }


def _global_solubility_witness() -> dict[str, Any]:
    return {
        "status": "globally_soluble",
        "certificate_type": "explicit_integral_point_on_C_d",
        "point_on_cover": dict(LOCAL_POINT),
        "equation_checks": [
            "152 + 40 = 3*8^2 = 192",
            "152 - 104 = 3*4^2 = 48",
            "152 + 104 = 16^2 = 256",
        ],
        "induced_point_on_E_L": {
            **ELLIPTIC_POINT,
            "check": "1536^2 = (152+40)*(152^2 - 4*2704)",
        },
        "route_impact": (
            "The u_3 candidate is not a Sha-style locally-soluble globally-"
            "pointless obstruction; it is represented by a rational point."
        ),
    }


def _hensel_certificate(
    *,
    place: str,
    residue_modulus: int,
    residue_point: dict[str, int],
    determinant_mod_p: int,
) -> dict[str, Any]:
    return {
        "place": place,
        "field": f"Q_{place}",
        "status": "locally_soluble",
        "certificate_type": "hensel_lift_from_mod_p",
        "residue_modulus": residue_modulus,
        "residue_point": residue_point,
        "equations_mod_p": [
            (
                "u_minus_p^2 - u_pos_2sqrt_q^2 - 48 == "
                f"0 mod {residue_modulus}"
            ),
            (
                "3*u_minus_p^2 - u_neg_2sqrt_q^2 + 64 == "
                f"0 mod {residue_modulus}"
            ),
        ],
        "jacobian_minor": {
            "rows": list(NORMALIZED_EQUATIONS),
            "columns": ["u_minus_p", "u_neg_2sqrt_q"],
            "determinant_mod_p": determinant_mod_p,
            "nonzero": True,
        },
    }


def _place_certificates() -> list[dict[str, Any]]:
    return [
        _real_certificate(),
        _dyadic_certificate(),
        _hensel_certificate(
            place="3",
            residue_modulus=3,
            residue_point={
                "X": 2,
                "u_minus_p": 1,
                "u_pos_2sqrt_q": 1,
                "u_neg_2sqrt_q": 1,
            },
            determinant_mod_p=2,
        ),
        _hensel_certificate(
            place="13",
            residue_modulus=13,
            residue_point={
                "X": 9,
                "u_minus_p": 8,
                "u_pos_2sqrt_q": 4,
                "u_neg_2sqrt_q": 3,
            },
            determinant_mod_p=8,
        ),
    ]


def _local_solubility_gate(wl485: dict[str, Any]) -> dict[str, Any]:
    cover = wl485["explicit_c_d_cover"]
    return {
        "candidate_id": cover["candidate_id"],
        "coordinate_order": list(cover["coordinate_order"]),
        "d_vector": dict(cover["d_vector"]),
        "checked_places": list(RELEVANT_PLACES),
        "place_certificates": _place_certificates(),
        "candidate_survives_local_gate": True,
        "global_solubility_witness": _global_solubility_witness(),
        "next_gate": "route_impact_of_global_point",
        "global_solubility_deferred": False,
    }


def build_wl486_local_solubility_gate(*, wl485: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    if not _wl485_ready(wl485):
        violations.append("wl485_input_not_ready_or_not_scoped")

    status = "ok" if not violations else "issues"
    return {
        "status": status,
        "ready": status == "ok",
        "source": "wl485 explicit C_d cover equation instantiation",
        "pattern": "AA+BB",
        "lemma_id": "WL486_local_solubility_gate",
        "work_log": "wl486",
        "input_work_log": "wl485",
        "local_solubility_gate": (
            _local_solubility_gate(wl485) if status == "ok" else {}
        ),
        "relevant_places": list(RELEVANT_PLACES),
        "local_solubility_decided_here": status == "ok",
        "local_solubility_summary": (
            "locally_soluble_at_all_relevant_places"
            if status == "ok"
            else "not_decided_input_not_ready"
        ),
        "global_solubility_decided_here": status == "ok",
        "global_solubility_summary": (
            "globally_soluble_integral_point_found_during_local_gate"
            if status == "ok"
            else "not_decided_input_not_ready"
        ),
        "obstruction_proved_here": False,
        "candidate_obstruction_refuted_here": status == "ok",
        "explicit_c_d_cover_solved_here": status == "ok",
        "symbolic_rank_status": "not_computed_here",
        "computed_rank_status": "not_run_local_gate_only",
        "broad_rank_or_selmer_diagnostics_run": False,
        "complete_selmer_upper_bound_proved": False,
        "selmer_rank_upper_bound_proved_count": 0,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
        "old_package_x_coordinate_collapse_used": False,
        "search_count_used_as_progress": False,
        "violations": violations,
        "boundary": BOUNDARY,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wl485", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = build_wl486_local_solubility_gate(wl485=load_json(args.wl485))
    write_json(args.out, audit)
    print(f"wrote AA+BB wl486 local solubility gate to {args.out}")
    print(f"status={audit['status']}")
    print(f"work_log={audit['work_log']}")
    print(f"local_solubility_decided_here={audit['local_solubility_decided_here']}")
    print(f"global_solubility_decided_here={audit['global_solubility_decided_here']}")
    print(f"global_solubility_summary={audit['global_solubility_summary']}")
    if audit["status"] == "ok":
        survives = audit["local_solubility_gate"]["candidate_survives_local_gate"]
        print(f"candidate_survives_local_gate={survives}")
    if args.strict and audit["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
