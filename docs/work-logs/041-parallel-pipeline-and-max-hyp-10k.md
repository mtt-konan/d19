# 041 — Parallel pipeline + max_hyp=10000 scaling + hard_case 分布

**日期**: 2026-05-25（紧接 wl040）
**触发原因**: wl040 把 hard_case 砍到 0.01%，但跑 max_hyp ≥ 5000 时单线程
pipeline 因 commit 风暴慢得难以使用。本 worklog 加并行支持，把 max_hyp
推到 10000，看 hard_case 数量趋势 + 拿 326 个 survivor 的 rank/sha2 数据。
**输出**: 1 个新 workflow.process_pairs_parallel + CLI `--workers` +
max_hyp=5000/10000 实证数据 + 326 hard_case 的 rank/sha2 分布 + 与 wl036/038
的对比。

---

## 一、为什么单线程 pipeline 在 max_hyp=5000 上不行

profiling 之前 `prove_no_solution.py --max-hyp 5000`（用户取消）发现：

- 总 pair 估计 ~620k
- safe_sieve 砍 91% = ~565k pair
- 每个 pair 至少 2 次 SQLite commit (record_method_attempt + upsert_pair_status)
- → ~1.13M commit
- WAL mode 单线程 commit ~1000/s → **理论 ~19 分钟纯 IO**

CPU 已经被 commit IO bound 死。需要两件事：
- **batched commit**（commit 10x 减少 → IO 减 99%）
- **并行 worker**（进一步 ~6-8x speedup）

---

## 二、设计：纯函数 + 主进程 batch 写

把 `process_pair`（混合了计算和 db 写）拆成：

1. **`compute_pair_status(A, B, methods)`**: 纯函数，跑完整 method pipeline，
   返回 `PairComputeResult` dataclass（final_status + method_results +
   aggregate columns）。**不碰 db。**

2. **`_persist_compute_result(conn, result)`**: 把 PairComputeResult 写进
   db，但 `commit=False`。

3. **`process_pairs_parallel(conn, pairs, *, workers, commit_every)`**: 
   - 用 `multiprocessing.Pool(spawn)` 把 pair 分给 worker
   - 主进程串行收 worker 的 PairComputeResult，调用 `_persist_compute_result`
   - 每 `commit_every` 个 pair `conn.commit()` 一次

为什么 `spawn`：fork 在 macOS 上跟 PARI 库的 C 状态有兼容问题；spawn 让
每个 worker 自己 import + 自己起 PARI cache，干净。

为什么 `commit=False` keyword（`schema.upsert_pair_status` 和
`record_method_attempt`）：保持向后兼容。默认行为不变，老代码不受影响；
新批量代码显式传 `commit=False`。

---

## 三、实证：max_hyp=500 → 10000 的耗时与 hard_case

8 workers，spawn context，commit_every=1000：

| max_hyp | pair 总数 | hard_case | wall time | CPU% |
|---:|---:|---:|---:|---:|
| 500   | 6,172     | **2**   | 0.4s   | 337% |
| 2,000 | 99,311    | **18**  | ~3s    | ~600% |
| 5,000 | 617,432   | **77**  | 19s    | 599% |
| **10,000** | **2,513,057** | **326** | **1m25s** | **594%** |

每多 1 个数量级 max_hyp，时间约 ×4–5。完全可以预算。

跟单线程相比（旧路径，commit 风暴）：
- max_hyp=5000: 估计 5–10 分钟 → 19s ≈ **20× 加速**
- max_hyp=10000: 估计 30–60 分钟 → 1m25s ≈ **25× 加速**

---

## 四、326 个 max_hyp=10000 hard_case 的 rank / sha2 分布

跑 `batch_ell2cover_hard_cases.py` (复用 wl036 的脚本，6.6 秒)：

### Rank 分布（lower == upper for all 326）

