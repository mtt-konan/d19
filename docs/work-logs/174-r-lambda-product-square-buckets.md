# wl174 — `R_lambda` product-square buckets

日期：2026-06-09

## 1. 本轮目标

wl173 修正了边界：

```text
有理 lambda 下，product-square residual 真实存在。
```

所以不能再问：

```text
product-square 是否只来自 centerline 或 reciprocal？
```

本轮改成更安全的问题：

```text
把 product-square hit 分桶，
然后问 residual 桶里有没有 true R_lambda member pair。
```

普通话说：

```text
第三桶删不掉。
那就看第三桶里有没有真货。
```

---

## 2. 新字段

`closure_product_square_conditions(...)` 新增：

```text
product_square_bucket
```

取值：

```text
none        : 不是 product-square hit，或没有两个正有理根
centerline  : r=s
reciprocal  : rs=lambda
residual    : 非 centerline、非 reciprocal，但 product-square 通过
```

普通话说：

```text
让工具直接告诉我们这个点属于哪个桶。
```

---

## 3. 三个桶样本

### centerline

```text
lambda = 2
roots = (3/2, 3/2)
product_square_bucket = centerline
true_member_pair = False
```

### reciprocal

```text
lambda = 7
roots = (1, 7)
product_square_bucket = reciprocal
true_member_pair = False
```

### residual

```text
lambda = 535/161
roots = (14/23, 26/7)
product_square_bucket = residual
true_member_pair = False
```

普通话说：

```text
这三个样本都能让 product-square 通过，
但目前都不是真 R_lambda 成员对。
```

---

## 4. 小扫描

扫描内容：

```text
整数 lambda=1..15 的有限池
+ 已知有理 residual guard
```

结果：

```text
bucket_counts
centerline     230
reciprocal      40
known:residual   1
```

true member 统计：

```text
('centerline', False)       230
('reciprocal', False)        40
('known:residual', False)     1
```

可以说：

```text
这些诊断样本里，没有 true_member_pair。
```

不能说：

```text
已经证明 residual 桶没有真点。
```

---

## 5. 路线修正

之前一度想证明：

```text
product-square + closure
=> centerline or reciprocal
```

这在一般有理 lambda 下不对，因为 residual 样本存在。

更准确的主线应该是：

```text
product-square + closure + true_member_pair
=> reciprocal
```

或者分桶说：

```text
centerline 桶没有 true_member_pair；
residual 桶没有 true_member_pair；
剩下只能是 reciprocal。
```

普通话总结：

```text
现在不是证明第三桶不存在，
而是证明第三桶没有真点。
```

---

## 6. 下一步

下一步值得做：

```text
扫描 residual bucket 中的 member_squareclass_pair，
专门找 true_member_pair 或接近 true 的样本。
```

如果仍然没有真点，尝试提炼：

```text
residual 桶为什么会强迫共同非 1 squareclass？
```

已知 residual guard：

```text
member_squareclass_pair = (29,29)
member_square_flags = (False,False,False,False)
```

这提示 residual 的失败机制可能是：

```text
四项同一个非平凡 squareclass。
```

但这仍需更多样本，不可直接当定理。

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
