# Rational Distance to Unit Square Vertices

> **平面内是否存在一点，到单位正方形四个顶点的距离均为有理数？**（Harborth 猜想，至今未解）

本项目通过穷举三顶点有理距离解来逐步缩小搜索范围，同时捎带检查第四距离。

---

## 安装与运行

需要 [uv](https://github.com/astral-sh/uv)：

```bash
uv sync

# 参数化暴力搜索（GPU/CPU）
uv run python scripts/search.py parametric --scale 80
uv run python scripts/search.py parametric --scale 200 --backend torch  # AMD/NVIDIA GPU
uv run python scripts/search.py parametric --scale 80  --backend numpy  # CPU 多进程
uv run python scripts/search.py parametric --scale 80 --max-k-den 500   # 只覆盖一个参数，其余仍沿用 scale

# 椭圆曲线引导搜索
uv run python scripts/search.py ec --max-m 30 --max-k-num 400 --max-k-den 800
uv run python scripts/search.py ec --max-m 30 --max-k-num 400 --max-k-den 800 --db .cache/rational_distance.sqlite3
uv run python scripts/search.py ec --max-m 30 --max-k-num 400 --max-k-den 800 --db .cache/rational_distance.sqlite3 --resume

# 分析已持久化的 EC 结果
uv run python scripts/analyze_ec_db.py --db .cache/rational_distance.sqlite3 --run latest
uv run python scripts/analyze_ec_db.py --db .cache/rational_distance.sqlite3 --run latest --triple 8,15,17 --html triple_8_15_17.html

# 查看所有参数
uv run python scripts/search.py parametric --help
uv run python scripts/search.py ec --help

# 对照 CPU 和加速后端是否一致
uv run python scripts/compare_parametric.py --scale 20 --backend torch
uv run python scripts/compare_parametric.py --scale 20 --backend numpy  # 本机 CPU 验证

# 代码质量检查
uv run ruff check .
uv run ruff format .
```

**当前结果**（`parametric --scale 400 --inside`）：37 个 D4 等价类，0 个四顶点解。

`EC` 数据库模式只在显式传入 `--db` 时启用。默认搜索行为不变；数据库主要用于断点续跑、保存 `三元组 -> 种子 -> 曲线节点 -> 最终点` 的来源链，以及后续分析。

---

## 文档

如果你只想快速搞清楚“现在到底主线是哪条、代码从哪看、别把路线混了”，先读 [docs/DIRECTIONS.md](docs/DIRECTIONS.md)。

| 文档 | 内容 |
|------|------|
| [docs/DIRECTIONS.md](docs/DIRECTIONS.md) | 项目方向总地图：当前主线、基线、暂停路线，以及每条线对应的代码、测试、脚本、worklog 入口 |
| [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) | 项目当前主线、基线、暂停路线，以及现在真正的瓶颈 |
| [docs/SEARCH_METHODS.md](docs/SEARCH_METHODS.md) | 5 个子命令分别做什么，只讲方法，不负责判断当前优先级 |
| [docs/CURRENT_FINDINGS.md](docs/CURRENT_FINDINGS.md) | 当前已经基本确认的工程和数学结论，优先看高置信结论 |
| [docs/CHAIN_FAST_PERFORMANCE.md](docs/CHAIN_FAST_PERFORMANCE.md) | `chain-fast` 的 profile、并行实测和当前瓶颈判断 |
| [docs/CHAIN_FAST_MOD_SIEVE.md](docs/CHAIN_FAST_MOD_SIEVE.md) | `chain-fast` 的 `mod` 预筛实验：筛掉了多少、为什么目前还没更快 |
| [docs/CHAIN_FAST_SAFE_FILTERS.md](docs/CHAIN_FAST_SAFE_FILTERS.md) | `chain-fast` 的安全前筛：哪些条件已证明安全、为什么当前还没更快 |
| [docs/CHAIN_FAST_BUCKET_STATS.md](docs/CHAIN_FAST_BUCKET_STATS.md) | `chain-fast` 的结构桶统计：为什么先采证据、SQLite 里到底多了什么 |
| [docs/CHAIN_FAST_STRUCTURE_FINDINGS.md](docs/CHAIN_FAST_STRUCTURE_FINDINGS.md) | `chain-fast` 结构统计首轮结论：`10w` 上已经看出的稳定信号和工程边界 |
| [docs/CHAIN_FAST_OPTIMIZATION.md](docs/CHAIN_FAST_OPTIMIZATION.md) | `chain-fast` 当前到底慢在哪、数据库解决什么、后续更该优先做什么 |
| [docs/MATH.md](docs/MATH.md) | 数学总库：参数化推导、chain 化简、concordant 椭圆曲线等推导 |
| [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) | 工程结构参考：代码分区、兼容层原则、未来整理边界 |
| [docs/work-logs/](docs/work-logs/) | 各版本工作日志（不可修改） |

当前建议的阅读顺序是：

1. [docs/DIRECTIONS.md](docs/DIRECTIONS.md)
2. [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)
3. [docs/SEARCH_METHODS.md](docs/SEARCH_METHODS.md)
4. [docs/CURRENT_FINDINGS.md](docs/CURRENT_FINDINGS.md)
