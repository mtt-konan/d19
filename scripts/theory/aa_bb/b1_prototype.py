"""Canonical B1 extraction for the wl528-wl529 prototype and square locus."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any, Literal

import sympy as sp

try:
    from scripts.theory.aa_bb.consolidation_inputs import B0Document, load_b0
except ModuleNotFoundError:
    from consolidation_inputs import B0Document, load_b0

TARGET_CANDIDATE_IDS = (
    "AA_A1_B4_v_5_m_tail_refresh_candidate",
    "BB_A4_B1_v_5_m_tail_refresh_candidate",
)
D_VECTOR = {"d_minus_p": 5, "d_pos_2sqrt_q": 1, "d_neg_2sqrt_q": 5}
SAGE_MARKER = "WL529_SAGE_JSON "
SAGE_CURVE = {
    "a_invariants": [0, 78, 0, 7921, 0],
    "equation": "Y^2 = X^3 + 78*X^2 + 7921*X",
}
LEGACY_SOURCE = (
    "results/closure_quotient_rank_zero_aa_bb_wl529_v5_l1_t5_square_locus.json",
    "889aec034ecd479b1b2a12d6e83a605febe6ef6364a8e87d24e3847525041fca",
    19629,
)
EXPECTED_SAGE = {
    "status": "ok",
    "rank": 0,
    "rank_method": "E.rank(proof=True)",
    "rank_is_proved": True,
    "torsion_invariants": [4],
    "torsion_points": [
        {"kind": "infinity"},
        {"x": "0", "y": "0", "x_is_rational_square": True},
        {"x": "89", "y": "-1424", "x_is_rational_square": False},
        {"x": "89", "y": "1424", "x_is_rational_square": False},
    ],
    "square_x_values": ["0"],
}
NO_CLAIM_KEYS = (
    "shell11_executed_here",
    "m_tail_diagnostics_extended_here",
    "new_supports_computed_here",
    "new_c_d_solubility_tested_here",
    "wl491_filter_applied_to_new_point_here",
    "broad_rank_or_selmer_diagnostics_run",
    "complete_selmer_upper_bound_proved",
    "dim_sel2_eq_2_claimed",
    "rank_zero_claimed",
    "sha2_trivial_claimed",
    "uniform_m_tail_full_rank_claimed",
    "family_exclusion_proved_count",
    "old_package_x_coordinate_collapse_used",
    "package_x_s_tilde_bridge_used",
    "advance_to_next_cover_family",
    "advance_to_next_roadmap_step",
)
SCOPE = {
    "support": "v_5",
    "L": 1,
    "T": 5,
    "d_vector": D_VECTOR,
    "candidate_ids": list(TARGET_CANDIDATE_IDS),
    "touches_only_one_cover_family": True,
}


class B1Error(ValueError):
    """Raised when canonical B1 evidence is incomplete or inconsistent."""


@dataclass(frozen=True)
class SageCertificate:
    document: dict[str, Any]


@dataclass(frozen=True)
class B1Evidence:
    projections: dict[str, dict[str, Any]]
    sage_certificate: SageCertificate

    @property
    def status(self) -> str:
        return self.projections["wl528"]["status"]


def _exact(value: Any, keys: set[str], context: str) -> dict[str, Any]:
    if type(value) is not dict or set(value) != keys:
        raise B1Error(f"{context}: exact keys required")
    return value


def _json_object(path: Path, context: str) -> dict[str, Any]:
    if "results" in path.parts:
        raise B1Error(f"{context}: runtime refuses ignored results path")
    try:
        value = json.loads(path.read_bytes())
    except (OSError, json.JSONDecodeError) as exc:
        raise B1Error(f"{context}: cannot read JSON: {exc}") from exc
    if type(value) is not dict:
        raise B1Error(f"{context}: expected object")
    return value


def _validate_sage_document(payload: dict[str, Any]) -> dict[str, Any]:
    _exact(payload, {"schema_version", "kind", "curve", "sage", "provenance"}, "B1")
    if payload["schema_version"] != 1 or payload["kind"] != "b1-sage-certificate":
        raise B1Error("B1: unsupported schema or kind")
    if payload["curve"] != SAGE_CURVE:
        raise B1Error("B1.curve: curve drift")
    if payload["sage"] != EXPECTED_SAGE:
        raise B1Error("B1.sage: exact rank/torsion/square-X certificate required")
    provenance_keys = {
        "marker",
        "program",
        "command",
        "source_mode",
        "source_work_log",
        "source_selector",
        "source_result_path",
        "source_payload_sha256",
        "source_payload_size",
    }
    provenance = _exact(payload["provenance"], provenance_keys, "B1.provenance")
    header_keys = ("marker", "program", "command", "source_work_log")
    header = tuple(provenance[key] for key in header_keys)
    expected = (
        SAGE_MARKER,
        "scripts/theory/aa_bb/b1_prototype.py::_sage_program",
        ["sage", "-python", "-c"],
        "wl529",
    )
    if header != expected:
        raise B1Error("B1.provenance: Sage program boundary drift")
    source_keys = ("source_result_path", "source_payload_sha256", "source_payload_size")
    source = tuple(provenance[key] for key in source_keys)
    if provenance["source_mode"] == "legacy_result_projection":
        if provenance["source_selector"] != "$.genus_one_certificate" or source != LEGACY_SOURCE:
            raise B1Error("B1.provenance: legacy source binding is incomplete")
    elif provenance["source_mode"] == "external_sage_refresh":
        if (provenance["source_selector"], *source) != (
            "sage marker output",
            "external-sage",
            "external-sage",
            0,
        ):
            raise B1Error("B1.provenance: external refresh binding is invalid")
    else:
        raise B1Error("B1.provenance: Sage program boundary drift")
    return payload


def load_sage_certificate(path: Path) -> SageCertificate:
    """Load the tracked B1 Sage artifact without consulting ignored results."""

    payload = _json_object(Path(path), "B1 Sage artifact")
    return SageCertificate(_validate_sage_document(payload))


def _sage_program() -> str:
    return f"""import json
