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

# 推荐：用 --scale 统一控制搜索规模
uv run python scripts/search_3vertex.py --scale 80   # ~300M 组合，~3s

# 关闭 D4 对称去重，看所有对称像
uv run python scripts/search_3vertex.py --scale 80 --no-dedup-symmetry

# 专门找四顶点解
uv run python scripts/search_3vertex.py --min-rational 4 --scale 120

# 结果保存到 JSON
uv run python scripts/search_3vertex.py --scale 80 --out my_results.json

# 手动控制三个参数（高级）
uv run python scripts/search_3vertex.py --max-m 80 --max-k-num 640 --max-k-den 320

# 查看所有选项
uv run python scripts/search_3vertex.py --help
```

### CLI 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--scale N` | — | 一键设置规模：`max_m=N, max_k_den=4N, max_k_num=8N` |
| `--max-m` | 60 | 勾股数生成参数上限（越大覆盖越多三元组） |
| `--max-k-num` | 300 | 比例因子 k=a/b 的分子上限 |
| `--max-k-den` | 150 | 比例因子 k 的分母上限 |
| `--min-rational` | 3 | 至少几个有理距离才报告（3 或 4） |
| `--no-dedup-symmetry` | — | 关闭 D4 对称去重，输出所有对称像 |
| `--brute-den` | 0 | 同时做暴力枚举，分母上限（0=跳过） |
| `--workers` | 0 | 进程数（0=自动按 CPU 核数） |
| `--out` | — | 结果写入 JSON 文件路径 |
| `--top` | 50 | 打印前 N 行（0=全部） |

---

## 速度优化

三层叠加，相比朴素 Fraction 实现提升约 **1400×**：

| 优化 | 原理 | 效果 |
|------|------|------|
| 整数 isqrt 替代 Fraction | 距离平方的分子可化为纯整数完全平方判断 | **~20×** |
| 预建互素对列表 | 工作进程初始化时一次性算好所有 gcd=1 的 (a,b) 对 | **~2×** |
| Numpy 向量化 | 每个三元组的所有 (a,b) 组合一次性用数组运算处理 | **~7×** |
| 多进程 ProcessPoolExecutor | 每个三元组独立，按 CPU 核数并行 | **~核数×** |

---

## 侧边排除

**定理（椭圆曲线证明）**：满足到单位正方形任意三个顶点距离均为有理数的点，不可能落在正方形的延伸边上（即 x=0, x=1, y=0, y=1 这四条直线）。

因此，搜索时**无论 `min_rational` 取 3 还是 4**，所有满足 x=1 或 y=1 的候选点均被自动跳过。这将有效解数从 402（含侧边）降至 118（纯非侧边解），结果更纯净。

---

## 当前结果

最近搜索（`--scale 80`，约 327M 组合，~3s）：

- **118 个**非侧边三顶点有理距离解（原始，含对称像）
- **37 个** D4 等价类（去掉对称重复后）
- **0 个**四顶点解

侧边上的 x=1/y=1 解（约 284 个）已按定理排除。与 Harborth 猜想一致，但尚不能排除存在更大参数范围内的解。

---

## 代码模块说明

### `math_utils.py`
- `rational_sqrt(f)` — 若 Fraction f 是完全有理平方则返回其平方根，否则 None
- `primitive_pythagorean_triples(max_m)` — 生成参数 ≤ max_m 的所有本原勾股数三元组（含两种方向）
- `scale_triple(a, b, c, k)` — 用有理数 k 缩放三元组

### `square.py`
- `RationalPoint` — 冻结 dataclass，存储 (x,y) 和四个距离（irrational 用 None 表示）
- `RationalPoint.denominator` — lcm(x.den, y.den)，衡量点的"复杂度"
- `compute_distances(x, y)` — 计算到四顶点的距离，返回 4 元组
- `make_point(x, y)` — 构造 RationalPoint 便捷函数
- `d4_images(x, y)` — 单位正方形的 D4 对称群（8 个变换）下点的所有像
- `canonical_xy(x, y)` — 取 D4 轨道中字典序最小的像，作为轨道代表元

### `search.py`
- `parametric_search_fast(...)` — **推荐**：整数运算 + numpy 向量化 + 多进程，带进度条
- `parametric_search(...)` — Fraction 生成器（慢，兼容备用）
- `brute_force_search(...)` — 暴力枚举有理点（小范围验证用）
- `merge_results(*iterables)` — 合并多路搜索结果并去重
- `dedup_by_symmetry(points)` — 按 D4 等价类去重，每轨道保留 rational_count 最高、分母最小的代表

---

## 后续方向

- **更大范围搜索**：`--scale 150`、`--scale 300`（64GB RAM 机器上可轻松运行）
- **其他顶点锚定**：当前以 A 为锚，通过三元组方向互换已覆盖 B/D；可验证 C 锚情况
- **解析法**：对固定三元组，将"d(D) 也有理"化为椭圆曲线方程，可能得到无穷参数族
- **四顶点专项**：利用三顶点解的代数结构加额外约束，针对性缩小搜索

详细实现说明见 [docs/DESIGN.md](docs/DESIGN.md)。
