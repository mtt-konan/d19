# wl180 — `R_lambda` root-grid residual generator

日期：2026-06-09

## 1. 本轮目标

wl179 说：

```text
小高度 lambda 池没有扫到 residual，
但已知 lambda=535/161 的 residual 高度超过 20。
```

所以本轮换一个视角：

```text
不要先枚举 lambda。
先枚举两个闭合根 r,s，
再由 sum=A+B 反推 lambda = r+s-1。
```

普通话说：

```text
以前是先定长宽比，再找点。
现在是先找两个候选点，再看它们会逼出什么长宽比。
```

---

## 2. 新 helper

新增：

```text
sum_ab_product_square_residuals_from_root_grid(
    max_numerator,
    max_denominator,
)
```

它做的事：

```text
1. 枚举正有理 r,s。
2. 令 lambda = r+s-1。
3. 要求 lambda > 0。
4. 调 closure_product_square_conditions。
5. 只保留 product_square_bucket == residual。
```

这里的 residual 仍然只是：

```text
过了 product-square 必要条件，
但不是 centerline，
也不是 reciprocal。
```

它不是反例。

---

## 3. 已知 guard 可自动找回

测试覆盖：

```text
max_numerator = 26
max_denominator = 23
```

能找回：

```text
lambda = 535/161
r = 14/23
s = 26/7
member_squareclass_pair = (29,29)
true_member_pair = False
```

普通话说：

```text
这个 residual 现在不需要手写 lambda 才能出现。
它可以从 r,s 网格自然长出来。
```

---

## 4. 小探针

本轮跑了：

```text
sum_ab_product_square_residuals_from_root_grid(26, 23)
```

结果：

```text
residual_count = 1
true_count = 0
```

唯一项就是：

```text
lambda = 535/161
roots = (14/23, 26/7)
pair = (29,29)
true = False
```

可以说：

```text
在这个很小的 root-grid 边界里，
只看到了已知 residual，
而且它不是真点。
```

不能说：

```text
residual 只有这一个。
residual 永远不是真点。
有理比例主定理已经证明。
```

---

## 5. 对主方向的意义

主目标是：

```text
若 r,s ∈ R_lambda 且 full-plane closure，
是否必须 s = lambda/r？
```

这轮没有证明它。

但它把危险区分得更清楚：

```text
product-square 层面的 residual 可以存在；
真正要证明的是 residual 不能同时让四个单项 squareclass 都变成 1。
```

普通话说：

```text
弱筛会放进假人。
下一步不是证明“假人不存在”，
而是证明“假人永远拿不到真身份证”。
```

---

## 6. 下一步

更值得走的是：

```text
1. 用 root-grid 生成更多 residual 形态。
2. 统计 member_squareclass_pair，尤其看是否总是非平凡。
3. 尝试把 residual 条件写成：
   r^2+1 与 s^2+1 同 squareclass，
   r^2+lambda^2 与 s^2+lambda^2 同 squareclass，
   但这两个 squareclass 无法同时为 1。
```

这比继续盲扫小高度 lambda 更贴近方程本身。

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_product_square_residuals_from_root_grid_finds_known_residual -q
```

结果：

```text
1 passed
```

后续还需要跑：

```text
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```
