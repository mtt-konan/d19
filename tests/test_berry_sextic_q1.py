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


def test_q1_separates_ambient_fake_and_norm_objects() -> None:
    payload = _module().build_certificate()
    ambient = payload["ambient_space"]
    descent = payload["descent_object"]
    fake = payload["fake_target"]
    constants = fake["ambient_supported_image"]["constant_subspace"]
    norm = payload["norm_square_kernel"]

    assert payload["schema_version"] == "berry-c1-q1-fake-descent-v2"
    assert ambient["dimension"] == 16
    assert ambient["dimension_claim"] == "conservative ambient S-unit coordinates only"
    assert ambient["is_fake_target"] is False
    assert ambient["is_selmer_group"] is False
    assert descent["target"] == "F_L=L^*/(L^{*2}K^*)"
    assert descent["not_the_16_dimensional_target"] is True
    assert fake["definition"] == ("F_L=L^*/(L^{*2}K^*)=(L^*/L^{*2})/im(K^*/K^{*2} -> L^*/L^{*2})")
    assert constants["definition"] == ("C_S=V_S intersect im(K^*/K^{*2} -> L^*/L^{*2})")
    assert fake["ambient_supported_image"]["definition"] == "F_{L,S}=V_S/C_S"
    assert norm["definition"] == "K_L^N=ker(barN_L: F_L -> K^*/K^{*2})"
    assert norm["is_separate_from_constant_quotient"] is True
    assert norm["dimension"] is None


def test_q1_defines_local_fake_quotient_and_global_localization() -> None:
    payload = _module().build_certificate()
    local = payload["local_fake_quotient"]
    localization = payload["localization"]
    missing = {entry["symbol"]: entry for entry in payload["q2_missing_matrices"]}

    assert local["fake_quotient"]["definition"] == "F_pi=A_pi^*/(A_pi^{*2}K_pi^*)"
    assert local["norm_square_kernel"] == "H_pi=ker(N_pi)"
    assert local["accepted_j_over_2j_dimension"] == 2
    assert local["local_fake_image_computed"] is False
    assert local["local_basis_or_generators_supplied"] is False
    assert localization["global_map"] == "loc_pi^fake: F_L -> F_pi"
    assert localization["ambient_coordinate_map"].startswith("Lambda_pi,S=")
    assert localization["matrix"]["symbol"] == "M_loc_pi"
    assert {"M_const", "M_norm", "M_loc_pi"} == set(missing)
    assert all(entry["status"] == "missing" for entry in missing.values())


def test_q1_restates_infinity_kernel_without_torsion_overclaim() -> None:
    payload = _module().build_certificate()
    infinity = payload["infinity_kernel"]
    d_inf = payload["d_inf_kummer"]

    assert infinity["class"] == "D_inf=[P_+-P_-] in J(K)/2J(K)"
    assert "lies in the kernel" in infinity["kernel_statement"]
    assert "D_inf is nonzero torsion in J(K)" in infinity["not_claimed"]
    assert d_inf["fake_class"] == "[1]=0 in F_L"
    assert d_inf["ambient_representative"]["coordinate_vector"] == [0] * 16
    assert "not a coordinate vector for F_L" in d_inf["ambient_representative"]["meaning"]


def test_q1_explicitly_does_not_claim_later_stages() -> None:
    not_proved = _module().build_certificate()["proof_boundary"]["not_proved"]
    assert "any local Kummer image or local generator" in not_proved
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
    assert "berry-c1-q1-fake-descent-v2" in result.stdout
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["ambient_space"]["dimension"] == 16
    assert saved["ambient_space"]["is_fake_target"] is False
    assert saved["d_inf_kummer"]["ambient_representative"]["coordinate_vector"] == [0] * 16
