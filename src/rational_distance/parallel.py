"""公共并行工具模块。

提供统一的多进程并行接口，让项目中所有脚本都能轻松使用多核加速。

核心设计
========

1. **默认并行**：`default_workers()` 返回 CPU 核数，脚本默认就是多核
2. **统一接口**：`parallel_map(fn, items, ...)` 封装 `multiprocessing.Pool`
3. **spawn 上下文**：macOS/Linux 安全，避免 fork + PARI 库冲突
4. **进度回调**：可选 `on_result` 回调，兼容 tqdm 进度条
5. **优雅降级**：`workers=1` 时直接串行，无 Pool 开销

用法示例
========

    from rational_distance.parallel import parallel_map, default_workers

    def process_item(x):
        return x * x

    results = parallel_map(process_item, range(1000))

    # 或带进度回调
    from tqdm import tqdm
    pbar = tqdm(total=1000)
    results = parallel_map(
        process_item,
        range(1000),
        on_result=lambda r: pbar.update(1),
    )

    # 显式串行（调试用）
    results = parallel_map(process_item, range(1000), workers=1)
"""

from __future__ import annotations

import argparse
import itertools
import multiprocessing as mp
import os
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from types import TracebackType
from typing import Protocol, TypeVar, cast

T = TypeVar("T")
R = TypeVar("R")


class _PoolProtocol(Protocol):
    def imap(
        self,
        func: Callable[[object], object],
        iterable: Iterable[object],
        chunksize: int = 1,
    ) -> Iterator[object]: ...

    def imap_unordered(
        self,
        func: Callable[[object], object],
        iterable: Iterable[object],
        chunksize: int = 1,
    ) -> Iterator[object]: ...

    def close(self) -> None: ...

    def join(self) -> None: ...


class _ContextProtocol(Protocol):
    def Pool(self, processes: int) -> _PoolProtocol: ...


class _ParallelArgsProtocol(Protocol):
    workers: int
    chunksize: int
    serial: bool


def default_workers() -> int:
    """返回默认 worker 数：CPU 核数，至少 1。

    可通过环境变量 RD_WORKERS 覆盖：
      - RD_WORKERS=4  → 固定 4 核
      - RD_WORKERS=1  → 串行
      - RD_WORKERS=0  → 使用 CPU 核数（默认）
    """
    env_val = os.environ.get("RD_WORKERS", "").strip()
    if env_val:
        try:
            n = int(env_val)
            if n > 0:
                return n
            # n <= 0 表示使用默认
        except ValueError:
            pass
    return os.cpu_count() or 1


def parallel_map(
    fn: Callable[[T], R],
    items: Iterable[T],
    *,
    workers: int | None = None,
    chunksize: int = 50,
    on_result: Callable[[R], None] | None = None,
    ordered: bool = False,
    collect_results: bool = True,
) -> list[R]:
    """并行 map：对 items 中每个元素应用 fn，返回结果列表。

    参数
    ----
    fn : Callable[[T], R]
        处理函数，必须是 top-level 可 pickle 的函数
    items : Iterable[T]
        输入数据
    workers : int | None
        worker 数，None 表示使用 default_workers()
    chunksize : int
        Pool.imap 的 chunksize，影响调度粒度
    on_result : Callable[[R], None] | None
        每个结果返回时的回调（用于进度条）
    ordered : bool
        True 保持顺序（imap），False 不保证顺序但更快（imap_unordered）

    返回
    ----
    list[R]
        结果列表（ordered=True 时与输入顺序一致）

    注意
    ----
    - workers=1 时直接串行，无 Pool 开销
    - 使用 spawn 上下文，避免 fork 问题
    """
    if workers is None:
        workers = default_workers()

    iterator = iter(items)
    try:
        first_item = next(iterator)
    except StopIteration:
        return []
    items_iter = itertools.chain((first_item,), iterator)

    results: list[R] = []

    if workers <= 1:
        # 串行路径：无 Pool 开销
        for item in items_iter:
            r = fn(item)
            if collect_results:
                results.append(r)
            if on_result is not None:
                on_result(r)
        return results

    # 并行路径
    ctx = mp.get_context("spawn")
    with ctx.Pool(processes=workers) as pool:
        mapper = pool.imap if ordered else pool.imap_unordered
        for r in mapper(fn, items_iter, chunksize=chunksize):
            if collect_results:
                results.append(r)
            if on_result is not None:
                on_result(r)

    return results


