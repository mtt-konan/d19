# proof_status 快速模式用法手册

这份文档只讲 `scripts/prove_no_solution.py` 的大范围跑法。背景记录见：

- [wl069 — proof_status fast-core 两阶段模式](./work-logs/069-proof-status-fast-core-mode.md)
- [wl070 — PARI 内部多线程导致 survivor 审计挂起](./work-logs/070-pari-mt-engine-and-survivor-audit-hang.md)

## 1. 先选运行模式

### 模式 A：完整审计

命令不带 `--fast-core`。

行为：

- 每个 pair 都走完整 `proof_status` pipeline。
- 每个 pair 都写 SQLite 审计。
- 会调用 PARI 的秩计算。

适用场景：小范围复核、需要每个 pair 的完整方法流水。

不适合 20k / 50k 大范围全量跑。

### 模式 B：fast-core + survivor 审计

命令带 `--fast-core`，不带 `--fast-core-only`。

行为：

- 全量 pair 先跑核心筛。
- 核心筛杀掉的 pair 只计入 summary JSON。
- survivor 再走完整 `proof_status` 审计。
- DB 只写 survivor。

适用场景：10k / 20k 这种想拿完整疑难对审计的规模。

### 模式 C：fast-core-only

命令同时带：

```text
--fast-core
--fast-core-only
--fast-summary-json PATH
```

行为：

- 全量 pair 只跑核心筛。
- 写 summary JSON。
- 不跑 survivor 审计。
- 不调用 PARI。
- DB 可能只有 schema，没有 pair 行。

适用场景：50k 以上大范围扫描，先拿 survivor 列表。

## 2. 20k 推荐命令

### 只拿核心筛结果

```bash
PARI_MT_ENGINE=single /usr/bin/time -p uv run python scripts/prove_no_solution.py \
  --db /tmp/proof_status_20k_core.db \
  --max-hyp 20000 \
  --workers 6 \
  --fast-core \
  --fast-core-only \
  --force \
  --fast-summary-json /tmp/proof_status_fast_20k_summary.json \
  --no-progress
```

看结果：

```bash
uv run python - <<'PY'
import json
from pathlib import Path
p = Path('/tmp/proof_status_fast_20k_summary.json')
d = json.loads(p.read_text())
print('checked       ', d['checked'])
print('no_solution   ', d['no_solution'])
print('survivor_count', d['survivor_count'])
print('first 10      ', d['survivors'][:10])
PY
```

### 核心筛后审计 survivor

```bash
PARI_MT_ENGINE=single /usr/bin/time -p uv run python scripts/prove_no_solution.py \
  --db /tmp/proof_status_20k_audit.db \
  --max-hyp 20000 \
  --workers 6 \
  --fast-core \
  --force \
  --fast-summary-json /tmp/proof_status_fast_20k_summary.json \
  --no-progress
```

看 DB：

```bash
sqlite3 /tmp/proof_status_20k_audit.db \
  "SELECT status, COUNT(*) FROM pair_proof_status GROUP BY status;"
```

注意：DB 行数只代表 survivor 审计数，不代表全量 checked 数。

## 3. 50k 以上推荐命令

先跑 fast-core-only：

```bash
PARI_MT_ENGINE=single /usr/bin/time -p uv run python scripts/prove_no_solution.py \
  --db /tmp/proof_status_50k_core.db \
  --max-hyp 50000 \
  --workers 6 \
  --fast-core \
  --fast-core-only \
  --force \
  --fast-summary-json /tmp/proof_status_fast_50k_summary.json \
  --no-progress
```

不要一开始就对 50k survivor 做完整审计。先看 `survivor_count`。如果 survivor 数量小，再单独设计审计任务。

## 4. 参数说明

### `--db PATH`

SQLite DB 路径。

在 fast-core-only 模式下，这个 DB 主要用于初始化 schema。主结果在 summary JSON。

### `--max-hyp N`

生成所有 reduced `(A,B)` pair，来源是勾股斜边不超过 `N` 的 pair 组合。

注意：并行路径现在仍会物化和排序 pair 列表。20k 约 1000 万 pair，生成阶段会先花一些时间和内存。

### `--workers N`

外层 Python 单任务子进程数。

建议：

- 笔记本先用 `6`。
- 如果系统开始换页或温度过高，降到 `4`。
- 不建议同时让 PARI 内部开多线程。

### `PARI_MT_ENGINE=single`

请求关闭 PARI 内部多线程。

注意：在当前 macOS + cypari2 + PARI 2.17.2 组合里，单独设置这个环境变量后，`default(nbthreads)` 仍可能是 `10`。所以代码现在还会在创建 `Pari()` 后显式执行：

```text
default(nbthreads,1)
```

即使代码已经默认设置，长跑命令也建议显式写上。这样命令记录里能看出运行意图。

### `--fast-core`

启用核心筛两阶段模式。

核心筛包含：

```text
safe_sieve
chain_closure_mod_sieve
factor_concordant
```

这三个方法不调用 PARI。

### `--fast-core-only`

只跑核心筛，不审计 survivor。

必须配合 `--fast-summary-json` 使用。

### `--fast-summary-json PATH`

写出 fast-core 主结果。

字段：

