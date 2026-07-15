"""Exact Q1 object hierarchy for the selected Berry sextic.

The conservative S-unit data supplies an ambient coordinate space only.  This
certificate defines the constant quotient, the norm-square kernel, and the
local fake quotient without fabricating either a Selmer group or local
generators.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TASK_ID = "berry-sextic-genus2-classification-20260715"
SCHEMA_VERSION = "berry-c1-q1-fake-descent-v2"


def build_certificate() -> dict[str, object]:
    from scripts.theory.berry_sextic_magma_segmented import stage_snapshot

    snapshot = stage_snapshot(include_conjugate_support=True)
    basis = snapshot["s_unit_group"]["squareclass_basis"]
    assert isinstance(basis, list)
    ambient_dimension = len(basis)
    assert ambient_dimension == 16

    return {
        "schema_version": SCHEMA_VERSION,
        "task_id": TASK_ID,
        "curve": {
            "base_field": "K=Q(i)",
            "equation": "v^2=g6(t)",
            "degree": 6,
            "genus": 2,
            "leading_coefficient": "1",
            "infinity_points": ["P_+", "P_-"],
        },
        "ambient_space": {
            "notation": "V_S",
            "definition": (
                "V_S=image(U_{L,S}/U_{L,S}^2 -> L^*/L^{*2}), where U_{L,S} "
                "is the conservative S-unit group"
            ),
            "field": "F_2",
            "support": "conservative support above 2 and 37397",
            "coordinates": basis,
            "coordinate_order": "zeta4, epsilon_1..epsilon_5, S_prime_1..S_prime_10",
            "dimension": ambient_dimension,
            "dimension_claim": "conservative ambient S-unit coordinates only",
            "source_invariants": "U_{L,S}=C4 x Z^15, hence dim_F2(U_{L,S}/U_{L,S}^2)=16",
            "is_fake_target": False,
            "is_selmer_group": False,
            "fake_target_dimension_computed": False,
        },
        "descent_object": {
            "etale_algebra": "L=K[theta]/(g6(theta))",
            "degree_over_K": 6,
            "absolute_degree": 12,
            "target": "F_L=L^*/(L^{*2}K^*)",
            "norm_condition": (
                "separate condition N_{L/K}(alpha) in K^{*2}; not part of the quotient definition"
            ),
            "ambient_coordinate_space": "V_S",
            "coordinates": basis,
            "coordinate_order": "zeta4, epsilon_1..epsilon_5, S_prime_1..S_prime_10",
            "ambient_coordinate_dimension": ambient_dimension,
            "constant_quotient_is_part_of_target": True,
            "not_the_16_dimensional_target": True,
            "not_a_selmer_group": True,
        },
        "fake_target": {
            "notation": "F_L",
            "definition": ("F_L=L^*/(L^{*2}K^*)=(L^*/L^{*2})/im(K^*/K^{*2} -> L^*/L^{*2})"),
            "ambient_supported_image": {
                "notation": "F_{L,S}",
                "definition": "F_{L,S}=V_S/C_S",
                "constant_subspace": {
                    "notation": "C_S",
                    "definition": ("C_S=V_S intersect im(K^*/K^{*2} -> L^*/L^{*2})"),
                    "quotient_map": "q_S: V_S -> V_S/C_S",
                    "known_constant_class": "[i]=[zeta4] belongs to C_S",
                    "coordinate_matrix": {
                        "status": "not_computed",
                        "domain": "K^*/K^{*2} classes represented in V_S",
                        "codomain": "F_2^16",
                        "warning": "the 16 labels do not determine C_S",
                    },
                },
                "injects_into_exact_target": True,
                "dimension_computed": False,
            },
            "dimension": None,
            "dimension_status": "not computed",
            "selmer_claim": False,
        },
        "norm_square_kernel": {
            "map_notation": "barN_L",
            "kernel_notation": "K_L^N",
            "ambient_map": ("barN_L: F_L -> K^*/K^{*2}, barN_L([alpha])=[N_{L/K}(alpha)]"),
            "well_defined_reason": (
                "squares have square norm, and replacing alpha by k*alpha "
                "multiplies the norm by k^6, a square because [L:K]=6"
            ),
            "definition": "K_L^N=ker(barN_L: F_L -> K^*/K^{*2})",
            "ambient_preimage": ("V_S^N={v in V_S: N_{L/K}(alpha_v) in K^{*2}}"),
            "supported_kernel": "K_{L,S}^N=q_S(V_S^N)=F_{L,S} intersect K_L^N",
            "is_separate_from_constant_quotient": True,
            "dimension": None,
            "dimension_status": "not computed",
            "coordinate_matrix": {
                "symbol": "M_norm",
                "map": "F_2^16 -> K^*/K^{*2}",
                "columns": "M_norm(e_j)=[N_{L/K}(alpha_j)] for the fixed S-unit lifts alpha_j",
                "status": "missing",
                "needed_for_q2": True,
            },
        },
        "infinity_kernel": {
            "class": "D_inf=[P_+-P_-] in J(K)/2J(K)",
            "kernel_statement": (
                "the image of D_inf in J(K)/2J(K) lies in the kernel of the "
                "fake divisor-evaluation map"
            ),
            "divisor_formula_over_L": "div(t-theta)=2W_theta-P_+-P_-",
            "reason": (
                "the two infinity signs occur with the same coefficient in "
                "the even-degree evaluation divisor"
            ),
            "not_claimed": [
                "D_inf is nonzero in J(K)/2J(K)",
                "D_inf is nonzero torsion in J(K)",
                "the displayed class generates the full kernel",
            ],
        },
        "d_inf_kummer": {
            "divisor": "D_inf=P_+-P_-",
            "fake_class": "[1]=0 in F_L",
            "ambient_representative": {
                "class": "[1] in V_S",
                "coordinate_vector": [0] * ambient_dimension,
                "meaning": (
                    "zero coordinates for the representative 1 in V_S; "
                    "this is not a coordinate vector for F_L"
                ),
            },
            "verification": (
                "the standard infinity evaluation is the leading coefficient "
                "class [1], which is trivial in the fake quotient"
            ),
            "interpretation": (
                "D_inf has trivial fake image; this does not make D_inf zero in J(K)/2J(K)"
            ),
        },
        "local_fake_quotient": {
            "place": "pi=(94*i-169)",
            "completion": "K_pi",
            "local_algebra": "A_pi=L tensor_K K_pi=K_pi[t]/(g6(t))",
            "fake_quotient": {
                "notation": "F_pi",
                "definition": "F_pi=A_pi^*/(A_pi^{*2}K_pi^*)",
            },
            "local_norm_map": (
                "N_pi: F_pi -> K_pi^*/K_pi^{*2}, N_pi([alpha])=[N_{A_pi/K_pi}(alpha)]"
            ),
            "norm_square_kernel": "H_pi=ker(N_pi)",
            "local_fake_image": "I_pi=delta_pi(J(K_pi)/2J(K_pi)) subset H_pi",
            "accepted_j_over_2j_dimension": 2,
            "local_fake_image_computed": False,
            "local_basis_or_generators_supplied": False,
        },
        "localization": {
            "global_map": "loc_pi^fake: F_L -> F_pi",
            "formula": "loc_pi^fake([alpha])=[alpha tensor 1]",
            "ambient_coordinate_map": ("Lambda_pi,S=loc_pi^fake o q_S o phi_S: F_2^16 -> F_pi"),
            "norm_compatibility": (
                "N_pi(Lambda_pi,S(v))=loc_pi^K(N_L(phi_S(v))); therefore N_{L,S} maps into H_pi"
            ),
            "matrix": {
                "symbol": "M_loc_pi",
                "columns": "M_loc_pi(e_j)=loc_pi^fake(q_S(phi_S(e_j)))",
                "codomain": "F_pi, with no local basis chosen",
                "status": "missing",
                "needed_for_q2": True,
            },
        },
        "q2_missing_matrices": [
            {
                "symbol": "M_const",
                "role": "coordinate image of global constants C_S inside V_S",
                "status": "missing",
            },
            {
                "symbol": "M_norm",
                "role": "global ambient norm map to K^*/K^{*2}",
                "status": "missing",
            },
            {
                "symbol": "M_loc_pi",
                "role": "localization of the quotient ambient classes at pi",
                "status": "missing",
            },
        ],
        "proof_boundary": {
            "proved": [
                "the exact fake quotient F_L=L^*/(L^{*2}K^*)",
                "the conservative 16-dimensional ambient S-unit space V_S",
                "the constant subspace C_S and supported quotient V_S/C_S as definitions",
                "the norm-square kernel as a separate kernel of the descended norm map",
                "the local fake quotient F_pi and its norm-square kernel H_pi as definitions",
                "the localization map from global ambient coordinates to local classes",
                "the even-degree infinity kernel inclusion and trivial fake class of D_inf",
            ],
            "not_proved": [
                "the rank of C_S or the dimension of the supported fake quotient",
                "the global norm matrix M_norm or the supported norm-square kernel dimension",
                "the local norm/localization matrices at pi",
                "any local Kummer image or local generator",
                "fake Selmer or true Selmer dimension",
                "rank or saturation",
                "the set of rational t-values",
            ],
        },
    }


def main(path: Path | None = None) -> None:
    payload = build_certificate()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if path is None:
        print(rendered, end="")
    else:
        path.write_text(rendered, encoding="utf-8")
        print(f"schema={SCHEMA_VERSION}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    main(args.out)
