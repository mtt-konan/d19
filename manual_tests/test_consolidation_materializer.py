from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.consolidation_inputs import (  # noqa: E402
    A1_SOURCE_FILENAMES,
    A2_SOURCE_SUFFIXES,
    B0_TARGET_IDS,
    CANONICAL_FILES,
    EXPECTED_WITNESS_IDS,
    FROZEN_SOURCE_PAYLOADS,
    SOURCE_FILENAMES,
    SOURCE_PROVENANCE,
    ConsolidationInputError,
    load_a0,
    load_all,
    load_b0,
    load_manifest,
    materialize_a0,
    materialize_all,
    materialize_b0,
    materialize_manifest,
)

RESULTS = ROOT / "results"
CANONICAL_DIR = ROOT / "data" / "theory" / "aa_bb" / "wl500"

SOURCE_FILES = {
    "wl495": RESULTS / "closure_quotient_rank_zero_aa_bb_wl495_route_refreshed_support.json",
    "wl505": RESULTS
    / (
        "closure_quotient_rank_zero_aa_bb_wl505_route_active_shell7_m_tail_supports_"
        "through_ambient_c_d_solubility_then_wl491_filter.json"
    ),
    "wl521": RESULTS
    / "closure_quotient_rank_zero_aa_bb_wl521_support_family_synthesis_after_wl519.json",
    "wl522": RESULTS
    / (
        "closure_quotient_rank_zero_aa_bb_wl522_support_cover_taxonomy_to_lemma_"
        "candidate_checkpoint.json"
    ),
    "wl527": RESULTS
    / "closure_quotient_rank_zero_aa_bb_wl527_function_field_squareclass_proof_data_scope.json",
}

EXPECTED_CONSUMER_PATHS = {
    "wl495": [
        "scripts/theory/aa_bb/consolidation_inputs.py",
        "scripts/theory/aa_bb/b1_prototype.py",
        "tests/theory/aa_bb/test_b1_prototype.py",
    ],
    "wl505": [
        "scripts/theory/aa_bb/consolidation_inputs.py",
        "scripts/theory/aa_bb/a1_certificates.py",
        "scripts/theory/aa_bb/a2_evidence.py",
        "scripts/theory/aa_bb/d4_factor_twist.py",
        "tests/theory/aa_bb/test_a1_a2_parity.py",
        "tests/theory/aa_bb/test_d4_factor_twist.py",
    ],
    "wl521": [
        "scripts/theory/aa_bb/consolidation_inputs.py",
        "scripts/theory/aa_bb/a1_certificates.py",
        "scripts/theory/aa_bb/a2_evidence.py",
        "scripts/theory/aa_bb/d4_factor_twist.py",
        "tests/theory/aa_bb/test_a1_a2_parity.py",
        "tests/theory/aa_bb/test_d4_factor_twist.py",
    ],
    "wl522": [
        "scripts/theory/aa_bb/consolidation_inputs.py",
        "scripts/theory/aa_bb/a2_evidence.py",
        "scripts/theory/aa_bb/d4_factor_twist.py",
        "tests/theory/aa_bb/test_a1_a2_parity.py",
        "tests/theory/aa_bb/test_d4_factor_twist.py",
    ],
    "wl527": [
        "scripts/theory/aa_bb/consolidation_inputs.py",
        "scripts/theory/aa_bb/a2_evidence.py",
        "scripts/theory/aa_bb/d4_factor_twist.py",
        "tests/theory/aa_bb/test_a1_a2_parity.py",
        "tests/theory/aa_bb/test_d4_factor_twist.py",
    ],
}


def _source(work_log: str) -> dict[str, object]:
    return json.loads(SOURCE_FILES[work_log].read_text(encoding="utf-8"))


def _document(kind: str, rows: list[dict[str, object]]) -> dict[str, object]:
    return {"schema_version": 1, "kind": kind, "rows": rows}


