from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.b1_prototype import (
    B1Error,
    build_b1,
    load_sage_certificate,
    project_b1,
)
from scripts.theory.aa_bb.consolidation_inputs import B0Document, load_b0
from tests.theory.aa_bb.projection_digests import assert_projection_digest

DATA = ROOT / "data/theory/aa_bb/wl500"
SAGE_ARTIFACT = DATA / "b1-sage-certificate.v1.json"
IGNORED_RESULT = (
    ROOT / "results" / "closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.json"
)


def _build():
    return build_b1(b0=load_b0(DATA), sage_certificate=load_sage_certificate(SAGE_ARTIFACT))


def _write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_b1_recomputes_wl528_function_field_and_nonsquare_specialization() -> None:
    payload = _build().projections["wl528"]
    model = payload["function_field_model"]
    assert payload["status"] == "ok"
    assert model["function_field"] == "Q(r,y)/(y^2 - (5*r^4 - 264*r^2 + 2000))"
    assert model["derived_from_complete_d_equations"] == [
        "X - 42 = 5*u_minus_p^2",
        "X - 58 = u_pos_2sqrt_q^2",
        "X + 58 = 5*u_neg_2sqrt_q^2",
        "5*u_minus_p^2 - u_pos_2sqrt_q^2 = 16",
        "u_minus_p^2 - u_neg_2sqrt_q^2 = -20",
    ]
    assert all(model["identity_checks"].values())
    certificate = payload["opposite_side_product"]["function_field_nonsquare_certificate"]
    assert certificate["values"] == {
        "r": 10,
        "y": 160,
        "u_minus_p": 4,
        "u_pos_2sqrt_q": 8,
        "u_neg_2sqrt_q": 6,
        "X": 122,
        "Y": 960,
        "t": 6,
        "N": "11/2",
        "M": "-1/2",
    }
    assert set(certificate["checks"]) == {
        "specialization_lies_on_quartic",
        "specialization_is_smooth",
        "chart_open_denominators_nonzero",
        "maps_to_recorded_cover_point",
        "maps_to_recorded_e_point",
        "specialized_t_n_m_match_recorded_values",
        "opposite_product_matches_recorded_value",
        "opposite_product_regular_and_nonzero_at_specialization",
        "specialized_value_is_not_rational_square",
    }
    assert all(certificate["checks"].values())
    assert certificate["specialized_value"] == "12025/16"
    assert certificate["specialized_value_is_rational_square"] is False


def test_b1_preserves_positivity_exceptions_and_theorem_boundary() -> None:
    b1 = _build()
    wl528, wl529 = b1.projections["wl528"], b1.projections["wl529"]
    exceptional = wl528["exceptional_divisors_and_positivity"]
    assert exceptional["poles_or_undefined_loci"] == [
        "r = 0 for the chosen cover chart",
        "r^2 = 20 where X+p = 0 and the centered-even t map is undefined",
    ]
    assert "M positivity fails" in exceptional["positivity_status"]
    assert wl529["square_locus_models"]["positivity_domain"] == "|t| < 5"
    for payload in (wl528, wl529):
        assert payload["complete_selmer_upper_bound_proved"] is False
        assert payload["rank_zero_claimed"] is False
        assert payload["family_exclusion_proved_count"] == 0
        assert payload["advance_to_next_cover_family"] is False
        assert payload["stop_after_current_task"] is True
    assert wl528["proof_status"]["uniform_cover_family_obstruction_proved_here"] is False
    assert wl529["proof_status"]["uniform_cover_family_obstruction_proved_here"] is False


