# wl196 — `R_lambda` centerline quartic self-similarity

日期：2026-06-09

## 1. 本轮目标

wl190 把中心线真点问题化成：

```text
Y^2 = Q(t)
Q(t)=t^4+8t^3+18t^2-8t+1
```

wl195 说明：

```text
继续堆模数筛不会自动变成证明。
```

本轮换方向：

```text
先看 Q(t) 自己有没有递降/曲线结构。
```

普通话说：

```text
不再只问“模 p 能不能筛掉它”，
而是问“如果它真的有解，会不会自己生出一个更小的同类解”。
```

---

## 2. 新 helper

新增：

```text
sum_ab_centerline_quartic_self_similarity(parameter)
```

返回：

```text
SumAbCenterlineQuarticSelfSimilarity
```

记录：

```text
parameter
quartic_value
first_square_term
second_square_term
quadratic_coefficients
quadratic_discriminant
has_rational_lift
lift_roots
```

---

## 3. 关键恒等式

四次式可以写成：

```text
Q(q) = (q^2 + 4q - 1)^2 + (2q)^2
```

也就是说：

```text
Q(q) 是平方
```

等价于：

```text
(q^2 + 4q - 1)^2 + (2q)^2 是平方
```

普通话说：

```text
中心线剩下的条件本身又是一个勾股条件。
```

---

## 4. 自相似入口

若：

```text
Y^2 = Q(q)
```

则二次方程：

```text
q t^2 + (q^2 + 4q - 1)t - q = 0
```

的判别式是：

```text
(q^2 + 4q - 1)^2 + 4q^2 = Q(q)
```

所以如果 `Q(q)` 是有理平方，这个二次方程有有理根。

普通话说：

```text
一个 q 解，会给出 t 解。
而判别式又是同一个 Q(q)。
```

这就是“自相似”的意思：

```text
同一条四次曲线又从二次参数里冒出来。
```

---

## 5. 样本

输入：

```text
q = 3/5
```

得到：

```text
Q(q) = 2836/625
q^2 + 4q - 1 = 44/25
2q = 6/5
Q(q) = (44/25)^2 + (6/5)^2
```

对应二次方程：

```text
(3/5)t^2 + (44/25)t - 3/5 = 0
```

判别式：

```text
2836/625
```

这个数不是有理平方，所以：

```text
has_rational_lift = False
```

基点：

```text
q = 0
Q(q) = 1
lift_roots = (0)
```

---

## 6. PARI 小探针

跑了：

```text
hyperellratpoints(x^4+8*x^3+18*x^2-8*x+1, h)
```

结果：

```text
h=100       -> [0, 1], [0, -1]
h=10000     -> [0, 1], [0, -1]
h=1000000   -> [0, 1], [0, -1]
```

普通话说：

```text
小高度里只看到显然点。
```

但这只是诊断。

不能说：

```text
已经证明只有显然点。
```

---

## 7. 可以说 / 不能说

可以说：

```text
centerline quartic 有一个明确的自相似二次账本。
Q(q) 是平方时，q t^2 + (q^2+4q-1)t - q = 0 有有理根。
这给无限递降证明提供了一个可能入口。
```

不能说：

```text
centerline 已经证明无解。
自相似自动推出递降。
PARI height 1e6 搜索能替代证明。
```

因为还缺最关键一步：

```text
证明从 q 到 t 会严格降低某个高度，
或者证明这条四次曲线的有理点只有 (0,±1)。
```

---

## 8. 下一步

最值得继续的是：

```text
1. 研究二次根 t = (-(q^2+4q-1) ± Y)/(2q) 的高度变化。
2. 尝试证明若 0<q<1 且 Q(q) 是平方，则可得到更小正有理解。
3. 若高度不单调，把 Y^2=Q(t) 显式变成 Weierstrass 椭圆曲线，再用 rank/torsion 工具列点。
```

和 `A=kB` 的关系：

```text
这条中心线是固定比例路线的样板。
如果这里能做递降，
再看 A=kB 时能不能得到类似的“一个解生出更小解”的账本。
```

普通话总结：

```text
中心线现在不只是一个四次方程，
它有一个会把自己复制出来的结构。
这还不是证明，但已经比模筛更像证明入口。
```

---

## 9. 验证

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
