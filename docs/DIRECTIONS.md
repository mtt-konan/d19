# 项目方向地图（唯一入口）

这份文档只回答一件事：项目现在有哪些路线、各自负责什么、应该从哪里读代码。

统一口径（维护视角）：

- `concordant`：`active`。当前主线，重点是固定 `(A,B)` 后共同腿 `N` 的数论结构。
- `chain-fast`：`baseline`。当前最可信的四顶点基线搜索器，负责做对照和留数据。
- `parametric` / `ec` / `chain`：`paused`。保留，但暂时不是继续扩展的主方向。

项目对外仍保留 5 个子命令，CLI 语义不变：

- `parametric`
- `ec`
- `chain`
- `chain-fast`
- `concordant`

从维护角度看，代码大致分成 4 个区：

- `three_vertex`：三顶点相关（参数化、坐标、EC）
- `four_cycle_baseline`：四边链与四顶点基线搜索
- `concordant`：固定 `(A,B)`、研究共同腿 `N`
- `shared`：公共数学工具、平方判定、后端与 CLI

---

## 0. 推荐阅读顺序

1. 本文：先把"现在有哪些路线"搞清楚。
2. [docs/PROJECT_STATUS.md](PROJECT_STATUS.md)：只看现状、主线和瓶颈。
3. [docs/GLOSSARY.md](GLOSSARY.md)：英文术语 → 中文叫法 + 一句话解释。第一次读 `concordant`/沙群/Selmer 相关 worklog 时查表。
4. [docs/MULTI_CONCORDANT_N_STRATEGY.md](MULTI_CONCORDANT_N_STRATEGY.md)：multi-N / 高 rank / closure 障碍的新主线。
5. [docs/CLOSURE_QUOTIENT_MAINLINE.md](CLOSURE_QUOTIENT_MAINLINE.md)：`tmp.txt` 里闭合商曲线方向的正式主线入口。
6. [docs/THEORY_DIRECTIONS.md](THEORY_DIRECTIONS.md)：短中期可落地的理论方向（安全前筛）。
7. [docs/THEORY_DIRECTIONS_ADVANCED.md](THEORY_DIRECTIONS_ADVANCED.md)：长期数学突破方向（Heegner / Chabauty / Brauer–Manin / K3）。
8. [docs/archive/SEARCH_METHODS.md](archive/SEARCH_METHODS.md)：把 5 个子命令当成词典看（已归档，仅供参考）。
9. [docs/MATH.md](MATH.md)：数学推导总库，`concordant` 相关章节是当前重点。
10. [docs/IMPLEMENTATION.md](IMPLEMENTATION.md)：看当前工程结构和兼容层现状。
11. [docs/literature/](literature/README.md)：相关文献的索引、时间轴、BibTeX、阅读笔记。⭐ 重点看 `notes/peschmann-2604-09328.md`，那是 d19 的"完美双胞胎"对标论文。
12. `chain-fast` 相关文档或 `docs/work-logs/`：只在需要工程细节或历史背景时回看。

---

## 1. 5 条方向（CLI 维度）

下面每条都给出：状态、它在做什么、代码入口、文档入口、测试入口和脚本入口。

### 1.1 `parametric`（paused）

一句话：从参数化坐标直接生成候选点，检查四个顶点里有几个距离是有理数。

- 运行入口：`uv run python scripts/search.py parametric --help`
- 代码入口：
  - `src/rational_distance/search.py`
  - `src/rational_distance/parametric_core.py`
  - `src/rational_distance/search_gpu.py`
- 文档入口：
  - [docs/archive/SEARCH_METHODS.md](archive/SEARCH_METHODS.md)
  - [docs/MATH.md](MATH.md)
- 测试入口：
  - `tests/test_parametric.py`
  - `tests/test_cli.py`
- 脚本入口：
  - `scripts/search.py`
  - `scripts/archive/compare_parametric.py`
  - `scripts/archive/visualize.py`

### 1.2 `ec`（paused）

一句话：先找三顶点 seed，再沿椭圆曲线轨道扩出更多相关解，并支持 SQLite 持久化和后续分析。

- 运行入口：`uv run python scripts/search.py ec --help`
- 代码入口：
  - `src/rational_distance/ec_search/`
  - `src/rational_distance/search_ec.py`（兼容入口）
  - `src/rational_distance/ec_db.py`
  - `src/rational_distance/ec_analysis.py`
- 文档入口：
  - [docs/archive/SEARCH_METHODS.md](archive/SEARCH_METHODS.md)
  - [docs/MATH.md](MATH.md)
  - [docs/IMPLEMENTATION.md](IMPLEMENTATION.md)
- 测试入口：
  - `tests/test_ec.py`
- 脚本入口：
  - `scripts/search.py`
  - `scripts/archive/analyze_ec_db.py`

### 1.3 `chain`（paused）

一句话：枚举整数 `a,b,c,d`，要求四条相邻边都能拼成直角三角形；默认不强制正方形约束 `a+c=b+d`。

- 运行入口：`uv run python scripts/search.py chain --help`
- 代码入口：
  - `src/rational_distance/search_chain.py`
- 文档入口：
  - [docs/archive/SEARCH_METHODS.md](archive/SEARCH_METHODS.md)
  - [docs/PROJECT_STATUS.md](PROJECT_STATUS.md)
  - [docs/MATH.md](MATH.md)
- 测试入口：
  - `tests/test_chain.py`
- 脚本入口：
  - `scripts/search.py`

### 1.4 `chain-fast`（baseline）

