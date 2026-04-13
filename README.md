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

| 文档 | 内容 |
|------|------|
| [docs/MATH.md](docs/MATH.md) | 数学：参数化推导、距离公式、侧边定理、D4对称群 |
| [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) | 实现：模块结构、搜索策略、向量化、溢出处理、GPU、EC搜索 |
| [docs/work-logs/](docs/work-logs/) | 各版本工作日志（不可修改） |