def _legacy_projections() -> dict[str, dict[str, object]]:
    wl495 = _source("wl495")
    wl505 = _source("wl505")
    wl521 = _source("wl521")
    wl522 = _source("wl522")
    wl527 = _source("wl527")

    ledger_rows = []
    for row in wl521["final_candidate_ledgers"]:
        sample = row["sample"]
        summary = row["cover_summary"]
        ledger_rows.append(
            {
                "candidate_id": row["candidate_id"],
                "support_family": row["support_family"],
                "cover_family": row["cover_family"],
                "sample": {key: sample[key] for key in ("A", "B", "L", "T", "side")},
                "cover_summary": {
                    "L": summary["L"],
                    "T": summary["T"],
                    "d_vector": summary["d_vector"],
                },
                "classification": row["classification"],
                "ambient_c_d_global_solubility_status": row["ambient_c_d_global_solubility_status"],
                "ledger_route": row["ledger_route"],
                "source_work_log": row["source_work_log"],
            }
        )
    ledger_rows.sort(key=lambda row: row["candidate_id"])

    witness_rows = []
    for row in wl505["routed_active_shell7_supports"]:
        ambient = row["ambient_c_d_global_solubility"]
        if ambient["status"] != "globally_soluble":
            continue
        cover = row["complete_c_d_cover"]
        witness_rows.append(
            {
                "candidate_id": row["candidate_id"],
                "candidate_support": list(row["candidate_support"]),
                "sample": {
                    key: row["sample"][key]
                    for key in ("A", "B", "L", "T", "primitive", "side", "sqrt_q")
                },
                "parameters": {key: cover["parameters"][key] for key in ("p", "q", "sqrt_q")},
                "d_vector": {
                    key: cover["d_vector"][key]
                    for key in (
                        "d_minus_p",
                        "d_pos_2sqrt_q",
                        "d_neg_2sqrt_q",
                    )
                },
                "point_on_cover": {
                    key: ambient["point_on_cover"][key]
                    for key in ("X", "u_minus_p", "u_pos_2sqrt_q", "u_neg_2sqrt_q")
                },
                "point_on_E_L": {key: ambient["induced_point_on_E_L"][key] for key in ("X", "Y")},
            }
        )
    witness_rows.sort(key=lambda row: row["candidate_id"])

    taxonomy_rows = []
    for row in wl522["support_cover_taxonomy"]:
        taxonomy_rows.append(
            {
                "support_family": row["support_family"],
                "cover_family": row["cover_family"],
                "classification": row["classification"],
                "failure_mode": row["failure_mode"],
                "ambient_c_d_global_solubility_status": row["ambient_c_d_global_solubility_status"],
                "lemma_candidate_status": row["lemma_candidate_status"],
                "candidate_ids": sorted(row["candidate_ids"]),
                "entry_count": row["entry_count"],
                "work_logs": sorted(row["work_logs"]),
                "cover_summary": row["cover_summary"],
                "blocking_reasons": sorted(row["blocking_reasons"]),
            }
        )
    taxonomy_rows.sort(key=lambda row: (row["support_family"], row["cover_family"]))

    inventory_rows = []
    for row in wl527["cover_family_proof_data_inventory"]:
        model = row["cover_family_model_availability"]
        available = model["available_data"]
        maps = row["rational_source_side_maps"]
        elements = row["candidate_function_field_elements"]
        formulas = elements["point_level_formula_template_only"]
        target = row["opposite_side_target"]
        inventory_rows.append(
            {
                "cover_family": row["cover_family"],
                "support_family": row["support_family"],
                "classification": row["classification"],
                "failure_mode": row["failure_mode"],
                "ambient_c_d_global_solubility_status": row["ambient_c_d_global_solubility_status"],
                "lemma_candidate_status": row["lemma_candidate_status"],
                "entry_count": row["entry_count"],
                "candidate_ids": sorted(row["candidate_ids"]),
                "source_sides_to_map": sorted(row["source_sides_to_map"]),
                "work_logs": sorted(row["work_logs"]),
                "blocking_reasons_seen_at_point_level": sorted(
                    row["blocking_reasons_seen_at_point_level"]
                ),
                "cover_family_model_availability": {
                    "has_cover_family_label": model["has_cover_family_label"],
                    "has_l_t_parameters": model["has_l_t_parameters"],
                    "has_explicit_d_vector": model["has_explicit_d_vector"],
                    "has_explicit_equation": model["has_explicit_equation"],
                    "has_function_field_coordinates": model["has_function_field_coordinates"],
                    "available_data": {
                        "L": available["L"],
                        "T": available["T"],
                        "d_vector": available["d_vector"],
                    },
                },
                "rational_source_side_maps": {
                    "point_level_wl491_failures_available": maps[
                        "point_level_wl491_failures_available"
                    ],
                    "uniform_family_maps_available": maps["uniform_family_maps_available"],
                    "needed": maps["needed"],
                },
                "candidate_function_field_elements": {
                    "point_level_formula_template_only": {
                        "N": formulas["N"],
                        "M": formulas["M"],
                    },
                    "N_in_function_field_available": elements["N_in_function_field_available"],
                    "M_in_function_field_available": elements["M_in_function_field_available"],
                },
                "opposite_side_target": {
                    "AA_source_target": target["AA_source_target"],
                    "BB_source_target": target["BB_source_target"],
                    "certificate_needed": target["certificate_needed"],
                },
                "exceptional_specialization_positivity_checklist": list(
                    row["exceptional_specialization_positivity_checklist"]
                ),
                "missing_data_classes": list(row["missing_data_classes"]),
            }
        )
    inventory_rows.sort(key=lambda row: row["cover_family"])

    selected = {
        row["candidate_id"]: row
        for row in wl495["routed_refreshed_supports"]
        if row["candidate_id"] in B0_TARGET_IDS
    }
    b0_rows = []
    for candidate_id in B0_TARGET_IDS:
        row = selected[candidate_id]
        cover = row["complete_c_d_cover"]
        ambient = row["ambient_c_d_global_solubility"]
        routing = row["routing_state"]
        b0_rows.append(
            {
                "candidate_id": candidate_id,
                "candidate_support": list(row["candidate_support"]),
                "sample": {
                    key: row["sample"][key]
                    for key in ("A", "B", "L", "T", "primitive", "side", "sqrt_q")
                },
                "complete_d_cover": {
                    "parameters": {key: cover["parameters"][key] for key in ("p", "q", "sqrt_q")},
                    "d_vector": {
                        key: cover["d_vector"][key]
                        for key in ("d_minus_p", "d_pos_2sqrt_q", "d_neg_2sqrt_q")
                    },
                    "root_values": {
                        key: cover["root_data"][key]["value"]
                        for key in ("e_minus", "e_pos", "e_neg")
                    },
                },
                "ambient_witness": {
                    "point_on_cover": {
                        key: ambient["point_on_cover"][key]
                        for key in ("X", "u_minus_p", "u_pos_2sqrt_q", "u_neg_2sqrt_q")
                    },
                    "point_on_E_L": {
                        key: ambient["induced_point_on_E_L"][key] for key in ("X", "Y")
                    },
                },
                "routing": {
                    "ambient_status": routing["ambient_c_d_global_solubility_status"],
                    "admissibility_status": routing["aa_bb_admissibility_status"],
                    "ledger_route": routing["ledger_route"],
                    "blocking_reasons": list(row["wl491_filter_result"]["blocking_reasons"]),
                },
            }
        )

    return {
        "a0-ledger": _document("a0-ledger", ledger_rows),
        "a0-witnesses": _document("a0-witnesses", witness_rows),
        "a0-taxonomy": _document("a0-taxonomy", taxonomy_rows),
        "a0-inventory": _document("a0-inventory", inventory_rows),
        "b0-prototype-rows": _document("b0-prototype-rows", b0_rows),
    }


