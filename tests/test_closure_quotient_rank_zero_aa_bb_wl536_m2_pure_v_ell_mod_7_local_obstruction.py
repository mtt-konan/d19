from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def _module():
    try:
        return importlib.import_module(
            "scripts.theory."
            "audit_closure_quotient_rank_zero_aa_bb_wl536_m2_pure_v_ell_mod_7_local_obstruction"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(str(exc))


def _audit() -> dict[str, object]:
    return _module().build_wl536_m2_pure_v_ell_mod_7_local_obstruction()


def test_wl536_records_the_exact_mod_7_local_obstruction() -> None:
    audit = _audit()

    assert audit["status"] == "ok"
    assert audit["ready"] is True
    assert audit["work_log"] == "wl536"
    assert audit["object_layer"] == "m2_q_root_coordinate_mod_7_local_obstruction_inside_wl535"
    assert audit["family_scope"] == {
        "support": "v_ell",
        "L": 1,
        "T": "ell",
        "d_vector": {"d_minus_p": "ell", "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": "ell"},
        "parameter_restrictions": [
            "ell is an odd prime with ell ≡ 1 mod 4",
            "ell ≡ 5 mod 7",
            "q is rational",
            "ell-q^2 is a rational square",
            "ell*q^2+4 is a rational square",
            "ell*q^4+4*q^2-4*ell is positive",
            (
                "V^2 = q^8 + (16-8*ell)q^6 + (32*ell^2-96*ell+72)q^4 "
                "+ (32*ell-64)q^2 + 16"
            ),
        ],
        "touches_only_M2_for_the_wl535_pure_family": True,
    }


def test_wl536_case_table_eliminates_every_q_square_residue_mod_7() -> None:
    audit = _audit()

    obstruction = audit["local_obstruction"]["mod_7_case_table"]
    assert obstruction["local_prime"] == 7
    assert obstruction["target_ell_residue_mod_7"] == 5
    assert obstruction["square_residues_mod_7"] == [0, 1, 2, 4]
    assert obstruction["g_ell_mod_7_specialization"] == (
        "G_ell(Q) ≡ Q^4 + 4*Q^3 + 5*Q + 2 (mod 7)"
    )
    assert obstruction["integrality_lemma"]["minus_one_is_nonsquare_mod_7"] is True
    assert obstruction["surviving_q_square_residues_mod_7"] == []
    assert obstruction["obstruction_proved"] is True

    cases = {
        entry["q_square_mod_7"]: entry for entry in obstruction["q_square_residue_cases"]
    }
    assert cases[0]["failure_reasons"] == ["ell-q^2 is a nonsquare mod 7"]
    assert cases[1]["failure_reasons"] == ["G_ell(q^2) is a nonsquare mod 7"]
    assert cases[2]["failure_reasons"] == ["ell-q^2 is a nonsquare mod 7"]
    assert cases[4]["failure_reasons"] == ["ell*q^2+4 is a nonsquare mod 7"]
    assert all(entry["survives_all_mod_7_square_conditions"] is False for entry in cases.values())


def test_wl536_proves_only_the_partial_local_obstruction_and_stops() -> None:
    audit = _audit()

    proof = audit["proof_status"]
    assert proof == {
        "wl535_residue_class_ell_eq_5_mod_7_excluded_here": True,
        "local_prime_7_integrality_obstruction_proved_here": True,
        "remaining_problem_shrunk_to_complementary_prime_classes": True,
        "uniform_full_wl535_obstruction_proved_here": False,
        "strict_counterexample_found_here": False,
        "advance_to_m3": False,
    }

    local = audit["local_obstruction"]
    assert "ell ≡ 5 mod 7" in local["statement"]
    assert local["removed_prime_class_mod_28"] == 5
    assert local["remaining_prime_classes_mod_28"] == [1, 9, 13, 17, 25]
    assert local["infinite_prime_subfamily_reason"] == (
        "gcd(5,28)=1, so Dirichlet's theorem gives infinitely many primes "
        "ell congruent to 5 mod 28."
    )
    assert audit["uniform_infinite_subfamily_exclusion_proved_here"] is False
    assert audit["strict_counterexample_found_here"] is False
    assert audit["complete_selmer_upper_bound_proved"] is False
    assert audit["dim_sel2_eq_2_claimed"] is False
    assert audit["rank_zero_claimed"] is False
    assert audit["sha2_trivial_claimed"] is False
    assert audit["advance_to_m3"] is False
    assert audit["stop_after_current_task"] is True


def test_wl536_status_fails_when_input_breaks(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(module, "_wl535_ready", lambda _: False)

    audit = module.build_wl536_m2_pure_v_ell_mod_7_local_obstruction()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "wl535_input_not_ready" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl536_status_fails_when_a_mod_7_survivor_is_left(monkeypatch) -> None:
    module = _module()
    monkeypatch.setattr(
        module,
        "_local_obstruction_data",
        lambda: {
            "obstruction_proved": False,
            "surviving_q_square_residues_mod_7": [1],
        },
    )

    audit = module.build_wl536_m2_pure_v_ell_mod_7_local_obstruction()

    assert audit["status"] == "issues"
    assert audit["ready"] is False
    assert "mod_7_local_obstruction_not_complete" in audit["violations"]
    assert audit["proof_status"] == {}


def test_wl536_cli_writes_result_json(tmp_path: Path) -> None:
    out = tmp_path / "wl536.json"
    script = (
        ROOT
        / "scripts/theory/"
        "audit_closure_quotient_rank_zero_aa_bb_wl536_m2_pure_v_ell_mod_7_local_obstruction.py"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(script),
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
    assert "work_log=wl536" in result.stdout
    assert "wl535_residue_class_ell_eq_5_mod_7_excluded_here=True" in result.stdout
    assert "local_prime_7_integrality_obstruction_proved_here=True" in result.stdout
    assert "advance_to_m3=False" in result.stdout
    assert payload["work_log"] == "wl536"
