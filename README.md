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

# 累积式证明无解（新）：每个 pair 的判定都进 SQLite，下次跑会跳过已 terminal 的
uv run python scripts/prove_no_solution.py --max-hyp 100 --db .cache/proofs.sqlite3
uv run python scripts/prove_no_solution.py --pair 264,420 --db .cache/proofs.sqlite3
uv run python scripts/prove_no_solution.py --db .cache/proofs.sqlite3 --report

# 保留的三顶点 / 背景路线
uv run python scripts/search.py parametric --scale 80
uv run python scripts/search.py ec --max-m 30 --max-k-num 400 --max-k-den 800
uv run python scripts/search.py chain --max-val 500 --require-square

# 辅助分析与可视化脚本
uv run python scripts/search.py ec --max-m 30 --max-k-num 400 --max-k-den 800 --db .cache/rational_distance.sqlite3
uv run python scripts/archive/analyze_ec_db.py --db .cache/rational_distance.sqlite3 --run latest
uv run python scripts/archive/analyze_ec_db.py --db .cache/rational_distance.sqlite3 --run latest --triple 8,15,17 --html triple_8_15_17.html
uv run python scripts/archive/visualize.py results.json --out report.html

# 查看所有参数
uv run python scripts/search.py --help
uv run python scripts/search.py chain-fast --help
uv run python scripts/search.py concordant --help

# 对照 CPU 和加速后端是否一致
uv run python scripts/archive/compare_parametric.py --scale 20 --backend torch
uv run python scripts/archive/compare_parametric.py --scale 20 --backend numpy  # 本机 CPU 验证

# 代码质量检查
uv run ruff check .
uv run ruff format .
```

截至目前，项目仍未找到四顶点正方形解。`EC` 数据库模式只在显式传入 `--db` 时启用；`visualize.py` 继续保留为读取 JSON 并输出 HTML 的辅助工具。

---

## 文档

如果你只想快速搞清楚“现在到底主线是哪条、下一步做什么”，先读 [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)。

| 文档 | 内容 |
|------|------|
| [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) | 当前主线、已经证明什么、还没证明什么 |
| [docs/NEXT_RESEARCH_GATE.md](docs/NEXT_RESEARCH_GATE.md) | 下一窄门：`wl521` 已完成 post-`wl519` support/cover-family synthesis；shell 11 只被选作后续有限壳，未执行 |
| [docs/OPEN_DIRECTIONS.md](docs/OPEN_DIRECTIONS.md) | 当前下一步和停止条件 |
| [docs/CLOSURE_QUOTIENT_MAINLINE.md](docs/CLOSURE_QUOTIENT_MAINLINE.md) | closure quotient / rank-zero Selmer 主线细账 |
| [docs/MATH.md](docs/MATH.md) | 数学总库：参数化推导、chain 化简、concordant 椭圆曲线等推导 |
| [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) | 工程结构参考：代码分区、实现入口、兼容层现状 |
| [AGENTS.md](AGENTS.md) | agent 接手规则、禁止过度声称、测试和 worklog 约定 |
| [docs/archive/](docs/archive/) | 历史文档与实验记录（参考用，不是当前主线） |
| [docs/work-logs/](docs/work-logs/) | 各版本工作日志（不可修改） |

当前建议的阅读顺序是：

1. [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)
2. [docs/NEXT_RESEARCH_GATE.md](docs/NEXT_RESEARCH_GATE.md)
3. [docs/OPEN_DIRECTIONS.md](docs/OPEN_DIRECTIONS.md)
4. [docs/CLOSURE_QUOTIENT_MAINLINE.md](docs/CLOSURE_QUOTIENT_MAINLINE.md)
5. [docs/MATH.md](docs/MATH.md)（需要数学细节时）