def _materialized_directory(tmp_path: Path) -> Path:
    output = tmp_path / "canonical"
    materialize_all(RESULTS, "9b73cd4", output)
    return output


def _source_fixture(tmp_path: Path) -> Path:
    source_dir = tmp_path / "results"
    source_dir.mkdir()
    for metadata in FROZEN_SOURCE_PAYLOADS.values():
        filename = Path(metadata["path"]).name
        shutil.copyfile(RESULTS / filename, source_dir / filename)
    return source_dir


def test_frozen_materializer_selection_has_exact_30_unique_sources() -> None:
    selected = set(SOURCE_FILENAMES.values())
    selected.update(A1_SOURCE_FILENAMES.values())
    selected.update(
        f"closure_quotient_rank_zero_aa_bb_wl{number}_{suffix}.json"
        for number, suffix in A2_SOURCE_SUFFIXES.items()
    )
    assert len(FROZEN_SOURCE_PAYLOADS) == 30
    assert selected == set(FROZEN_SOURCE_PAYLOADS)


def test_materializer_cli_uses_explicit_source_directory(tmp_path: Path) -> None:
    source_dir = _source_fixture(tmp_path)
    output = tmp_path / "cli-output"
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/theory/aa_bb/consolidation_inputs.py"),
            "--results-dir",
            str(source_dir),
            "--output-dir",
            str(output),
            "--baseline-commit",
            "9b73cd4",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "status=ok" in completed.stdout
    assert load_all(output)[2]["baseline_commit"] == "9b73cd4"


