# 工程结构参考

这份文档只说明一件事：代码现在怎么分区、入口在哪里、兼容层怎么理解。
它不负责判断“当前先推进哪条线”，那个请看 [docs/DIRECTIONS.md](./DIRECTIONS.md) 和 [docs/PROJECT_STATUS.md](./PROJECT_STATUS.md)。

## 一、先看总原则

当前结构有几个固定原则：

- `scripts/search.py` 仍是统一用户入口，5 个子命令名不变。
- CLI 壳层继续放在 `src/rational_distance/cli/search/`。
- 真正实现优先看包目录：`ec_search/`、`chain_fast/`、`concordant/`。
- 旧导入路径先继续保留，不因为内部结构变清楚就立刻删兼容层。

这里说的“兼容层”，当前主要是顶层这 4 个 stub 文件：

- [src/rational_distance/search_ec.py](../src/rational_distance/search_ec.py)
- [src/rational_distance/search_chain_fast.py](../src/rational_distance/search_chain_fast.py)
- [src/rational_distance/concordant_ec.py](../src/rational_distance/concordant_ec.py)
- [src/rational_distance/pair_generator.py](../src/rational_distance/pair_generator.py)

每个都已经缩成 9 行的极简 stub，只做一件事：从 [_legacy/](../src/rational_distance/_legacy)
转发 `*` 与 `__all__`。真实的 re-export 列表在 `_legacy/` 子目录里。

它们现在不是“历史垃圾”，而是还在承担旧导入路径的兼容职责。

## 二、代码分成 5 个维护区

### 1. `three_vertex`

职责：

- 三顶点参数化搜索
- 三顶点椭圆曲线扩展
- 三顶点相关持久化和分析

主要代码：

- [src/rational_distance/search.py](../src/rational_distance/search.py)
- [src/rational_distance/parametric_core.py](../src/rational_distance/parametric_core.py)
- [src/rational_distance/search_gpu.py](../src/rational_distance/search_gpu.py)
- [src/rational_distance/ec_search/](../src/rational_distance/ec_search)
- [src/rational_distance/search_ec.py](../src/rational_distance/search_ec.py)
- [src/rational_distance/ec_db.py](../src/rational_distance/ec_db.py)
- [src/rational_distance/ec_analysis.py](../src/rational_distance/ec_analysis.py)

实现备注：

- `parametric_core.py` 是三顶点参数化判定的共享核心。
- `search.py` 和 `search_gpu.py` 更偏编排与后端执行。
- `ec_search/` 是三顶点 EC 路径的主实现；`search_ec.py` 是兼容入口。

### 2. `four_cycle_baseline`

职责：

- 四边闭环问题
- `chain-fast` 基线搜索
- chain / chain-fast 的数据库与分析

主要代码：

- [src/rational_distance/search_chain.py](../src/rational_distance/search_chain.py)
- [src/rational_distance/chain_fast/](../src/rational_distance/chain_fast)
- [src/rational_distance/search_chain_fast.py](../src/rational_distance/search_chain_fast.py)
- [src/rational_distance/chain_db.py](../src/rational_distance/chain_db.py)
- [src/rational_distance/chain_analysis.py](../src/rational_distance/chain_analysis.py)

实现备注：

- `search_chain.py` 偏原始 chain / 长方形路线。
- `chain_fast/` 是当前 `chain-fast` 的主实现区。
- `search_chain_fast.py` 是兼容入口。
- `chain_db.py` 和 `chain_analysis.py` 负责 `chain-fast` 的 SQLite 与分析辅助。

### 3. `concordant`

职责：

- 固定 `(A,B)` 后的 concordant / 椭圆曲线分析
- 从 chain / chain-fast 结构中提取 `(A,B)` 对

主要代码：

- [src/rational_distance/concordant/](../src/rational_distance/concordant)
- [src/rational_distance/concordant_ec.py](../src/rational_distance/concordant_ec.py)
- [src/rational_distance/pair_generator.py](../src/rational_distance/pair_generator.py)

