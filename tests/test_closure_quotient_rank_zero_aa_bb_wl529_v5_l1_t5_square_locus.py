from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import (
    audit_closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus as wl529_module,
)

build_wl529_v5_l1_t5_square_locus = wl529_module.build_wl529_v5_l1_t5_square_locus


def _wl495() -> dict[str, object]:
    return json.loads(
        (
            ROOT
            / "results/"
            "closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.json"
        ).read_text(encoding="utf-8")
    )


def _wl529() -> dict[str, object]:
    return build_wl529_v5_l1_t5_square_locus(wl495=_wl495())


def test_wl529_builds_only_the_selected_v5_l1_t5_square_locus() -> None:
    audit = _wl529()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["work_log"] == "wl529"
    assert audit["object_layer"] == "single_cover_family_square_specialization_locus"

    assert audit["prototype_scope"] == {
        "support": "v_5",
        "L": 1,
        "T": 5,
        "d_vector": {"d_minus_p": 5, "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": 5},
        "candidate_ids": [
            "AA_A1_B4_v_5_m_tail_refresh_candidate",
            "BB_A4_B1_v_5_m_tail_refresh_candidate",
        ],
        "touches_only_one_cover_family": True,
    }


def test_wl529_records_exact_square_locus_models_and_identities() -> None:
    audit = _wl529()

    models = audit["square_locus_models"]
    assert models["square_locus_affine_curve"]["definition"] == "U^2 = t^4 + 78*t^2 + 7921"
    assert models["square_locus_and_elliptic_quotient"]["elliptic_quotient"] == (
        "Y^2 = X^3 + 78*X^2 + 7921*X"
    )
    assert models["projective_intersection_of_quadrics"] == [
        "V*Z = T^2 + 39*Z^2",
        "U^2 = V^2 + 6400*Z^2",
    ]
    assert all(check["verified"] is True for check in audit["identity_checks"])


def test_wl529_preimage_exclusion_is_an_executable_certificate() -> None:
    audit = _wl529()

    preimage = audit["rational_point_analysis"]["t_zero_preimage_analysis"]
    assert preimage["certificate_verified"] is True
    assert preimage["t_zero_forces_y_zero"] is True
    assert preimage["quadratic_discriminant_computed"] is True
    assert preimage["discriminant"] == 29696
    assert preimage["discriminant_factorization"] == {"2": 10, "29": 1}
    assert preimage["discriminant_is_rational_square"] is False
    assert preimage["rational_preimage_exists_on_wl528_quartic"] is False


def test_wl529_closes_the_positive_square_specialization_gap_for_this_one_family() -> None:
    audit = _wl529()

    certificate = audit["genus_one_certificate"]
    assert certificate["status"] == "ok"
    assert certificate["rank"] == 0
    assert certificate["rank_method"] == "E.rank(proof=True)"
    assert certificate["rank_is_proved"] is True
    assert certificate["torsion_invariants"] == [4]
    assert certificate["square_x_values"] == ["0"]

    analysis = audit["rational_point_analysis"]
    assert analysis["affine_square_locus_rational_t_candidates"] == [0]
    assert (
        analysis["t_zero_preimage_analysis"]["rational_preimage_exists_on_wl528_quartic"]
        is False
    )
    assert analysis["nonexceptional_positive_square_specializations_exist"] is False

    proof = audit["proof_status"]
    assert proof["divisor_parity_only_proves_generic_nonsquareness"] is True
    assert proof["genus_one_rational_point_certificate_proved_here"] is True
    assert proof["one_family_positive_square_obstruction_proved_here"] is True
    assert proof["uniform_cover_family_obstruction_proved_here"] is False


def test_wl529_status_fails_when_square_locus_identity_check_fails(monkeypatch) -> None:
    monkeypatch.setattr(
        wl529_module,
        "_square_locus_identity_checks",
        lambda: [
            {
                "check_id": "broken_identity",
                "identity": "0 = 1",
                "verified": False,
            }
        ],
    )

    audit = _wl529()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "square_locus_identity_check_failed" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl529_status_fails_when_genus_one_certificate_does_not_close_rational_points(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        wl529_module,
        "_sage_genus_one_certificate",
        lambda: {
            "status": "ok",
            "rank": 1,
            "rank_method": "E.rank(proof=True)",
            "rank_is_proved": True,
            "torsion_invariants": [4],
            "square_x_values": ["0", "1"],
        },
    )

    audit = _wl529()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "genus_one_rational_point_certificate_failed" in audit["violations"]
    assert "nonexceptional_positive_square_specialization_not_closed" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl529_status_fails_when_t_zero_preimage_certificate_fails(monkeypatch) -> None:
    monkeypatch.setattr(
        wl529_module,
        "_t_zero_preimage_analysis",
        lambda: {
            "certificate_verified": False,
            "rational_preimage_exists_on_wl528_quartic": None,
        },
    )

    audit = _wl529()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "t_zero_preimage_certificate_failed" in audit["violations"]
    assert "nonexceptional_positive_square_specialization_not_closed" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl529_keeps_route_boundaries_and_forbidden_claims_false() -> None:
    audit = _wl529()

    assert audit["shell11_executed_here"] is False
    assert audit["m_tail_diagnostics_extended_here"] is False
    assert audit["new_supports_computed_here"] is False
    assert audit["new_c_d_solubility_tested_here"] is False
    assert audit["wl491_filter_applied_to_new_point_here"] is False
    assert audit["broad_rank_or_selmer_diagnostics_run"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["uniform_m_tail_full_rank_claimed"] is False
    assert audit["family_exclusion_proved_count"] == 0
    assert audit["old_package_x_coordinate_collapse_used"] is False
    assert audit["package_x_s_tilde_bridge_used"] is False
    assert audit["advance_to_next_cover_family"] is False
    assert audit["advance_to_next_roadmap_step"] is False
    assert audit["stop_after_current_task"] is True


def test_wl529_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl529.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--wl495",
            str(
                ROOT
                / "results/"
                "closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.json"
            ),
            "--out",
            str(out),
            "--strict",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "status=ok" in result.stdout
    assert "work_log=wl529" in result.stdout
    assert "one_family_positive_square_obstruction_proved_here=True" in result.stdout
    assert "uniform_cover_family_obstruction_proved_here=False" in result.stdout
    assert "shell11_executed_here=False" in result.stdout
    assert payload["work_log"] == "wl529"
