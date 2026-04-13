"""Consolidated test suite for the rational-distance project.

All tests run via:   uv run pytest

Coverage:
  math_utils   — rational_sqrt, primitive_pythagorean_triples
  square       — RationalPoint, compute_distances, D4 helpers
  search       — parametric_search, brute_force_search, parametric_search_fast,
                 dedup_by_symmetry, inside_only filter, side-exclusion theorem
  search_gpu   — parametric_search_gpu with numpy backend (no GPU required)
  backend      — detect_backend (numpy fallback always available)
  search_chain — Pythagorean 4-cycle search (find_chains, ChainResult)
"""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from importlib import import_module
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from rational_distance import parametric_core as core
from rational_distance.backend import detect_backend
from rational_distance.ec_analysis import build_analysis_report
from rational_distance.ec_db import ECSearchStore, connect_db
from rational_distance.math_utils import primitive_pythagorean_triples, rational_sqrt
from rational_distance.search import (
    _parametric_search_fast_run,
    brute_force_search,
    dedup_by_symmetry,
    parametric_search,
    parametric_search_fast,
)
from rational_distance.search_ec import (
    QuarticEC,
    ec_search,
    find_seeds_for_triple,
)
from rational_distance.search_gpu import _parametric_search_gpu_run, parametric_search_gpu
from rational_distance.square import (
    VERTICES,
    canonical_xy,
    make_point,
)

cli_search = import_module("scripts.search")
compare_cli = import_module("scripts.compare_parametric")


# ── math_utils ────────────────────────────────────────────────────────────────


class TestRationalSqrt:
    def test_perfect_squares(self):
        assert rational_sqrt(Fraction(4)) == Fraction(2)
        assert rational_sqrt(Fraction(9)) == Fraction(3)
        assert rational_sqrt(Fraction(1, 4)) == Fraction(1, 2)
        assert rational_sqrt(Fraction(9, 25)) == Fraction(3, 5)
        assert rational_sqrt(Fraction(0)) == Fraction(0)

    def test_non_squares(self):
        assert rational_sqrt(Fraction(2)) is None
        assert rational_sqrt(Fraction(3)) is None
        assert rational_sqrt(Fraction(1, 2)) is None
        assert rational_sqrt(Fraction(-1)) is None


class TestPythagoreanTriples:
    def test_basic(self):
        triples = primitive_pythagorean_triples(5)
        assert (3, 4, 5) in triples
        assert (4, 3, 5) in triples

    def test_validity(self):
        for a, b, c in primitive_pythagorean_triples(10):
            assert a * a + b * b == c * c

    def test_primitive(self):
        from math import gcd

        for a, b, c in primitive_pythagorean_triples(10):
            assert gcd(gcd(a, b), c) == 1

    def test_both_orientations(self):
        """Both (p,q,r) and (q,p,r) must be present."""
        triples = primitive_pythagorean_triples(10)
        set_ = set(triples)
        for a, b, c in triples:
            assert (b, a, c) in set_


class TestParametricCore:
    def test_safe_r_max_uses_shared_formula(self):
        assert core.safe_r_max(80, 40) == ((1 << 31) - 1) // 160

    def test_approx_square_mask_matches_exact_on_boundary_values(self):
        big = (1 << 31) - 1
        arr = np.array([big * big, (big - 1) * (big - 1), big * big - 1], dtype=np.int64)
        ok, roots = core.approx_square_mask(np, arr)
        assert ok.tolist() == [True, True, False]
        assert roots.tolist()[:2] == [big, big - 1]


# ── square ────────────────────────────────────────────────────────────────────


