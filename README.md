# Rational Distance to Unit Square Vertices

> **平面内是否存在一点，到单位正方形四个顶点的距离均为有理数？**（Harborth 猜想，至今未解）

本项目通过穷举三顶点有理距离解来逐步缩小搜索范围，同时捎带检查第四距离。

---

## 安装与运行

需要 [uv](https://github.com/astral-sh/uv)：

```bash
uv sync
uv run python scripts/search_3vertex.py --scale 80   # ~300M 组合，约 3s
uv run python scripts/search_3vertex.py --help       # 查看所有参数
```

**当前结果**（`--scale 80`）：37 个 D4 等价类（118 个原始解），0 个四顶点解。

---

## 文档

| 文档 | 内容 |
|------|------|
| [docs/MATH.md](docs/MATH.md) | 数学：参数化推导、距离公式、侧边定理、D4对称群 |
| [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) | 实现：模块结构、搜索策略、向量化、溢出处理、GPU |
| [docs/work-logs/](docs/work-logs/) | 各版本工作日志（不可修改） |