class ParallelExecutor:
    def __init__(
        self,
        *,
        workers: int | None = None,
        chunksize: int = 50,
        ordered: bool = False,
    ) -> None:
        self.workers: int = default_workers() if workers is None else workers
        self.chunksize: int = chunksize
        self.ordered: bool = ordered
        self._ctx: _ContextProtocol | None = None
        self._pool: _PoolProtocol | None = None

    def _ensure_pool(self) -> _PoolProtocol | None:
        if self.workers <= 1:
            return None
        if self._pool is None:
            self._ctx = mp.get_context("spawn")
            self._pool = self._ctx.Pool(processes=self.workers)
        return self._pool

    def map(
        self,
        fn: Callable[[T], R],
        items: Iterable[T],
        on_result: Callable[[R], None] | None = None,
        *,
        collect_results: bool = True,
    ) -> list[R]:
        iterator = iter(items)
        try:
            first_item = next(iterator)
        except StopIteration:
            return []
        items_iter = itertools.chain((first_item,), iterator)

        results: list[R] = []
        pool = self._ensure_pool()
        if pool is None:
            for item in items_iter:
                result = fn(item)
                if collect_results:
                    results.append(result)
                if on_result is not None:
                    on_result(result)
            return results

        mapper = pool.imap if self.ordered else pool.imap_unordered
        worker_fn = cast(Callable[[object], object], fn)
        worker_items = cast(Iterable[object], items_iter)
        for raw_result in mapper(worker_fn, worker_items, chunksize=self.chunksize):
            result = cast(R, raw_result)
            if collect_results:
                results.append(result)
            if on_result is not None:
                on_result(result)
        return results

    def close(self) -> None:
        if self._pool is not None:
            self._pool.close()
            self._pool.join()
            self._pool = None
            self._ctx = None

    def __enter__(self) -> "ParallelExecutor":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()


@dataclass(frozen=True)
class ParallelConfig:
    """并行配置，可在脚本间共享。"""

    workers: int
    chunksize: int = 50
    ordered: bool = False

    @classmethod
    def default(cls, chunksize: int = 50, ordered: bool = False) -> "ParallelConfig":
        """使用默认 worker 数创建配置。"""
        return cls(workers=default_workers(), chunksize=chunksize, ordered=ordered)

    def map(
        self,
        fn: Callable[[T], R],
        items: Iterable[T],
        on_result: Callable[[R], None] | None = None,
        *,
        collect_results: bool = True,
    ) -> list[R]:
        """使用此配置执行 parallel_map。"""
        return parallel_map(
            fn,
            items,
            workers=self.workers,
            chunksize=self.chunksize,
            on_result=on_result,
            ordered=self.ordered,
            collect_results=collect_results,
        )

    def executor(self) -> ParallelExecutor:
        return ParallelExecutor(
            workers=self.workers,
            chunksize=self.chunksize,
            ordered=self.ordered,
        )


def add_parallel_args(
    parser: argparse.ArgumentParser,
    default_workers_value: int | None = None,
) -> None:
    """为 argparse.ArgumentParser 添加标准并行参数。

    添加的参数：
      --workers N    : worker 数（默认 CPU 核数）
      --chunksize N  : Pool chunksize（默认 50）
      --serial       : 等价于 --workers 1

    用法
    ----
        parser = argparse.ArgumentParser()
        add_parallel_args(parser)
        args = parser.parse_args()
        cfg = ParallelConfig(
            workers=1 if args.serial else args.workers,
            chunksize=args.chunksize,
        )
    """
    if default_workers_value is None:
        default_workers_value = default_workers()

    _ = parser.add_argument(
        "--workers",
        type=int,
        default=default_workers_value,
        help=f"Number of parallel workers (default: {default_workers_value}, i.e. CPU count)",
    )
    _ = parser.add_argument(
        "--chunksize",
        type=int,
        default=50,
        help="Pool imap chunksize (default: 50)",
    )
    _ = parser.add_argument(
        "--serial",
        action="store_true",
        help="Run in serial mode (equivalent to --workers 1)",
    )


def get_parallel_config_from_args(args: _ParallelArgsProtocol) -> ParallelConfig:
    """从 argparse 结果创建 ParallelConfig。

    配合 add_parallel_args 使用。
    """
    workers = 1 if args.serial else args.workers
    chunksize = args.chunksize
    return ParallelConfig(workers=workers, chunksize=chunksize)


__all__ = [
    "ParallelConfig",
    "ParallelExecutor",
    "add_parallel_args",
    "default_workers",
    "get_parallel_config_from_args",
    "parallel_map",
]
