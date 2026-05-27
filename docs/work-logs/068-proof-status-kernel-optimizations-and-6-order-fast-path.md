# wl068 — proof_status 计算核优化 + AB sieve 3 层 / 6 排序收口

## 触发

前一轮工作把 `proof_status` 的大样本跑通了，也把 AB sieve 的顺序问题压缩到了前几层的工程调度。
但 `max_hyp=10000` 那次实跑之后，热点已经很清楚：

- `chain_closure_mod_sieve` 还在把全部 killer modulus 扫完
- `factor_search` 还在对 `B^2-A^2` 做 `O(sqrt(diff))` 级别的试除扫描
- `factor_concordant` 和 `f2_rank` 会对同一个 pair 重复做 factor search
- benchmark / pair 入口在 `limit` 场景下还会先把整份 pair 列表攒出来

这轮不是加新数学结论。
这轮做两件事：

1. 把已经确认的 4 个内核优化落进代码。
2. 按最新结论把 AB sieve core benchmark 收口成 3 层，也就是 `3! = 6` 种顺序。

用户同时明确了一条新的边界：

- 原来 benchmark 里拆开的第 3 / 第 4 层，现在可以合并
- 那对顺序不再需要继续当成默认 core 排序问题处理
- 旧的 split 模式可以保留，但它们只适合诊断，不再代表默认 benchmark 口径

## 本轮实现

### 1. `chain_closure_mod_sieve` 改成首个 killer 即停

文件：`src/rational_distance/proof_status/methods.py`

之前 `run_chain_closure_mod_sieve()` 调 `all_killer_moduli(...)`，会把整组模数跑完，再把全部 killer 收集出来。
这对证明语义没有帮助，因为只要找到一个 killer modulus，结论已经成立。

现在改成：

- 调 `find_killer_modulus(...)`
- 找到首个 killer 就返回
- `details["killer_moduli"]` 只保留首个 killer
- `details["moduli_tested"]` 只记录实际测试过的前缀

这一步直接砍掉了不必要的模筛尾部工作。

### 2. `proof_status` 主路径共享 concordant `N` 缓存

文件：

- `src/rational_distance/proof_status/methods.py`
- `src/rational_distance/proof_status/workflow.py`
- `src/rational_distance/proof_status/ab_sieve_methods.py`

做法分两层。

第一层在方法接口：

- `run_factor_concordant(...)` 新增可选参数 `concordant_n`
- `run_f2_rank(...)` 新增可选参数 `concordant_n`

第二层在调用方：

- `workflow.process_pair(...)` 为每个 pair 建一份本地 cache
- `workflow.compute_pair_status(...)` 也建同样的 cache
- `factor_concordant` 和 `f2_rank` 都从这份 cache 取 concordant `N`
- benchmark 侧的 `PairEvalContext` 也同步复用这份 cache

结果很直接：

- 一个 pair 在 `proof_status` 主路径里，factor search 只做一次
- benchmark 侧的 `factor_concordant` / `f2_rank` / `concordant_search` / `multi_n_sieve` 也不会重复做同一份 factor search

### 3. `factor_search` 改写成“分解 `B-A` / `B+A` 后生成约数”

文件：`src/rational_distance/concordant/factor_search.py`

旧版本的主成本在这里：

- 先算 `diff = B^2 - A^2`
- 再从 `1` 扫到 `sqrt(diff)` 找因子

新版本改成：

- 先分解 `diff_left = B-A`
- 再分解 `diff_right = B+A`
- 合并素因子指数得到 `diff` 的分解
- 从素因子分解递归生成 `<= sqrt(diff)` 的约数
- 继续沿用原来的奇偶过滤、`h3 < A` 过滤、平方判定

接口没有变：

- 仍然是 `find_concordant_by_factorization(A, B) -> list[int]`
- 仍然返回排序去重后的正整数 `N` 列表

但热点成本从“对整个 `diff` 扫到平方根”改成了“分解两个更小的数，再生成约数”。

### 4. pair 生成改成可流式入口

文件：`src/rational_distance/concordant/pairs.py`

新增：

- `iter_ab_pairs(max_hyp)`

保留：

- `generate_ab_pairs(max_hyp)`

兼容策略很简单：

- `iter_ab_pairs(...)` 负责流式生成去重后的 `(A, B)`
- `generate_ab_pairs(...)` 继续返回排好序的完整列表，内部改成 `sorted(iter_ab_pairs(...))`

这样旧调用方不破，新调用方可以按需消费。

### 5. AB sieve benchmark 默认口径改成 3 层 / 6 排序

文件：

- `src/rational_distance/proof_status/ab_sieve_benchmark.py`
- `scripts/benchmark_ab_sieve_orders.py`

