# wl106 — D4 点图与中心线分支

日期：2026-06-07

承接 wl105。本轮做两件事：

1. 把 closure-first `3/4` near-miss 还原到正方形坐标系，画出 `480` 个 D4 代表点。
2. 查 `A=B` / `N1=N2` 中心线分支，确认它可以走理论路线，不需要先扩大实验。

---

## 1. D4 点图

输入：

```text
max_leg=100000
diff_tail=250000
raw 3/4 near-miss records: 41,736
same coordinate points: 857
D4 point orbits: 480
4/4 hits: 0
```

脚本：

```text
scripts/theory/closure_first_three_square_search.py
scripts/theory/plot_closure_first_d4_points.py
```

结果图：

```text
results/counterexample_first/2026-06-07/closure_first_3of4_d4_points_max100000_tail250000.png
```

图的读法：

```text
每个点 = 一个 D4-canonical 坐标代表
点大小 = 这个 D4 轨道合并掉多少 raw near-miss
颜色 = 这个轨道里最小 failed nearest-square delta
红圈 = delta <= 10
```

肉眼结论：

```text
480 个 D4 代表点里，84 个落在单位正方形内部。
大部分点集中在正方形左下的 canonical 基本区域。
小 delta 点不是均匀散开，而是落在几条带状/边界附近。
没有看到足够清楚的几何规律，不能靠看图继续推进。
```

所以图的用途不是直接给证明，而是提醒下一步别继续“凭眼睛找规律”。更有用的切法是：

```text
按 raw_count 拆高重复家族。
按小 delta 拆最靠近平方的失败边。
```

---

## 2. 中心线分支怎么翻译

`A=B` 是中心竖线。交换横纵轴后，它等价于中心横线：

```text
N1 = N2 = n
```

此时四个角距离只剩两种勾股条件：

```text
a^2 + n^2 = square
b^2 + n^2 = square
```

闭合条件分两支：

```text
inside:   a + b = 2n
outside: |a - b| = 2n
```

所以用户说的“找多 n pair，n >= 1，取其中一个 n，查 a+b=2n”是对的，但要补两个口径：

```text
不需要旧 strict multi-N 的 >=2，一个公共 n 就够。
如果允许点在正方形外，也要查 |a-b|=2n。
```

---

## 3. 已知 theorem

找到一篇直接相关的论文：

```text
Yang Ji, "Several special cases of a square problem", arXiv:2105.05250
https://arxiv.org/abs/2105.05250
```

文中 Theorem 2 证明：

```text
On the midline of a unit square, no point has four rational distances to the vertices.
```

作者还在 Remark 1 说明，这些定理不要求点在正方形内部，可以推广到整个平面。

这正好覆盖本分支：

```text
N1=N2 center horizontal line
A=B center vertical line by D4 axis swap
inside and outside center-line closures
```

论文证明路线：

1. 假设中心线反例存在。
2. 清分母成整数正方形。
3. 用勾股参数化，把问题化成整数方程：

```text
(a^2 + b^2)^2 + (2ab)^2 = e^2
```

4. 用 Fermat 无限递降说明该方程没有正整数解。

这不是 Harborth 全问题证明，只关闭中心线低维分支。

---

## 4. 当前判断

中心线分支可以先标记为理论关闭：

```text
status: closed by known midline theorem, pending local proof rewrite
```

如果要放进项目正式理论框架，不建议只引用论文一句话。更稳的做法是写一个短 proof note：

```text
center-line-impossibility.md
```

里面把 Theorem 2 翻译成当前变量，并补完整无限递降步骤。这样以后审查时不用依赖论文里较压缩的推导。

实验路线仍可做 sanity check：

```text
按 n 建 legs_by_n
查 leg1+leg2=2n
查 |leg1-leg2|=2n
```

但这已经不是最高优先级。下一步更值得做：

```text
拆 480 个 D4 点中的高 raw_count 家族。
拆 delta <= 10，尤其唯一 delta=1 样本。
```

---

## 5. 验证

```text
uv run pytest -q
346 passed, 2 warnings
```

两个 warning 是既有的 `pytest.mark.slow` 未注册。
