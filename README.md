# Rational Distance to Unit Square Vertices

> **平面内是否存在一点，到单位正方形四个顶点的距离均为有理数？**（Harborth 猜想，至今未解）

研究取向是寻找能统一控制一类情形的结构性理由。数学成果以 [项目状态](docs/PROJECT_STATUS.md) 为准；[当前上下文](docs/codex/current-context.md) 保存最近记录的研究任务入口，具体状态、范围和下一步由对应任务锚点维护。本轮工作由用户当前请求决定。

已有工具继续保留，但不是自动执行的研究清单：

- `concordant`：固定 `(A,B)`，研究共同腿 `N` 的数论结构。
- `chain-fast`：四顶点问题的有限搜索与对照工具。
- `parametric` / `ec` / `chain`：参数化、椭圆曲线和历史研究工具。

旧路线的成果、缺口和失效机制见 [研究路线归档](docs/archive/RESEARCH_ROUTES.md)。历史记录中的“下一步”不再自动决定新会话的任务。

---

## 安装与快速上手

需要 [uv](https://github.com/astral-sh/uv)：

```bash
uv sync

# 已明确选择有限计算任务时，可参考以下命令
uv run python scripts/search.py concordant --pair 264,420
uv run python scripts/search.py concordant --max-hyp 100 --ec-bound 100000
uv run python scripts/search.py chain-fast --max-hyp 200 --no-progress
uv run python scripts/search.py chain-fast --max-hyp 1000 --profile --no-progress

# 固定 pair 的累积判定：写入 SQLite，跳过已 terminal 的记录；不是全局排除
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

# 需要全仓验证时的代码质量检查
uv run ruff check .
uv run ruff format --check .
```

代码修改优先检查受影响的测试和 Python 路径；只有明确需要全仓验证时
才运行上面的全仓命令。文档修改使用链接、范围和差异检查，不启动研究计算。

截至目前，项目仍未找到四顶点正方形解。`EC` 数据库模式只在显式传入 `--db` 时启用；`visualize.py` 继续保留为读取 JSON 并输出 HTML 的辅助工具。

---

## 文档

先区分“已经证明什么”和“本次准备研究什么”，不要从历史编号推定下一步。

| 文档 | 内容 |
|------|------|
| [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) | 已接受的数学成果与尚未证明的结论 |
| [docs/codex/current-context.md](docs/codex/current-context.md) | 最近记录的研究任务入口；具体状态见任务锚点 |
| [docs/NEXT_RESEARCH_GATE.md](docs/NEXT_RESEARCH_GATE.md) | 新任务的选择边界；不默认续跑旧路线 |
| [docs/OPEN_DIRECTIONS.md](docs/OPEN_DIRECTIONS.md) | 研究取向和进展判据，不是优先级任务队列 |
| [docs/archive/RESEARCH_ROUTES.md](docs/archive/RESEARCH_ROUTES.md) | 旧路线的已证成果、缺口、停止原因和恢复条件 |
| [docs/CLOSURE_QUOTIENT_MAINLINE.md](docs/CLOSURE_QUOTIENT_MAINLINE.md) | 按需查阅的 closure quotient / Selmer 架构 |
| [docs/MATH.md](docs/MATH.md) | 数学总库：参数化推导、chain 化简、concordant 椭圆曲线等推导 |
| [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) | 工程结构参考：代码分区、实现入口、兼容层现状 |
| [AGENTS.md](AGENTS.md) | agent 接手规则、禁止过度声称、测试和 worklog 约定 |
| [docs/archive/](docs/archive/) | 历史文档与实验记录（参考用，不是当前主线） |
| [docs/work-logs/](docs/work-logs/) | 各版本工作日志（不可修改） |

按任务选择所需文档，入口见 [AGENTS.md 的按需读取表](AGENTS.md#read-for-the-task)。局部代码或文档修改不要求先恢复研究上下文；最近记录的研究任务不会自动成为本轮任务。