| rank | 数量 | 占比 |
|---:|---:|---:|
| 1 | 88  | 27.0% |
| 2 | 146 | 44.8% |
| 3 | 72  | 22.1% |
| 4 | 18  | 5.5% |
| 5 | 2   | 0.6% |
| 0 | **0** | — |

PARI `ellrank(E, 1)` 给 326/326 精确 rank，**0 imprecise**。这跟 wl030 在
max_hyp=500 上的 320 case 一致。Direction 6 (L-function) 仍然冗余。

### Sha[2] 分布（PARI ellrank effort=1）

| sha2_lower | 数量 |
|---:|---:|
| 0 | 313 |
| **2** | **13** |
| ≥4 | 0 |

### Selmer 维度公式仍然 100% 成立

wl036/039 的公式 `n_quartic_covers = rank_lower + 2 + sha2_lower` 在 326
case 上完全验证：

| rank, sha2 | 期望 n_covers | 实测 |
|---|---|---|
| (1, 0) | 3 | 79 |
| (1, 2) | 5 | 9 |
| (2, 0) | 4 | 143 |
| (2, 2) | 6 | 3 |
| (3, 0) | 5 | 71 |
| (3, 2) | 7 | 1 |
| (4, 0) | 6 | 18 |
| (5, 0) | 7 | 2 |

校验 sha2=2 子集合计 9+3+1 = 13 ✓

---

## 五、关键发现：chain_closure_sieve 改变了 hard_case 的"质量"

跟之前 worklog 的对比：

| 阶段 | max_hyp | hard_case | sha2≥2 数 | sha2≥2 占比 |
|---|---|---|---|---|
| wl036 (no chain_closure) | 500   | 320  | 2   | 0.6% |
| wl038 (no chain_closure) | 2000  | 4653 | 156 | 3.4% |
| **wl041 (with chain_closure)** | **10000** | **326** | **13** | **4.0%** |

观察：

1. **chain_closure_sieve 砍掉的主要是 sha2=0 的"简单 local 障碍" case**。
   留下来的 hard_case 中 sha2≥2 比例显著更高 (4%)。
2. 直觉解释：chain_closure_sieve 的 obstruction 是 mod p² 上的简单同余
   矛盾，它正好覆盖了"low Selmer arithmetic complexity"的 case。
   留下的 326 个 case 是 mod p² 上无简单矛盾、但 global 解仍不存在——
   正是 deep arithmetic（Sha / Brauer-Manin / Heegner）的范畴。

意义：之前每次 scale up（max_hyp 500 → 2000）都让 sha2≥2 case 增加几百倍。
现在加了 chain_closure_sieve 后 hard_case 数量不再爆炸增长，但 sha2≥2 比例
反而更高，**这是 priority queue 缩小且更聚焦的标志**。

---

## 六、Direction 5/7/8 reach 重新估算

| direction | 适用范围 | max_hyp=10000 上的目标数 |
|---|---|---|
| 5 (Heegner + canonical height) | rank=1 | **88** |
| 7 (Chabauty / QC) | rank=2 | 146 |
| 7/8 (high rank deep theory) | rank≥3 | 92 |
| 8 (Brauer-Manin) | sha2≥2 子集 | **13** |

之前 wl030 估计 direction 5 能升级 ~37% hard_case (118/320 at max_hyp=500)。
现在 max_hyp=10000 上 rank=1 子集是 88——绝对数量基本不变，**但目标质量
更高**：每个都是 chain_closure-resistant + concordant N exists + chain
closure fails，纯纯 deep theory 目标。

13 个 sha2≥2 case 是 Brauer-Manin / Cassels-Tate 的最佳 priority queue。

---

## 七、Pipeline 现状

```
1. safe_sieve              ~91% kill (mod 4 必要条件)
2. chain_closure_mod_sieve ~99.6% kill on safe_sieve survivors (wl040)
3. factor_concordant       少量 kill + chain refutation 检查
4. rank_zero               PARI ellrank
5. heegner                 (rank=1 only) inconclusive，未升级 no_solution
6. chabauty/brauer_manin   stub
```

