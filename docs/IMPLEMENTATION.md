# 工程结构参考

这份文档只说明一件事：代码现在怎么分区、入口在哪里、兼容层怎么理解。
它不负责判断“当前先推进哪条线”，那个请看 [docs/DIRECTIONS.md](./DIRECTIONS.md) 和 [docs/PROJECT_STATUS.md](./PROJECT_STATUS.md)。

## 一、先看总原则

当前结构有几个固定原则：

- `scripts/search.py` 仍是统一用户入口，5 个子命令名不变。
- CLI 壳层继续放在 `src/rational_distance/cli/search/`。
- 真正实现优先看包目录：`ec_search/`、`chain_fast/`、`concordant/`。
- 旧导入路径先继续保留，不因为内部结构变清楚就立刻删兼容层。

这里说的“兼容层”，当前主要是这些文件：

- [src/rational_distance/search_ec.py](../src/rational_distance/search_ec.py)
- [src/rational_distance/search_chain_fast.py](../src/rational_distance/search_chain_fast.py)
- [src/rational_distance/concordant_ec.py](../src/rational_distance/concordant_ec.py)
- [src/rational_distance/pair_generator.py](../src/rational_distance/pair_generator.py)

它们现在不是“历史垃圾”，而是还在承担旧导入路径的兼容职责。

## 二、代码分成 4 个维护区

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

### 4. `shared`

职责：

- 公共数学工具
- 公共点/对称逻辑
- 后端检测
- CLI 壳层
- 通用脚本

主要代码：

- [src/rational_distance/math_utils.py](../src/rational_distance/math_utils.py)
- [src/rational_distance/square.py](../src/rational_distance/square.py)
- [src/rational_distance/backend.py](../src/rational_distance/backend.py)
- [src/rational_distance/cli/](../src/rational_distance/cli)

脚本层：

- [scripts/search.py](../scripts/search.py)
- [scripts/analyze_ec_db.py](../scripts/analyze_ec_db.py)
- [scripts/analyze_chain_db.py](../scripts/analyze_chain_db.py)
- [scripts/compare_parametric.py](../scripts/compare_parametric.py)
- [scripts/visualize.py](../scripts/visualize.py)

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

当前兼容层主要有两类：

- 搜索方向兼容入口：`search_ec.py`、`search_chain_fast.py`
- `concordant` 兼容入口：`concordant_ec.py`、`pair_generator.py`

它们当前仍有真实调用方，包括测试、数据库层和部分 CLI 代码。
所以“包目录已经更清楚了”不等于“这些文件已经可以直接删”。

## 五、当前测试结构映射

当前映射如下：

- [tests/test_parametric.py](../tests/test_parametric.py)：`parametric` + 一部分 `shared`
- [tests/test_ec.py](../tests/test_ec.py)：`ec`
- [tests/test_chain.py](../tests/test_chain.py)：`chain`
- [tests/test_chain_fast.py](../tests/test_chain_fast.py)：`chain-fast`
- [tests/test_chain_db.py](../tests/test_chain_db.py)：`chain-fast` DB
- [tests/test_chain_fast_cli.py](../tests/test_chain_fast_cli.py)：`chain-fast` CLI / 脚本冒烟
- [tests/test_concordant.py](../tests/test_concordant.py)：`concordant` + 兼容入口校验
- [tests/test_cli.py](../tests/test_cli.py)：CLI 参数与 compare 脚本冒烟

## 六、历史记录怎么读

- `docs/work-logs/` 反映的是每次提交当时的结构和判断。
- 如果历史日志和当前目录结构不完全一致，以当前源码和本文件为准。
- 当前主线与状态判断仍以 [docs/DIRECTIONS.md](./DIRECTIONS.md) 和 [docs/PROJECT_STATUS.md](./PROJECT_STATUS.md) 为准。
