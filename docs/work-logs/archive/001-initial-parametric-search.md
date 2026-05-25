# [001] 初始实现：参数化搜索框架

**日期**：2026-04-10  
**提交**：`d97ad33`

---

## 本次工作摘要

建立了项目的完整基础框架。核心数学思路是：利用本原勾股数三元组 (p,q,r) 参数化平面有理点，使 d(A)=k=a/b 自动为有理数，将其余三个距离的有理性化为整数完全平方判断（isqrt）。实现了三种搜索模式、RationalPoint 数据结构和完整的测试。

---

## 主要改动

- `src/rational_distance/math_utils.py` — 新建：`rational_sqrt`、`primitive_pythagorean_triples`、`scale_triple`
- `src/rational_distance/square.py` — 新建：`RationalPoint` dataclass、`compute_distances`、`make_point`、顶点常量
- `src/rational_distance/search.py` — 新建：三种搜索模式
  - `parametric_search_fast`：整数运算 + `ProcessPoolExecutor`（主路径）
  - `parametric_search`：Fraction 生成器（慢速备用）
  - `brute_force_search`：枚举分母 ≤ max_den 的所有有理点
- `scripts/search_3vertex.py` — 新建：CLI 入口，含进度条、JSON 输出、格式化表格
- `tests/test_math_utils.py`、`tests/test_search.py` — 新建：覆盖核心数学和搜索逻辑
- `pyproject.toml` — 项目元数据，依赖 numpy、sympy、tqdm

---

## 关键决策

**整数 isqrt 替代 Fraction**：d(B) ∈ ℚ 的条件等价于 tB = (ar-bp)²+(bq)² 是完全平方数。Python 的 `isqrt` 可在 O(1) 内完成判断，比 `Fraction` 运算快约 20 倍。

**ProcessPoolExecutor + initializer 模式**：每个 triple 是独立任务，天然适合并行。`_init_worker` 在子进程启动时预建互素对列表，避免每次任务重复计算 gcd。macOS 使用 `spawn` 模式，worker 函数必须为模块级（不能是 lambda）。

**两种方向 (p,q,r) 和 (q,p,r)**：交换 p↔q 对应交换 x↔y，保证参数化覆盖所有"以 A 为锚点"的解。

**`package=false` in pyproject.toml**：项目目录名 `d19` ≠ Python 包名 `rational_distance`，需要此设置绕过 uv 的包名校验。

---

## 注意点 / 后续

- 此版本无 D4 对称去重，等价类重复输出
- 无侧边过滤，结果中包含 x=1/y=1 的点（后续证明这些点不可能是解）
- Fraction 生成器模式保留作为慢速备用和教学参考
