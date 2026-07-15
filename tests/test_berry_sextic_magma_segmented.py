from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/theory/berry_sextic_magma_segmented.py"
sys.path.insert(0, str(ROOT))


def _module():
    import scripts.theory.berry_sextic_magma_segmented as segmented

    return segmented


def test_exact_order_support_and_local_targets() -> None:
    payload = _module().build_certificate()

    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["accepted_outcome"] == "segmented_free_magma_route_ready"
    assert payload["field_and_order"]["relative_degree"] == 6
    assert payload["field_and_order"]["absolute_degree"] == 12
    assert payload["global_data"]["model_squareclass_dimension"] == 12
    assert payload["global_data"]["conservative_squareclass_dimension"] == 16
    assert payload["local_target"]["dyadic"]["dim_J_over_2J"] == 5
    assert payload["local_target"]["odd_pi"]["dim_J_over_2J"] == 2


def test_support_slots_and_relations_are_rebuildable() -> None:
    segmented = _module()
    snapshot = segmented.stage_snapshot()
    serialized = segmented.serialize_stage_snapshot(snapshot)
    rebuilt = segmented.deserialize_stage_snapshot(serialized)

    assert rebuilt == snapshot
    assert [entry["ideal_number"] for entry in rebuilt["support"]] == list(range(1, 7))
    assert len(rebuilt["unit_group"]["relation_matrix"][0]) == 6
    assert len(rebuilt["s_unit_group"]["relation_matrix"][0]) == 12
    assert all(entry["generator_encoding"] for entry in rebuilt["support"])


def test_magma_probes_are_segmented_and_do_not_call_selmer() -> None:
    probe_names = (
        "berry_sextic_magma_field_order.m",
        "berry_sextic_magma_sunits.m",
        "berry_sextic_magma_local.m",
        "berry_sextic_magma_rebuild.m",
    )
    for name in probe_names:
        source = (ROOT / "scripts/theory" / name).read_text(encoding="utf-8")
        assert "BERRY_C1_" in source
        assert "TwoSelmerGroup" not in source
        assert "TwoCoverDescent" not in source


def test_independent_sage_certificate_is_available() -> None:
    sage_source = (ROOT / "scripts/theory/berry_sextic_magma_segmented.sage").read_text(
        encoding="utf-8"
    )
    assert "proof.all(True)" in sage_source
    assert "TwoSelmerGroup" not in sage_source
    assert "5019340374016" in sage_source


def test_segmented_certificate_cli(tmp_path: Path) -> None:
    out = tmp_path / "berry-c1-segmented.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(out)],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert "accepted_outcome=segmented_free_magma_route_ready" in result.stdout
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["calculator_observations"]["prior_full_global_probe"]["max_time"] == 60
    assert saved["calculator_observations"]["segmented_submissions"]["all_below_public_limit"]