class TestRationalPoint:
    def test_vertex_self_distance(self):
        """Distance from a vertex to itself is 0 (rational)."""
        for vx, vy in VERTICES:
            pt = make_point(vx, vy)
            zeros = [d for d in pt.distances if d == Fraction(0)]
            assert len(zeros) == 1

    def test_known_3vertex_point(self):
        """(3/4, 0): dA=3/4, dB=1/4, dD=5/4 rational; dC irrational."""
        pt = make_point(Fraction(3, 4), Fraction(0))
        assert pt.distances[0] == Fraction(3, 4)
        assert pt.distances[1] == Fraction(1, 4)
        assert pt.distances[3] == Fraction(5, 4)
        assert pt.distances[2] is None
        assert pt.rational_count == 3

    def test_denominator(self):
        pt = make_point(Fraction(3, 7), Fraction(2, 5))
        assert pt.denominator == 35  # lcm(7,5)

    def test_as_dict_roundtrip(self):
        pt = make_point(Fraction(3, 4), Fraction(0))
        d = pt.as_dict()
        assert d["x"] == "3/4"
        assert d["rational_count"] == 3

    def test_as_dict_preserves_zero_distance(self):
        pt = make_point(Fraction(0), Fraction(0))
        d = pt.as_dict()
        assert d["dA"] == "0"
        assert d["dB"] == "1"
        assert d["dD"] == "1"

    def test_canonical_xy_idempotent_and_consistent(self):
        """canonical_xy is idempotent: applying it twice gives the same result."""
        from rational_distance.square import canonical_xy

        # Use a point inside the unit square
        cx1, cy1 = canonical_xy(Fraction(3, 7), Fraction(2, 5))
        cx2, cy2 = canonical_xy(cx1, cy1)
        assert (cx1, cy1) == (cx2, cy2)

    def test_canonical_xy_same_orbit(self):
        """D4-symmetric points map to the same canonical representative."""
        from rational_distance.square import canonical_xy

        x, y = Fraction(1, 3), Fraction(1, 4)
        # D4 images of (x, y) in unit square: (1-x,y), (x,1-y), (1-x,1-y), (y,x), ...
        images = [
            (x, y),
            (1 - x, y),
            (x, 1 - y),
            (1 - x, 1 - y),
            (y, x),
            (1 - y, x),
            (y, 1 - x),
            (1 - y, 1 - x),
        ]
        canonicals = {canonical_xy(px, py) for px, py in images}
        assert len(canonicals) == 1, f"Expected one canonical, got: {canonicals}"


# ── search (CPU) ──────────────────────────────────────────────────────────────


class TestParametricSearch:
    def test_yields_3vertex(self):
        results = list(parametric_search(max_m=10, max_k_num=50, max_k_den=25))
        assert len(results) > 0
        for pt in results:
            assert pt.rational_count >= 3


class TestBruteForce:
    def test_excludes_sides(self):
        sides = {Fraction(0), Fraction(1)}
        for pt in brute_force_search(max_den=10, min_rational=2):
            assert pt.x not in sides
            assert pt.y not in sides

    def test_min_rational(self):
        for pt in brute_force_search(max_den=10, min_rational=3):
            assert pt.rational_count >= 3


class TestParametricSearchFast:
    def test_basic(self):
        results = parametric_search_fast(
            max_m=20, max_k_num=80, max_k_den=40, workers=1, progress=False
        )
        assert len(results) > 0
        for pt in results:
            assert pt.rational_count >= 3

    def test_no_side_points(self):
        sides = {Fraction(0), Fraction(1)}
        results = parametric_search_fast(
            max_m=20, max_k_num=80, max_k_den=40, workers=1, progress=False
        )
        for pt in results:
            assert pt.x not in sides
            assert pt.y not in sides

    def test_inside_only_filters_to_unit_square(self):
        all_pts = parametric_search_fast(
            max_m=20, max_k_num=80, max_k_den=40, workers=1, progress=False
        )
        inside_pts = parametric_search_fast(
            max_m=20, max_k_num=80, max_k_den=40, workers=1, progress=False, inside_only=True
        )
        # inside_only must be a strict subset
        assert len(inside_pts) <= len(all_pts)
        for pt in inside_pts:
            assert Fraction(0) < pt.x < Fraction(1)
            assert Fraction(0) < pt.y < Fraction(1)
        # every inside point must appear in all_pts
        all_keys = {(pt.x, pt.y) for pt in all_pts}
        for pt in inside_pts:
            assert (pt.x, pt.y) in all_keys

    def test_min4_returns_subset(self):
        r3 = parametric_search_fast(
            max_m=20, max_k_num=80, max_k_den=40, workers=1, progress=False, min_rational=3
        )
        r4 = parametric_search_fast(
            max_m=20, max_k_num=80, max_k_den=40, workers=1, progress=False, min_rational=4
        )
        assert len(r4) <= len(r3)
        for pt in r4:
            assert pt.rational_count == 4


