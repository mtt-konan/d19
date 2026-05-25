"""Tests for CLI argument parsing and CLI smoke scripts."""

from __future__ import annotations

import subprocess
import sys
from importlib import import_module
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

cli_search = import_module("scripts.search")
compare_cli = import_module("scripts.archive.compare_parametric")

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
                str(ROOT / "scripts" / "archive" / "compare_parametric.py"),
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
