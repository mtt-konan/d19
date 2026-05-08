# Rational Distance to Unit Square Vertices

> **平面内是否存在一点，到单位正方形四个顶点的距离均为有理数？**（Harborth 猜想，至今未解）

本项目现在主要沿两条线理解最清楚：

- `concordant`：当前主线。固定 `(A,B)`，研究共同腿 `N` 的数论结构。
- `chain-fast`：当前基线。直接做四顶点正方形主问题的可信搜索与对照。

`parametric` / `ec` / `chain` 继续保留，但目前更像研究工具和背景路线，不是当前主战场。

---

## 安装与快速上手

需要 [uv](https://github.com/astral-sh/uv)：

```bash
uv sync

# 当前建议先看这两条
uv run python scripts/search.py concordant --pair 264,420
uv run python scripts/search.py concordant --max-hyp 100 --ec-bound 100000
uv run python scripts/search.py chain-fast --max-hyp 200 --no-progress
uv run python scripts/search.py chain-fast --max-hyp 1000 --profile --no-progress

# 保留的三顶点 / 背景路线
uv run python scripts/search.py parametric --scale 80
uv run python scripts/search.py ec --max-m 30 --max-k-num 400 --max-k-den 800
uv run python scripts/search.py chain --max-val 500 --require-square

# 辅助分析与可视化脚本
uv run python scripts/search.py ec --max-m 30 --max-k-num 400 --max-k-den 800 --db .cache/rational_distance.sqlite3
uv run python scripts/analyze_ec_db.py --db .cache/rational_distance.sqlite3 --run latest
uv run python scripts/analyze_ec_db.py --db .cache/rational_distance.sqlite3 --run latest --triple 8,15,17 --html triple_8_15_17.html
uv run python scripts/visualize.py results.json --out report.html

# 查看所有参数
uv run python scripts/search.py --help
uv run python scripts/search.py chain-fast --help
uv run python scripts/search.py concordant --help

# 对照 CPU 和加速后端是否一致
uv run python scripts/compare_parametric.py --scale 20 --backend torch
uv run python scripts/compare_parametric.py --scale 20 --backend numpy  # 本机 CPU 验证

# 代码质量检查
uv run ruff check .
uv run ruff format .
```

截至目前，项目仍未找到四顶点正方形解。`EC` 数据库模式只在显式传入 `--db` 时启用；`visualize.py` 继续保留为读取 JSON 并输出 HTML 的辅助工具。

---

## 文档

如果你只想快速搞清楚“现在到底主线是哪条、代码从哪看、别把路线混了”，先读 [docs/DIRECTIONS.md](docs/DIRECTIONS.md)。

| 文档 | 内容 |
|------|------|
| [docs/DIRECTIONS.md](docs/DIRECTIONS.md) | 项目方向总地图：当前主线、基线、暂停路线，以及每条线对应的代码、测试、脚本和入口 |
| [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) | 项目当前主线、基线、暂停路线，以及现在真正的瓶颈 |
| [docs/SEARCH_METHODS.md](docs/SEARCH_METHODS.md) | 5 个子命令分别做什么，只讲方法，不负责判断当前优先级 |
| [docs/CURRENT_FINDINGS.md](docs/CURRENT_FINDINGS.md) | 当前已经基本确认的工程和数学结论，优先看高置信结论 |
| [docs/CHAIN_PERFORMANCE.md](docs/CHAIN_PERFORMANCE.md) | `chain` 默认路线的实测耗时记录：时间拆分、增长趋势，以及当前主要瓶颈 |
| [docs/CHAIN_FAST_PERFORMANCE.md](docs/CHAIN_FAST_PERFORMANCE.md) | `chain-fast` 的 profile、并行实测和当前瓶颈判断 |
| [docs/CHAIN_FAST_MOD_SIEVE.md](docs/CHAIN_FAST_MOD_SIEVE.md) | `chain-fast` 的 `mod` 预筛实验：筛掉了多少、为什么目前还没更快 |
| [docs/CHAIN_FAST_SAFE_FILTERS.md](docs/CHAIN_FAST_SAFE_FILTERS.md) | `chain-fast` 的安全前筛：哪些条件已证明安全、为什么当前还没更快 |
| [docs/CHAIN_FAST_BUCKET_STATS.md](docs/CHAIN_FAST_BUCKET_STATS.md) | `chain-fast` 的结构桶统计：为什么先采证据、SQLite 里到底多了什么 |
| [docs/CHAIN_FAST_STRUCTURE_FINDINGS.md](docs/CHAIN_FAST_STRUCTURE_FINDINGS.md) | `chain-fast` 结构统计首轮结论：`10w` 上已经看出的稳定信号和工程边界 |
| [docs/CHAIN_FAST_OPTIMIZATION.md](docs/CHAIN_FAST_OPTIMIZATION.md) | `chain-fast` 当前到底慢在哪、数据库解决什么、后续更该优先做什么 |
| [docs/MATH.md](docs/MATH.md) | 数学总库：参数化推导、chain 化简、concordant 椭圆曲线等推导 |
| [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) | 工程结构参考：代码分区、实现入口、兼容层现状 |
| [docs/work-logs/](docs/work-logs/) | 各版本工作日志（不可修改） |

当前建议的阅读顺序是：

1. [docs/DIRECTIONS.md](docs/DIRECTIONS.md)
2. [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)
3. [docs/SEARCH_METHODS.md](docs/SEARCH_METHODS.md)
4. [docs/CURRENT_FINDINGS.md](docs/CURRENT_FINDINGS.md)