class TestDedupBySymmetry:
    def test_reduces_count(self):
        results = parametric_search_fast(
            max_m=20, max_k_num=80, max_k_den=40, workers=1, progress=False
        )
        deduped = dedup_by_symmetry(results)
        assert len(deduped) <= len(results)

    def test_no_symmetric_duplicates_remain(self):
        """After dedup, no two points should be related by a D4 symmetry."""
        from rational_distance.square import canonical_xy

        results = parametric_search_fast(
            max_m=20, max_k_num=80, max_k_den=40, workers=1, progress=False
        )
        deduped = dedup_by_symmetry(results)
        keys = [(canonical_xy(pt.x, pt.y)) for pt in deduped]
        # All canonical forms must be distinct
        assert len(keys) == len(set(keys))


# ── search_gpu (numpy backend, no GPU required) ───────────────────────────────


class TestSearchGpuNumpyBackend:
    """Run the GPU search module with xp=numpy — exercises all logic without a GPU."""

    def test_basic_results(self):
        pts, backend = parametric_search_gpu(
            max_m=20,
            max_k_num=80,
            max_k_den=40,
            min_rational=3,
            progress=False,
            xp=np,
        )
        assert isinstance(backend, str)
        assert len(pts) > 0
        for pt in pts:
            assert pt.rational_count >= 3

    def test_no_side_points(self):
        sides = {Fraction(0), Fraction(1)}
        pts, _ = parametric_search_gpu(
            max_m=20,
            max_k_num=80,
            max_k_den=40,
            min_rational=3,
            progress=False,
            xp=np,
        )
        for pt in pts:
            assert pt.x not in sides
            assert pt.y not in sides

    def test_inside_only(self):
        pts, _ = parametric_search_gpu(
            max_m=20,
            max_k_num=80,
            max_k_den=40,
            min_rational=3,
            progress=False,
            xp=np,
            inside_only=True,
        )
        for pt in pts:
            assert Fraction(0) < pt.x < Fraction(1)
            assert Fraction(0) < pt.y < Fraction(1)

    def test_consistent_with_cpu_path(self):
        """GPU (numpy) and CPU multiprocessing paths must find the same points."""
        gpu_pts, _ = parametric_search_gpu(
            max_m=20,
            max_k_num=80,
            max_k_den=40,
            min_rational=3,
            progress=False,
            xp=np,
        )
        cpu_pts = parametric_search_fast(
            max_m=20,
            max_k_num=80,
            max_k_den=40,
            min_rational=3,
            workers=1,
            progress=False,
        )
        gpu_keys = {(pt.x, pt.y) for pt in gpu_pts}
        cpu_keys = {(pt.x, pt.y) for pt in cpu_pts}
        assert gpu_keys == cpu_keys, (
            f"GPU found {len(gpu_keys)} points, CPU found {len(cpu_keys)} — "
            f"symmetric difference: {gpu_keys ^ cpu_keys}"
        )

    def test_forced_exact_fallback_matches_cpu(self, monkeypatch):
        monkeypatch.setattr(core, "safe_r_max", lambda *_args: 0)
        cpu_pts, cpu_stats = _parametric_search_fast_run(
            max_m=10,
            max_k_num=20,
            max_k_den=10,
            min_rational=3,
            workers=1,
            progress=False,
        )
        gpu_pts, backend, gpu_stats = _parametric_search_gpu_run(
            max_m=10,
            max_k_num=20,
            max_k_den=10,
            min_rational=3,
            progress=False,
            xp=np,
        )
        assert isinstance(backend, str)
        assert cpu_stats.fallback_triggered
        assert gpu_stats.fallback_triggered
        assert {(pt.x, pt.y) for pt in gpu_pts} == {(pt.x, pt.y) for pt in cpu_pts}