一句话：把四顶点正方形主问题改写成“两组本原勾股数的配对 O(n^2)”，是当前最可信、覆盖最完整的基线搜索器。

- 运行入口：`uv run python scripts/search.py chain-fast --help`
- 代码入口：
  - `src/rational_distance/chain_fast/`
  - `src/rational_distance/search_chain_fast.py`（兼容入口）
  - `src/rational_distance/chain_db.py`
  - `src/rational_distance/chain_analysis.py`
- 文档入口：
  - [docs/archive/CHAIN_FAST_SAFE_FILTERS.md](archive/CHAIN_FAST_SAFE_FILTERS.md)（safe_sieve 说明，已归档）
  - 历史背景（已归档）：
    [PERFORMANCE](archive/CHAIN_FAST_PERFORMANCE.md)、
    [OPTIMIZATION](archive/CHAIN_FAST_OPTIMIZATION.md)、
    [MOD_SIEVE](archive/CHAIN_FAST_MOD_SIEVE.md)、
    [BUCKET_STATS](archive/CHAIN_FAST_BUCKET_STATS.md)、
    [STRUCTURE_FINDINGS](archive/CHAIN_FAST_STRUCTURE_FINDINGS.md)
- 测试入口：
  - `tests/test_chain_fast.py`
  - `tests/test_chain_db.py`
  - `tests/test_chain_fast_cli.py`
- 脚本入口：
  - `scripts/search.py`
  - `scripts/archive/analyze_chain_db.py`

### 1.5 `concordant`（active）

一句话：固定 `(A,B)`，研究是否存在共同腿 `N` 使 `N^2+A^2` 与 `N^2+B^2` 同时为平方；这是当前继续推进主问题的数学主线。

- 运行入口：`uv run python scripts/search.py concordant --help`
- 代码入口：
  - `src/rational_distance/concordant/`（当前主实现）
  - `src/rational_distance/concordant_ec.py`（兼容入口）
  - `src/rational_distance/pair_generator.py`（兼容入口）
- 文档入口：
  - [docs/MATH.md](MATH.md)
  - [docs/PROJECT_STATUS.md](PROJECT_STATUS.md)
  - [docs/MULTI_CONCORDANT_N_STRATEGY.md](MULTI_CONCORDANT_N_STRATEGY.md)
  - [docs/CLOSURE_QUOTIENT_MAINLINE.md](CLOSURE_QUOTIENT_MAINLINE.md)
- 测试入口：
  - `tests/test_concordant.py`
  - `tests/test_mixed_closure_curves.py`
  - `tests/test_mixed_closure_rank_cli.py`
- 脚本入口：
  - `scripts/search.py`
  - `scripts/theory/rank_mixed_closure_curves.py`

---

## 2. 4 个维护区（代码归并视角）

这不是对外 API，只是为了让代码边界更清楚。

- `three_vertex`
  - 典型入口：`src/rational_distance/search.py`、`src/rational_distance/ec_search/`
- `four_cycle_baseline`
  - 典型入口：`src/rational_distance/search_chain.py`、`src/rational_distance/chain_fast/`
- `concordant`
  - 典型入口：`src/rational_distance/concordant/`
- `shared`
  - 典型入口：`src/rational_distance/square.py`、`src/rational_distance/backend.py`、`src/rational_distance/cli/`

---

## 3. `tmp.txt` 与 `concordant` 的关系

结论一句话：`tmp.txt` 已经收进 `concordant` 主线，但要分成两层看。

第一层是旧的共同腿问题：

```text
固定 (A,B)，找 N，使 N^2+A^2 和 N^2+B^2 同时为平方。
```

这一层对应现有 `concordant` 曲线 $E_{A,B}$，负责解释为什么很多 pair 会有半解。

第二层是现在正式接入的 closure quotient 子方向：

```text
令 M=A+B-N，再同时要求 M^2+A^2 和 M^2+B^2 也是平方。
```

普通话说：第一层只看一条腿 `N`，第二层把另一条闭合腿 `M` 也放回同一个对象里。这个子方向的入口是
[docs/CLOSURE_QUOTIENT_MAINLINE.md](CLOSURE_QUOTIENT_MAINLINE.md)。

当前已经收清楚的结论是：

- `AB/BA` 没有按 `tmp.txt` 预期变成 rank-0 击杀器。
- `AA/BB rank=0` 才是当前可用的新信号。
- 对 `AA/BB rank=0` 的行，torsion 回拉已经能严格列尽仿射点；两批样本里只回到中点，没有完整闭合点。
- 这仍是局部判据，不是 Harborth 猜想的全局证明。
- 后续不再把单个 `(A,B)` 证书数量增长当主进展；closure quotient 先作为离线局部证书工具收尾，
  新主线转向 `lambda=A/B` 的本原比例类结构证明。

---

## 4. 兼容入口和历史文档怎么看

- `search_ec.py`、`search_chain_fast.py`、`concordant_ec.py`、`pair_generator.py` 现在仍然保留，用来兼容旧导入路径。
- 真正想看当前实现时，优先看 `ec_search/`、`chain_fast/`、`concordant/` 这些包目录。
- `docs/work-logs/` 记录的是“当时那一版”的实现和判断，适合查历史背景，不保证和当前结构一模一样。
- 当前结构与方向的最新口径，以本文、[docs/PROJECT_STATUS.md](PROJECT_STATUS.md) 和 [docs/IMPLEMENTATION.md](IMPLEMENTATION.md) 为准。
