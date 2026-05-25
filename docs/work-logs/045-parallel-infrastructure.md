# Worklog 045: 公共并行基础设施

**日期**: 2026-05-25
**状态**: 完成

## 背景

用户反馈 `prove_no_solution.py` 脚本默认是串行执行（`--workers=1`），需要显式传参才能使用多核。项目中有多个脚本各自实现 `multiprocessing`，逻辑零散重复。

## 目标

1. 创建公共并行工具模块，统一多进程接口
2. 让脚本默认使用多核（CPU 核数）
3. 提供 `--serial` 选项方便显式串行（调试用）
4. 减少重复代码，提升可维护性

## 实现

### 1. 新增 `src/rational_distance/parallel.py`

公共并行工具模块，提供：

- `default_workers()`: 返回默认 worker 数（CPU 核数），支持 `RD_WORKERS` 环境变量覆盖
- `parallel_map(fn, items, ...)`: 统一的并行 map 接口，封装 `multiprocessing.Pool`
- `ParallelConfig`: 并行配置 dataclass，可在脚本间共享
- `add_parallel_args(parser)`: 为 argparse 添加标准并行参数（`--workers`, `--chunksize`, `--serial`）
- `get_parallel_config_from_args(args)`: 从 argparse 结果创建 ParallelConfig

关键设计：
- **默认并行**: `default_workers()` 返回 CPU 核数
- **spawn 上下文**: 避免 fork + PARI 库冲突（macOS/Linux 安全）
- **优雅降级**: `workers=1` 时直接串行，无 Pool 开销
- **进度回调**: `on_result` 参数兼容 tqdm 进度条

### 2. 重构 `workflow.process_pairs_parallel`

- 使用 `parallel_map` 替代手动 Pool 管理
- `workers` 参数默认值改为 `None`（自动 CPU 核数）
- 保持 batched commit 逻辑（workflow 特有需求）

### 3. 重构 `scripts/prove_no_solution.py`

- `--workers` 默认值从 1 改为 CPU 核数（本机 10）
- 新增 `--serial` 选项（等价于 `--workers 1`）
- 帮助信息更新，说明默认行为

### 4. 重构 `scripts/multi_concordant_n_scan.py`

- 使用 `add_parallel_args` 和 `get_parallel_config_from_args`
- 使用 `parallel_map` 替代手动 Pool 管理
- 代码更简洁，与其他脚本风格一致

### 5. 新增 `tests/test_parallel.py`

14 个单元测试覆盖：
- `default_workers()` 基本行为和环境变量
- `parallel_map()` 串行/并行执行、回调、顺序保持
- `ParallelConfig` 配置和 map 方法

## 验证

```bash
# 测试全部通过
uv run pytest tests/test_parallel.py -v
# 14 passed

# proof_status 测试全部通过
uv run pytest tests/test_proof_status.py -v
# 25 passed

# 实际运行验证
uv run python scripts/prove_no_solution.py --db /tmp/test.db --max-hyp 100 --no-progress
# workers: 10 (自动检测 CPU 核数)
# 254 pairs 全部 no_solution
```

## 用法示例

```python
# 简单用法
from rational_distance.parallel import parallel_map, default_workers

results = parallel_map(process_item, items)  # 默认多核

# 带进度条
from tqdm import tqdm
pbar = tqdm(total=len(items))
results = parallel_map(process_item, items, on_result=lambda r: pbar.update(1))

# 显式串行（调试）
results = parallel_map(process_item, items, workers=1)

# 脚本标准参数
import argparse
from rational_distance.parallel import add_parallel_args, get_parallel_config_from_args

parser = argparse.ArgumentParser()
add_parallel_args(parser)
args = parser.parse_args()
cfg = get_parallel_config_from_args(args)
results = cfg.map(process_item, items)
```

## 文件变更

| 文件 | 变更 |
|------|------|
| `src/rational_distance/parallel.py` | 新增 |
| `src/rational_distance/proof_status/workflow.py` | 重构使用公共工具 |
| `scripts/prove_no_solution.py` | 默认多核 + --serial |
| `scripts/multi_concordant_n_scan.py` | 重构使用公共工具 |
| `tests/test_parallel.py` | 新增 |

## 后续

其他脚本（如 `generator_lattice_search.py`, `probe_chain_closure_mod_sieve.py`）可按需迁移到公共并行工具。