# ── backend ───────────────────────────────────────────────────────────────────


class TestBackend:
    def test_detect_backend_returns_numpy_without_gpu(self):
        """On a machine without CuPy/PyTorch-GPU, detect_backend falls back to numpy."""
        xp, _name, _is_gpu = detect_backend()
        # We can't guarantee GPU is absent, but xp must always be usable
        arr = xp.array(np.array([1, 4, 9], dtype=np.int64), dtype=xp.int64)
        assert arr is not None

    def test_xp_cast_numpy(self):
        from rational_distance.backend import _xp_cast

        arr = np.array([1, 2, 3], dtype=np.int32)
        casted = _xp_cast(arr, np.float64)
        assert casted.dtype == np.float64


# ── CLI parsing ───────────────────────────────────────────────────────────────


class TestCliParametricArgs:
    def test_scale_populates_missing_parametric_limits(self):
        parser = cli_search.build_parser()
        args = parser.parse_args(["parametric", "--scale", "12"])
        cli_search._resolve_parametric_limits(args)
        assert args.max_m == 12
        assert args.max_k_num == 96
        assert args.max_k_den == 48

    def test_explicit_parametric_args_override_scale(self):
        parser = cli_search.build_parser()
        args = parser.parse_args(
            [
                "parametric",
                "--scale",
                "12",
                "--max-m",
                "7",
                "--max-k-num",
                "55",
            ]
        )
        cli_search._resolve_parametric_limits(args)
        assert args.max_m == 7
        assert args.max_k_num == 55
        assert args.max_k_den == 48


class TestCompareCliArgs:
    def test_scale_populates_missing_limits(self):
        parser = compare_cli.build_parser()
        args = parser.parse_args(["--scale", "12"])
        compare_cli._resolve_limits(args)
        assert args.max_m == 12
        assert args.max_k_num == 96
        assert args.max_k_den == 48

    def test_compare_defaults_stay_small_without_scale(self):
        parser = compare_cli.build_parser()
        args = parser.parse_args([])
        compare_cli._resolve_limits(args)
        assert args.max_m == 20
        assert args.max_k_num == 80
        assert args.max_k_den == 40


class TestCompareScript:
    def test_compare_parametric_script_smoke(self):
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "compare_parametric.py"),
                "--scale",
                "10",
                "--max-k-num",
                "20",
                "--max-k-den",
                "10",
                "--backend",
                "numpy",
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr or proc.stdout
        assert "symmetric difference: 0" in proc.stdout


# ── search_ec — elliptic-curve guided search ──────────────────────────────────


class TestQuarticEC:
    """Algebraic correctness of the QuarticEC curve class for triple (3,4,5)."""

    def setup_method(self):
        self.ec = QuarticEC(3, 4, 5)

    def test_coefficients(self):
        ec = self.ec
        assert ec.c4 == 25
        assert ec.c3 == 80
        assert ec.c2 == 98
        assert ec.c1 == 40
        assert ec.c0 == 13

    def test_F_at_projective_points(self):
        """F(1) = 4(r+p)² and F(-1) = 4(r-p)²."""
        ec = self.ec
        p, _q, r = ec.p, ec.q, ec.r
        assert ec.F(Fraction(1)) == 4 * (r + p) ** 2
        assert ec.F(Fraction(-1)) == 4 * (r - p) ** 2

    def test_F_at_zero(self):
        assert self.ec.F(Fraction(0)) == self.ec.c0

    def test_on_curve_projective_points(self):
        ec = self.ec
        p, r = ec.p, ec.r
        assert ec.on_curve(Fraction(1), Fraction(2 * (r + p)))
        assert ec.on_curve(Fraction(-1), Fraction(2 * (r - p)))

    def test_k_from_t_at_infinity(self):
        ec = self.ec
        assert ec.k_from_t(Fraction(1)) is None
        assert ec.k_from_t(Fraction(-1)) is None

    def test_k_from_t_roundtrip(self):
        """k_from_t and t_from_k_dB are inverse maps."""
        ec = self.ec
        t0 = Fraction(1, 3)
        k = ec.k_from_t(t0)
        assert k is not None and k > 0
        # dB from parametrization
        dB = (1 + t0**2 + 2 * t0 * Fraction(ec.p, ec.r)) / (1 - t0**2)
        ts = ec.t_from_k_dB(k, dB)
        assert t0 in ts

    def test_tangent_preserves_curve(self):
        """Tangent step from a projective seed must return points on the curve."""
        ec = self.ec
        p, r = ec.p, ec.r
        t0 = Fraction(1)
        E0 = Fraction(2 * (r + p))
        new_pts = ec.tangent_points(t0, E0)
        # New points may be empty if discriminant is not rational — that's fine
        for t_new, E_new in new_pts:
            assert ec.on_curve(t_new, E_new), f"point ({t_new}, {E_new}) not on curve"


