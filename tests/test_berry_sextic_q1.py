import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/theory/berry_sextic_q1.py"
sys.path.insert(0, str(ROOT))


def _module():
    from scripts.theory import berry_sextic_q1

    return berry_sextic_q1


def test_q1_freezes_fake_object_and_infinity_kernel() -> None:
    payload = _module().build_certificate()
    descent = payload["descent_object"]
    infinity = payload["infinity_kernel"]
    d_inf = payload["d_inf_kummer"]

    assert payload["schema_version"] == "berry-c1-q1-fake-descent-v1"
    assert descent["target"] == "L^*/L^{*2}K^*"
    assert descent["norm_condition"] == "N_{L/K}(alpha) in K^{*2}"
    assert descent["squareclass_dimension"] == 16
    assert infinity["even_degree_kernel"] == "<P_+-P_-> in J(K)/2J(K)"
    assert d_inf["fake_class"] == "1 in L^*/L^{*2}K^*"
    assert all(value == 0 for value in d_inf["coordinate_vector"])


def test_q1_explicitly_does_not_claim_later_stages() -> None:
    not_proved = _module().build_certificate()["proof_boundary"]["not_proved"]
    assert "either local Kummer image" in not_proved
    assert "fake Selmer or true Selmer dimension" in not_proved
    assert "rank or saturation" in not_proved
    assert "the set of rational t-values" in not_proved


def test_q1_cli_round_trip(tmp_path: Path) -> None:
    out = tmp_path / "berry-c1-q1.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(out)],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert "berry-c1-q1-fake-descent-v1" in result.stdout
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["d_inf_kummer"]["coordinate_vector"] == [0] * 16