- `checked`：核心筛检查的 pair 总数。
- `no_solution`：核心筛证明无解的 pair 数。
- `survivor_count`：核心筛无法判死的 pair 数。
- `survivors`：survivor pair 列表。

### `--pair-chunk-size N`

每个并行任务包含多少 pair。

默认：

```text
50000
```

调参建议：

- 默认适合 20k / 50k。
- 如果主进程等待时间太长，可以降到 `20000`。
- 如果调度开销明显，可以升到 `100000`。

### `--force`

从头重跑，并删除旧 DB sidecar：

```text
DB
DB-wal
DB-shm
```

这个参数适合 benchmark。增量续跑不要用。

### `--moduli PRESET`

控制 `chain_closure_mod_sieve` 用哪些模数。

可选：

```text
minimal
balanced
standard
extended
```

默认 `standard`。fast-core benchmark 建议先用默认值，不要为了单步更快改成 `minimal`。`minimal` 会留下更多 survivor，后面可能更慢。

## 5. 常见误读

### DB 是空的，是不是没跑？

如果你用了 `--fast-core-only`，DB 空是正常现象。看 summary JSON。

### DB 只有几千行，是不是漏了 1000 万 pair？

没有漏。fast-core 只把 survivor 写 DB。核心筛杀掉的 pair 只进入 summary。

### CPU 不是 600%，是不是没吃满？

不一定。fast-core 目标是最短 wall time，不是让 CPU 曲线好看。

pair 生成、排序、主进程合并、最后几个 chunk 都可能让 CPU 利用率短时间下降。

### 卡在 PARI 怎么判断？

如果 DB 长时间不增长，CPU 接近 0，且 `sample` 里看到：

```text
ellrank
ell2selmer
mt_queue_reset
pthread_join
```

那就是 PARI 内部多线程等待。先确认命令里有没有 `PARI_MT_ENGINE=single`。

如果命令里已经有 `PARI_MT_ENGINE=single`，还要确认当前代码是否已经包含 `_ensure_pari()` 里的 `default(nbthreads,1)` 修复。只看环境变量不够，因为这台机器上环境变量没有自动把 `nbthreads` 改成 1。

## 6. 推荐工作流

### 大范围采样

1. 先跑 `--fast-core-only`。
2. 看 summary JSON。
3. 如果 survivor 数很小，再决定是否审计。

### 小范围出审计材料

1. 跑 `--fast-core`。
2. 保留 summary JSON。
3. 用 SQLite 查 survivor 的方法流水。

### 复查已有 DB

```bash
uv run python scripts/prove_no_solution.py \
  --db /tmp/proof_status_20k_audit.db \
  --report
```

## 7. 相关脚本

### `scripts/benchmark_ab_sieve_orders.py`

用途：比较 AB 核心筛的顺序。

默认口径已经收口为 3 层：

```text
safe_sieve
chain_closure_mod_sieve
factor_concordant
```

所以默认只比较 `3! = 6` 种顺序。

小样本调度检查：

```bash
uv run python scripts/benchmark_ab_sieve_orders.py \
  --max-hyp 10000 \
  --limit 200000 \
  --workers 6 \
  --batch-size 512 \
  --json-out /tmp/ab_sieve_orders_10k_limit.json
```

只看 `safe_sieve` 固定第一位后的候选：

```bash
uv run python scripts/benchmark_ab_sieve_orders.py \
  --max-hyp 20000 \
  --safe-first-only \
  --workers 6 \
  --batch-size 512 \
  --json-out /tmp/ab_sieve_safe_first_20k.json
```

参数说明：

- `--limit N`：只消费前 `N` 个 pair，调试时用。
- `--skip-extra`：只跑 core order，不跑 tail / baseline 对照。
- `--head-only` / `--safe-top2-only`：历史 split 诊断模式，默认结论不用它们。
- `--json-out PATH`：保存完整 benchmark summary。

读 JSON 时优先看：

- `pair_count`
- `core_order_count`
- `best_core_order`
- `core[].total_elapsed_s`

### `scripts/bench_mod_sieve.py`

用途：看 `chain_closure_mod_sieve` 每个模数的单步耗时和杀伤数。

运行：

```bash
uv run python scripts/bench_mod_sieve.py
```

当前脚本内置：

```python
MAX_HYP = 20000
```

输出列：

- `模数`：实际测试的 `p²`。
- `素数`：对应的 `p`。
- `耗时ms`：当前 survivor 集合上测试这个模数的耗时。
- `kills`：这个模数新杀掉的 pair 数。
- `μs/kill`：每杀一个 pair 的平均微秒成本。

这个脚本只做诊断，不写 DB。它适合回答：

- `minimal` / `balanced` / `standard` / `extended` 模数档位该怎么设。
- 后续模数是否已经性价比很低。
- 大样本 survivor 压力是否值得用更多模数提前削掉。

如果要改 `MAX_HYP`，直接改脚本里的常量。它目前是轻量诊断脚本，还没有 CLI 参数。

## 8. 当前已知边界

- fast-core-only 不提供每个被杀 pair 的方法流水。
- survivor 审计仍可能被单个 PARI 秩计算拖慢。
- 当前还没有 per-pair PARI timeout。
- 并行 `--max-hyp` 路径仍会物化 pair 列表，50k 以上要注意内存。

如果要做完全稳定的超大规模审计，需要把 PARI 审计拆成可设置超时的外部任务。