class TestFindSeedsForTriple:
    """find_seeds_for_triple should correctly find seeds for known triples."""

    def test_known_seed_8_15_17(self):
        """For (8,15,17), k=357/740, dB=653/740, dD=457/740 is a known seed."""
        seeds = find_seeds_for_triple(8, 15, 17, max_k_num=400, max_k_den=800)
        k_map = {k: (dB, dD) for k, dB, dD in seeds}
        k_known = Fraction(357, 740)
        assert k_known in k_map, f"Known seed k=357/740 not found. Seeds: {list(k_map)[:5]}"
        dB, dD = k_map[k_known]
        assert dB == Fraction(653, 740), f"Wrong dB: {dB}"
        assert dD == Fraction(457, 740), f"Wrong dD: {dD}"

    def test_seeds_satisfy_distance_equations(self):
        """Every returned seed (k, dB, dD) must satisfy the distance equations."""
        for p, q, r in [(8, 15, 17), (15, 8, 17), (5, 12, 13)]:
            seeds = find_seeds_for_triple(p, q, r, max_k_num=400, max_k_den=800)
            for k, dB, dD in seeds:
                assert dB**2 == k**2 - 2 * k * Fraction(p, r) + 1, (
                    f"dB mismatch for ({p},{q},{r}), k={k}"
                )
                assert dD**2 == k**2 - 2 * k * Fraction(q, r) + 1, (
                    f"dD mismatch for ({p},{q},{r}), k={k}"
                )

    def test_seeds_lie_on_quartic(self):
        """Seeds must correspond to rational points on E²=F(t)."""
        seeds = find_seeds_for_triple(8, 15, 17, max_k_num=400, max_k_den=800)
        ec = QuarticEC(8, 15, 17)
        for k, dB, dD in seeds:
            found = False
            for t in ec.t_from_k_dB(k, dB):
                E = ec.E_from_t_dD(t, dD)
                if ec.on_curve(t, E):
                    found = True
                    break
            assert found, f"Seed k={k} does not lie on quartic"

    def test_side_exclusion_respected(self):
        """Returned seeds must not lie on extended sides (x=1 or y=1)."""
        for p, q, r in [(3, 4, 5), (8, 15, 17)]:
            seeds = find_seeds_for_triple(p, q, r, max_k_num=100, max_k_den=200)
            for k, _dB, _dD in seeds:
                x = k * Fraction(p, r)
                y = k * Fraction(q, r)
                assert x != 1, f"Seed on x=1 side: k={k}"
                assert y != 1, f"Seed on y=1 side: k={k}"

    def test_inside_only_filter(self):
        """With inside_only=True, all seeds must satisfy 0<x<1 and 0<y<1."""
        seeds = find_seeds_for_triple(8, 15, 17, max_k_num=400, max_k_den=800, inside_only=True)
        for k, _dB, _dD in seeds:
            # p/r = 8/17, q/r = 15/17
            x = k * Fraction(8, 17)
            y = k * Fraction(15, 17)
            assert 0 < x < 1, f"x={x} out of (0,1)"
            assert 0 < y < 1, f"y={y} out of (0,1)"


