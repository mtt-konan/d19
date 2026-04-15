# 项目方向地图（唯一入口）

这份文档是“项目现在有哪些路线、各自负责什么、该从哪里下手读代码”的唯一入口。

统一口径（维护视角）：
- `concordant`：`active`（当前主线，目标是从数学结构继续往前推）
- `chain-fast`：`baseline`（最可信的四顶点基线搜索器，用来做对照与提供数据）
- `parametric` / `ec` / `chain`：`paused`（保留，但暂不作为推进主线）

项目对外仍保留 5 个子命令（CLI 语义不改）：
- `parametric`
- `ec`
- `chain`
- `chain-fast`
- `concordant`

但从维护和整理角度，把代码分成 4 个“区”（后续文件移动也按这个边界）：
- `three_vertex`：三顶点相关（坐标/参数化/EC）
- `four_cycle_baseline`：四边链 + 四顶点基线搜索（chain / chain-fast）
- `concordant`：固定 `(A,B)`、研究共同腿 `N` 的数学主线
- `shared`：共享数学工具、平方判定、后端与 CLI

---

## 0. 推荐阅读顺序（两跳到入口）

1. 本文：先把“路线和入口”搞清楚。
2. [docs/PROJECT_STATUS.md](PROJECT_STATUS.md)：只看现状、主线、瓶颈。
3. [docs/SEARCH_METHODS.md](SEARCH_METHODS.md)：把 5 个子命令当成“词典”理解。
4. [docs/MATH.md](MATH.md)：数学推导库。`concordant` 相关章节是主线。
5. `chain-fast` 相关文档：看 profile/安全筛/结构统计结论（用于找证据）。
6. `docs/work-logs/`：按时间线回看每次工作内容（用完整文件名索引）。

---

## 1. 5 条方向（CLI 维度）

下面每条都给出：状态、它在干什么、代码入口、文档入口、测试入口、脚本入口、worklog 入口。

### 1.1 `parametric`（paused）

一句话：从“参数化/坐标”直接生成候选点，检查四个顶点里有几个距离是有理数。

- 运行入口：`uv run python scripts/search.py parametric --help`
- 代码入口：
  - `src/rational_distance/search.py`
  - `src/rational_distance/parametric_core.py`
  - `src/rational_distance/search_gpu.py`
- 文档入口：
  - [docs/SEARCH_METHODS.md](SEARCH_METHODS.md)
  - [docs/MATH.md](MATH.md)
- 测试入口：
  - `tests/test_parametric.py`
  - `tests/test_cli.py`（部分 CLI 冒烟）
- 脚本入口：
  - `scripts/search.py`
  - `scripts/compare_parametric.py`
  - `scripts/visualize.py`
- worklog 入口（节选）：
  - `docs/work-logs/001-initial-parametric-search.md`
  - `docs/work-logs/002-numpy-vectorization.md`
  - `docs/work-logs/005-gpu-search.md`
  - `docs/work-logs/013-parametric-shared-core.md`

### 1.2 `ec`（paused）

一句话：基于“三顶点 seed”，沿椭圆曲线轨道扩展出更多三顶点有理解，并支持 SQLite 持久化与分析。

- 运行入口：`uv run python scripts/search.py ec --help`
- 代码入口：
  - `src/rational_distance/search_ec.py`
  - `src/rational_distance/ec_search/`
  - `src/rational_distance/ec_db.py`
  - `src/rational_distance/ec_analysis.py`
- 文档入口：
  - [docs/SEARCH_METHODS.md](SEARCH_METHODS.md)
  - [docs/MATH.md](MATH.md)
  - [docs/IMPLEMENTATION.md](IMPLEMENTATION.md)
- 测试入口：
  - `tests/test_ec.py`
- 脚本入口：
  - `scripts/search.py`
  - `scripts/analyze_ec_db.py`
- worklog 入口（节选，注意有两个 `014-*` 同号文件，必须用全名）：
  - `docs/work-logs/010-ec-search-foundation.md`
  - `docs/work-logs/012-ec-vectorization-gpu.md`
  - `docs/work-logs/014-ec-db-analysis.md`
  - `docs/work-logs/020-ec-concordant-analysis-pipeline.md`

### 1.3 `chain`（paused）

一句话：枚举整数 `a,b,c,d`，让四条相邻边都能拼成直角三角形（长方形问题）；默认不强制正方形约束 `a+c=b+d`。

- 运行入口：`uv run python scripts/search.py chain --help`
- 代码入口：
  - `src/rational_distance/search_chain.py`
- 文档入口：
  - [docs/SEARCH_METHODS.md](SEARCH_METHODS.md)
  - [docs/PROJECT_STATUS.md](PROJECT_STATUS.md)（解释“半解很多但主问题很硬”）
  - [docs/MATH.md](MATH.md)（chain 结构到 `(A,B,N)` 的推导）
- 测试入口：
  - `tests/test_chain.py`（目前这里混放了一部分 concordant/pair 相关测试，见“下一轮整理点”）
- 脚本入口：
  - `scripts/search.py`
- worklog 入口（节选）：
  - `docs/work-logs/014-pythagorean-chain-search.md`
  - `docs/work-logs/015-cross-product-family-exclusion.md`
  - `docs/work-logs/016-primitive-decomposition-display.md`
  - `docs/work-logs/017-chain-reduction-math.md`

### 1.4 `chain-fast`（baseline）

