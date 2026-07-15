"""Exact Q2c constant, norm, localization, and lift checks."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))


def _module():
    from scripts.theory import berry_sextic_q2c_maps as q2c

    return q2c


def test_q2c_builds_and_verifies_all_exact_maps() -> None:
    q2c = _module()
    certificate = q2c.build_certificate()

    assert certificate["status"] == "ok"
    assert certificate["constant_matrix_rank"] == 4
    assert certificate["norm_matrix_rank"] == 4
    assert certificate["combined_equation_rank"] == 8
    assert all(certificate["checks"].values())


def test_q2c_norm_values_and_matrices_are_fixed_in_the_payload_order() -> None:
    q2c = _module()
    certificate = q2c.build_certificate()

    assert certificate["ambient_labels"] == list(q2c.LABELS)
    assert certificate["norm_values"] == [list(value) for value in q2c.NORM_VALUES]
    assert certificate["constant_matrix_columns"] == [list(row) for row in q2c.M_CONST]
    assert certificate["norm_matrix_rows"] == [list(row) for row in q2c.M_NORM]


def test_q2c_localization_uses_q2a_h_basis_and_global_lifts_exist() -> None:
    q2c = _module()
    certificate = q2c.build_certificate()
    labels = certificate["ambient_labels"]

    assert certificate["local_flat_order"] == [
        "a_1",
        "b_1",
        "a_2",
        "b_2",
        "c",
        "d",
        "e",
        "f",
    ]
    assert certificate["local_h_order"] == ["h_varpi", "h_nu", "h_r", "h_u"]

    beta_12 = certificate["beta_solutions"]["beta_12"]
    beta_r = certificate["beta_solutions"]["beta_r"]
    assert [labels[index] for index, bit in enumerate(beta_12["ambient_vector"]) if bit] == [
        "epsilon_1"
    ]
    assert [labels[index] for index, bit in enumerate(beta_r["ambient_vector"]) if bit] == [
        "epsilon_1",
        "epsilon_4",
    ]
    assert beta_12["solution_space_dimension"] == 8
    assert beta_r["solution_space_dimension"] == 8


def test_q2c_audits_zero_support_and_unramified_pi_normalization() -> None:
    q2c = _module()
    certificate = q2c.build_certificate()
    local_data = certificate["local_hensel_data"]
    assert local_data["pi_to_varpi_linear_bit"] == 1
    assert local_data["pi_to_varpi_unramified_bit"] == 0

    audit = {
        record["label"]: record
        for record in local_data["zero_audit"]
        if record["zero_factor"] is not None
    }
    assert {label: record["zero_factor"] for label, record in audit.items()} == {
        "S_prime_3": "F1",
        "S_prime_4": "F2",
        "S_prime_7": "Fr",
        "S_prime_9": "Fu",
    }
    assert audit["S_prime_9"]["norm_pi_valuation"] == 2
    assert audit["S_prime_9"]["local_valuation"] == 1
    assert certificate["local_flat_matrix_rows"][7][14] == 1