每个 pair 在 max_hyp=10000 上平均经历前 3 个 method 就被砍掉，只有 326
个进 method 4-6。

---

## 八、326 hard_case 上 chain refutation 检查：0 反例

复用 factor_concordant 的因子分解枚举（穷举所有 concordant N），对每个
concordant N 检查 chain closure：

```
hard_case count: 326
#concordant N distribution: [(1, 325), (2, 1)]
Failure modes among all (concordant N, survivor) pairs:
  b <= 0 (degenerate)          : 59
  b > 0 but b²+A²/b²+B² not sq : 268
  chain REFUTATIONS            : 0
```

跟 max_hyp=2000 的 18 个 survivor 比：
- 18 全部正好 1 个 concordant N
- max_hyp=10000: 325 个有 1 个，**1 个有 2 个**——出现了新的（轻微）多重
  concordant 模式

degenerate vs non-degenerate failure 比例：
- max_hyp=2000:  6/18  ≈ 33% degenerate, 67% closure fail
- max_hyp=10000: 59/326 ≈ 18% degenerate, 82% closure fail

→ 大的 (A, B) 让 N < A+B 的可行区间相对更宽，degenerate 比例下降，"真实
chain closure 失败"主导。这正是 deep arithmetic 应该攻的目标。

**Harborth 在 max_hyp ≤ 10000 范围（2.5M reduced pair）继续成立。**

---

## 九、输出物

### 修改

- `src/rational_distance/proof_status/schema.py`
  - `upsert_pair_status` / `record_method_attempt` 加 `commit=True` 默认参数
- `src/rational_distance/proof_status/workflow.py`
  - 新增 `PairComputeResult` dataclass
  - 新增 `compute_pair_status(A, B, methods)` 纯函数
  - 新增 `process_pairs_parallel(conn, pairs, *, workers, commit_every, ...)`
- `scripts/prove_no_solution.py`
  - 新增 `--workers N` / `--commit-every N` 参数
  - main 函数路径分叉：workers > 1 走 parallel，否则走原 sequential

198/198 测试通过，零回归。

### 数据

- `/tmp/proofs_parallel_5k.sqlite3`   — max_hyp=5000 (77 hard_case)
- `/tmp/proofs_parallel_10k.sqlite3`  — max_hyp=10000 (326 hard_case)
- `/tmp/ell2cover_10k.jsonl`          — 326 case × ellrank+ell2cover 数据

### 复现命令

```bash
# 跑 max_hyp=10000 完整 pipeline (8 workers, ~1m25s)
uv run python scripts/prove_no_solution.py \
    --max-hyp 10000 \
    --db .cache/proofs_10k.sqlite3 \
    --workers 8 --no-progress

# 拿 326 hard_case 的 ell2cover/rank 数据 (~6.6s)
uv run python scripts/batch_ell2cover_hard_cases.py \
    --db .cache/proofs_10k.sqlite3 \
    --out results/ell2cover_10k.jsonl
```

---

## 十、下一步候选

| priority | 任务 | 工作量 |
|---|---|---|
| ⭐⭐⭐ | 13 个 sha2≥2 case 的 ell2cover quartic + hyperellratpoints (复用 wl039 工具) | 1-2 小时 |
| ⭐⭐⭐ | 88 个 rank=1 case 的 Heegner generator scan (`run_heegner_height` 加深) | 1-2 天 |
| ⭐⭐ | max_hyp=20000 / 50000 看 hard_case ratio 是否仍稳定 ~0.01% | 5-30 分钟跑 |
| ⭐⭐ | 1 个有 2 个 concordant N 的特殊 case manual deep-dive | 1 小时 |
| ⭐ | Brauer-Manin manual analysis on 13 sha2≥2 case | 学术合作级 |

---

## 十一、Commit 历史

```
1b9d89a  feat(proof_status): parallel pipeline + batched commits
(本 worklog 计划: docs(worklog): 041 parallel pipeline + max_hyp 10k data)
```
