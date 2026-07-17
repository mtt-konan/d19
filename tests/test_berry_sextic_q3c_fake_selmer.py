"""Focused checks for the Berry Q3c fake-to-true Selmer boundary."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))


def _result():
    from scripts.theory.berry_sextic_q3c_fake_selmer import verify_q3c

    return verify_q3c()


def test_q3c_universal_boundary_lemma_has_exact_algebra_checks() -> None:
    from scripts.theory.berry_sextic_q3c_fake_selmer import (
        verify_universal_divisor_evaluation_lemma,
    )

    lemma = verify_universal_divisor_evaluation_lemma()
    assert lemma["status"] == "proved_lemma"
    assert lemma["boundary_identity"] == "partial_F(-1)=kappa_F(D_inf)"
    assert all(lemma["machine_checked_identities"].values())
    assert lemma["machine_checked_identities"]["factor_zero_other_root_sign"] is True


def test_q3c_pulls_back_the_two_intersection_classes_exactly() -> None:
    result = _result()
    assert result["status"] == "ok"
    assert result["accepted_outcome"] == (
        "q3c_exact_supported_fake_selmer_true_lift_with_universal_boundary_lemma"
    )
    pullback = result["pullback"]
    assert pullback["quotient_coordinates"] == ["110100", "010100"]
    assert pullback["intersection_basis"] == ["01111000", "01100010"]
    assert [entry["ambient_labels"] for entry in pullback["ambient_representatives"]] == [
        ["epsilon_1", "epsilon_2", "epsilon_4"],
        ["epsilon_2", "epsilon_4"],
    ]
    assert [entry["ambient_coordinates"] for entry in pullback["ambient_representatives"]] == [
        "0110100000000000",
        "0010100000000000",
    ]
    assert pullback["fake_selmer_dimension"] == 2


def test_q3c_outside_support_is_not_assumed_from_pi_and_varpi() -> None:
    result = _result()
    support = result["support"]
    assert support["allowed_support_base_places"] == ["1+i", "94*i-169"]
    assert support["reduction_status"] == {
        "1+i": "unresolved",
        "94*i-169": "bad_reduction_proved",
        "-94*i-169": "good_reduction_proved",
        "outside_allowed_support": "good_reduction_proved",
    }
    assert support["good_conjugate_place"] == "-94*i-169"
    assert support["model_support_prime_count"] == 6
    assert support["conservative_support_prime_count"] == 10
    assert support["class_group_trivial"] is True


def test_q3c_true_selmer_sequence_keeps_brauer_and_dinf_distinct() -> None:
    result = _result()
    true_lift = result["true_lift"]
    assert true_lift["brauer_cokernel"] == "ker(Br(K)[2] -> Br(L)[2])"
    assert true_lift["brauer_cokernel_kept_separate"] is True
    assert true_lift["universal_boundary_lemma"]["status"] == "proved_lemma"
    assert all(true_lift["universal_boundary_lemma"]["machine_checked_identities"].values())
    assert true_lift["infinity_boundary_identity_proved"] is True
    assert true_lift["true_selmer_sequence"] == (
        "0 -> F_2<kappa(D_inf)> -> Sel_2(J/K) -> Sel_fake^S -> 0"
    )
    assert true_lift["global_norm_image"] == ["+1"]
    assert true_lift["norm_zero_fake_classes_have_global_h1_lifts"] is True
    assert true_lift["local_fake_membership_makes_every_h1_lift_kummer"] is True
    assert true_lift["global_dinf_nonzero"] is True
    assert true_lift["kernel_dimension"] == 1
    assert true_lift["true_selmer_dimension"] == 3
    assert true_lift["true_selmer_upper_bound"] == 3
    assert result["rank_claimed"] is False
    assert result["saturation_claimed"] is False
    assert result["rational_t_claimed"] is False