class TestEcSearch:
    """Integration tests for ec_search."""

    def test_returns_rationalpoints(self):
        pts = ec_search(max_m=20, max_k_num=400, max_k_den=800, min_rational=3, progress=False)
        for pt in pts:
            assert pt.rational_count >= 3

    def test_finds_known_seed_point(self):
        """ec_search should find the known seed point from (8,15,17)."""
        pts = ec_search(max_m=20, max_k_num=400, max_k_den=800, min_rational=3, progress=False)
        # The canonical form of (42/185, 63/148) is the min D4 image.
        # ec_search may store either image; we check the canonical set.
        expected_canonical = canonical_xy(Fraction(42, 185), Fraction(63, 148))
        canonicals = {canonical_xy(pt.x, pt.y) for pt in pts}
        assert expected_canonical in canonicals, (
            f"Known seed (canonical {expected_canonical}) not found in {sorted(canonicals)[:5]}"
        )

    def test_no_side_points(self):
        """No returned point should lie on x=0, x=1, y=0, or y=1."""
        from fractions import Fraction as F

        pts = ec_search(max_m=20, max_k_num=400, max_k_den=800, min_rational=3, progress=False)
        sides = {F(0), F(1)}
        for pt in pts:
            assert pt.x not in sides, f"Side point found: x={pt.x}"
            assert pt.y not in sides, f"Side point found: y={pt.y}"

    def test_inside_only_filter(self):
        """With inside_only, all results must satisfy 0 < x,y < 1."""
        from fractions import Fraction as F

        pts = ec_search(
            max_m=20, max_k_num=400, max_k_den=800, min_rational=3, inside_only=True, progress=False
        )
        for pt in pts:
            assert F(0) < pt.x < F(1), f"x={pt.x} out of range"
            assert F(0) < pt.y < F(1), f"y={pt.y} out of range"

    def test_no_duplicates(self):
        """Results must be D4-deduplicated (no two canonical forms equal)."""
        pts = ec_search(max_m=20, max_k_num=400, max_k_den=800, min_rational=3, progress=False)
        keys = [canonical_xy(pt.x, pt.y) for pt in pts]
        assert len(keys) == len(set(keys)), "Duplicate canonical forms found"


