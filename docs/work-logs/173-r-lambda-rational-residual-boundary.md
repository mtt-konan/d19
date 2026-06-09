# wl173 — `R_lambda` rational residual boundary

日期：2026-06-09

## 1. 本轮修正

wl172 记录了一个有限扫描：

```text
lambda = 1..15 整数
small rational r
sum=A+B
```

结果是：

```text
centerline + reciprocal 吃掉了所有 product-square hit
residual = 0
```

这个结论只对那个有限整数池成立。

本轮必须补一条边界：

```text
一般有理 lambda 下，已知存在非 centerline、非 reciprocal 的 product-square residual。
```

普通话说：

```text
整数小池很干净，
不代表有理世界也干净。
这里不能说过头。
```

---

## 2. 已知残差样本

样本：

```text
lambda = 535/161
r = 14/23
s = 26/7
```

它满足：

```text
r+s = lambda + 1
p = rs != lambda
r != s
D 是平方
A_p 是平方
B_p 是平方
```

在 helper 里：

```text
centerline = False
reciprocal_pair = False
product_terms_are_squares = True
true_member_pair = False
member_squareclasses = (29, 29, 29, 29)
member_squareclass_pair = (29, 29)
```

普通话说：

```text
它不是中心线，
也不是 reciprocal 镜像，
但乘积平方层面仍然能过。
这就是第三桶。
```

---

## 3. 为什么它不反驳主猜想

它不是：

```text
true_member_pair
```

也就是说：

```text
r 不在 R_lambda
s 不在 R_lambda
```

四个真实单项都不是平方：

```text
member_square_flags = (False, False, False, False)
```

所以它不能反驳：

```text
若 r,s in R_lambda 且 closure，则是否 reciprocal？
```

普通话说：

```text
它是 product-square 假点，
不是 R_lambda 真点。
```

---

## 4. 对 wl172 的更正

wl172 可以保留的说法：

```text
在 lambda=1..15 的整数有限池里，
centerline + reciprocal 吃掉了所有 product-square hit。
```

wl172 不能推广成：

```text
所有有理 lambda 下，
product-square hit 都只有 centerline 或 reciprocal。
```

更准确的下一步是：

```text
整数 lambda 和一般有理 lambda 要分开看。
```

普通话说：

```text
整数世界可能比较干净；
有理世界会长出第三类假象。
```

---

## 5. 新断言

测试里对这个样本补了明确断言：

```text
not conditions.centerline
not conditions.reciprocal_pair
conditions.product_terms_are_squares
not conditions.true_member_pair
```

这条断言的作用是：

```text
防止后续 agent 把 residual 当成已经消失。
```

---

## 6. 下一步

下一步不应该马上证明：

```text
product-square => centerline or reciprocal
```

因为这在有理 lambda 下已经被 residual 样本否掉。

更合理的问题是：

```text
product-square residual 虽然存在，
但是否永远不是真 R_lambda member pair？
```

换句话说：

```text
第三桶存在，
但第三桶里有没有真点？
```

普通话总结：

```text
主线没有死，
只是命题要改准：
不能排除所有第三桶；
要排除第三桶里的真 R_lambda 点。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_product_square_conditions_do_not_imply_membership -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```

结果：

```text
1 passed
31 passed
395 passed, 2 warnings
```
