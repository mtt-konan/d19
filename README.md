# Rational Distance to Unit Square Vertices

这个项目探索一个经典的数论未解问题：

> **平面内是否存在一点，到单位正方形四个顶点的距离均为有理数？**

目前已知答案未定（Harborth 猜想认为不存在）。本项目的策略是先穷举到三个顶点距离为有理数的所有解，同时捎带检查第四个距离是否也有理，逐步缩小搜索范围。

---

## 数学背景

设单位正方形顶点为 A(0,0)、B(1,0)、C(1,1)、D(0,1)，点 P=(x,y)。

**参数化方法**：利用勾股数三元组 (p,q,r)（满足 p²+q²=r²），令

$$P = \left(\frac{ap}{br},\ \frac{aq}{br}\right), \quad k = \frac{a}{b} \in \mathbb{Q}^+$$

则 d(A)=k 自动是有理数。其余三个距离的有理性等价于以下整数判断：

| 距离 | 条件（分子为完全平方数） |
|------|------------------------|
| d(B) | $(ar - bp)^2 + (bq)^2 = \square$ |
| d(D) | $(ar - bq)^2 + (bp)^2 = \square$ |
| d(C) | $(ar - b(p+q))^2 + (b(p-q))^2 = \square$ |

这样所有判断都化为纯整数运算（`isqrt`），无需 Fraction 对象，是速度提升的核心。

---

## 项目结构

```
d19/
├── src/rational_distance/
│   ├── __init__.py
│   ├── math_utils.py   # 有理平方根、勾股数三元组生成
│   ├── square.py       # RationalPoint 数据类、顶点定义、距离计算
│   └── search.py       # 三种搜索策略（快速整数法、Fraction回退、暴力枚举）
├── scripts/
│   ├── search_3vertex.py  # 主入口 CLI
│   └── search_4vertex.py  # 专门找四顶点解（min_rational=4 的封装）
├── tests/
│   ├── test_math_utils.py
│   └── test_search.py
├── results_3v.json     # 最近一次搜索结果（示例）
└── pyproject.toml
```

---

## 安装与运行

需要 [uv](https://github.com/astral-sh/uv)：

```bash
# 安装依赖
uv sync

# 用默认参数搜索（max_m=60，约 60M 组合，~5s）
uv run python scripts/search_3vertex.py

# 更大范围（max_m=80，约 287M，~20s）
uv run python scripts/search_3vertex.py --max-m 80 --max-k-num 600 --max-k-den 300

# 专门找四顶点解
uv run python scripts/search_3vertex.py --min-rational 4 --max-m 120 --max-k-num 1000 --max-k-den 500

# 结果保存到 JSON
uv run python scripts/search_3vertex.py --out my_results.json

# 查看所有选项
uv run python scripts/search_3vertex.py --help
```

### CLI 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--max-m` | 60 | 勾股数生成参数上限（越大覆盖越多三元组） |
| `--max-k-num` | 300 | 比例因子 k=a/b 的分子上限 |
| `--max-k-den` | 150 | 比例因子 k 的分母上限 |
| `--min-rational` | 3 | 至少几个有理距离才报告（3 或 4） |
| `--brute-den` | 0 | 同时做暴力枚举，分母上限（0=跳过） |
| `--workers` | 0 | 进程数（0=自动按 CPU 核数） |
| `--out` | — | 结果写入 JSON 文件路径 |
| `--top` | 50 | 打印前 N 行（0=全部） |

---

## 速度优化

三层叠加，相比朴素 Fraction 实现提升约 **200×**：

| 优化 | 原理 | 效果 |
|------|------|------|
| 整数 isqrt 替代 Fraction | 距离平方的分子可化为纯整数完全平方判断 | **~20×** |
| 预建互素对列表 | 工作进程初始化时一次性算好所有 gcd=1 的 (a,b) 对 | **~2×** |
| 多进程 ProcessPoolExecutor | 每个三元组独立，按 CPU 核数并行 | **~核数×** |

---

## 当前结果

最近搜索（`max_m=80, max_k=600/300`，287M 组合，约 21s）：

- **402 个**三顶点有理距离解
- **0 个**四顶点解

与 Harborth 猜想一致，但尚不能排除存在更大参数范围内的解。

---

## 代码模块说明

### `math_utils.py`
- `rational_sqrt(f)` — 若 Fraction f 是完全有理平方则返回其平方根，否则 None
- `primitive_pythagorean_triples(max_m)` — 生成参数 ≤ max_m 的所有本原勾股数三元组（含两种方向）
- `scale_triple(a, b, c, k)` — 用有理数 k 缩放三元组

### `square.py`
- `RationalPoint` — 冻结 dataclass，存储 (x,y) 和四个距离（irrational 用 None 表示）
- `compute_distances(x, y)` — 计算到四顶点的距离，返回 4 元组
- `make_point(x, y)` — 构造 RationalPoint 便捷函数

### `search.py`
- `parametric_search_fast(...)` — **推荐**：整数运算 + 多进程，带进度条
- `parametric_search(...)` — Fraction 生成器（慢，兼容备用）
- `brute_force_search(...)` — 暴力枚举有理点（小范围验证用）
- `merge_results(*iterables)` — 合并多路搜索结果并去重

---

## 后续方向

- **更大范围搜索**：`--max-m 150 --max-k-num 2000` 等
- **其他顶点锚定**：当前以 A 为锚，通过三元组方向互换已覆盖 B/D；可验证 C 锚情况
- **解析法**：对固定三元组，将"d(D) 也有理"化为椭圆曲线方程，可能得到无穷参数族
- **四顶点专项**：利用三顶点解的代数结构加额外约束，针对性缩小搜索