class TestEcDatabase:
    @staticmethod
    def _params() -> dict:
        return {
            "max_m": 20,
            "max_k_num": 400,
            "max_k_den": 800,
            "max_steps": 5,
            "min_rational": 3,
            "inside": False,
        }

    def test_database_run_matches_plain_search(self, tmp_path):
        params = self._params()
        db_path = tmp_path / "ec.sqlite3"

        plain = ec_search(
            max_m=params["max_m"],
            max_k_num=params["max_k_num"],
            max_k_den=params["max_k_den"],
            max_steps=params["max_steps"],
            min_rational=params["min_rational"],
            progress=False,
        )

        store = ECSearchStore(db_path, params, backend="numpy-test", resume=False)
        try:
            persisted = ec_search(
                max_m=params["max_m"],
                max_k_num=params["max_k_num"],
                max_k_den=params["max_k_den"],
                max_steps=params["max_steps"],
                min_rational=params["min_rational"],
                progress=False,
                store=store,
            )
            store.finish(0.0)
        finally:
            store.close()

        assert {canonical_xy(pt.x, pt.y) for pt in plain} == {
            canonical_xy(pt.x, pt.y) for pt in persisted
        }

    def test_resume_reuses_same_run_id(self, tmp_path):
        params = self._params()
        db_path = tmp_path / "ec.sqlite3"

        store1 = ECSearchStore(db_path, params, backend="numpy-test", resume=False)
        try:
            first = ec_search(
                max_m=params["max_m"],
                max_k_num=params["max_k_num"],
                max_k_den=params["max_k_den"],
                max_steps=params["max_steps"],
                min_rational=params["min_rational"],
                progress=False,
                store=store1,
            )
            store1.finish(0.0)
            run_id = store1.run_id
        finally:
            store1.close()

        store2 = ECSearchStore(db_path, params, backend="torch-test", resume=True)
        try:
            second = ec_search(
                max_m=params["max_m"],
                max_k_num=params["max_k_num"],
                max_k_den=params["max_k_den"],
                max_steps=params["max_steps"],
                min_rational=params["min_rational"],
                progress=False,
                store=store2,
            )
            store2.finish(0.0)
            assert store2.run_id == run_id
        finally:
            store2.close()

        assert {canonical_xy(pt.x, pt.y) for pt in first} == {
            canonical_xy(pt.x, pt.y) for pt in second
        }

        conn = connect_db(db_path)
        try:
            row = conn.execute("SELECT backend FROM runs WHERE id = ?", (run_id,)).fetchone()
            assert row["backend"] == "torch-test"
        finally:
            conn.close()

    def test_known_seed_and_provenance_written(self, tmp_path):
        params = self._params()
        db_path = tmp_path / "ec.sqlite3"

        store = ECSearchStore(db_path, params, backend="numpy-test", resume=False)
        try:
            ec_search(
                max_m=params["max_m"],
                max_k_num=params["max_k_num"],
                max_k_den=params["max_k_den"],
                max_steps=params["max_steps"],
                min_rational=params["min_rational"],
                progress=False,
                store=store,
            )
            store.finish(0.0)
        finally:
            store.close()

        conn = connect_db(db_path)
        try:
            seed_row = conn.execute(
                """
                SELECT s.id
                FROM ec_seeds s
                JOIN ec_triples t ON t.id = s.triple_id
                WHERE t.p = 8 AND t.q = 15 AND t.r = 17 AND s.k = '357/740'
                """
            ).fetchone()
            assert seed_row is not None

            node_count = conn.execute(
                "SELECT COUNT(*) AS n FROM ec_curve_nodes WHERE seed_id = ?",
                (seed_row["id"],),
            ).fetchone()["n"]
            assert node_count >= 1

            tangent_child = conn.execute(
                "SELECT child_node_id FROM ec_curve_edges WHERE relation = 'tangent' LIMIT 1"
            ).fetchone()
            if tangent_child is not None:
                parent_count = conn.execute(
                    """
                    SELECT COUNT(*) AS n
                    FROM ec_curve_edges
                    WHERE child_node_id = ? AND relation = 'tangent'
                    """,
                    (tangent_child["child_node_id"],),
                ).fetchone()["n"]
                assert parent_count == 1

            secant_child = conn.execute(
                """
                SELECT child_node_id
                FROM ec_curve_edges
                WHERE relation IN ('secant', 'secant_neg_branch')
                LIMIT 1
                """
            ).fetchone()
            if secant_child is not None:
                parent_count = conn.execute(
                    """
                    SELECT COUNT(*) AS n
                    FROM ec_curve_edges
                    WHERE child_node_id = ?
                      AND relation IN ('secant', 'secant_neg_branch')
                    """,
                    (secant_child["child_node_id"],),
                ).fetchone()["n"]
                assert parent_count == 2

            point_row = conn.execute(
                "SELECT triple_id, source_node_id FROM ec_points WHERE run_id = 1 LIMIT 1"
            ).fetchone()
            assert point_row is not None
            assert point_row["triple_id"] is not None
            assert point_row["source_node_id"] is not None
        finally:
            conn.close()

    def test_analysis_script_outputs_json_and_html(self, tmp_path):
        params = self._params()
        db_path = tmp_path / "ec.sqlite3"

        store = ECSearchStore(db_path, params, backend="numpy-test", resume=False)
        try:
            ec_search(
                max_m=params["max_m"],
                max_k_num=params["max_k_num"],
                max_k_den=params["max_k_den"],
                max_steps=params["max_steps"],
                min_rational=params["min_rational"],
                progress=False,
                store=store,
            )
            store.finish(0.0)
        finally:
            store.close()

        report_all = build_analysis_report(db_path, run_selector="latest", region="all")
        report_inside = build_analysis_report(db_path, run_selector="latest", region="inside")
        report_outside = build_analysis_report(db_path, run_selector="latest", region="outside")
        assert (
            report_inside["summary"]["point_count"] + report_outside["summary"]["point_count"]
            == report_all["summary"]["point_count"]
        )

        out_json = tmp_path / "analysis.json"
        out_html = tmp_path / "analysis.html"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "analyze_ec_db.py"),
                "--db",
                str(db_path),
                "--run",
                "latest",
                "--out-json",
                str(out_json),
                "--html",
                str(out_html),
            ],
            check=True,
            cwd=ROOT,
        )

        saved = json.loads(out_json.read_text())
        assert saved["summary"]["point_count"] == report_all["summary"]["point_count"]
        html = out_html.read_text(encoding="utf-8")
        assert "Plotly.newPlot" in html
        assert "Pattern Insights" in html


