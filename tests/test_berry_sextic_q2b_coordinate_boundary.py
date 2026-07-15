"""Pure-Python audit of the stored Q2b coordinate boundary.

This test records only exact metadata implications.  It does not run Sage or
Magma and deliberately does not fabricate global or local coordinate vectors.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))


def _segmented():
    from scripts.theory import berry_sextic_magma_segmented as segmented

    return segmented


def test_current_snapshot_is_not_a_fixed_power_basis_sunit_payload() -> None:
    segmented = _segmented()
    snapshot = segmented.stage_snapshot(include_conjugate_support=True)

    assert len(snapshot["s_unit_group"]["squareclass_basis"]) == 16
    assert "generator_coordinates" not in snapshot["s_unit_group"]
    assert snapshot["field"]["basis_policy"].startswith(
        "Sage maximal-order coordinates"
    )
    assert all(
        entry["generator_encoding"] == "sage_maximal_order_basis_coordinates"
        for entry in snapshot["support"]
    )

    source = (ROOT / "scripts/theory/berry_sextic_magma_sunits.m").read_text(
        encoding="utf-8"
    )
    assert "BERRY_C1_SUNIT_BASIS" in source
    assert "Eltseq(La!sunit_map(sunit_generators[j]))" in source


def test_support_metadata_only_fixes_ideal_parity_skeleton() -> None:
    segmented = _segmented()
    snapshot = segmented.stage_snapshot(include_conjugate_support=True)
    support = snapshot["support"]

    assert tuple(entry["e"] % 2 for entry in support) == (
        0,
        0,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
    )
    assert tuple(entry["f"] % 2 for entry in support) == (
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
    )


def test_q1_and_q2a_vectors_remain_separate_objects() -> None:
    from scripts.theory import berry_sextic_q1

    q1 = berry_sextic_q1.build_certificate()
    assert q1["fake_target"]["ambient_supported_image"]["constant_subspace"][
        "known_constant_class"
    ] == "[i]=[zeta4] belongs to C_S"
    assert q1["norm_square_kernel"]["coordinate_matrix"]["status"] == "missing"
    assert q1["localization"]["matrix"]["status"] == "missing"

    q2a_report = (
        ROOT
        / "docs/codex/tasks/berry-sextic-genus2-classification-20260715"
        / "q2a-local-kummer-generators.md"
    ).read_text(encoding="utf-8")
    assert "[beta_12] = (0,1,1,0)" in q2a_report
    assert "[beta_r]  = (0,0,1,0)" in q2a_report
    assert "global 16-coordinate localization" in q2a_report
