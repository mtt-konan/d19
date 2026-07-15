import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))


def test_q2_boundary_certificate_is_exact_and_non_overclaiming() -> None:
    path = (
        ROOT / "docs/codex/tasks/berry-sextic-genus2-classification-20260715/q2_odd_pi_boundary.py"
    )
    spec = importlib.util.spec_from_file_location("q2_odd_pi_boundary", path)
    assert spec is not None and spec.loader is not None
    q2_odd_pi_boundary = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(q2_odd_pi_boundary)

    payload = q2_odd_pi_boundary.build_boundary_certificate()
    assert payload["status"] == "precise_q2_missing_coordinate_certificate"
    assert payload["place"] == "pi=(94*i-169)"
    assert payload["local_factor_degrees"] == [1, 1, 2, 2]
    assert payload["orbit_dimension"] == 2
    assert payload["global_coordinate_dimension"] == 16
    assert payload["local_image_coordinates_certified"] is False
    assert payload["global_selmer_or_rank_claimed"] is False
