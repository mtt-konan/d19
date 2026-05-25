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

import multiprocessing as mp
import os
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


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

    items_list = list(items)
    if not items_list:
        return []

    results: list[R] = []

    if workers <= 1:
        # 串行路径：无 Pool 开销
        for item in items_list:
            r = fn(item)
            results.append(r)
            if on_result is not None:
                on_result(r)
        return results

    # 并行路径
    ctx = mp.get_context("spawn")
    with ctx.Pool(processes=workers) as pool:
        mapper = pool.imap if ordered else pool.imap_unordered
        for r in mapper(fn, items_list, chunksize=chunksize):
            results.append(r)
            if on_result is not None:
                on_result(r)

    return results


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
    ) -> list[R]:
        """使用此配置执行 parallel_map。"""
        return parallel_map(
            fn,
            items,
            workers=self.workers,
            chunksize=self.chunksize,
            on_result=on_result,
            ordered=self.ordered,
        )


def add_parallel_args(parser, default_workers_value: int | None = None) -> None:
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

    parser.add_argument(
        "--workers",
        type=int,
        default=default_workers_value,
        help=f"Number of parallel workers (default: {default_workers_value}, i.e. CPU count)",
    )
    parser.add_argument(
        "--chunksize",
        type=int,
        default=50,
        help="Pool imap chunksize (default: 50)",
    )
    parser.add_argument(
        "--serial",
        action="store_true",
        help="Run in serial mode (equivalent to --workers 1)",
    )


def get_parallel_config_from_args(args) -> ParallelConfig:
    """从 argparse 结果创建 ParallelConfig。

    配合 add_parallel_args 使用。
    """
    workers = 1 if getattr(args, "serial", False) else getattr(args, "workers", default_workers())
    chunksize = getattr(args, "chunksize", 50)
    return ParallelConfig(workers=workers, chunksize=chunksize)


__all__ = [
    "ParallelConfig",
    "add_parallel_args",
    "default_workers",
    "get_parallel_config_from_args",
    "parallel_map",
]
