# wl067 — AB sieve 顺序基准与交接说明：首两位基本锁定，后两位进入 top-2 大样本判定

## 触发

这一轮不是在做新的数学定理，而是在 `(A,B)` 路线里，为 `proof_status` 的前四层筛子回答一个更工程化的问题：

- `safe_sieve`
- `chain_closure_mod_sieve`
- `concordant_search`
- `multi_n_sieve`

如果把它们拆开后重排，哪种顺序最省时间？

这里有两个边界必须写清楚：

1. 这次 benchmark **不把 `closure` 当最终验证步骤**放进排序里。
2. 这次 benchmark **不改动现有 `DEFAULT_METHOD_PIPELINE` 的生产语义**，只是为后续实验路径学习更好的顺序。

因此，这条线的定位是：

- 它属于 `(A,B)` / `proof_status` 路线里的一个**工程子项目**
- 它服务于更快地枚举和诊断 pair
- 它**不是**整个 d19 项目的唯一后续方向，更不是“只剩下调顺序”

## 本轮实现

### 1. 新增的代码与脚本

本轮围绕 AB sieve benchmark 新增 / 扩展了以下文件：

- `src/rational_distance/proof_status/ab_sieve_methods.py`
  - 把旧的 layer 1-4 拆成可独立重排的 context-aware 方法
  - 关键拆分是把 `factor_concordant` 分成：
    - `concordant_search`
    - `multi_n_sieve`
  - 通过 `PairEvalContext` 共享 concordant `N` 缓存，避免 benchmark 因重复 factor search 而失真

- `src/rational_distance/proof_status/ab_sieve_benchmark.py`
  - `OrderSpec` / `OrderBenchmarkSummary` / `PairBenchmarkResult`
  - core / tail / incremental / full 等 order builder
  - 复用 `ParallelConfig.executor()` + `collect_results=False` 的批量 benchmark runner

- `scripts/benchmark_ab_sieve_orders.py`
  - benchmark CLI 驱动
  - 支持输出 JSON 报告

- `tests/test_ab_sieve_benchmark.py`
  - 新 benchmark 层的单测与 CLI smoke test

### 2. 新增的 benchmark 模式

除了默认的 `24 + 6 + 3 + 1` 方案外，本轮又增加了几个为大样本探索服务的缩减模式：

- `--safe-first-only`
  - 固定 `safe_sieve` 在第一位
  - 只比较其余三层的 `3! = 6` 种顺序

- `--skip-extra`
  - 只跑 core，不跑 tail / incremental / legacy extra

- `--head-only`
  - 每个可能的首位方法只取一个代表顺序
  - 用来回答“第一名到底该是谁”

- `--safe-top2-only`
  - 只比较这两个 safe-first 决赛顺序：
  - `safe_sieve -> chain_closure_mod_sieve -> multi_n_sieve -> concordant_search`
  - `safe_sieve -> chain_closure_mod_sieve -> concordant_search -> multi_n_sieve`

### 3. 兼容性原则

这一轮始终保持一条红线：

- benchmark harness 是**旁路实验层**
- 旧的 `proof_status.workflow` / `DEFAULT_METHOD_PIPELINE` 继续保留
- benchmark 结果只能指导后续实验，不应在没有额外确认的情况下直接替换生产默认顺序

## 主要实测结果

下面只记对交接最重要的几轮。

### 1. 先固定第一名：`safe_sieve`

用 `--head-only` 跑到 `max_hyp=3000`、`223,037` pairs、`10 workers`：

- `14.469s` — `safe_sieve -> multi_n_sieve -> concordant_search -> chain_closure_mod_sieve`
- `46.759s` — `chain_closure_mod_sieve -> multi_n_sieve -> concordant_search -> safe_sieve`
- `503.807s` — `multi_n_sieve -> safe_sieve -> concordant_search -> chain_closure_mod_sieve`
- `507.533s` — `concordant_search -> safe_sieve -> multi_n_sieve -> chain_closure_mod_sieve`

结论：

- `safe_sieve` 放第一位的优势非常明显
- 第二名 `chain_closure_mod_sieve` 开头也远慢于它
- `multi_n_sieve` / `concordant_search` 开头都明显过重

所以“第一名是谁”这件事，在当前数据下已经基本锁定为：

```text
safe_sieve
```

### 2. 再固定第二名：`chain_closure_mod_sieve`

用 `--safe-first-only --skip-extra` 跑到 `max_hyp=5000`、`617,432` pairs、`10 workers`：

- `11.080s` — `safe_sieve -> chain_closure_mod_sieve -> multi_n_sieve -> concordant_search`
- `12.228s` — `safe_sieve -> chain_closure_mod_sieve -> concordant_search -> multi_n_sieve`
- `101.413s` — `safe_sieve -> multi_n_sieve -> concordant_search -> chain_closure_mod_sieve`
- `103.152s` — `safe_sieve -> multi_n_sieve -> chain_closure_mod_sieve -> concordant_search`
- `108.568s` — `safe_sieve -> concordant_search -> multi_n_sieve -> chain_closure_mod_sieve`
- `111.041s` — `safe_sieve -> concordant_search -> chain_closure_mod_sieve -> multi_n_sieve`

结论：

- 一旦第一位固定成 `safe_sieve`，第二位的赢家已经非常明确：

```text
chain_closure_mod_sieve
```

- 这不是轻微领先，而是数量级领先

### 3. 只剩最后两位：进入 top-2 大样本判定

