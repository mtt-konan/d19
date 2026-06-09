from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.theory import equationize_closure_first_near_miss as eq


def test_equationize_high_repetition_inside_sum_sample() -> None:
    summary = eq.equationize_sample(7, 45, 24, 28, "sum=A+B")

    assert summary["closure"] == {
        "relation": "sum=A+B",
        "target": 52,
        "left": 52,
        "holds": True,
    }
    assert summary["square_count"] == 3
    assert summary["missing_edges"] == ["A-N2"]
    assert summary["shared_variables"] == {
        "B": [
            {
                "edge": "B-N1",
                "value": 45,
                "scale": 3,
                "euclid": {"m": 4, "n": 1},
                "role": "odd_leg",
                "formula": "scale*(m^2-n^2)",
            },
            {
                "edge": "B-N2",
                "value": 45,
                "scale": 1,
                "euclid": {"m": 7, "n": 2},
                "role": "odd_leg",
                "formula": "scale*(m^2-n^2)",
            },
        ],
        "N1": [
            {
                "edge": "A-N1",
                "value": 24,
                "scale": 1,
                "euclid": {"m": 4, "n": 3},
                "role": "even_leg",
                "formula": "scale*(2*m*n)",
            },
            {
                "edge": "B-N1",
                "value": 24,
                "scale": 3,
                "euclid": {"m": 4, "n": 1},
                "role": "even_leg",
                "formula": "scale*(2*m*n)",
            },
        ],
    }
    assert summary["edges"]["A-N1"]["triple"] == {
        "leg1": 7,
        "leg2": 24,
        "hypotenuse": 25,
        "primitive": [7, 24, 25],
        "euclid": {"m": 4, "n": 3, "odd_leg": 7, "even_leg": 24},
        "generated_legs": {
            "A": {
                "value": 7,
                "primitive_value": 7,
                "role": "odd_leg",
                "formula": "scale*(m^2-n^2)",
            },
            "N1": {
                "value": 24,
                "primitive_value": 24,
                "role": "even_leg",
                "formula": "scale*(2*m*n)",
            },
        },
        "scale": 1,
    }
    assert summary["edges"]["B-N1"]["triple"]["primitive"] == [8, 15, 17]
    assert summary["edges"]["B-N1"]["triple"]["scale"] == 3
    assert summary["edges"]["B-N1"]["triple"]["euclid"] == {
        "m": 4,
        "n": 1,
        "odd_leg": 15,
        "even_leg": 8,
    }
    assert summary["edges"]["B-N1"]["triple"]["generated_legs"] == {
        "B": {
            "value": 45,
            "primitive_value": 15,
            "role": "odd_leg",
            "formula": "scale*(m^2-n^2)",
        },
        "N1": {
            "value": 24,
            "primitive_value": 8,
            "role": "even_leg",
            "formula": "scale*(2*m*n)",
        },
    }
    assert summary["edges"]["B-N2"]["triple"]["primitive"] == [28, 45, 53]
    assert summary["edges"]["B-N2"]["triple"]["euclid"]["m"] == 7
    assert summary["edges"]["B-N2"]["triple"]["euclid"]["n"] == 2
    assert summary["edges"]["A-N2"]["nearest_delta"] == 8
    assert summary["edges"]["A-N2"]["signed_delta"] == -8


def test_equationize_delta_one_sample_tracks_failed_edge() -> None:
    summary = eq.equationize_sample(17745, 53911, 60840, 132496, "diff=A+B")

    assert summary["closure"]["target"] == 71656
    assert summary["closure"]["left"] == 71656
    assert summary["square_count"] == 3
    assert summary["missing_edges"] == ["B-N2"]
    assert summary["edges"]["B-N2"]["nearest_delta"] == 1
    assert summary["edges"]["B-N2"]["signed_delta"] == 1
    assert summary["edges"]["A-N1"]["triple"]["scale"] == 2535
    assert summary["edges"]["A-N1"]["triple"]["primitive"] == [7, 24, 25]


def test_cli_writes_selected_samples(tmp_path) -> None:
    out = tmp_path / "near_miss.json"

    assert eq.main(["--sample", "7,45,24,28,sum=A+B", "--out", str(out)]) == 0

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["sample_count"] == 1
    assert payload["samples"][0]["A"] == 7
    assert payload["samples"][0]["missing_edges"] == ["A-N2"]
