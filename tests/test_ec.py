"""Tests for elliptic-curve search and EC persistence."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.ec_analysis import build_analysis_report
from rational_distance.ec_db import ECSearchStore, connect_db
from rational_distance.search_ec import QuarticEC, ec_search, find_seeds_for_triple
from rational_distance.square import canonical_xy


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
