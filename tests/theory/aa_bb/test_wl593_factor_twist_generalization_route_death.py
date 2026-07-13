from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
SCRIPT = ROOT / "scripts/theory/aa_bb/wl593_factor_twist_generalization_route_death.py"
sys.path.insert(0, str(ROOT))


def _module():
    assert SCRIPT.is_file()
    return importlib.import_module(
        "scripts.theory.aa_bb.wl593_factor_twist_generalization_route_death"
    )


def test_wl593_compares_only_the_frozen_inputs_and_accepts_outcome_3() -> None:
    payload = _module().build_wl593_factor_twist_generalization_route_death()

    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["work_log"] == "wl593"
    assert payload["input_work_logs"] == ["wl587", "wl589", "wl590", "wl591", "wl592"]
    assert payload["accepted_outcome"] == "route_death_certificate"
    assert payload["verification"]["violations"] == []
    assert all(payload["verification"]["checks"].values())
    assert payload["conclusion"] == (
        "The current fixed-representative factor-twist local-image mechanism "
        "cannot be promoted from these fixed inputs alone; it requires new "
        "parameterized family-level coefficient/local-image input."
    )


def test_wl593_verifies_fixed_bases_and_nonshared_data() -> None:
    payload = _module().build_wl593_factor_twist_generalization_route_death()
    comparison = payload["fixed_input_comparison"]

    assert comparison["bases"]["pure_u7"]["base"] == "Spec(Q)"
    assert comparison["bases"]["mixed_u3_v5_w17"]["base"] == "Spec(Q)"
    assert comparison["difference_checks"] == {
        "coefficient_data_differ": True,
        "source_data_differ": True,
        "factor_data_differ": True,
        "bad_prime_supports_differ": True,
    }
    assert comparison["bases"]["pure_u7"]["bad_prime_support"] == [
        2,
        3,
        5,
        7,
        53,
        97,
        277,
    ]
    assert comparison["bases"]["mixed_u3_v5_w17"]["bad_prime_support"] == [
        2,
        3,
        5,
        7,
        17,
        29,
        37,
    ]
    assert "Q_p^*/Q_p^{*2}" in payload["local_image_quantifier"]
    assert "factor-zero" in payload["local_image_quantifier"]
    assert "positivity" in payload["local_image_quantifier"]


def test_wl593_records_p5_disagreement_and_mixed_instance_chain() -> None:
    payload = _module().build_wl593_factor_twist_generalization_route_death()

    p5 = payload["p5_comparison"]
    assert p5["prime"] == 5
    assert p5["pure_u7_image"] == []
    assert p5["mixed_u3_v5_w17_image"] == ["[5]"]
    assert p5["images_disagree"] is True

    chain = payload["mixed_instance_chain"]
    assert chain["p5_survivors"] == [5, 3045, 66045, 91205]
    assert chain["p7_prime"] == 7
    assert chain["p7_image"] == ["[1]"]
    assert chain["p7_survivors"] == [91205]
    assert chain["p17_prime"] == 17
    assert chain["p17_image"] == ["[u]"]
    assert chain["p17_target"] == 91205
    assert chain["p17_target_class"] == "[17u]"
    assert chain["p17_target_in_image"] is False
    assert chain["instance_specific"] is True


def test_wl593_retains_all_frozen_boundary_checks() -> None:
    payload = _module().build_wl593_factor_twist_generalization_route_death()
    boundaries = payload["frozen_boundaries"]

    assert all(boundaries["checks"].values())
    assert boundaries["positivity_intervals"] == {
        "pure_u7": "-9<t<9",
        "mixed_u3_v5_w17": "-10<t<10",
    }
    assert boundaries["fixed_cover_equations"] == {
        "pure_u7": "R^2=(N^2+4)*(M^2+4)",
        "mixed_u3_v5_w17": "R^2=(N^2+49)*(M^2+49)",
    }
    assert boundaries["aa_bb_source_products"] == {
        "pure_u7": "(N^2+49)*(M^2+49)=(Z/4)^2",
        "mixed_u3_v5_w17": "(N^2+9)*(M^2+9)=(Z/4)^2",
    }


def test_wl593_strict_cli_output(tmp_path: Path) -> None:
    out = tmp_path / "wl593.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(out), "--strict"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert result.stdout.splitlines() == [
        "status=ok",
        "work_log=wl593",
        "ready=True",
        "accepted_outcome=route_death_certificate",
        "violations=[]",
    ]
    assert json.loads(out.read_text(encoding="utf-8"))["work_log"] == "wl593"
