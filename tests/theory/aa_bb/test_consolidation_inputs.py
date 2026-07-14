from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT))

from scripts.theory.aa_bb.consolidation_inputs import (
    B0_TARGET_IDS,
    CANONICAL_FILES,
    EXPECTED_WITNESS_IDS,
    SOURCE_PROVENANCE,
    ConsolidationInputError,
    load_a0,
    load_all,
    load_b0,
    load_manifest,
)

CANONICAL_DIR = ROOT / "data" / "theory" / "aa_bb" / "wl500"


def _copy_canonical(tmp_path: Path) -> Path:
    output = tmp_path / "canonical"
    shutil.copytree(CANONICAL_DIR, output)
    return output


def _rewrite_json(path: Path, mutate) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    mutate(payload)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_checked_in_canonical_directory_loads_and_preserves_views() -> None:
    a0, b0, manifest = load_all(CANONICAL_DIR)

    assert len(a0.ledger) == 43
    assert len(a0.witnesses) == 8
    assert len(a0.taxonomy) == 22
    assert len(a0.inventory) == 15
    assert len(b0.rows) == 2
    assert {row["candidate_id"] for row in a0.witnesses} == EXPECTED_WITNESS_IDS
    assert [row["candidate_id"] for row in b0.rows] == list(B0_TARGET_IDS)
    assert manifest["baseline_commit"] == "9b73cd4"
    assert len(manifest["bindings"]) == 5
    assert {row["canonical_path"] for row in manifest["auxiliary_bindings"]} == {
        "a1-certificates.v1.json",
        "a2-boundary-spec.v1.json",
        "b1-sage-certificate.v1.json",
    }

    wl522 = a0.to_wl522_view()
    assert wl522["taxonomy_summary"] == {
        "aa_bb_admissible_cover_family_count": 0,
        "aa_bb_admissible_entry_count": 0,
        "taxonomy_row_count": 22,
        "already_closed_entry_count": 4,
        "ambient_globally_not_soluble_cover_family_count": 5,
        "ambient_globally_not_soluble_entry_count": 10,
        "cover_family_count": 22,
        "final_candidate_ledger_entry_count": 43,
        "genuinely_deferred_cover_family_count": 0,
        "genuinely_deferred_entry_count": 0,
        "globally_soluble_but_not_aa_bb_admissible_cover_family_count": 15,
        "globally_soluble_but_not_aa_bb_admissible_entry_count": 29,
        "processed_or_duplicate_cover_family_count": 2,
        "support_family_count": 13,
    }
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


def test_manifest_bindings_match_frozen_source_provenance() -> None:
    manifest = load_manifest(CANONICAL_DIR / CANONICAL_FILES["manifest"], CANONICAL_DIR)
    for binding in manifest["bindings"]:
        provenance = SOURCE_PROVENANCE[binding["source_worklog"]]
        for key, value in provenance.items():
            assert binding[key] == value


def test_canonical_projection_bytes_match_manifest() -> None:
    manifest = load_manifest(CANONICAL_DIR / CANONICAL_FILES["manifest"], CANONICAL_DIR)
    for binding in [*manifest["bindings"], *manifest["auxiliary_bindings"]]:
        raw = (CANONICAL_DIR / binding["canonical_path"]).read_bytes()
        assert len(raw) == binding["canonical_projection_size"]
        assert hashlib.sha256(raw).hexdigest() == binding["canonical_projection_sha256"]


def test_missing_and_duplicate_rows_fail_closed(tmp_path: Path) -> None:
    output = _copy_canonical(tmp_path)
    witnesses = output / CANONICAL_FILES["a0-witnesses"]
    _rewrite_json(witnesses, lambda payload: payload["rows"].pop())
    with pytest.raises(ConsolidationInputError):
        load_a0(output)

    output = _copy_canonical(tmp_path / "duplicate")
    ledger = output / CANONICAL_FILES["a0-ledger"]
    _rewrite_json(ledger, lambda payload: payload["rows"].append(copy.deepcopy(payload["rows"][0])))
    with pytest.raises(ConsolidationInputError):
        load_a0(output)


@pytest.mark.parametrize("cached_field", ["ready", "status", "violations", "route_rank"])
def test_unknown_and_cached_fields_are_rejected(tmp_path: Path, cached_field: str) -> None:
    output = _copy_canonical(tmp_path)
    ledger = output / CANONICAL_FILES["a0-ledger"]
    _rewrite_json(ledger, lambda payload: payload.__setitem__(cached_field, True))
    with pytest.raises(ConsolidationInputError):
        load_a0(output)

    output = _copy_canonical(tmp_path / "nested")
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
    output = _copy_canonical(tmp_path)
    witnesses = output / CANONICAL_FILES["a0-witnesses"]
    _rewrite_json(
        witnesses,
        lambda payload: payload["rows"][0]["point_on_cover"].__setitem__(
            "X", payload["rows"][0]["point_on_cover"]["X"] + 1
        ),
    )
    with pytest.raises(ConsolidationInputError):
        load_a0(output)

    output = _copy_canonical(tmp_path / "b0")
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
    output = _copy_canonical(tmp_path)
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
    output = _copy_canonical(tmp_path)
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
    output = _copy_canonical(tmp_path)
    target = output / filename
    target.write_bytes(target.read_bytes() + b" ")
    with pytest.raises(ConsolidationInputError, match="auxiliary projection hash mismatch"):
        load_manifest(output / CANONICAL_FILES["manifest"], output)


def test_manifest_rejects_unauthorized_baseline_but_loaders_remain_usable(
    tmp_path: Path,
) -> None:
    output = _copy_canonical(tmp_path)
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
    output = _copy_canonical(tmp_path)
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
    output = _copy_canonical(tmp_path)
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
    original_read_bytes = Path.read_bytes
    touched_results = []

    def guarded_read_bytes(path: Path) -> bytes:
        if "results" in path.parts:
            touched_results.append(path)
            raise AssertionError(f"loader touched results: {path}")
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", guarded_read_bytes)
    load_a0(CANONICAL_DIR)
    load_b0(CANONICAL_DIR)
    load_manifest(CANONICAL_DIR / CANONICAL_FILES["manifest"])
    with pytest.raises(ConsolidationInputError):
        load_a0(tmp_path / "missing-canonical")
    with pytest.raises(ConsolidationInputError):
        load_a0(tmp_path / "results")
    with pytest.raises(ConsolidationInputError):
        load_manifest(tmp_path / "results" / "manifest.v1.json")
    assert touched_results == []