from sage.all import EllipticCurve, QQ
def is_square(v):
    return bool(v >= 0 and v.numerator().is_square() and v.denominator().is_square())
E = EllipticCurve([0, 78, 0, 7921, 0])
points, square_x = [], []
for p in E.torsion_points():
    if p.is_zero():
        points.append({{"kind": "infinity"}})
        continue
    x, y = QQ(p[0]), QQ(p[1])
    record = {{"x": str(x), "y": str(y), "x_is_rational_square": is_square(x)}}
    points.append(record)
    if record["x_is_rational_square"]:
        square_x.append(record["x"])
payload = {{"status":"ok", "rank":int(E.rank(proof=True)),
"rank_method":"E.rank(proof=True)", "rank_is_proved":True,
"torsion_invariants":[int(v) for v in E.torsion_subgroup().invariants()],
"torsion_points":points, "square_x_values":square_x}}
print({SAGE_MARKER!r} + json.dumps(payload, separators=(",", ":")), flush=True)
"""


def _parse_marker(stdout: str) -> dict[str, Any] | None:
    for line in stdout.splitlines():
        if line.startswith(SAGE_MARKER):
            try:
                value = json.loads(line[len(SAGE_MARKER) :])
            except json.JSONDecodeError as exc:
                raise B1Error(f"Sage marker: invalid JSON: {exc}") from exc
            return value if type(value) is dict else None
    return None


def refresh_sage_certificate(output: Path, sage: str = "sage") -> Path:
    """Explicitly refresh B1 evidence with one strict external Sage process."""

    env = os.environ.copy()
    with (
        tempfile.TemporaryDirectory(prefix="d19-b1-sage-", dir="/private/tmp") as dot_sage,
        tempfile.TemporaryDirectory(prefix="d19-b1-tmp-", dir="/private/tmp") as tmpdir,
    ):
        env.update(DOT_SAGE=dot_sage, TMPDIR=tmpdir)
        completed = subprocess.run(
            [sage, "-python", "-c", _sage_program()],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
    certificate = _parse_marker(completed.stdout)
    if completed.returncode != 0 or certificate is None:
        tail = completed.stderr.splitlines()[-5:]
        raise B1Error(f"Sage refresh failed: returncode={completed.returncode} stderr={tail}")
    provenance = {
        "marker": SAGE_MARKER,
        "program": "scripts/theory/aa_bb/b1_prototype.py::_sage_program",
        "command": ["sage", "-python", "-c"],
        "source_mode": "external_sage_refresh",
        "source_work_log": "wl529",
        "source_selector": "sage marker output",
        "source_result_path": "external-sage",
        "source_payload_sha256": "external-sage",
        "source_payload_size": 0,
    }
    document = {
        "schema_version": 1,
        "kind": "b1-sage-certificate",
        "curve": SAGE_CURVE,
        "sage": certificate,
        "provenance": provenance,
    }
    _validate_sage_document(document)
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    return path


def _is_square(value: Fraction) -> bool:
    return value >= 0 and all(
        isqrt(part) ** 2 == part for part in (value.numerator, value.denominator)
    )


def _json_fraction(value: Fraction) -> int | str:
    return value.numerator if value.denominator == 1 else str(value)


def _reduces_to_zero(expr: sp.Expr, r: sp.Symbol, y: sp.Symbol) -> bool:
    rhs = 5 * r**4 - 264 * r**2 + 2000
    numerator = sp.together(expr).as_numer_denom()[0]
    remainder = sp.rem(sp.Poly(sp.expand(numerator), y), sp.Poly(y**2 - rhs, y))
    return sp.factor(remainder.as_expr()) == 0


def _function_field_model() -> dict[str, Any]:
    r, y = sp.symbols("r y")
    minus, pos, neg = (r**2 - 20) / (2 * r), y / (2 * r), (r**2 + 20) / (2 * r)
    x_coord = 42 + 5 * minus**2
    y_coord = 5 * minus * pos * neg
    t_value = y * (r**2 + 20) / (4 * r * (r**2 - 20))
    z_value = x_coord / 2 - t_value**2
    source_product = (((5 + t_value) / 2) ** 2 + 1) * (((5 - t_value) / 2) ** 2 + 1)
    formulas = [
        ("X_minus_42_relation", "X - 42 = 5*u_minus_p^2", x_coord - 42 - 5 * minus**2),
        ("X_minus_58_relation", "X - 58 = u_pos_2sqrt_q^2", x_coord - 58 - pos**2),
        ("X_plus_58_relation", "X + 58 = 5*u_neg_2sqrt_q^2", x_coord + 58 - 5 * neg**2),
        (
            "centered_even_t_formula",
            "t = Y/(2*(X+p)) = y*(r^2+20)/(4*r*(r^2-20))",
            y_coord / (2 * (x_coord - 42)) - t_value,
        ),
        (
            "source_leg_one_product_square",
            "(N^2+1)(M^2+1) = (z/4)^2",
            source_product - (z_value / 4) ** 2,
        ),
    ]
    checks = {key: _reduces_to_zero(expr, r, y) for key, _identity, expr in formulas}
    return {
        "function_field": "Q(r,y)/(y^2 - (5*r^4 - 264*r^2 + 2000))",
        "cover_maps": {
            "u_minus_p": "(r^2 - 20)/(2*r)",
            "u_pos_2sqrt_q": "y/(2*r)",
            "u_neg_2sqrt_q": "(r^2 + 20)/(2*r)",
            "X": "42 + 5*((r^2 - 20)/(2*r))^2",
            "Y": "5*y*(r^4 - 400)/(8*r^3)",
        },
        "derived_from_complete_d_equations": [
            "X - 42 = 5*u_minus_p^2",
            "X - 58 = u_pos_2sqrt_q^2",
            "X + 58 = 5*u_neg_2sqrt_q^2",
            "5*u_minus_p^2 - u_pos_2sqrt_q^2 = 16",
            "u_minus_p^2 - u_neg_2sqrt_q^2 = -20",
        ],
        "identity_checks": checks,
        "open_conditions_for_this_chart": ["r != 0", "r^2 != 20", "X+p != 0"],
    }


def _reduce_model(model: dict[str, Any]) -> dict[str, Any]:
    checks = model["identity_checks"]
    if type(checks) is list:
        checks = {item["check_id"]: item["verified_in_function_field"] for item in checks}
    return {
        "function_field": model["function_field"],
        "cover_maps": model["cover_maps"],
        "derived_from_complete_d_equations": model["derived_from_complete_d_equations"],
        "identity_checks": checks,
        "open_conditions_for_this_chart": model["open_conditions_for_this_chart"],
    }


def _source_maps() -> dict[str, Any]:
    t_formula = "y*(r^2+20)/(4*r*(r^2-20))"
    return {
        "t": t_formula,
        "z": "X/2 - t^2",
        "N": f"(5 + {t_formula})/2",
        "M": f"(5 - {t_formula})/2",
        "source_product_square_identity": "(N^2+1)(M^2+1) = (z/4)^2",
        "AA_opposite": "(N^2+B^2)(M^2+B^2)",
        "BB_opposite": "(N^2+A^2)(M^2+A^2)",
        "candidate_ids": list(TARGET_CANDIDATE_IDS),
    }


def _reduce_source_maps(maps: dict[str, Any]) -> dict[str, Any]:
    if "t" in maps:
        return maps
    shared = maps["shared_centered_even_map"]
    return {
        "t": shared["t"],
        "z": shared["z"],
        "N": shared["N"],
        "M": shared["M"],
        "source_product_square_identity": shared["source_product_square_identity"],
        "AA_opposite": maps["AA_source"]["opposite_side_product"],
        "BB_opposite": maps["BB_source"]["opposite_side_product"],
        "candidate_ids": [maps["AA_source"]["candidate_id"], maps["BB_source"]["candidate_id"]],
    }


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    cover = row.get("complete_d_cover") or row["complete_c_d_cover"]
    roots = cover.get("root_values") or {
        key: cover["root_data"][key]["value"] for key in ("e_minus", "e_pos", "e_neg")
    }
    ambient = row.get("ambient_witness") or row["ambient_c_d_global_solubility"]
    routing = row.get("routing") or row["routing_state"]
    return {
        "candidate_id": row["candidate_id"],
        "candidate_support": list(row["candidate_support"]),
        "sample": dict(row["sample"]),
        "complete_d_cover": {
            "parameters": dict(cover["parameters"]),
            "d_vector": dict(cover["d_vector"]),
            "root_values": dict(roots),
        },
        "ambient_witness": {
            "point_on_cover": dict(ambient["point_on_cover"]),
            "point_on_E_L": dict(ambient.get("point_on_E_L") or ambient["induced_point_on_E_L"]),
        },
        "routing": {
            "ambient_status": routing.get("ambient_status")
            or routing["ambient_c_d_global_solubility_status"],
            "admissibility_status": routing.get("admissibility_status")
            or routing["aa_bb_admissibility_status"],
            "ledger_route": routing["ledger_route"],
            "blocking_reasons": sorted(routing["blocking_reasons"]),
        },
    }


def _input_rows(b0: B0Document) -> list[dict[str, Any]]:
    if not isinstance(b0, B0Document):
        raise B1Error("B0: exact selected candidate pair required")
    rows = [_normalize_row(row) for row in b0.rows]
    if [row["candidate_id"] for row in rows] != list(TARGET_CANDIDATE_IDS):
        raise B1Error("B0: exact selected candidate pair required")
    for index, row in enumerate(rows):
        cover = row["complete_d_cover"]
        exact = (
            row["candidate_support"] == ["v_5"],
            row["sample"]["L"] == 1,
            row["sample"]["T"] == 5,
            cover["parameters"] == {"p": -42, "q": 841, "sqrt_q": 29},
            cover["d_vector"] == D_VECTOR,
            cover["root_values"] == {"e_minus": 42, "e_pos": 58, "e_neg": -58},
        )
        if not all(exact):
            raise B1Error(f"B0 row {index}: prototype input drift")
    return rows


def _specialization(rows: list[dict[str, Any]]) -> dict[str, Any]:
    r, y = Fraction(10), Fraction(160)
    minus, pos, neg = (r**2 - 20) / (2 * r), y / (2 * r), (r**2 + 20) / (2 * r)
    x_coord = 42 + 5 * minus**2
    y_coord = 5 * y * (r**4 - 400) / (8 * r**3)
    t_value = y * (r**2 + 20) / (4 * r * (r**2 - 20))
    n_value, m_value = (5 + t_value) / 2, (5 - t_value) / 2
    product = (n_value**2 + 16) * (m_value**2 + 16)
    values = {
        "r": r,
        "y": y,
        "u_minus_p": minus,
        "u_pos_2sqrt_q": pos,
        "u_neg_2sqrt_q": neg,
        "X": x_coord,
        "Y": y_coord,
        "t": t_value,
        "N": n_value,
        "M": m_value,
    }
    cover_point = {
        key: int(values[key]) for key in ("X", "u_minus_p", "u_pos_2sqrt_q", "u_neg_2sqrt_q")
    }
    checks = {
        "specialization_lies_on_quartic": y**2 == 5 * r**4 - 264 * r**2 + 2000,
        "specialization_is_smooth": -(20 * r**3 - 528 * r) != 0 or 2 * y != 0,
        "chart_open_denominators_nonzero": all(v != 0 for v in (r, r**2 - 20, x_coord - 42)),
        "maps_to_recorded_cover_point": all(
            row["ambient_witness"]["point_on_cover"] == cover_point for row in rows
        ),
        "maps_to_recorded_e_point": all(
            row["ambient_witness"]["point_on_E_L"] == {"X": 122, "Y": 960} for row in rows
        ),
        "specialized_t_n_m_match_recorded_values": (t_value, n_value, m_value)
        == (6, Fraction(11, 2), Fraction(-1, 2)),
        "opposite_product_matches_recorded_value": product == Fraction(12025, 16),
        "opposite_product_regular_and_nonzero_at_specialization": product != 0,
        "specialized_value_is_not_rational_square": not _is_square(product),
    }
    return {
        "values": {key: _json_fraction(value) for key, value in values.items()},
        "checks": checks,
        "specialized_value": _json_fraction(product),
        "specialized_value_is_rational_square": _is_square(product),
    }


def _square_locus() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    r, y, t, u, x_coord, y_coord = sp.symbols("r y t u X Y")
    t_value = y * (r**2 + 20) / (4 * r * (r**2 - 20))
    product = (((5 + t_value) / 2) ** 2 + 16) * (((5 - t_value) / 2) ** 2 + 16)
    quartic = t**4 + 78 * t**2 + 7921
    formulas = [
        ("exact_opposite_square_locus_identity", 16 * product - ((t_value**2 + 39) ** 2 + 6400)),
        (
            "cleared_denominator_t_square_relation",
            16 * r**2 * (r**2 - 20) ** 2 * t_value**2
            - (r**2 + 20) ** 2 * (5 * r**4 - 264 * r**2 + 2000),
        ),
    ]
    checks = [{"check_id": key, "verified": _reduces_to_zero(expr, r, y)} for key, expr in formulas]
    quotient = y_coord**2 - (x_coord**3 + 78 * x_coord**2 + 7921 * x_coord)
    verified = (
        sp.factor(quotient.subs({x_coord: t**2, y_coord: t * u}) - t**2 * (u**2 - quartic)) == 0
    )
    checks.append({"check_id": "genus_one_elliptic_quotient_map", "verified": verified})
    poly = sp.Poly(quartic, t)
    checks.append(
        {
            "check_id": "square_locus_quartic_is_squarefree",
            "verified": sp.gcd(poly, poly.diff()) == 1,
        }
    )
    models = {
        "t_parameter": "t = y*(r^2+20)/(4*r*(r^2-20))",
        "positivity_domain": "|t| < 5",
        "positive_source_condition": "N=(5+t)/2 > 0 and M=(5-t)/2 > 0",
        "square_locus_affine_curve": {
            "variables": ["t", "U"],
            "definition": "U^2 = t^4 + 78*t^2 + 7921",
            "note": "Here U = 4*s, so U^2 = 16*(N^2+16)(M^2+16).",
        },
        "cleared_denominator_relation_over_wl528_quartic": (
            "16*r^2*(r^2-20)^2*t^2 = (r^2+20)^2*(5*r^4-264*r^2+2000)"
        ),
        "projective_intersection_of_quadrics": [
            "V*Z = T^2 + 39*Z^2",
            "U^2 = V^2 + 6400*Z^2",
        ],
        "square_locus_and_elliptic_quotient": {
            "square_locus": "U^2 = t^4 + 78*t^2 + 7921",
            "elliptic_quotient": "Y^2 = X^3 + 78*X^2 + 7921*X",
            "degree_two_map": "X = t^2, Y = t*U",
            "point_classification_rule": (
                "D(Q) maps into E(Q) with X a rational square; this map is not asserted "
                "to be a birational equivalence"
            ),
        },
    }
    return models, checks


def _t_zero() -> dict[str, Any]:
    x = sp.symbols("x")
    quadratic = 5 * x**2 - 264 * x + 2000
    discriminant = int(sp.discriminant(quadratic, x))
    factors = {str(prime): exponent for prime, exponent in sp.factorint(discriminant).items()}
    verified = (
        discriminant == 29696
        and factors == {"2": 10, "29": 1}
        and not _is_square(Fraction(discriminant))
    )
    return {
        "candidate_t_value": 0,
        "derived_r2_equation": "5*x^2 - 264*x + 2000 = 0 with x = r^2",
        "t_zero_forces_y_zero": True,
        "quadratic_discriminant_computed": True,
        "discriminant": discriminant,
        "discriminant_factorization": factors,
        "discriminant_is_rational_square": False,
        "certificate_verified": verified,
        "rational_preimage_exists_on_wl528_quartic": False if verified else None,
    }


def _flags() -> dict[str, Any]:
    flags = dict.fromkeys(NO_CLAIM_KEYS, False)
    flags["family_exclusion_proved_count"] = 0
    flags["stop_after_current_task"] = True
    return flags


def _proof_status(work_log: str) -> dict[str, Any]:
    if work_log == "wl528":
        return {
            "function_field_nonsquare_certificate_proved_here": True,
            "divisor_parity_certificate_proved_here": False,
            "uniform_specialization_survival_proved_here": False,
            "uniform_cover_family_obstruction_proved_here": False,
            "ready_as_reviewable_single_prototype": True,
            "ready_as_uniform_cover_family_theorem": False,
        }
    return {
        "divisor_parity_only_proves_generic_nonsquareness": True,
        "genus_one_rational_point_certificate_proved_here": True,
        "nonexceptional_positive_square_specialization_absent": True,
        "one_family_positive_square_obstruction_proved_here": True,
        "uniform_cover_family_obstruction_proved_here": False,
        "ready_as_reviewable_single_family_square_locus": True,
        "ready_as_uniform_cover_family_theorem": False,
    }


def build_b1(*, b0: B0Document, sage_certificate: SageCertificate) -> B1Evidence:
    """Recompute the protected B1 mathematics from tracked B0 and Sage inputs."""

    rows = _input_rows(b0)
    model = _function_field_model()
    specialization = _specialization(rows)
    models, square_checks = _square_locus()
    t_zero = _t_zero()
    checks_ok = (
        all(model["identity_checks"].values())
        and all(specialization["checks"].values())
        and all(item["verified"] for item in square_checks)
        and t_zero["certificate_verified"]
        and sage_certificate.document["sage"] == EXPECTED_SAGE
    )
    if not checks_ok:
        raise B1Error("B1: protected mathematical prerequisite failed")
    flags = _flags()
    wl528 = {
        "status": "ok",
        "ready": True,
        "work_log": "wl528",
        "object_layer": "single_cover_family_function_field_prototype",
        "prototype_scope": SCOPE,
        "selected_wl495_entries": rows,
        "function_field_model": model,
        "source_side_maps_and_N_M": _source_maps(),
        "opposite_side_product": {
            "opposite_product_in_t": "((t^2 + 89)^2 - 100*t^2)/16",
            "opposite_product_in_N_M": "(N^2+16)(M^2+16)",
            "function_field_nonsquare_certificate": specialization,
        },
        "exceptional_divisors_and_positivity": {
            "poles_or_undefined_loci": [
                "r = 0 for the chosen cover chart",
                "r^2 = 20 where X+p = 0 and the centered-even t map is undefined",
            ],
            "zero_loci_not_fully_classified_here": [
                "zeros of the opposite-side product",
                "zeros of N, M, and source/opposite product factors",
            ],
            "positivity_status": (
                "The recorded rational specialization has N=11/2 and M=-1/2, so M "
                "positivity fails at that point."
            ),
        },
        "proof_status": _proof_status("wl528"),
        **flags,
    }
    wl529 = {
        "status": "ok",
        "ready": True,
        "work_log": "wl529",
        "object_layer": "single_cover_family_square_specialization_locus",
        "prototype_scope": SCOPE,
        "selected_wl495_entries": rows,
        "square_locus_models": models,
        "identity_checks": square_checks,
        "genus_one_certificate": sage_certificate.document["sage"],
        "rational_point_analysis": {
            "positivity_domain": "|t| < 5",
            "positive_source_condition": "N=(5+t)/2 > 0 and M=(5-t)/2 > 0",
            "affine_square_locus_rational_t_candidates": [0],
            "t_zero_preimage_analysis": t_zero,
            "nonexceptional_positive_square_specializations_exist": False,
        },
        "proof_status": _proof_status("wl529"),
        **flags,
    }
    return B1Evidence({"wl528": wl528, "wl529": wl529}, sage_certificate)


def _no_claims(payload: dict[str, Any]) -> dict[str, Any]:
    proof = payload.get("proof_status", {})
    return {key: payload.get(key, proof.get(key, False)) for key in NO_CLAIM_KEYS}


def _reduce_product(payload: dict[str, Any]) -> dict[str, Any]:
    product = payload["opposite_side_product"]
    certificate = product["function_field_nonsquare_certificate"]
    if "checks" in certificate:
        reduced = certificate
    else:
        reduced = {
            "values": certificate["specialization"],
            "checks": {
                item["check_id"]: item["passed"]
                for item in certificate["certificate_prerequisite_checks"]
            },
            "specialized_value": certificate["specialized_value"],
            "specialized_value_is_rational_square": certificate[
                "specialized_value_is_rational_square"
            ],
        }
    return {
        "opposite_product_in_t": product["opposite_product_in_t"],
        "opposite_product_in_N_M": product["opposite_product_in_N_M"],
        "function_field_nonsquare_certificate": reduced,
    }


def _reduce_proof(proof: dict[str, Any], work_log: str) -> dict[str, Any]:
    return {key: proof[key] for key in _proof_status(work_log)}


def semantic_projection(
    payload: dict[str, Any], work_log: Literal["wl528", "wl529"]
) -> dict[str, Any]:
    """Project legacy or B1 output onto the protected mathematical surface."""

    if work_log not in {"wl528", "wl529"} or payload["work_log"] != work_log:
        raise B1Error(f"unsupported B1 work log: {work_log}")
    projection = {
        "work_log": work_log,
        "object_layer": payload["object_layer"],
        "prototype_scope": payload["prototype_scope"],
        "selected_input_rows": [_normalize_row(row) for row in payload["selected_wl495_entries"]],
        "proof_status": _reduce_proof(payload["proof_status"], work_log),
        "no_claims": _no_claims(payload),
    }
    if work_log == "wl528":
        exceptional = payload["exceptional_divisors_and_positivity"]
        projection.update(
            function_field_model=_reduce_model(payload["function_field_model"]),
            source_side_maps_and_N_M=_reduce_source_maps(payload["source_side_maps_and_N_M"]),
            opposite_side_product=_reduce_product(payload),
            exceptional_divisors_and_positivity={
                "poles_or_undefined_loci": exceptional["poles_or_undefined_loci"],
                "zero_loci_not_fully_classified_here": exceptional[
                    "zero_loci_not_fully_classified_here"
                ],
                "positivity_fails_at_specialization": "M positivity fails"
                in exceptional["positivity_status"],
            },
        )
    else:
        analysis = payload["rational_point_analysis"]
        t_zero = analysis["t_zero_preimage_analysis"]
        projection.update(
            square_locus_models=payload["square_locus_models"],
            identity_checks=[
                {"check_id": item["check_id"], "verified": item["verified"]}
                for item in payload["identity_checks"]
            ],
            genus_one_certificate=payload["genus_one_certificate"],
            rational_point_analysis={
                "positivity_domain": analysis["positivity_domain"],
                "positive_source_condition": analysis["positive_source_condition"],
                "affine_square_locus_rational_t_candidates": analysis[
                    "affine_square_locus_rational_t_candidates"
                ],
                "t_zero": {
                    key: t_zero[key]
                    for key in (
                        "candidate_t_value",
                        "derived_r2_equation",
                        "t_zero_forces_y_zero",
                        "discriminant",
                        "discriminant_factorization",
                        "discriminant_is_rational_square",
                        "certificate_verified",
                        "rational_preimage_exists_on_wl528_quartic",
                    )
                },
                "nonexceptional_positive_square_specializations_exist": analysis[
                    "nonexceptional_positive_square_specializations_exist"
                ],
            },
        )
    return projection


def project_b1(b1: B1Evidence, work_log: Literal["wl528", "wl529"]) -> dict[str, Any]:
    return semantic_projection(b1.projections[work_log], work_log)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path)
    parser.add_argument("--sage-artifact", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--refresh-sage-artifact", action="store_true")
    parser.add_argument("--sage", default="sage")
    args = parser.parse_args()
    if args.refresh_sage_artifact:
        if args.sage_artifact is None:
            parser.error("--sage-artifact is required with --refresh-sage-artifact")
        refresh_sage_certificate(args.sage_artifact, args.sage)
        return 0
    if args.data_dir is None or args.sage_artifact is None or args.out is None:
        parser.error("--data-dir, --sage-artifact, and --out are required")
    b1 = build_b1(
        b0=load_b0(args.data_dir),
        sage_certificate=load_sage_certificate(args.sage_artifact),
    )
    output = {"status": b1.status, "work_log": "b1", **b1.projections}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(f"status={b1.status} work_log=b1")
    return int(args.strict and b1.status != "ok")


if __name__ == "__main__":
    raise SystemExit(main())
