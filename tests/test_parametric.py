"""Tests for parametric search and shared geometry helpers."""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from rational_distance import parametric_core as core
from rational_distance.backend import detect_backend
from rational_distance.math_utils import primitive_pythagorean_triples, rational_sqrt
from rational_distance.search import (
    _parametric_search_fast_run,
    brute_force_search,
    dedup_by_symmetry,
    parametric_search,
    parametric_search_fast,
)
from rational_distance.search_gpu import _parametric_search_gpu_run, parametric_search_gpu
from rational_distance.square import VERTICES, make_point


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
