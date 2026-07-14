from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/theory/berry_sextic_pilot.py"
sys.path.insert(0, str(ROOT))


def _module():
    import scripts.theory.berry_sextic_pilot as pilot

    return pilot


def test_visual_row_and_exact_pullback_certificate() -> None:
    payload = _module().build_certificate()

    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["outcome"] == "berry_sextic_pipeline_ready"
    assert payload["verification"]["violations"] == []
    assert all(payload["verification"]["checks"].values())
    assert payload["selected_curve"]["visual_transcription_checked"] is True
    assert payload["selected_curve"]["symbolic_substitution_checked"] is True
    assert payload["surface"]["pullback_degree"] == 12
    assert payload["surface"]["smooth_projective_genus"] == 5


def test_projective_nodes_inverse_and_trivial_points_are_retained() -> None:
    boundary = _module().build_certificate()["projective_and_degenerate_parameters"]
    inverse = _module().build_certificate()["map_and_converse"]

    assert boundary["basepoint_free"] is True
    assert boundary["rational_branch_parameters"].startswith("none")
    assert len(boundary["known_rational_trivial_points"]) == 2
    assert "h(t)=0" in boundary["node_preimages"]
    assert "generic_inverse" in inverse
    assert "infinity via F(A,B)" in inverse["converse"]


def test_qi_factorization_and_realized_support_are_finite() -> None:
    payload = _module().build_certificate()
    factor = payload["Q_i_factorization"]
    support = payload["realized_support_descent"]

    assert factor["factorization_over_Qi"] == {
        "g_is_irreducible": True,
        "gbar_is_irreducible": True,
    }
    assert factor["gcd_common_root"] == "1"
    assert factor["resultant"] == "2^40"
    assert support["support_group"] == "<i>={1,i} in Q(i)^*/Q(i)^{*2}"
    assert len(support["covers"]) == 2
    assert "t in P^1(Q)" in support["exact_obligation"]
    assert payload["quotient_and_jacobian_audit"]["genuine_Qi_PGL2_quotient"] is False
    assert payload["quotient_and_jacobian_audit"]["rank_or_decomposition_obtained"] is False


def test_strict_cli_materializes_certificate(tmp_path: Path) -> None:
    out = tmp_path / "berry-sextic-pilot.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert result.stdout.splitlines() == [
        "status=ok",
        "task=berry-sextic-pilot-feasibility-certificate",
        "ready=True",
        "outcome=berry_sextic_pipeline_ready",
        "violations=[]",
    ]
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["realized_support_descent"]["covers"][0]["genus"] == 2
