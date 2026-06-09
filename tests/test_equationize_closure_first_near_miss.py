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
    assert summary["equation_network"] == {
        "shared_equations": {
            "B": {
                "value": 45,
                "forms": [
                    {
                        "edge": "B-N1",
                        "scale": 3,
                        "m": 4,
                        "n": 1,
                        "role": "odd_leg",
                        "readable": "45 = 3*(4^2-1^2)",
                    },
                    {
                        "edge": "B-N2",
                        "scale": 1,
                        "m": 7,
                        "n": 2,
                        "role": "odd_leg",
                        "readable": "45 = 1*(7^2-2^2)",
                    },
                ],
                "readable": "B = 45 = 3*(4^2-1^2) = 1*(7^2-2^2)",
            },
            "N1": {
                "value": 24,
                "forms": [
                    {
                        "edge": "A-N1",
                        "scale": 1,
                        "m": 4,
                        "n": 3,
                        "role": "even_leg",
                        "readable": "24 = 1*(2*4*3)",
                    },
                    {
                        "edge": "B-N1",
                        "scale": 3,
                        "m": 4,
                        "n": 1,
                        "role": "even_leg",
                        "readable": "24 = 3*(2*4*1)",
                    },
                ],
                "readable": "N1 = 24 = 1*(2*4*3) = 3*(2*4*1)",
            },
        },
        "closure_equation": {
            "relation": "sum=A+B",
            "readable": "N1 + N2 = A + B = 52",
            "holds": True,
        },
        "missing_square_questions": [
            {
                "edge": "A-N2",
                "readable": "A^2 + N2^2 = 7^2 + 28^2 = 833",
                "nearest_square": "29^2 = 841",
                "signed_delta": -8,
            }
        ],
    }
    assert summary["template_constraints"] == {
        "scope": "focus_bucket_sum_ab_B_odd_odd_N1_even_even",
        "passed_edge_templates": [
            {
                "edge": "A-N1",
                "scale_symbol": "u",
                "m_symbol": "p",
                "n_symbol": "q",
                "assignments": {
                    "u": 1,
                    "p": 4,
                    "q": 3,
                },
                "constraints": [
                    "A = u*(p^2-q^2)",
                    "N1 = u*(2*p*q)",
                ],
                "side_conditions": [
                    {"condition": "p > q > 0", "holds": True},
                    {"condition": "gcd(p,q) = 1", "holds": True},
                    {"condition": "p and q have opposite parity", "holds": True},
                    {"condition": "u > 0", "holds": True},
                ],
            },
            {
                "edge": "B-N1",
                "scale_symbol": "v",
                "m_symbol": "r",
                "n_symbol": "s",
                "assignments": {
                    "v": 3,
                    "r": 4,
                    "s": 1,
                },
                "constraints": [
                    "B = v*(r^2-s^2)",
                    "N1 = v*(2*r*s)",
                ],
                "side_conditions": [
                    {"condition": "r > s > 0", "holds": True},
                    {"condition": "gcd(r,s) = 1", "holds": True},
                    {"condition": "r and s have opposite parity", "holds": True},
                    {"condition": "v > 0", "holds": True},
                ],
            },
            {
                "edge": "B-N2",
                "scale_symbol": "w",
                "m_symbol": "x",
                "n_symbol": "y",
                "assignments": {
                    "w": 1,
                    "x": 7,
                    "y": 2,
                },
                "constraints": [
                    "B = w*(x^2-y^2)",
                    "N2 = w*(2*x*y)",
                ],
                "side_conditions": [
                    {"condition": "x > y > 0", "holds": True},
                    {"condition": "gcd(x,y) = 1", "holds": True},
                    {"condition": "x and y have opposite parity", "holds": True},
                    {"condition": "w > 0", "holds": True},
                ],
            },
        ],
        "shared_constraints": [
            "v*(r^2-s^2) = w*(x^2-y^2)",
            "u*(2*p*q) = v*(2*r*s)",
        ],
        "closure_constraint": "N1 + N2 = A + B",
        "missing_square_constraint": "A^2 + N2^2 = square?",
    }
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