上面两步做完之后，真正剩下的就只有：

- `... -> multi_n_sieve -> concordant_search`
- `... -> concordant_search -> multi_n_sieve`

为此增加了 `--safe-top2-only`。

在 `max_hyp=7000`、`1,226,838` pairs、`10 workers` 上的结果：

- `25.945s` — `safe_sieve -> chain_closure_mod_sieve -> concordant_search -> multi_n_sieve`
- `26.093s` — `safe_sieve -> chain_closure_mod_sieve -> multi_n_sieve -> concordant_search`

总 wall time：`54.76s`。

按这轮实测线性折算：

- `1,000,000` pairs 只跑这两组，约 `44.6s`

这里必须保守解释：

- 这轮里 `concordant_search -> multi_n_sieve` 略快
- 但二者差距只有 `0.147s`
- 相对 `26s` 级别总耗时，这只是一个**很小的领先**

所以当前更稳妥的结论不是“第 3/4 位已经彻底封板”，而是：

```text
第 1 位：safe_sieve
第 2 位：chain_closure_mod_sieve
第 3/4 位：目前轻微偏向 concordant_search -> multi_n_sieve，仍值得再用更大样本或重复跑确认
```

## 当前最可信的实验顺序

如果一定要给出一个当前最可信的**实验顺序**，那么可以写成：

```text
safe_sieve -> chain_closure_mod_sieve -> concordant_search -> multi_n_sieve
```

但这里有两个保留条件：

1. 这说的是**实验 benchmark 顺序**，不是已经要替换生产默认 pipeline。
2. `concordant_search` 与 `multi_n_sieve` 的先后差距目前仍很小，最好不要把它包装成“已经数学确定”。

## 这条线在整个项目里的位置

这部分最容易让接手的人误解，所以单独写清楚。

AB sieve 排序基准回答的是：

- 在 `proof_status` 的 `(A,B)` 路线里
- 已知前四层都是必要条件 / 安全筛时
- 哪个顺序更节省 wall time

它**没有**回答这些更大的问题：

- Harborth / Steiner-Beukers 反例到底是否存在
- 大范围无解是不是可以被证明
- `concordant` 椭圆曲线上的 rank / Sha / Heegner / Chabauty / Brauer-Manin 方向应该怎样继续推进
- `chain-fast` baseline 应该如何继续作为主问题对照

所以它只是整个项目中的一个分支：

- 它属于 `concordant` / `proof_status` 方向里的**工程调度问题**
- 它能帮后续批量实验省时间
- 但它不替代更核心的数学路线，也不替代 `chain-fast` baseline

## 后续接手建议

### 1. 如果只想把第 3 / 第 4 位彻底确认

不要再跑 24 组，也不要再跑 34 组。

直接用：

```bash
uv run python scripts/benchmark_ab_sieve_orders.py --max-hyp 7000 --workers 10 --chunksize 8 --batch-size 128 --safe-top2-only --json-out results/ab_top2_7000.json
```

或者继续放大到 `8000+`。

更稳的做法是：

- 固定 `--safe-top2-only`
- 在 `~1m pairs` 量级重复 3-5 次
- 比较 median / mean，而不是只看单次最小值

原因很简单：

- 前两位已经确定
- 最后一对的差距非常小
- 继续把预算花在 24 组 / 34 组上，性价比很低

### 2. 如果要从项目总线继续推进

不要把“AB sieve 排序”误读成“现在只剩下调顺序”。

更准确的说法是：

- 这条线只是让 `(A,B)` 路线里的前筛更快
- 它为更大范围的 `proof_status` / `concordant` 诊断服务
- 项目的主难点仍然是：如何得到更硬的必要条件，或者怎样跳出 `O(n^2)` 暴力与局部筛的范式

因此交接时，应该把后续工作分成两层：

#### A. 工程近线

- 用当前锁定的前两位顺序，继续跑更大范围的 `(A,B)` 诊断
- 整理 surviving pairs 的结构特征
- 只在 top-2 之间继续判定第 3/4 位

#### B. 数学主线

- Heegner 点直接构造
- Chabauty / Quadratic Chabauty
- Brauer-Manin 障碍
- K3 / Mordell-Weil lattice
- 以及 `chain-fast` 作为 baseline 的交叉验证

## 代码与入口（给接手的人）

如果要从源码继续接手，推荐阅读顺序：

1. `src/rational_distance/proof_status/ab_sieve_methods.py`
2. `src/rational_distance/proof_status/ab_sieve_benchmark.py`
3. `scripts/benchmark_ab_sieve_orders.py`
4. `tests/test_ab_sieve_benchmark.py`
5. `src/rational_distance/proof_status/methods.py`
6. `src/rational_distance/proof_status/workflow.py`

其中：

- `ab_sieve_methods.py` 负责“可重排”的 layer 1-4
- `ab_sieve_benchmark.py` 负责 order builder 与并行 benchmark
- `benchmark_ab_sieve_orders.py` 是所有实验模式的 CLI 入口
- `methods.py` / `workflow.py` 仍然代表生产 `proof_status` 的默认语义

## 本轮最终判断

一句话版本：

```text
AB sieve 排序基准已经把前两位基本锁定为
safe_sieve -> chain_closure_mod_sieve
最后两位目前轻微偏向 concordant_search -> multi_n_sieve，
但这仍然只是 proof_status / (A,B) 分支里的一个工程子方向，
不是整个项目后续方向的全部。
```
