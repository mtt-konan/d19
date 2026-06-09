# wl197 — centerline self-similarity negative-reciprocal guard

日期：2026-06-09

## 1. 本轮目标

wl196 发现中心线四次式有自相似入口：

```text
Q(q) = (q^2 + 4q - 1)^2 + (2q)^2
```

并且：

```text
q t^2 + (q^2+4q-1)t - q = 0
```

的判别式正好是：

```text
Q(q)
```

本轮检查一个危险问题：

```text
这个自相似能不能直接当成正有理解的无限递降？
```

结论：

```text
不能直接这么说。
```

---

## 2. 新增字段

扩展：

```text
SumAbCenterlineQuarticSelfSimilarity
```

新增：

```text
quadratic_root_sum
quadratic_root_product
roots_are_negative_reciprocals
direct_positive_descent_warning
```

普通话说：

```text
不只记录“判别式是 Q(q)”，
还记录二次根之间到底是什么关系。
```

---

## 3. 关键 guard

对：

```text
q t^2 + (q^2+4q-1)t - q = 0
```

若：

```text
q != 0
```

由韦达公式：

```text
t1 + t2 = -(q^2+4q-1)/q
t1 * t2 = -1
```

所以：

```text
t2 = -1/t1
```

普通话说：

```text
两个根不是“一大一小的正数”，
而是一正一负的负倒数对。
```

这会挡住一种天真的证明：

```text
有一个正解 q
推出一个更小正解 t
无限递降
```

这句话目前不能说。

---

## 4. 样本

输入：

```text
q = 3/5
```

二次方程：

```text
(3/5)t^2 + (44/25)t - 3/5 = 0
```

根和：

```text
-44/15
```

根积：

```text
-1
```

因此：

```text
roots_are_negative_reciprocals = True
direct_positive_descent_warning = "negative-reciprocal-roots"
```

退化基点：

```text
q = 0
```

记录为：

```text
quadratic_root_sum = None
quadratic_root_product = None
roots_are_negative_reciprocals = False
direct_positive_descent_warning = "degenerate-linear-root"
```

---

## 5. 可以说 / 不能说

可以说：

```text
centerline quartic 的自相似关系真实存在。
但 q != 0 时，它给出的两个根乘积恒为 -1。
所以直接正高度递降还没有成立。
```

不能说：

```text
wl196 已经给出无限递降证明。
从任意正有理解 q 可以直接生成更小正有理解。
```

因为：

```text
二次根天然跨到负倒数方向。
```

---

## 6. 下一步

这不等于自相似路线死了。

更正确的下一步是：

```text
1. 研究 t -> -1/t 是否对应中心线参数中的几何对称。
2. 看能否把负参数重新归一化回 0<t<1，同时严格降低高度。
3. 如果不能，转成 Weierstrass 椭圆曲线，直接列尽有理点。
```

普通话总结：

```text
这轮不是拿下证明，
而是拆掉一个容易误说的证明。
自相似还在，但递降必须多走一步符号/倒数归一化。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_centerline_remaining_quartic_matches_lambda_leg_value -q
```

结果：

```text
1 passed
```

后续还需要跑：

```text
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```
