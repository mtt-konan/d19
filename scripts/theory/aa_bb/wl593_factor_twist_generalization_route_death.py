#!/usr/bin/env python3
"""Certify route death for the frozen factor-twist local-image mechanism.

Only the frozen wl587/wl589 D0 payloads and wl590-wl592 local certificates
are imported.  This checkpoint compares their quantifiers and coefficient
dependencies; it does not add a family, a local row, or another descent.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

try:
    from scripts.theory.aa_bb import wl587_pure_u7_d0_relative_2_descent as wl587
    from scripts.theory.aa_bb import wl589_mixed_d0_relative_2_descent as wl589
    from scripts.theory.aa_bb import wl590_p5_factor_twist_local_image_comparison as wl590
    from scripts.theory.aa_bb import wl591_mixed_p7_factor_twist_local_image as wl591
    from scripts.theory.aa_bb import wl592_mixed_p17_factor_twist_local_image as wl592
    from scripts.theory.json_io import write_json
except ModuleNotFoundError:
    import wl587_pure_u7_d0_relative_2_descent as wl587
    import wl589_mixed_d0_relative_2_descent as wl589
    import wl590_p5_factor_twist_local_image_comparison as wl590
    import wl591_mixed_p7_factor_twist_local_image as wl591
    import wl592_mixed_p17_factor_twist_local_image as wl592
    from json_io import write_json


INPUT_WORK_LOGS = ["wl587", "wl589", "wl590", "wl591", "wl592"]
PURE_SCOPE = "support=u_7|L=7|T=9|d=(7,7,1), R^2=P_op only"
MIXED_SCOPE = "support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85), R^2=P_op only"
P5_SCOPE = "p=5 local factor-twist images for frozen wl587 and wl589 only"
P7_SCOPE = "frozen wl589 mixed cover support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85) at p=7 only"
P17_SCOPE = "frozen wl589 mixed cover support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85) at p=17 only"
LOCAL_IMAGE_QUANTIFIER = (
    "For each frozen representative j, selected prime p, and [d] in "
    "Q_p^*/Q_p^{*2}, [d] is in I_{p,j} iff there exists a Q_p-point "
    "(c,a_plus,a_minus,R) on the already audited complete normalized "
    "factor-cover charts, including finite, pole, infinity, factor-zero, "
    "and R=0 charts, with d in Q_p^* and F_plus(c)=d*a_plus^2, "
    "F_minus(c)=d*a_minus^2, and R=d*a_plus*a_minus.  The real positivity "
    "interval and exact AA+BB source-product lift remain global boundaries "
    "and are not added as a p-adic filter."
)
CONCLUSION = (
    "The current fixed-representative factor-twist local-image mechanism "
    "cannot be promoted from these fixed inputs alone; it requires new "
    "parameterized family-level coefficient/local-image input."
)


def _all_true(values: dict[str, Any]) -> bool:
    return bool(values) and all(value is True for value in values.values())


def _contains_all(values: list[Any], needles: tuple[str, ...]) -> bool:
    text = " ".join(str(value) for value in values)
    return all(needle in text for needle in needles)


def _ready(payload: dict[str, Any], work_log: str) -> bool:
    verification = payload.get("verification", {})
    return (
        payload.get("status") == "ok"
        and payload.get("ready") is True
        and payload.get("work_log") == work_log
        and verification.get("violations") == []
    )


def _d0_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
    source = payload["source_cover"]
    divisors = payload["divisors_and_branch_cover"]
    local = payload["local_exception_and_bad_fiber_data"]
    return {
        "base": source["base"],
        "scope": payload["scope"],
        "parameters": source["parameters"],
        "source_data": source["function_field"],
        "factor_data": {
            "factor_functions": divisors["factor_functions"],
            "factor_covering_equations": divisors["factor_covering_equations"],
        },
        "bad_prime_support": local["bad_fiber_set"]["S"],
        "aa_bb_exact_conditions": payload["aa_bb_lift"]["exact_conditions"],
    }


def _fixed_input_comparison(pure: dict[str, Any], mixed: dict[str, Any]) -> dict[str, Any]:
    bases = {
        "pure_u7": _d0_snapshot(pure),
        "mixed_u3_v5_w17": _d0_snapshot(mixed),
    }
    pure_source = pure["source_cover"]
    mixed_source = mixed["source_cover"]
    pure_divisors = pure["divisors_and_branch_cover"]
    mixed_divisors = mixed["divisors_and_branch_cover"]
    difference_checks = {
        "coefficient_data_differ": pure_source["parameters"] != mixed_source["parameters"],
        "source_data_differ": pure_source["function_field"] != mixed_source["function_field"],
        "factor_data_differ": (
            pure_divisors["factor_functions"] != mixed_divisors["factor_functions"]
            and pure_divisors["factor_covering_equations"]
            != mixed_divisors["factor_covering_equations"]
        ),
        "bad_prime_supports_differ": bases["pure_u7"]["bad_prime_support"]
        != bases["mixed_u3_v5_w17"]["bad_prime_support"],
    }
    return {
        "bases": bases,
        "difference_checks": difference_checks,
    }


def _d0_checks(pure: dict[str, Any], mixed: dict[str, Any]) -> dict[str, bool]:
    pure_boundary = pure["proof_boundary"]
    mixed_boundary = mixed["proof_boundary"]
    return {
        "wl587_ready_fixed_input": _ready(pure, "wl587"),
        "wl589_ready_fixed_input": _ready(mixed, "wl589"),
        "wl587_base_is_Spec_Q": pure["source_cover"]["base"] == "Spec(Q)",
        "wl589_base_is_Spec_Q": mixed["source_cover"]["base"] == "Spec(Q)",
        "wl587_scope_is_fixed": pure["scope"] == PURE_SCOPE,
        "wl589_scope_is_fixed": mixed["scope"] == MIXED_SCOPE,
        "wl587_is_D0_not_family_theorem": (
            pure_boundary["D0_certificate_proved_here"] is True
            and pure_boundary["family_exclusion"] is False
            and pure_boundary["theorem_level_selmer_claim"] is False
        ),
        "wl589_is_D0_not_family_theorem": (
            mixed_boundary["D0_certificate_proved_here"] is True
            and mixed_boundary["family_exclusion"] is False
            and mixed_boundary["theorem_level_selmer_claim"] is False
        ),
    }


def _p5_comparison(payload: dict[str, Any]) -> dict[str, Any]:
    images = payload["local_images"]
    return {
        "prime": payload["prime"],
        "scope": payload["scope"],
        "pure_u7_image": images["pure_u7"],
        "mixed_u3_v5_w17_image": images["mixed_u3_v5_w17"],
        "images_disagree": images["pure_u7"] != images["mixed_u3_v5_w17"],
        "certificate_ready": _ready(payload, "wl590"),
    }


def _mixed_instance_chain(
    p5: dict[str, Any], p7: dict[str, Any], p17: dict[str, Any]
) -> dict[str, Any]:
    p5_mixed = p5["named_survivor_mapping"]["mixed_u3_v5_w17"]
    p7_mapping = p7["named_survivor_mapping"]
    return {
        "p5_survivors": p5_mixed["survive"],
        "p7_prime": p7["prime"],
        "p7_scope": p7["scope"],
        "p7_image": p7["local_image"],
        "p7_survivors": p7_mapping["survive"],
        "p17_prime": p17["prime"],
        "p17_scope": p17["scope"],
        "p17_image": p17["local_image"],
        "p17_target": p17["target_twist"],
        "p17_target_class": p17["target_twist_class"],
        "p17_target_in_image": p17["target_twist_in_image"],
        "instance_specific": (
            p7["scope"] == P7_SCOPE
            and p17["scope"] == P17_SCOPE
            and p7["object_layer"] == "normalized_mixed_Q7_relative_constant_factor_twist_image"
            and p17["object_layer"] == "normalized_mixed_Q17_relative_constant_factor_twist_image"
            and _ready(p7, "wl591")
            and _ready(p17, "wl592")
        ),
    }


def _frozen_boundary_certificate(
    pure: dict[str, Any],
    mixed: dict[str, Any],
    p5: dict[str, Any],
    p7: dict[str, Any],
    p17: dict[str, Any],
) -> dict[str, Any]:
    p5_pure_map = p5["fixed_cover_and_lift"]["pure_u7"]
    p5_mixed_map = p5["fixed_cover_and_lift"]["mixed_u3_v5_w17"]
    p7_maps = p7["proof_certificate"]["frozen_maps_certificate"]
    p17_maps = p17["proof_certificate"]["frozen_maps_certificate"]
    pure_conditions = p5_pure_map["aa_bb_conditions"]
    mixed_conditions = p5_mixed_map["aa_bb_conditions"]
    checks = {
        "wl587_exact_aa_bb_checks": _all_true(pure["aa_bb_lift"]["structural_checks"]),
        "wl589_exact_aa_bb_checks": _all_true(mixed["aa_bb_lift"]["structural_checks"]),
        "wl590_all_pole_infinity_factor_zero_checks": (
            _all_true(p5["verification"]["checks"])
            and _all_true(p5["proof_certificate"]["pure_u7"]["checks"])
            and _all_true(p5["proof_certificate"]["mixed_u3_v5_w17"]["checks"])
            and _contains_all(
                [p5["verification"]["strict_certificate"]],
                ("poles", "projective boundaries", "factor-zero", "AA+BB"),
            )
        ),
        "wl591_all_pole_infinity_factor_zero_checks": (
            _all_true(p7["verification"]["local_checks"])
            and _contains_all(
                [p7["strict_certificate"]],
                ("infinity", "D/A", "factor-zero", "fixed-cover R", "AA+BB"),
            )
        ),
        "wl592_all_pole_infinity_factor_zero_checks": (
            _all_true(p17["verification"]["local_checks"])
            and _contains_all(
                [p17["strict_certificate"]],
                ("infinity", "D/A", "factor-zero", "fixed cover R", "AA+BB"),
            )
        ),
        "wl590_fixed_cover_R_maps_retained": (
            p5_pure_map["identity_check"] is True
            and p5_mixed_map["identity_check"] is True
            and "R=d*a_plus*a_minus" in p5_pure_map["fixed_cover_map"]
            and "R=d*a_plus*a_minus" in p5_mixed_map["fixed_cover_map"]
        ),
        "wl591_fixed_cover_R_map_retained": (
            _all_true(p7_maps["checks"])
            and p7_maps["fixed_cover_equation"] == "R^2=(N^2+49)*(M^2+49)"
        ),
        "wl592_fixed_cover_R_map_retained": (
            _all_true(p17_maps["checks"])
            and p17_maps["fixed_cover_equation"] == "R^2=(N^2+49)*(M^2+49)"
        ),
        "wl590_positivity_and_aa_bb_retained": (
            _contains_all(
                pure_conditions,
                ("-9<t<9", "(N^2+49)*(M^2+49)=(Z/4)^2"),
            )
            and _contains_all(
                mixed_conditions,
                ("-10<t<10", "(N^2+9)*(M^2+9)=(Z/4)^2"),
            )
        ),
        "wl591_positivity_and_aa_bb_retained": (
            _contains_all(
                p7_maps["exact_aa_bb_lift"],
                ("-10<t<10", "(N^2+9)*(M^2+9)=(Z/4)^2"),
            )
        ),
        "wl592_positivity_and_aa_bb_retained": (
            _contains_all(
                p17_maps["exact_aa_bb_lift"],
                ("-10<t<10", "(N^2+9)*(M^2+9)=(Z/4)^2"),
            )
        ),
    }
    return {
        "checks": checks,
        "positivity_intervals": {
            "pure_u7": next(item for item in pure_conditions if item.startswith("-9<t<9")),
            "mixed_u3_v5_w17": next(
                item for item in mixed_conditions if item.startswith("-10<t<10")
            ),
        },
        "fixed_cover_equations": {
            "pure_u7": p5_pure_map["fixed_cover_map"].split(", ", 1)[1],
            "mixed_u3_v5_w17": p5_mixed_map["fixed_cover_map"].split(", ", 1)[1],
        },
        "aa_bb_source_products": {
            "pure_u7": pure_conditions[0],
            "mixed_u3_v5_w17": mixed_conditions[0],
        },
    }


def build_wl593_factor_twist_generalization_route_death() -> dict[str, Any]:
    pure = wl587.build_wl587_pure_u7_d0_relative_2_descent()
    mixed = wl589.build_wl589_mixed_d0_relative_2_descent()
    p5 = wl590.build_wl590_p5_factor_twist_local_image_comparison()
    p7 = wl591.build_wl591_mixed_p7_factor_twist_local_image()
    p17 = wl592.build_wl592_mixed_p17_factor_twist_local_image()

    fixed_input_comparison = _fixed_input_comparison(pure, mixed)
    d0_checks = _d0_checks(pure, mixed)
    p5_comparison = _p5_comparison(p5)
    mixed_instance_chain = _mixed_instance_chain(p5, p7, p17)
    frozen_boundaries = _frozen_boundary_certificate(pure, mixed, p5, p7, p17)
    checks = {
        "only_frozen_wl587_wl589_wl590_wl591_wl592_inputs": INPUT_WORK_LOGS
        == ["wl587", "wl589", "wl590", "wl591", "wl592"],
        **d0_checks,
        **{
            f"input_difference_{name}": passed
            for name, passed in fixed_input_comparison["difference_checks"].items()
        },
        "p5_certificate_is_ready": p5_comparison["certificate_ready"],
        "p5_local_images_disagree": p5_comparison["images_disagree"]
        and p5_comparison["prime"] == 5
        and p5_comparison["scope"] == P5_SCOPE,
        "mixed_p7_p17_chain_is_instance_specific": mixed_instance_chain["instance_specific"],
        "mixed_chain_starts_with_exact_p5_survivors": mixed_instance_chain["p5_survivors"]
        == [5, 3045, 66045, 91205],
        "mixed_p7_keeps_only_91205": mixed_instance_chain["p7_survivors"] == [91205]
        and mixed_instance_chain["p7_image"] == ["[1]"],
        "mixed_p17_excludes_91205": (
            mixed_instance_chain["p17_target"] == 91205
            and mixed_instance_chain["p17_target_class"] == "[17u]"
            and mixed_instance_chain["p17_target_in_image"] is False
            and mixed_instance_chain["p17_image"] == ["[u]"]
        ),
        **{f"boundary_{name}": passed for name, passed in frozen_boundaries["checks"].items()},
    }
    violations = [name for name, passed in checks.items() if not passed]
    ready = not violations
    return {
        "status": "ok" if ready else "issues",
        "ready": ready,
        "work_log": "wl593",
        "accepted_outcome": "route_death_certificate",
        "input_work_logs": INPUT_WORK_LOGS,
        "object_layer": "fixed_representative_factor_twist_local_image_generalization",
        "local_image_quantifier": LOCAL_IMAGE_QUANTIFIER,
        "fixed_input_comparison": fixed_input_comparison,
        "p5_comparison": p5_comparison,
        "mixed_instance_chain": mixed_instance_chain,
        "frozen_boundaries": frozen_boundaries,
        "conclusion": CONCLUSION,
        "proof_boundary": {
            "all_relative_2_descent_impossible": False,
            "family_level_local_image_theorem": False,
            "new_parameterized_family_added": False,
            "new_prime_or_local_row_added": False,
            "new_equivalent_model_or_quotient_added": False,
            "rank_computation": False,
            "rational_point_search": False,
            "D2": False,
            "D5": False,
            "Selmer_claim": False,
        },
        "verification": {
            "checks": checks,
            "violations": violations,
            "strict_certificate": (
                "Only wl587/wl589 and wl590-wl592 are imported.  The certificate "
                "compares fixed Spec(Q) coefficient/source/factor data, the "
                "bad-prime supports, the p=5 image disagreement, and the "
                "mixed p=7,p=17 instance chain.  All audited pole, infinity, "
                "factor-zero, positivity, fixed-cover R, and AA+BB boundaries "
                "remain in scope; no family-level local-image input is supplied."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = build_wl593_factor_twist_generalization_route_death()
    if args.out is not None:
        write_json(args.out, payload)
    if args.strict:
        print(f"status={payload['status']}")
        print(f"work_log={payload['work_log']}")
        print(f"ready={payload['ready']}")
        print(f"accepted_outcome={payload['accepted_outcome']}")
        print(f"violations={payload['verification']['violations']}")
        return 0 if payload["ready"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