def test_b1_keeps_one_way_quotient_and_closes_only_the_t_zero_lift() -> None:
    wl529 = _build().projections["wl529"]
    models = wl529["square_locus_models"]
    assert models["square_locus_affine_curve"]["definition"] == "U^2 = t^4 + 78*t^2 + 7921"
    quotient = models["square_locus_and_elliptic_quotient"]
    assert quotient["degree_two_map"] == "X = t^2, Y = t*U"
    assert "not asserted to be a birational equivalence" in quotient["point_classification_rule"]
    assert all(check["verified"] for check in wl529["identity_checks"])
    analysis = wl529["rational_point_analysis"]
    assert analysis["affine_square_locus_rational_t_candidates"] == [0]
    t_zero = analysis["t_zero_preimage_analysis"]
    assert t_zero["t_zero_forces_y_zero"] is True
    assert t_zero["derived_r2_equation"] == "5*x^2 - 264*x + 2000 = 0 with x = r^2"
    assert t_zero["discriminant"] == 29696
    assert t_zero["discriminant_factorization"] == {"2": 10, "29": 1}
    assert t_zero["rational_preimage_exists_on_wl528_quartic"] is False


def test_sage_artifact_records_proved_rank_full_torsion_and_square_x() -> None:
    certificate = load_sage_certificate(SAGE_ARTIFACT).document
    assert certificate["curve"]["a_invariants"] == [0, 78, 0, 7921, 0]
    sage = certificate["sage"]
    assert (sage["rank"], sage["rank_method"], sage["rank_is_proved"]) == (
        0,
        "E.rank(proof=True)",
        True,
    )
    assert sage["torsion_invariants"] == [4]
    assert sage["torsion_points"] == [
        {"kind": "infinity"},
        {"x": "0", "y": "0", "x_is_rational_square": True},
        {"x": "89", "y": "-1424", "x_is_rational_square": False},
        {"x": "89", "y": "1424", "x_is_rational_square": False},
    ]
    assert sage["square_x_values"] == ["0"]


@pytest.mark.parametrize(
    ("key", "value"),
    [("rank_is_proved", False), ("torsion_invariants", [2, 2]), ("square_x_values", ["0", "1"])],
)
def test_sage_artifact_fails_closed_on_proof_boundary_mutations(
    tmp_path: Path, key: str, value: object
) -> None:
    payload = json.loads(SAGE_ARTIFACT.read_text(encoding="utf-8"))
    payload["sage"][key] = value
    with pytest.raises(B1Error, match="exact rank/torsion/square-X"):
        load_sage_certificate(_write_json(tmp_path / "certificate.json", payload))


def test_runtime_loaders_refuse_results_paths() -> None:
    with pytest.raises(B1Error, match="runtime refuses ignored results path"):
        load_sage_certificate(IGNORED_RESULT)


def test_sage_artifact_fails_closed_on_provenance_drift(tmp_path: Path) -> None:
    payload = json.loads(SAGE_ARTIFACT.read_text(encoding="utf-8"))
    payload["provenance"]["source_payload_sha256"] = "0" * 64
    with pytest.raises(B1Error, match="legacy source binding is incomplete"):
        load_sage_certificate(_write_json(tmp_path / "certificate.json", payload))


def test_b1_fails_closed_when_tracked_b0_row_drifts() -> None:
    document = deepcopy(load_b0(DATA).document)
    document["rows"][0]["complete_d_cover"]["root_values"]["e_pos"] = 60
    with pytest.raises(B1Error, match="prototype input drift"):
        build_b1(b0=B0Document(document), sage_certificate=load_sage_certificate(SAGE_ARTIFACT))


def test_full_projections_have_frozen_digests() -> None:
    b1 = _build()
    for work_log in ("wl528", "wl529"):
        assert_projection_digest("b1", work_log, project_b1(b1, work_log))


def test_b1_python_cli_smoke_uses_tracked_inputs(tmp_path: Path) -> None:
    output = tmp_path / "b1.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/theory/aa_bb/b1_prototype.py"),
            "--data-dir",
            str(DATA),
            "--sage-artifact",
            str(SAGE_ARTIFACT),
            "--out",
            str(output),
            "--strict",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert "status=ok work_log=b1" in completed.stdout
    assert payload["wl528"]["ready"] is True
    assert payload["wl529"]["ready"] is True
