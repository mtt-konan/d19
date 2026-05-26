"""Tests for the parallel utility module."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest import mock

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from rational_distance.parallel import (
    ParallelConfig,
    ParallelExecutor,
    default_workers,
    parallel_map,
)


def _square(x: int) -> int:
    """Simple test function."""
    return x * x


class TestDefaultWorkers:
    """Tests for default_workers()."""

    def test_returns_positive_int(self) -> None:
        """default_workers() should return a positive integer."""
        result = default_workers()
        assert isinstance(result, int)
        assert result >= 1

    def test_respects_env_variable(self) -> None:
        """RD_WORKERS env var should override the default."""
        with mock.patch.dict(os.environ, {"RD_WORKERS": "4"}):
            assert default_workers() == 4

    def test_env_zero_uses_cpu_count(self) -> None:
        """RD_WORKERS=0 should fall back to CPU count."""
        with mock.patch.dict(os.environ, {"RD_WORKERS": "0"}):
            result = default_workers()
            assert result == (os.cpu_count() or 1)

    def test_env_invalid_uses_cpu_count(self) -> None:
        """Invalid RD_WORKERS should fall back to CPU count."""
        with mock.patch.dict(os.environ, {"RD_WORKERS": "invalid"}):
            result = default_workers()
            assert result == (os.cpu_count() or 1)


class TestParallelMap:
    """Tests for parallel_map()."""

    def test_empty_input(self) -> None:
        """Empty input should return empty list."""
        result = parallel_map(_square, [])
        assert result == []

    def test_serial_execution(self) -> None:
        """workers=1 should execute serially."""
        result = parallel_map(_square, [1, 2, 3, 4, 5], workers=1)
        assert sorted(result) == [1, 4, 9, 16, 25]

    def test_parallel_execution(self) -> None:
        """workers>1 should execute in parallel."""
        result = parallel_map(_square, range(10), workers=2)
        assert sorted(result) == [i * i for i in range(10)]

    def test_on_result_callback(self) -> None:
        """on_result callback should be called for each result."""
        results_seen: list[int] = []
        parallel_map(_square, [1, 2, 3], workers=1, on_result=results_seen.append)
        assert sorted(results_seen) == [1, 4, 9]

    def test_collect_results_false_returns_empty_list(self) -> None:
        """collect_results=False should stream to callback without storing results."""
        results_seen: list[int] = []
        result = parallel_map(
            _square,
            [1, 2, 3],
            workers=1,
            on_result=results_seen.append,
            collect_results=False,
        )
        assert result == []
        assert sorted(results_seen) == [1, 4, 9]

    def test_ordered_preserves_order(self) -> None:
        """ordered=True should preserve input order."""
        result = parallel_map(_square, [5, 3, 1, 4, 2], workers=1, ordered=True)
        assert result == [25, 9, 1, 16, 4]


class TestParallelConfig:
    """Tests for ParallelConfig."""

    def test_default_config(self) -> None:
        """default() should use CPU count."""
        cfg = ParallelConfig.default()
        assert cfg.workers >= 1
        assert cfg.chunksize == 50
        assert cfg.ordered is False

    def test_map_method(self) -> None:
        """map() should work like parallel_map."""
        cfg = ParallelConfig(workers=1, chunksize=10)
        result = cfg.map(_square, [1, 2, 3])
        assert sorted(result) == [1, 4, 9]

    def test_custom_chunksize(self) -> None:
        """Custom chunksize should be respected."""
        cfg = ParallelConfig.default(chunksize=100)
        assert cfg.chunksize == 100


class TestParallelExecutor:
    """Tests for reusable ParallelExecutor."""

    def test_reuses_pool_across_multiple_maps(self) -> None:
        """Executor should create one pool and reuse it across map calls."""
        mock_ctx = mock.Mock()
        mock_pool = mock.Mock()

        def _imap_unordered(fn, items, chunksize=1):
            return map(fn, items)

        mock_pool.imap_unordered.side_effect = _imap_unordered
        mock_ctx.Pool.return_value = mock_pool

        with mock.patch("rational_distance.parallel.mp.get_context", return_value=mock_ctx):
            executor = ParallelExecutor(workers=2, chunksize=10)
            first = executor.map(_square, [1, 2, 3])
            second = executor.map(_square, [4, 5])
            executor.close()

        assert first == [1, 4, 9]
        assert second == [16, 25]
        mock_ctx.Pool.assert_called_once_with(processes=2)
        mock_pool.close.assert_called_once()
        mock_pool.join.assert_called_once()


class TestParallelMapWithMultiprocessing:
    """Tests that actually use multiprocessing (slower)."""

    @pytest.mark.slow
    def test_large_parallel_execution(self) -> None:
        """Test parallel execution with larger dataset."""
        n = 1000
        result = parallel_map(_square, range(n), workers=2, chunksize=50)
        assert sorted(result) == [i * i for i in range(n)]

    @pytest.mark.slow
    def test_parallel_with_callback(self) -> None:
        """Test parallel execution with callback."""
        count = 0

        def counter(_: int) -> None:
            nonlocal count
            count += 1

        parallel_map(_square, range(100), workers=2, on_result=counter)
        assert count == 100
