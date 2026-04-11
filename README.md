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

# 椭圆曲线引导搜索
uv run python scripts/search.py ec --max-m 30 --max-k-num 400 --max-k-den 800

# 查看所有参数
uv run python scripts/search.py parametric --help
uv run python scripts/search.py ec --help
```

**当前结果**（`parametric --scale 400 --inside`）：37 个 D4 等价类，0 个四顶点解。

---

## 文档

| 文档 | 内容 |
|------|------|
| [docs/MATH.md](docs/MATH.md) | 数学：参数化推导、距离公式、侧边定理、D4对称群 |
| [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) | 实现：模块结构、搜索策略、向量化、溢出处理、GPU、EC搜索 |
| [docs/work-logs/](docs/work-logs/) | 各版本工作日志（不可修改） |
