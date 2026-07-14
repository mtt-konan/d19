from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
SCRIPT = ROOT / "scripts/theory/aa_bb/hrl_relative_descent_design.py"
sys.path.insert(0, str(ROOT))


def _module():
    assert SCRIPT.is_file()
    return importlib.import_module("scripts.theory.aa_bb.hrl_relative_descent_design")


def test_certificate_reconstructs_the_declared_matrix_and_kernel() -> None:
    payload = _module().build_hrl_relative_descent_design()
    matrix = payload["certificate"]["matrix"]

    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["accepted_input"] == "non_base_pullback_candidate_ready"
    assert payload["accepted_outcome"] == "precise_twist_support_blocker"
    assert matrix["columns"] == [
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
    ]
    assert matrix["shape"] == [160, 21]
    assert len(matrix["row_labels"]) == len(matrix["matrix"]) == 160
    assert all(len(row) == 21 for row in matrix["matrix"])
    assert matrix["rank_F2"] == 14
    assert matrix["kernel_dimension"] == 7
    assert matrix["kernel_basis_supports"] == [
        ["d13", "s13"],
        ["d13", "d24"],
        ["d13", "s24"],
        ["d12", "s12", "d34", "s34"],
        ["d12", "s12", "t"],
        ["d14", "s14", "l_plus"],
        ["d23", "s23", "l_minus"],
    ]
    assert matrix["relative_quotient"] == {
        "alternate_representative": "d13*s24",
        "cross_pair_relation": "(d13*s24)/(d13*d24)=4*Delta/d24^2",
        "dimension": 1,
        "representative": "H_RL=(r1-r3)*(r2-r4)=d13*d24",
        "trivial_relations": [
            "d13*s13=4*Delta",
            "d12*s12*d34*s34=(4*T*t)^2",
            "d12*s12*t=4*T*t^2",
            "d14*s14*l_plus=4*l_plus^2",
            "d23*s23*l_minus=4*l_minus^2",
        ],
    }
    assert payload["verification"]["violations"] == []
    assert all(payload["verification"]["checks"].values())


def test_certificate_reconstructs_hrl_divisor_and_ha_pullback() -> None:
    payload = _module().build_hrl_relative_descent_design()
    details = payload["certificate"]["divisor_and_pullback"]

    assert details["H_RL"]["definition"] == "(r1-r3)*(r2-r4)"
    assert details["H_RL"]["difference_relations"] == [
        "d13*s13=r1^2-r3^2=4*Delta",
        "d24*s24=r2^2-r4^2=4*Delta",
    ]
    assert details["H_RL"]["infinity_valuation_multiset"] == {
        "-2": 4,
        "0": 8,
        "2": 4,
    }
    assert "eps1=eps3,eps2=eps4" in details["H_RL"]["divisor"]
    assert details["H_RL"]["deck_action"]["e1e3"] == "H_RL -> -H_RL"
    assert details["H_A"]["norm_identity"] == ("(z_A+u_A)*(z_A-u_A)=16*A^2*t^2")
    assert details["H_A"]["pullback_divisor"] == ("2*pi_12^*(W_(0,+)-I_+) on C")
    assert details["H_A"]["class"].startswith("[H_A]=pi_12^*")


def test_twist_audit_stops_at_the_exact_infinite_support_blocker() -> None:
    payload = _module().build_hrl_relative_descent_design()
    twist = payload["twist_audit"]
    quotient = twist["twist_parameter_quotient"]

    assert quotient["twist_scope"] == "d is a base/parameter scalar in K^*"
    assert quotient["intrinsic_unscaled"] == "K^*/K^{*2}"
    assert quotient["scale_quotiented"] == "k^*/k^{*2} with k=Q(lambda)"
    assert quotient["fixed_rational_specialization"] == "Q^*/Q^{*2}"
    assert quotient["deck_orbit_quotient_scale_quotiented"] == ("k^*/(k^{*2}*<-1,lambda^2-1>)")
    support = twist["support_test"]
    assert support["infinite_family"] == "d_c=lambda-c for c in Q, c not equal to +/-1"
    assert "Distinct c give distinct odd valuations" in support["valuation_proof"]
    assert "no finite parameter-uniform" in support["conclusion"]
    assert "global divisor/norm/lift theorem" in twist["missing_input"]
    assert payload["proof_boundary"]["finite_twist_support_proved"] is False
    assert payload["proof_boundary"]["candidate_automatic_on_restricted_image_proved"] is False
    assert payload["proof_boundary"]["local_prime_tables_run"] is False
    assert all(payload["retained_constraints"].values())


def test_strict_cli_materializes_the_certificate(tmp_path: Path) -> None:
    out = tmp_path / "hrl-relative-descent.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert result.stdout.splitlines() == [
        "status=ok",
        "task=universal-four-factor-hrl-relative-descent-design",
        "ready=True",
        "accepted_outcome=precise_twist_support_blocker",
        "matrix_shape=[160, 21]",
        "rank_F2=14",
        "kernel_dimension=7",
        "violations=[]",
    ]
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["certificate"]["matrix"]["shape"] == [160, 21]
    assert saved["accepted_outcome"] == "precise_twist_support_blocker"