实现备注：

- `concordant/` 是当前主实现包。
- `concordant_ec.py` 和 `pair_generator.py` 保留为兼容入口，不是主实现所在处。

### 4. `proof_status`

职责：

- 对每个 reduced `(A, B)` pair，**累积式**地证明它是否存在四顶点 chain 解
- 每个判定方法独立，按"先便宜后昂贵"的顺序串成 pipeline
- 全部尝试和最终结论都进 SQLite，可重入、可增量

主要代码：

- [src/rational_distance/proof_status/](../src/rational_distance/proof_status)
  - `types.py`：`PairProofStatus` / `MethodResult` 等数据类
  - `schema.py`：SQLite schema、DAO（`pair_proof_status`、`pair_method_attempts`）
  - `methods.py`：6 个判定方法（`safe_sieve` / `factor_concordant` / `rank_zero` / 三个 stub）
  - `workflow.py`：pipeline 编排，遇 terminal outcome 即停
  - `ab_sieve_methods.py`：把前四层 sieve 拆成可重排的 context-aware benchmark 方法
  - `ab_sieve_benchmark.py`：order builder、pair evaluator、并行 benchmark 聚合

入口脚本：

- [scripts/prove_no_solution.py](../scripts/prove_no_solution.py)
- [scripts/benchmark_ab_sieve_orders.py](../scripts/benchmark_ab_sieve_orders.py)

实现备注：

- 它**不是搜索器**，而是"判定 + 落库"工具，跟 `chain-fast` / `concordant` 不互相替代。
- `safe_sieve` 与 `factor_concordant` 都是 PARI-free 的严格必要条件；`rank_zero` 通过 `cypari2` 调 PARI；其余三个（Heegner / Chabauty / Brauer–Manin）是 stub，留接口给后续 SageMath / Magma 集成。
- `ab_sieve_methods.py` / `ab_sieve_benchmark.py` / `benchmark_ab_sieve_orders.py` 是这轮新增的**实验 benchmark 层**：
  - 默认把 AB sieve core 当成 3 层：`safe_sieve`、`chain_closure_mod_sieve`、`factor_concordant`
  - 默认 core order search 因而是 `3! = 6`
  - `--head-only`、`--safe-top2-only` 等模式仍保留，但它们现在更偏 split 诊断和历史对照
  - 不会自动改写 `workflow.py` 的默认生产顺序
- 详见 [docs/THEORY_DIRECTIONS_ADVANCED.md](./THEORY_DIRECTIONS_ADVANCED.md) 中各方向的"实现状态"说明。

### 5. `shared`

职责：

- 公共数学工具
- 公共并行工具
- 公共点/对称逻辑
- 后端检测
- CLI 壳层
- 通用脚本

主要代码：

- [src/rational_distance/math_utils.py](../src/rational_distance/math_utils.py)
- [src/rational_distance/parallel.py](../src/rational_distance/parallel.py)
- [src/rational_distance/square.py](../src/rational_distance/square.py)
- [src/rational_distance/backend.py](../src/rational_distance/backend.py)
- [src/rational_distance/cli/](../src/rational_distance/cli)

脚本层：

- [scripts/search.py](../scripts/search.py)
- [scripts/analyze_ec_db.py](../scripts/analyze_ec_db.py)
- [scripts/analyze_chain_db.py](../scripts/analyze_chain_db.py)
- [scripts/benchmark_parallel_executor.py](../scripts/benchmark_parallel_executor.py)
- [scripts/compare_parametric.py](../scripts/compare_parametric.py)
- [scripts/visualize.py](../scripts/visualize.py)

实现备注：

- `parallel.py` 是公共并行层：统一 `parallel_map(...)`、`ParallelConfig`、标准参数
  （`--workers` / `--chunksize` / `--serial`）。
- **单次批处理**优先直接用 `cfg.map(...)`。
- **循环里反复 map 的脚本**（例如 BFS 每轮都要并行一批任务）优先用
  `with cfg.executor() as executor:` 复用同一个 `spawn` 进程池，避免每轮重复建池。