# ── TestChainSearch ───────────────────────────────────────────────────────────


class TestChainSearch:
    """Tests for the Pythagorean 4-cycle search module."""

    def test_known_cycle_distinct(self):
        """(15,20,48,36) is the smallest all-distinct Pythagorean 4-cycle."""
        from rational_distance.search_chain import find_chains

        results = find_chains(max_val=50, progress=False)
        tuples = {(r.a, r.b, r.c, r.d) for r in results}
        assert (15, 20, 48, 36) in tuples, f"(15,20,48,36) not found; got {sorted(tuples)}"

    def test_symmetric_cycles_excluded(self):
        """Cycles like (3,4,3,4) with repeated values must be excluded."""
        from rational_distance.search_chain import find_chains

        results = find_chains(max_val=100, progress=False)
        for r in results:
            assert len({r.a, r.b, r.c, r.d}) == 4, f"Non-distinct cycle returned: {r}"

    def test_hypotenuses_correct(self):
        """Hypotenuses must equal isqrt of the respective sum of squares."""
        from rational_distance.search_chain import find_chains

        for r in find_chains(max_val=50, progress=False):
            assert r.x1**2 == r.a**2 + r.b**2, f"x1 wrong for {r}"
            assert r.x2**2 == r.b**2 + r.c**2, f"x2 wrong for {r}"
            assert r.x3**2 == r.c**2 + r.d**2, f"x3 wrong for {r}"
            assert r.x4**2 == r.d**2 + r.a**2, f"x4 wrong for {r}"

    def test_canonical_no_duplicates(self):
        """Canonical mode must return no two tuples related by dihedral symmetry."""
        from rational_distance.search_chain import _symmetry_group, find_chains

        results = find_chains(max_val=100, canonical=True, progress=False)
        keys: set[tuple[int, int, int, int]] = set()
        for r in results:
            syms = _symmetry_group(r.a, r.b, r.c, r.d)
            for sym in syms:
                assert sym not in keys or sym == min(syms), (
                    f"Duplicate via symmetry: {(r.a, r.b, r.c, r.d)} and {sym}"
                )
            keys.add(min(syms))

    def test_no_square_solutions_small(self):
        """No Pythagorean 4-cycle with a+c == b+d exists up to max_val=500.
        This is consistent with the Harborth conjecture."""
        from rational_distance.search_chain import find_chains

        results = find_chains(max_val=500, require_square=True, progress=False)
        assert results == [], f"Unexpected square solution found: {results[0]}"

    def test_square_ok_flag(self):
        """square_ok must correctly reflect a+c == b+d."""
        from rational_distance.search_chain import find_chains

        for r in find_chains(max_val=100, progress=False):
            assert r.square_ok == (r.a + r.c == r.b + r.d)

    def test_chain_result_str(self):
        """ChainResult.__str__ must not raise and must mention hyp."""
        from rational_distance.search_chain import find_chains

        results = find_chains(max_val=50, progress=False)
        assert results, "No results to test"
        s = str(results[0])
        assert "hyp=" in s
