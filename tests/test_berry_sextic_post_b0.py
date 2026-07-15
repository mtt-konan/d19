from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/theory/berry_sextic_post_b0.py"
sys.path.insert(0, str(ROOT))


def _audit():
    from scripts.theory.berry_sextic_post_b0 import build_post_b0_audit

    return build_post_b0_audit()


def test_local_obstruction_keeps_all_projective_charts() -> None:
    local = _audit()["local_obstruction"]

    assert local["uniformizer"] == "pi=1+i"
    assert local["shifted_coefficient_valuations_low_to_high"] == [11, 10, 8, 9, 3, 2, 0]
    assert [row["v_pi(f(t))"] for row in local["valuation_partition"]] == [0, 6, 13, 11]
    assert local["v_pi_z_equals_2_residue_table"][-1]["Q(u)/pi^2_mod_pi"] == 1
    assert local["reciprocal_chart"]["coordinates"] == "x=1/t, w=v/t^3"
    assert "no K_(1+i)-point" in local["conclusion"]


def test_torsion_rows_use_primary_safe_specialization_bound() -> None:
    torsion = _audit()["torsion"]
    assert len(torsion["rows"]) >= 4
    assert torsion["raw_gcd_all_rows"] == {"C_1": 1, "C_i": 1}
    assert torsion["primary_safe_bound"]["C_1"] == 1
    assert torsion["primary_safe_bound"]["C_i"] == 1
    assert torsion["conclusion"] == "J_1(K)_tors=0 and J_i(K)_tors=0."


def test_support_distinguishes_sufficient_and_conservative_sets() -> None:
    support = _audit()["support"]
    assert support["model_sufficient_finite_support"] == ["(1+i)", "(94*i-169)"]
    assert support["minimality_claimed"] is False
    assert "(-94*i-169)" in support["conservative_finite_support"]
    assert "units" in support["extra_support_explanation"]["leading_coefficient"]
    assert "not Jacobian 2-descent support" in support["extra_support_explanation"]["chart_primes"]
    assert support["exact_base_field_squareclass_probe"]["orders"] == [2, 2, 2]


def test_toolchain_result_does_not_promote_a_dyadic_selmer_blocker() -> None:
    toolchain = _audit()["toolchain"]
    assert toolchain["sage"]["version"].startswith("10.9")
    assert toolchain["magma"]["executable_found"] is False
    assert toolchain["public_magma_calculator"]["version"] == "2.29-8"
    assert toolchain["public_magma_calculator"]["full_two_selmer_attempt"] == "service_timeout"
    assert toolchain["arithmetic_blocker_promoted"] is False


def test_post_b0_cli_materializes_certificate(tmp_path: Path) -> None:
    out = tmp_path / "berry-sextic-post-b0.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(out)],
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert result.returncode == 0
    assert result.stdout.splitlines() == [
        "status=complete",
        "task=berry-sextic-post-b0-feasibility",
        "outcome=post_b0_feasibility_audit",
        "C_i_local_at_(1+i)=obstructed",
        "J_1_torsion_bound=1",
        "J_i_torsion_bound=1",
        "arithmetic_blocker_promoted=False",
    ]
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["accepted_b0_checkpoint"] == "dccbd9a"
    assert saved["stable_model_required_before_B1_B2"] is False
