# wl070 — PARI 内部多线程导致 survivor 审计挂起

## 现场

在 wl069 的 fast-core 20k 运行中，第一阶段已经完成：

```text
checked        10090806
no_solution    10089445
survivors          1361
```

随后脚本进入 survivor 审计阶段。DB 卡在：

```text
pair_proof_status rows = 1000
status histogram: hard_case = 1000
```

进程没有退出。CPU 接近 0%。DB 不再增长。

## 先排除的假设

### 不是 pair 生成

早先有一次手动中断发生在：

```text
generate_ab_pairs(args.max_hyp)
return sorted(iter_ab_pairs(max_hyp))
g = gcd(A, B)
KeyboardInterrupt
```

那次还没有进入 fast-core。它说明 20k 会在生成和排序 1000 万级 pair 时花几秒，但这不是后面 survivor 审计挂起的原因。

### 不是 SQLite commit 卡住

DB 正好停在 1000 行，而默认 `commit_every=1000`，这个现象很显眼。

检查后得到：

```text
PRAGMA wal_checkpoint(PASSIVE) -> 0|732|732
pair_proof_status count        -> 1000
```

SQLite 没有处在写锁等待。主进程也没有卡在 commit。

### 不是 multiprocessing pool 自己空转

主进程采样显示它在等结果：

```text
_queue_SimpleQueue_get
poll
read
__psynch_cvwait
```

这说明主进程在等单任务子进程返回。问题需要继续看子进程。

## 关键证据

对 survivor 审计的单任务子进程做 `sample` 后，栈里出现：

```text
cypari2 Pari_auto ellrank
ellrank_flag
ell2selmer
QXQ_norm
ZX_resultant_all
gen_inccrt_i
mt_queue_reset
pthread_join
__ulock_wait
```

同一进程中的 PARI 内部线程在：

```text
mt_queue_run
pthread_cond_wait
__psynch_cvwait
```

中文解释：

- `ellrank` 是 PARI 的椭圆曲线秩计算入口。
- `ell2selmer` 是两降法里和塞尔默群（Selmer group）相关的步骤。
- `mt_queue_*` 是 PARI 内部多线程调度队列。
- worker 在等 PARI 内部线程结束，PARI 内部线程又在条件变量上睡眠。

所以根因不是 Python 的 pool 自己坏了，而是：

```text
多个 Python 单任务子进程同时调用 PARI，PARI 又在每个进程里启用内部多线程，最终卡在 PARI mt_queue。
```

## 当时环境

检查运行中主进程环境：

```bash
ps eww -p 78033 | tr ' ' '\n' | grep '^PARI_MT_ENGINE=' || true
```

输出为空。

这说明当前 run 没有设置：

```text
PARI_MT_ENGINE=single
```

实际组合变成：

```text
6 个 Python 单任务子进程 × PARI 内部多线程
```

macOS + cypari2 + PARI 在这个组合下触发了 `mt_queue` 等待。

## 修复

`scripts/prove_no_solution.py` 现在在解析参数后、导入会初始化 PARI 的模块前调用：

```python
def _configure_pari_runtime() -> None:
    os.environ.setdefault("PARI_MT_ENGINE", "single")
```

效果：

- 用户没有显式设置时，脚本默认把 PARI 内部多线程关掉。
- 如果用户提前设置了 `PARI_MT_ENGINE`，脚本尊重外部值。
- worker 用 `spawn` 启动，会继承主进程环境变量。

这不是数学变化。它只改变 PARI 的内部调度方式。

## 为什么还建议命令行显式写一次

代码已经默认设置。但长跑命令建议保留：

```bash
PARI_MT_ENGINE=single uv run python scripts/prove_no_solution.py ...
```

原因很简单：

- 你一眼能看出这次 run 关了 PARI 内部多线程。
- shell history 里会留下完整环境。
- 如果以后换入口脚本，这个环境变量仍然生效。

## 对性能的影响

`PARI_MT_ENGINE=single` 不一定让单个 `ellrank` 更快。它解决的是稳定性和进程组合问题。

当前 `proof_status` 并行模型已经有 Python 单任务子进程。让 PARI 在每个子进程里再开线程，会制造过度并行和内部锁等待。更安全的组合是：

```text
外层 Python 多进程并行
内层 PARI 单线程
```

如果要继续调 survivor 审计性能，优先调外层 `--workers`，不要让 PARI 自己开多线程。

## 对当前旧进程的判断

旧进程已经进入 PARI 内部等待。修改代码不会影响已经运行的进程。

旧进程停在：

```text
DB rows = 1000 / 1361 survivors
CPU     = 0%
```

建议停掉旧进程后重跑。旧 summary JSON 已经保存了 fast-core 结果，所以不会丢核心筛统计。

## 后续命令

### 重跑 20k 且保留 survivor 审计

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

### 50k 以上先不要跑 survivor 审计

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

## 还没有解决的事

这轮没有给单个 PARI `ellrank` 加 timeout。Python 无法安全中断已经卡进 C / PARI 内部的调用。

如果以后要做“完整审计必须长跑稳定”，更稳的架构是把 PARI 审计改成外部子命令级别的任务池：

- 每个 pair 或小 batch 由独立进程跑。
- 主进程给每个任务设置 wall-time timeout。
- 超时任务标成 `unknown` 或 `pari_timeout`，不中断整个批次。

这属于下一轮架构改造，不混进本轮 fast-core。