def test_materializer_missing_source_fails_closed(tmp_path: Path) -> None:
    source_dir = _source_fixture(tmp_path)
    (
        source_dir / Path(FROZEN_SOURCE_PAYLOADS[next(iter(FROZEN_SOURCE_PAYLOADS))]["path"]).name
    ).unlink()
    with pytest.raises(ConsolidationInputError, match="source payload unavailable"):
        materialize_all(source_dir, "9b73cd4", tmp_path / "output")


@pytest.mark.parametrize("mutation", ["size", "hash"])
def test_materializer_mutated_source_fails_closed(tmp_path: Path, mutation: str) -> None:
    source_dir = _source_fixture(tmp_path)
    filename = next(iter(FROZEN_SOURCE_PAYLOADS))
    source = source_dir / filename
    raw = source.read_bytes()
    if mutation == "size":
        source.write_bytes(raw + b" ")
        message = "source payload size mismatch"
    else:
        replacement = b" " if raw[-1:] == b"\n" else b"\n"
        source.write_bytes(raw[:-1] + replacement)
        message = "source payload hash mismatch"
    with pytest.raises(ConsolidationInputError, match=message):
        materialize_b0(source_dir, "9b73cd4", tmp_path / "output")


def test_materializer_extra_selected_source_fails_closed(tmp_path: Path, monkeypatch) -> None:
    import scripts.theory.aa_bb.consolidation_inputs as module

    suffixes = dict(module.A2_SOURCE_SUFFIXES)
    suffixes[528] = "unexpected_extra_source"
    monkeypatch.setattr(module, "A2_SOURCE_SUFFIXES", suffixes)
    with pytest.raises(ConsolidationInputError, match="source selection mismatch"):
        module.materialize_a2_boundary_spec(_source_fixture(tmp_path), tmp_path / "output")


@pytest.mark.parametrize(
    ("metadata_key", "metadata_value", "message"),
    [
        ("path", "results/not-the-frozen-source.json", "frozen source path mismatch"),
        ("size", 1, "source payload size mismatch"),
        ("sha256", "0" * 64, "source payload hash mismatch"),
    ],
)
def test_materializer_source_metadata_mismatch_fails_before_parse(
    tmp_path: Path,
    monkeypatch,
    metadata_key: str,
    metadata_value: object,
    message: str,
) -> None:
    import scripts.theory.aa_bb.consolidation_inputs as module

    filename = next(iter(module.FROZEN_SOURCE_PAYLOADS))
    metadata = copy.deepcopy(module.FROZEN_SOURCE_PAYLOADS)
    metadata[filename][metadata_key] = metadata_value
    monkeypatch.setattr(module, "FROZEN_SOURCE_PAYLOADS", metadata)
    with pytest.raises(ConsolidationInputError, match=message):
        module.materialize_b0(_source_fixture(tmp_path), "9b73cd4", tmp_path / "output")


def _rewrite_json(path: Path, mutate) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    mutate(payload)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _without_consumer_paths(value):
    if isinstance(value, dict):
        return {
            key: _without_consumer_paths(item)
            for key, item in value.items()
            if key != "consumer_paths"
        }
    if isinstance(value, list):
        return [_without_consumer_paths(item) for item in value]
    return value


def test_cutover_consumer_paths_are_exact_and_preserve_source_provenance(
    tmp_path: Path,
) -> None:
    materialized = _materialized_directory(tmp_path)
    checked_in = json.loads(
        (CANONICAL_DIR / CANONICAL_FILES["manifest"]).read_text(encoding="utf-8")
    )
    regenerated = json.loads(
        (materialized / CANONICAL_FILES["manifest"]).read_text(encoding="utf-8")
    )

    actual_source_paths = {
        work_log: SOURCE_PROVENANCE[work_log]["consumer_paths"]
        for work_log in EXPECTED_CONSUMER_PATHS
    }
    assert actual_source_paths == EXPECTED_CONSUMER_PATHS
    actual_manifest_paths = {
        binding["source_worklog"]: binding["consumer_paths"] for binding in checked_in["bindings"]
    }
    assert actual_manifest_paths == EXPECTED_CONSUMER_PATHS
    assert {
        binding["source_worklog"]: binding["consumer_paths"] for binding in regenerated["bindings"]
    } == EXPECTED_CONSUMER_PATHS

    for binding in checked_in["bindings"]:
        provenance = SOURCE_PROVENANCE[binding["source_worklog"]]
        for key, value in provenance.items():
            assert binding[key] == value

    assert _without_consumer_paths(checked_in) == _without_consumer_paths(regenerated)