默认 core 现在是：

```text
safe_sieve
chain_closure_mod_sieve
factor_concordant
```

因此默认 core order search 变成：

```text
3! = 6
```

这里的含义要写死：

- 默认 benchmark 已经不再把 `concordant_search` / `multi_n_sieve` 当成两个独立 core 层
- 它们保留在 `head_only` / `safe_top2_only` 这种 split 诊断模式里
- 这些模式现在主要服务历史对照和局部诊断，不再是默认排序结论的主出口

### 6. benchmark 入口也改成 pair factory / limit 流式消费

文件：

- `src/rational_distance/proof_status/ab_sieve_benchmark.py`
- `scripts/benchmark_ab_sieve_orders.py`

这一步补了两件事：

- `benchmark_specs(...)` 现在既能吃具体的 pair iterable，也能吃 `pair_source()` 这种 factory
- `benchmark_ab_sieve_orders.py` 在 `--limit` 场景下会走 `iter_ab_pairs + islice`，不再先把全量 pair 物化出来

额外收口：

- JSON 里的 `pair_count` 改成从 benchmark summary 回填，不再依赖 `len(pairs)`

## 回归测试

这轮按 TDD 落地，新增 / 更新了三组测试：

- `tests/test_proof_status.py`
- `tests/test_ab_sieve_benchmark.py`
- `tests/test_concordant.py`

重点回归面：

- `chain_closure_mod_sieve` 是否在首个 killer 后停止
- `process_pair()` / `compute_pair_status()` 是否只做一次 factor search
- benchmark context 下 `factor_concordant` / `f2_rank` 是否复用 concordant `N`
- 默认 core order 数是否从 24 收口到 6
- `--safe-first-only` 是否从 6 收口到 2
- `benchmark_specs(...)` 是否接受 pair factory
- `--limit` 模式是否走 `iter_ab_pairs(...)`
- `iter_ab_pairs(...)` 是否给出规范化、去重、互素的 pair 前缀

本轮验证命令：

```bash
uv run pytest tests/test_proof_status.py tests/test_ab_sieve_benchmark.py tests/test_concordant.py -q
```

结果：

```text
92 passed
```

## 对入口的实际影响

### 1. `scripts/prove_no_solution.py`

这个入口没有改 CLI 语义，但会自动吃到三类提速：

- chain closure 首个 killer 早停
- factor search 新算法
- `factor_concordant` / `f2_rank` 的共享 concordant `N` 缓存

所以你重新跑 `max_hyp=10000` 的 `proof_status`，不需要新参数，代码已经是快路径。

### 2. `scripts/benchmark_ab_sieve_orders.py`

默认口径现在变成：

- core：6 组
- `--safe-first-only`：2 组

而不是之前的：

- core：24 组
- `--safe-first-only`：6 组

这一步不是“少跑了所以看起来更快”。
它反映的是默认问题本身已经变了：

- 现在默认只比较 3 个 core 层
- split 模式只在你想回头看旧诊断问题时才需要

## 边界

这轮仍然守住两条边界。

第一条边界：

- 这轮只做内核优化和 benchmark 收口
- 不改 `proof_status` 的数学结论口径
- 不引入新的必要条件或新判定器

第二条边界：

- 这轮把默认 benchmark 收口到 3 层 / 6 排序
- 但 `head_only` / `safe_top2_only` 这些 split 模式没有删
- 你如果还想和旧结果对照，工具还在

## 输出物

### 代码

- `src/rational_distance/proof_status/methods.py`
- `src/rational_distance/proof_status/workflow.py`
- `src/rational_distance/proof_status/ab_sieve_methods.py`
- `src/rational_distance/proof_status/ab_sieve_benchmark.py`
- `src/rational_distance/concordant/factor_search.py`
- `src/rational_distance/concordant/pairs.py`
- `scripts/benchmark_ab_sieve_orders.py`

### 测试

- `tests/test_proof_status.py`
- `tests/test_ab_sieve_benchmark.py`
- `tests/test_concordant.py`

### 文档

- `docs/PROJECT_STATUS.md`
- `docs/IMPLEMENTATION.md`

## 本轮结论

一句话版本：

```text
proof_status 这轮把真正的计算核热点都削了一遍：
chain closure 不再扫完整组模数，factor_search 不再对 diff 做平方根级别全扫，
factor_concordant / f2_rank / benchmark split 方法都开始共享 concordant N，
AB sieve 默认 benchmark 也按最新结论收口成 3 层 / 6 排序。
```

这条 log 先记录“代码和测试已经到位”。
接下来的单独动作，就是在这份代码上重新跑一次 `max_hyp=10000`，只看当前最快路径到底把 wall time 压到了哪里。