一句话：把“四顶点正方形主问题”改写成“两组本原勾股数的配对 O(n^2)”；它是目前最可信、覆盖最完整的基线搜索器。

- 运行入口：`uv run python scripts/search.py chain-fast --help`
- 代码入口：
  - `src/rational_distance/search_chain_fast.py`
  - `src/rational_distance/chain_fast/`
  - `src/rational_distance/chain_db.py`（SQLite、near-miss、resume）
  - `src/rational_distance/chain_analysis.py`
- 文档入口：
  - [docs/CHAIN_FAST_PERFORMANCE.md](CHAIN_FAST_PERFORMANCE.md)
  - [docs/CHAIN_FAST_OPTIMIZATION.md](CHAIN_FAST_OPTIMIZATION.md)
  - [docs/CHAIN_FAST_SAFE_FILTERS.md](CHAIN_FAST_SAFE_FILTERS.md)
  - [docs/CHAIN_FAST_MOD_SIEVE.md](CHAIN_FAST_MOD_SIEVE.md)
  - [docs/CHAIN_FAST_BUCKET_STATS.md](CHAIN_FAST_BUCKET_STATS.md)
  - [docs/CHAIN_FAST_STRUCTURE_FINDINGS.md](CHAIN_FAST_STRUCTURE_FINDINGS.md)
- 测试入口：
  - `tests/test_chain_fast.py`
  - `tests/test_chain_db.py`（目前也混了 CLI/脚本集成，见“下一轮整理点”）
- 脚本入口：
  - `scripts/search.py`
  - `scripts/analyze_chain_db.py`
- worklog 入口（节选）：
  - `docs/work-logs/018-chain-fast-implementation.md`
  - `docs/work-logs/021-chain-numpy-db.md`
  - `docs/work-logs/022-chain-fast-profile-cache.md`
  - `docs/work-logs/023-chain-fast-mod-sieve-experiment.md`
  - `docs/work-logs/024-chain-fast-100k-structure-findings.md`
  - `docs/work-logs/025-chain-fast-safe-pair-sieve.md`

### 1.5 `concordant`（active）

一句话：固定 `(A,B)`，研究是否存在共同腿 `N` 使得 `N^2+A^2` 与 `N^2+B^2` 同时为平方；这是继续推进主问题的数学主线。

- 运行入口：`uv run python scripts/search.py concordant --help`
- 代码入口：
  - `src/rational_distance/concordant_ec.py`
  - `src/rational_distance/pair_generator.py`
- 文档入口：
  - [docs/MATH.md](MATH.md)（concordant form / EC 推导与对应关系）
  - [docs/PROJECT_STATUS.md](PROJECT_STATUS.md)（为什么把它定为主线）
- 测试入口：
  - `tests/test_chain.py`（目前混放了 concordant/pair 相关测试，见“下一轮整理点”）
- 脚本入口：
  - `scripts/search.py`
  - 目前不单独产出 HTML/JSON 作为主路径；优先以 SQLite/终端结果为准
- worklog 入口（节选）：
  - `docs/work-logs/020-ec-concordant-analysis-pipeline.md`
  - `docs/work-logs/017-chain-reduction-math.md`（从 chain 推到 `(A,B,N)` 的推导背景）

---

## 2. 4 个维护区（代码归并视角）

这不是对外接口，是为了让代码“分类放好、不混在一起”，也为下一轮整理铺路。

- `three_vertex`（三顶点）
  - 典型入口：`src/rational_distance/search.py`、`src/rational_distance/search_ec.py`
- `four_cycle_baseline`（四边链与四顶点基线）
  - 典型入口：`src/rational_distance/search_chain.py`、`src/rational_distance/chain_fast/`
- `concordant`（固定 `(A,B)` 与共同腿 `N`）
  - 典型入口：`src/rational_distance/concordant_ec.py`
- `shared`（共享）
  - 典型入口：`src/rational_distance/square.py`、`src/rational_distance/backend.py`、`src/rational_distance/cli/`

---

## 3. `tmp.txt` 与 `concordant` 的关系（必须说清）

结论一句话：`tmp.txt` 里讨论的“固定 `(A,B)`，研究共同腿 `N`”路线，和现在项目里的 `concordant` 是同一条数学路线，只是切入层次不同。

- `tmp.txt` 的切入点：
  - 从 `chain/chain-fast` 的结构出发，把问题化到 `(A,B,N)`，再讨论“共同腿 `N` 是否存在”
  - 更像“从枚举结构推到固定 `(A,B)`”
- 现在 `concordant` 代码的切入点：
  - 直接把 `(A,B)` 当作输入，走 concordant form / 椭圆曲线的分析框架
  - 再把结论回扣到 `chain-fast` 里“这对 `(A,B)` 是否值得、为什么会出现半解/near-miss”

所以方向不是两条，而是一条：都在研究同一个事实 “`C3+C4` 共享同一个 `N`” 能带来哪些硬约束。

---

## 4. 下一轮整理点（本轮不做，只写死边界）

这些问题已经存在，但本轮只做文档，不动代码结构：
- `tests/test_chain.py` 目前混放：`chain` + `pair_generator` + `concordant`。下一轮应拆出 `tests/test_concordant.py` 或 `tests/concordant/`。
- `tests/test_chain_db.py` 目前混放：DB 测试 + CLI 集成 + 分析脚本集成。下一轮应把 CLI/脚本集成单独拆出。
- `tests/test_parametric.py` 里包含部分 `shared` 测试。下一轮应抽离成更明确的 `shared` 单测文件。
