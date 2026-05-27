# wl069 — proof_status fast-core 两阶段模式

## 触发

`proof_status` 的 20k / 50k 目标暴露了两个工程瓶颈：

- 全量 pair 都走完整审计，会把大量时间花在主进程和单任务子进程之间传输结果。
- 全量 pair 都写 SQLite，会把已经由核心筛判死的 pair 也落成审计记录。

这轮目标不是改数学判定口径。目标是把“快速筛”和“完整审计”拆开：

1. 全量 pair 先跑只含低成本方法的核心筛。
2. 核心筛杀掉的 pair 只进入 summary，不写完整 DB 审计。
3. 核心筛没杀掉的 survivor 再走原来的完整 `proof_status` 流水线。

这条路服务大范围数据采样。它牺牲全量审计细节，换 wall time 和 SQLite 写入量。

## 新增模块

文件：`src/rational_distance/proof_status/fast_core.py`

新增数据结构：

```python
@dataclass(frozen=True)
class CoreChunkResult:
    checked: int
    no_solution: int
    survivors: tuple[tuple[int, int], ...]
```

核心函数：

- `evaluate_core_pair(A, B)`：对单个 pair 跑核心筛。
- `evaluate_core_chunk(pairs)`：对一个 chunk 跑核心筛并返回聚合结果。
- `merge_core_results(results)`：合并多个 chunk 结果。
- `iter_chunks(pairs, chunk_size)`：把 pair iterable 切成固定大小的 chunk。
- `run_fast_core(...)`：并行跑 chunk，最后合并成一份 `CoreChunkResult`。

当前核心筛顺序：

```text
safe_sieve
chain_closure_mod_sieve
factor_concordant
```

这三个方法都不调用 PARI。它们给出严格的 `no_solution` 判定。活下来的 pair 只表示“核心筛无法证明无解”，不表示存在解。

## CLI 新增参数

入口：`scripts/prove_no_solution.py`

新增：

```text
--fast-core
--fast-core-only
--pair-chunk-size N
--fast-summary-json PATH
--force
--moduli {minimal,balanced,standard,extended}
```

### `--fast-core`

启用两阶段模式：

1. 对全量 pair 跑核心筛。
2. 把核心筛结果写到 summary JSON。
3. 对 survivor 做完整 `proof_status` 审计并写 SQLite。

适合 10k / 20k 这种想保留疑难对审计信息的规模。

### `--fast-core-only`

只跑第一阶段：

1. 跑核心筛。
2. 写 summary JSON。
3. 直接退出。

这个参数必须和 `--fast-summary-json` 一起用。它不会进入 survivor 审计，不会跑 PARI，也不会给 survivor 写完整方法尝试表。

50k 以上默认建议先用这个参数拿 survivor 列表。

### `--fast-summary-json`

summary JSON 记录四类数据：

```json
{
  "checked": 10090806,
  "no_solution": 10089445,
  "survivor_count": 1361,
  "survivors": [[403, 9797], [23, 1573]]
}
```

这份文件是 fast-core 的主结果。`--fast-core-only` 模式下 DB 可能只有 schema，没有 pair 审计行；不要用 DB 行数推断核心筛覆盖量。

### `--force`

`--force` 现在会原地删除：

```text
DB
DB-wal
DB-shm
```

这样可以复用同一个 DB 路径，不需要每次生成一批临时库文件。

## 20k 实测记录

命令：

```bash
/usr/bin/time -p uv run python scripts/prove_no_solution.py \
  --db /tmp/proof_status_bench.db \
  --max-hyp 20000 \
  --workers 6 \
  --fast-core \
  --force \
  --fast-summary-json /tmp/proof_status_fast_20k_summary.json \
  --no-progress
```

fast-core 阶段写出的 summary：

```text
checked        10090806
no_solution    10089445
survivors          1361
```

解释：

- `checked` 是完整 pair 数。
- `no_solution` 是核心筛已经证明无解的 pair 数。
- `survivors` 是核心筛无法判死的疑难对。

这次 fast-core 阶段已经完成。后续 survivor 审计卡住的问题另见 wl070。

## 推荐命令

### 20k：保留 survivor 完整审计

```bash
PARI_MT_ENGINE=single /usr/bin/time -p uv run python scripts/prove_no_solution.py \
  --db /tmp/proof_status_20k.db \
  --max-hyp 20000 \
  --workers 6 \
  --fast-core \
  --force \
  --fast-summary-json /tmp/proof_status_fast_20k_summary.json \
  --no-progress
```

这会跑 PARI 审计 survivor。它比 full-audit 快很多，但后半段仍然受 PARI 的秩计算影响。

### 50k 以上：只拿核心筛结果

```bash
PARI_MT_ENGINE=single /usr/bin/time -p uv run python scripts/prove_no_solution.py \
  --db /tmp/proof_status_50k.db \
  --max-hyp 50000 \
  --workers 6 \
  --fast-core \
  --fast-core-only \
  --force \
  --fast-summary-json /tmp/proof_status_fast_50k_summary.json \
  --no-progress
```

这条命令不会跑 PARI。输出 JSON 是主要结果。

## 测试覆盖

新增 / 更新：

- `tests/test_proof_status_fast_core.py`
- `tests/test_prove_no_solution_fast_mode.py`
- `tests/test_prove_no_solution_reset_db.py`

覆盖点：

- chunk 级 fast-core 聚合。
- 并行 fast-core runner。
- CLI 只审计 survivor。
- `--fast-summary-json` 写出完整 summary。
- `--fast-core-only` 跳过 survivor 审计。
- `--force` 删除 DB / WAL / SHM。

验证命令：

```bash
uv run pytest \
  tests/test_proof_status_fast_core.py \
  tests/test_prove_no_solution_fast_mode.py \
  tests/test_prove_no_solution_reset_db.py \
  tests/test_proof_status_executor_prescan.py \
  tests/test_prove_no_solution_batches.py \
  tests/test_proof_status.py \
  -q
```

结果：

```text
48 passed
```

## 边界

fast-core 不保存每个被核心筛杀掉的 pair 的完整方法流水。它只保存总数和 survivor 列表。

如果你需要论文级审计材料，对 survivor 用普通 `--fast-core`。如果你只需要大范围估算和疑难对列表，用 `--fast-core-only`。