def test_materialization_has_exact_cardinalities_and_views(tmp_path: Path) -> None:
    output = _materialized_directory(tmp_path)
    a0 = load_a0(output)
    b0 = load_b0(output)
    manifest = load_manifest(output / CANONICAL_FILES["manifest"], output)

    assert len(a0.ledger) == 43
    assert len(a0.witnesses) == 8
    assert len(a0.taxonomy) == 22
    assert len(a0.inventory) == 15
    assert len(b0.rows) == 2
    assert {row["candidate_id"] for row in a0.witnesses} == EXPECTED_WITNESS_IDS
    assert [row["candidate_id"] for row in b0.rows] == list(B0_TARGET_IDS)
    assert manifest["baseline_commit"] == "9b73cd4"
    assert len(manifest["bindings"]) == 5
    wl522 = a0.to_wl522_view()
    assert wl522["taxonomy_summary"]["taxonomy_row_count"] == 22
    assert wl522["taxonomy_summary"]["already_closed_entry_count"] == 4
    assert wl522["taxonomy_summary"]["ambient_globally_not_soluble_entry_count"] == 10
    assert wl522["taxonomy_summary"]["globally_soluble_but_not_aa_bb_admissible_entry_count"] == 29
    scope_summary = a0.to_wl527_view()["scope_summary"]
    assert scope_summary["named_entry_count"] == 29
    assert (
        scope_summary["exact_missing_data_class"]
        == "uniform_function_field_model_maps_and_squareclass_certificate"
    )
    assert len(a0.to_wl586_inputs()["routed_active_shell7_supports"]) == 8
    wl495 = b0.to_wl528_view()
    assert wl495["status"] == "ok"
    assert wl495["ready"] is True
    assert wl495["work_log"] == "wl495"
    assert wl495["input_work_logs"] == ["wl491", "wl494"]
    assert [row["candidate_id"] for row in wl495["routed_refreshed_supports"]] == list(
        B0_TARGET_IDS
    )
    assert {
        key: wl495[key]
        for key in (
            "old_package_x_coordinate_collapse_used",
            "package_x_s_tilde_bridge_used",
            "broad_rank_or_selmer_diagnostics_run",
            "single_curve_diagnostics_run",
            "complete_selmer_upper_bound_proved",
            "dim_sel2_eq_2_claimed",
            "rank_zero_claimed",
            "sha2_trivial_claimed",
            "family_exclusion_proved_count",
        )
    } == {
        "old_package_x_coordinate_collapse_used": False,
        "package_x_s_tilde_bridge_used": False,
        "broad_rank_or_selmer_diagnostics_run": False,
        "single_curve_diagnostics_run": False,
        "complete_selmer_upper_bound_proved": False,
        "dim_sel2_eq_2_claimed": False,
        "rank_zero_claimed": False,
        "sha2_trivial_claimed": False,
        "family_exclusion_proved_count": 0,
    }


def test_rematerialization_is_byte_identical(tmp_path: Path) -> None:
    first = _materialized_directory(tmp_path / "first")
    second = _materialized_directory(tmp_path / "second")
    for filename in CANONICAL_FILES.values():
        assert (first / filename).read_bytes() == (second / filename).read_bytes()
    for filename in (
        "a1-certificates.v1.json",
        "a2-boundary-spec.v1.json",
        "b1-sage-certificate.v1.json",
    ):
        assert (first / filename).read_bytes() == (second / filename).read_bytes()


def test_checked_in_canonical_directory_is_manifest_bound_and_byte_identical(
    tmp_path: Path,
) -> None:
    a0, b0, manifest = load_all(CANONICAL_DIR)
    materialized = _materialized_directory(tmp_path)

    assert len(a0.ledger) == 43
    assert len(b0.rows) == 2
    assert manifest["baseline_commit"] == "9b73cd4"
    assert {row["canonical_path"] for row in manifest["auxiliary_bindings"]} == {
        "a1-certificates.v1.json",
        "a2-boundary-spec.v1.json",
        "b1-sage-certificate.v1.json",
    }
    for filename in CANONICAL_FILES.values():
        assert (CANONICAL_DIR / filename).read_bytes() == (materialized / filename).read_bytes()
    for filename in (
        "a1-certificates.v1.json",
        "a2-boundary-spec.v1.json",
        "b1-sage-certificate.v1.json",
    ):
        assert (CANONICAL_DIR / filename).read_bytes() == (materialized / filename).read_bytes()


