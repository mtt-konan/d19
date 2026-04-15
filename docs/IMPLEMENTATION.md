# 工程结构参考

这份文档只负责说明代码现在怎么分区、入口在哪、以后整理代码时边界怎么守。  
它不负责回答“现在先做哪条线”，那个请看 [docs/DIRECTIONS.md](./DIRECTIONS.md) 和 [docs/PROJECT_STATUS.md](./PROJECT_STATUS.md)。

## 一、先看总原则

这一轮先把工程边界写死，但不搬代码。

固定原则：

- 保留 `scripts/search.py` 的 5 个子命令名不变
- 保留 `cli/search/parser.py` 和 `cli/search/runners.py` 的用户接口不变
- 后续如果要整理目录，优先先整理 `concordant`
- 任何代码移动都必须保留旧 import 兼容层

这里说的“兼容层”，做法对齐现在已经存在的：

- [src/rational_distance/search_ec.py](../src/rational_distance/search_ec.py)
- [src/rational_distance/search_chain_fast.py](../src/rational_distance/search_chain_fast.py)

也就是：

- 可以把真正实现移到更清楚的包路径
- 但旧入口先保留为薄封装或转发层
- 不能一口气把老 import 和老命令全打断

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

- `parametric_core.py` 是三顶点参数化判定的共享核心
- `search.py` 和 `search_gpu.py` 更偏编排与后端执行
- `ec_search/` 是三顶点 EC 路径的主体

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

- `search_chain.py` 偏原始 chain / 长方形路线
- `chain_fast/` 是当前 `chain-fast` 真正的实现区
- `search_chain_fast.py` 是兼容入口
- `chain_db.py` 和 `chain_analysis.py` 负责 `chain-fast` 的 SQLite 与分析辅助

### 3. `concordant`

职责：

- 固定 `(A,B)` 后的 concordant / 椭圆曲线分析
- 从 chain / chain-fast 结构中提取 `(A,B)` 对

主要代码：

- [src/rational_distance/concordant_ec.py](../src/rational_distance/concordant_ec.py)
- [src/rational_distance/pair_generator.py](../src/rational_distance/pair_generator.py)

实现备注：

- 这一块现在还散在顶层，没有形成像 `chain_fast/`、`ec_search/` 那样清楚的包边界
- 所以下一轮如果要整理目录，第一优先级应当是 `concordant`

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

## 四、当前测试结构也要这样理解

这轮不拆测试，只先标注边界。

当前映射：

- [tests/test_parametric.py](../tests/test_parametric.py)：`parametric` + 一部分 `shared`
- [tests/test_ec.py](../tests/test_ec.py)：`ec`
- [tests/test_chain.py](../tests/test_chain.py)：`chain` + `pair_generator` + `concordant`
- [tests/test_chain_fast.py](../tests/test_chain_fast.py)：`chain-fast`
- [tests/test_chain_db.py](../tests/test_chain_db.py)：`chain-fast` DB + CLI + 分析脚本集成
- [tests/test_cli.py](../tests/test_cli.py)：目前主要是 `parametric`/compare 相关 smoke test

这里已经可以看出下一轮整理重点：

- `concordant` 测试要从 `tests/test_chain.py` 里拆出来
- `pair_generator` 测试也应该和 `concordant` 放到一起
- `chain-fast` CLI 集成测试要从 `tests/test_chain_db.py` 里拆清
- `shared` 单测要逐步从 `tests/test_parametric.py` 里分出来

## 五、如果下一轮开始搬代码，顺序应该怎样

建议顺序固定为：

1. 先给 `concordant` 建明确包路径。
2. 保留旧 import 兼容层。
3. 再拆对应测试。
4. 最后再考虑是否要继续整理别的方向。

不建议的做法：

- 先大规模搬所有模块
- 一次性改 import
- 先改 CLI，再回头收实现

这样很容易把方向边界、用户入口、测试归属同时打乱。

## 六、这份文档刻意不再写什么

这里不再写这些内容：

- “现在最该推进哪条路线”
- 历史阶段判断
- 很快就会失真的测试总数
- 旧的大一统测试文件名

这些信息变化太快，写在工程结构页里很容易变旧。  
当前主线和状态请回到 [docs/DIRECTIONS.md](./DIRECTIONS.md) 与 [docs/PROJECT_STATUS.md](./PROJECT_STATUS.md)。
