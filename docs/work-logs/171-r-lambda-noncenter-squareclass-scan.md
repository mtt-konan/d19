# wl171 — `R_lambda` non-center squareclass scan

日期：2026-06-09

## 1. 本轮目标

wl170 建议：

```text
先剔除 r=s 中心线样本，
再看非中心线的 (u,v) 模式。
```

本轮先加一个小字段：

```text
centerline
```

然后做有限诊断。

普通话说：

```text
先把最吵的中心线假象拿掉，
看看剩下的假象还长什么样。
```

---

## 2. 新字段

`closure_product_square_conditions(...)` 新增：

```text
centerline
```

含义：

```text
roots = (r,s) 且 r=s
```

这样扫描时可以直接过滤：

```text
if not conditions.centerline:
    ...
```

---

## 3. 小扫描

有限诊断：

```text
lambda = 1..15
relation = sum=A+B
target = lambda + 1
r = small rational with denominator <= 20
s = target - r
只保留 D square 且 A_p,B_p square 的点
```

结果：

```text
total hits     = 270
center hits    = 230
noncenter hits = 40
```

剔除中心线后：

```text
noncenter top:
(u,v) = (2,2), count = 40
```

典型例子：

```text
lambda = 7
roots = (1, 7)
p = 7
member_squareclasses = (2, 2, 2, 2)
```

普通话说：

```text
中心线拿掉后，
这个小池里剩下的最明显假象是 (1,lambda) 这种 reciprocal orbit。
```

---

## 4. 为什么 `(1,lambda)` 会出现

对：

```text
r = 1
s = lambda
```

有：

```text
r+s = lambda + 1
p = rs = lambda
```

所以这是 reciprocal pair：

```text
s = lambda/r
```

但它未必是真 `R_lambda` 成员。

例如：

```text
lambda = 7
r = 1
s = 7
```

四个单项：

```text
1^2 + 1   = 2
7^2 + 1   = 50
1^2 + 7^2 = 50
7^2 + 7^2 = 98
```

squareclass 都是：

```text
2
```

所以：

```text
member_squareclass_pair = (2,2)
```

但没有一项是平方。

普通话说：

```text
它是镜像闭合点，
但不是有理距离真点。
```

---

## 5. 当前判断

可以说：

```text
在这个有限池里，product-square 假象主要分成两类：
1. centerline: r=s
2. reciprocal-like: r=1, s=lambda
```

不能说：

```text
所有非中心线假象都只有 reciprocal orbit。
有限扫描证明了 R_lambda theorem。
```

普通话说：

```text
这不是证明，
但它把噪声分类得更干净了。
```

---

## 6. 下一步

自然下一步：

```text
给 closure_product_square_conditions 增加 reciprocal_pair 标记。
```

这样就可以扫描：

```text
非 centerline
非 reciprocal
但仍 product-square 的 (u,v)
```

如果这类还很多，就继续分类。

如果这类很少或为空，再回代数证明：

```text
product-square 假象是否基本由 centerline + reciprocal orbit 解释？
```

普通话总结：

```text
我们正在做的不是暴力证明，
而是给假象分桶。
桶分清楚以后，证明才可能有抓手。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_product_square_conditions_do_not_imply_membership -q
uv run pytest tests/test_rational_ratio.py::test_sum_ab_centerline_squareclass_conditions_explain_midpoint_hits -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```

结果：

```text
1 passed
1 passed
31 passed
395 passed, 2 warnings
```