def test_projection_matches_explicit_legacy_source_selectors(tmp_path: Path) -> None:
    output = _materialized_directory(tmp_path)
    expected = _legacy_projections()
    for kind in (
        "a0-ledger",
        "a0-witnesses",
        "a0-taxonomy",
        "a0-inventory",
        "b0-prototype-rows",
    ):
        actual = json.loads((output / CANONICAL_FILES[kind]).read_text(encoding="utf-8"))
        assert actual == expected[kind]


def test_missing_and_duplicate_rows_fail_closed(tmp_path: Path) -> None:
    output = _materialized_directory(tmp_path)
    witnesses = output / CANONICAL_FILES["a0-witnesses"]
    _rewrite_json(witnesses, lambda payload: payload["rows"].pop())
    with pytest.raises(ConsolidationInputError):
        load_a0(output)

    output = _materialized_directory(tmp_path / "duplicate")
    ledger = output / CANONICAL_FILES["a0-ledger"]
    _rewrite_json(ledger, lambda payload: payload["rows"].append(copy.deepcopy(payload["rows"][0])))
    with pytest.raises(ConsolidationInputError):
        load_a0(output)


@pytest.mark.parametrize("cached_field", ["ready", "status", "violations", "route_rank"])
def test_unknown_and_cached_fields_are_rejected(tmp_path: Path, cached_field: str) -> None:
    output = _materialized_directory(tmp_path)
    ledger = output / CANONICAL_FILES["a0-ledger"]
    _rewrite_json(ledger, lambda payload: payload.__setitem__(cached_field, True))
    with pytest.raises(ConsolidationInputError):
        load_a0(output)

    output = _materialized_directory(tmp_path / "nested")
    inventory = output / CANONICAL_FILES["a0-inventory"]
    _rewrite_json(
        inventory,
        lambda payload: payload["rows"][0]["cover_family_model_availability"].__setitem__(
            "status", "cached"
        ),
    )
    with pytest.raises(ConsolidationInputError):
        load_a0(output)


def test_altered_coordinates_fail_equation_validation(tmp_path: Path) -> None:
    output = _materialized_directory(tmp_path)
    witnesses = output / CANONICAL_FILES["a0-witnesses"]
    _rewrite_json(
        witnesses,
        lambda payload: payload["rows"][0]["point_on_cover"].__setitem__(
            "X", payload["rows"][0]["point_on_cover"]["X"] + 1
        ),
    )
    with pytest.raises(ConsolidationInputError):
        load_a0(output)

    output = _materialized_directory(tmp_path / "b0")
    b0 = output / CANONICAL_FILES["b0-prototype-rows"]
    _rewrite_json(
        b0,
        lambda payload: payload["rows"][0]["ambient_witness"]["point_on_cover"].__setitem__(
            "u_minus_p", 5
        ),
    )
    with pytest.raises(ConsolidationInputError):
        load_b0(output)


def test_coordinated_witness_rescaling_differs_from_ledger(tmp_path: Path) -> None:
    output = _materialized_directory(tmp_path)
    witnesses = output / CANONICAL_FILES["a0-witnesses"]

    def rescale(payload: dict[str, object]) -> None:
        row = payload["rows"][0]
        row["d_vector"] = {key: value * 4 for key, value in row["d_vector"].items()}
        for key in ("u_minus_p", "u_pos_2sqrt_q", "u_neg_2sqrt_q"):
            row["point_on_cover"][key] //= 2

    _rewrite_json(witnesses, rescale)
    with pytest.raises(ConsolidationInputError, match="d-vector differs from ledger"):
        load_a0(output)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("canonical_projection_sha256", "0" * 64),
        ("source_worklog_path", "docs/wrong.md"),
        ("source_selector", "$.wrong"),
    ],
)
def test_manifest_hash_provenance_and_selector_fail_closed(
    tmp_path: Path, field: str, value: str
) -> None:
    output = _materialized_directory(tmp_path)
    manifest = output / CANONICAL_FILES["manifest"]
    _rewrite_json(manifest, lambda payload: payload["bindings"][0].__setitem__(field, value))
    with pytest.raises(ConsolidationInputError):
        load_manifest(manifest, output)