- **只靠 `on_result` 回调汇总结果**的脚本，优先传 `collect_results=False`，避免在主进程
  里额外攒一整份返回列表。
- `scripts/benchmark_parallel_executor.py` 是小型基准脚本，用来比较“每轮重建进程池”与
  “复用进程池”两种写法的真实开销差。

## 三、入口层和实现层怎么区分

现在的工程入口大致分三层：

### 1. 用户入口

- [scripts/search.py](../scripts/search.py)

这是用户真正调用的统一命令入口，5 个子命令都从这里进。

### 2. CLI 壳层

- [src/rational_distance/cli/search/parser.py](../src/rational_distance/cli/search/parser.py)
- [src/rational_distance/cli/search/runners.py](../src/rational_distance/cli/search/runners.py)
- [src/rational_distance/cli/search/output.py](../src/rational_distance/cli/search/output.py)

这一层负责：

- 解析参数
- 选择 runner
- 组织输出

### 3. 各方向实现层

- `parametric` / `ec` / `chain` / `chain-fast` / `concordant` 各自的实现模块

整理代码时，尽量保持这个分层，不要把大量数学逻辑重新堆回 CLI 壳层。

## 四、兼容层现在怎么理解

兼容层物理上分两段：

**顶层 stub（4 个）**：

- `search_ec.py`、`search_chain_fast.py`、`concordant_ec.py`、`pair_generator.py`
- 每个文件 9 行，纯 `from rational_distance._legacy.* import *` 转发
- 目的：让 `from rational_distance.search_ec import ec_search` 这种历史导入路径继续可用

**真实 re-export 列表（4 个）**：

- 集中在 [src/rational_distance/_legacy/](../src/rational_distance/_legacy)
- 完整的 `from X import (...)` + `__all__` 列表都在这里
- 这个子目录里**不应该有任何新代码**——它是一个标记为 deprecated 的迁移地带

它们当前仍有真实调用方，包括测试、数据库层（`chain_db.py`、`ec_db.py`）和部分 CLI runners。
所以“包目录已经更清楚了”不等于“这些文件已经可以直接删”。

如果以后想彻底移除兼容层，路径是：

1. 把所有 `from rational_distance.search_chain_fast import X`
   改为 `from rational_distance.chain_fast import X`（其它三条类推）
2. 跑 `uv run pytest` 确认 191 测试仍过
3. 删除 4 个顶层 stub + `_legacy/` 子目录

## 五、当前测试结构映射

当前映射如下：

- [tests/test_parametric.py](../tests/test_parametric.py)：`parametric` + 一部分 `shared`
- [tests/test_ec.py](../tests/test_ec.py)：`ec`
- [tests/test_chain.py](../tests/test_chain.py)：`chain`
- [tests/test_chain_fast.py](../tests/test_chain_fast.py)：`chain-fast`
- [tests/test_chain_db.py](../tests/test_chain_db.py)：`chain-fast` DB
- [tests/test_chain_fast_cli.py](../tests/test_chain_fast_cli.py)：`chain-fast` CLI / 脚本冒烟
- [tests/test_concordant.py](../tests/test_concordant.py)：`concordant` + 兼容入口校验
- [tests/test_parallel.py](../tests/test_parallel.py)：公共并行层（串行回退、回调、复用进程池）
- [tests/test_proof_status.py](../tests/test_proof_status.py)：`proof_status` 各 method、schema DAO、workflow 流程
- [tests/test_cli.py](../tests/test_cli.py)：CLI 参数与 compare 脚本冒烟

## 六、历史记录怎么读

- `docs/work-logs/` 反映的是每次提交当时的结构和判断。
- 如果历史日志和当前目录结构不完全一致，以当前源码和本文件为准。
- 当前主线与状态判断仍以 [docs/DIRECTIONS.md](./DIRECTIONS.md) 和 [docs/PROJECT_STATUS.md](./PROJECT_STATUS.md) 为准。
