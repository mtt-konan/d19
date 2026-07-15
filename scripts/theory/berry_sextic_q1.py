"""Exact Q1 certificate for the selected Berry sextic fake 2-descent.

This records the object used by the later local-image stages.  It is only a
fake descent certificate: it does not compute a Selmer group or a rank.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TASK_ID = "berry-sextic-genus2-classification-20260715"
SCHEMA_VERSION = "berry-c1-q1-fake-descent-v1"


def build_certificate() -> dict[str, object]:
    from scripts.theory.berry_sextic_magma_segmented import stage_snapshot

    snapshot = stage_snapshot(include_conjugate_support=True)
    basis = snapshot["s_unit_group"]["squareclass_basis"]
    assert isinstance(basis, list)
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
        "descent_object": {
            "etale_algebra": "L=K[theta]/(g6(theta))",
            "degree_over_K": 6,
            "absolute_degree": 12,
            "target": "L^*/L^{*2}K^*",
            "norm_condition": "N_{L/K}(alpha) in K^{*2}",
            "support": "conservative support above 2 and 37397",
            "coordinates": basis,
            "coordinate_order": "zeta4, epsilon_1..epsilon_5, S_prime_1..S_prime_10",
            "squareclass_dimension": len(basis),
            "constant_quotient": "K^* is quotiented; zeta4 has relation 4=0 before mod 2",
        },
        "infinity_kernel": {
            "even_degree_kernel": "<P_+-P_-> in J(K)/2J(K)",
            "reason": (
                "div(t-theta)=2D_theta-P_+-P_-; the two infinity signs are "
                "invisible to the fake divisor evaluation"
            ),
            "order_bound": 2,
        },
        "d_inf_kummer": {
            "divisor": "D_inf=P_+-P_-",
            "fake_class": "1 in L^*/L^{*2}K^*",
            "coordinate_vector": [0] * len(basis),
            "verification": "leading coefficient is 1, hence its squareclass is trivial",
            "interpretation": (
                "D_inf lies in the even-degree fake-map kernel; this does not "
                "make D_inf zero in J(K)/2J(K)"
            ),
        },
        "proof_boundary": {
            "proved": [
                "the fixed fake target and coordinate convention",
                "the even-degree infinity kernel generator",
                "the trivial fake Kummer image of D_inf",
            ],
            "not_proved": [
                "either local Kummer image",
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