@pytest.mark.parametrize(
    "filename",
    [
        "a1-certificates.v1.json",
        "a2-boundary-spec.v1.json",
        "b1-sage-certificate.v1.json",
    ],
)
def test_altered_auxiliary_tracked_bytes_fail_manifest_closed(
    tmp_path: Path, filename: str
) -> None:
    output = _materialized_directory(tmp_path)
    target = output / filename
    target.write_bytes(target.read_bytes() + b" ")
    with pytest.raises(ConsolidationInputError, match="auxiliary projection hash mismatch"):
        load_manifest(output / CANONICAL_FILES["manifest"], output)


@pytest.mark.parametrize(
    "materializer",
    [materialize_a0, materialize_b0, materialize_manifest, materialize_all],
    ids=["a0", "b0", "manifest", "all"],
)
def test_materialization_rejects_unauthorized_baseline(tmp_path: Path, materializer) -> None:
    with pytest.raises(ConsolidationInputError, match="expected 9b73cd4"):
        materializer(RESULTS, "deadbeef", tmp_path / "output")


def test_manifest_rejects_unauthorized_baseline_but_individual_loaders_remain_usable(
    tmp_path: Path,
) -> None:
    output = _materialized_directory(tmp_path)
    manifest = output / CANONICAL_FILES["manifest"]
    _rewrite_json(manifest, lambda payload: payload.__setitem__("baseline_commit", "deadbeef"))

    load_a0(output)
    load_b0(output)
    with pytest.raises(ConsolidationInputError, match="expected 9b73cd4"):
        load_manifest(manifest, output)
    with pytest.raises(ConsolidationInputError, match="expected 9b73cd4"):
        load_all(output)


@pytest.mark.parametrize("field", ["ledger_route", "blocking_reasons"])
def test_b0_exact_routing_metadata_fails_closed(tmp_path: Path, field: str) -> None:
    output = _materialized_directory(tmp_path)
    b0 = output / CANONICAL_FILES["b0-prototype-rows"]

    def mutate(payload: dict[str, object]) -> None:
        routing = payload["rows"][0]["routing"]
        if field == "ledger_route":
            routing[field] = "wrong_route"
        else:
            routing[field] = ["M_not_positive"]

    _rewrite_json(b0, mutate)
    with pytest.raises(ConsolidationInputError):
        load_b0(output)


def test_b0_cross_file_identity_metadata_fails_after_manifest_rebind(tmp_path: Path) -> None:
    output = _materialized_directory(tmp_path)
    ledger = output / CANONICAL_FILES["a0-ledger"]
    _rewrite_json(
        ledger,
        lambda payload: next(
            row for row in payload["rows"] if row["candidate_id"] == B0_TARGET_IDS[0]
        )["sample"].update({"A": 2, "B": 3}),
    )
    load_a0(output)
    load_b0(output)

    manifest = output / CANONICAL_FILES["manifest"]

    def rebind_ledger(payload: dict[str, object]) -> None:
        binding = next(
            item
            for item in payload["bindings"]
            if item["canonical_path"] == CANONICAL_FILES["a0-ledger"]
        )
        raw = ledger.read_bytes()
        binding["canonical_projection_sha256"] = hashlib.sha256(raw).hexdigest()
        binding["canonical_projection_size"] = len(raw)

    _rewrite_json(manifest, rebind_ledger)
    with pytest.raises(ConsolidationInputError, match="B0 sample differs from A0 ledger"):
        load_all(output)


def test_loader_failure_does_not_fallback_to_results(tmp_path: Path, monkeypatch) -> None:
    output = _materialized_directory(tmp_path)
    original_read_bytes = Path.read_bytes
    touched_results = []

    def guarded_read_bytes(path: Path) -> bytes:
        if "results" in path.parts:
            touched_results.append(path)
            raise AssertionError(f"loader touched results: {path}")
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", guarded_read_bytes)
    load_a0(output)
    load_b0(output)
    load_manifest(output / CANONICAL_FILES["manifest"], output)
    with pytest.raises(ConsolidationInputError):
        load_a0(tmp_path / "missing-canonical")
    with pytest.raises(ConsolidationInputError):
        load_a0(RESULTS)
    with pytest.raises(ConsolidationInputError):
        load_manifest(RESULTS / "manifest.v1.json")
    assert touched_results == []
