# wl175 — `R_lambda` product-square bucket summary

日期：2026-06-09

## 1. 本轮目标

wl174 把 product-square hit 分成：

```text
centerline
reciprocal
residual
```

本轮把临时扫描变成正式 helper：

```text
sum_ab_product_square_bucket_summary(...)
```

普通话说：

```text
以后不用手写脚本数桶。
工具会直接告诉我们每个桶有多少，
以及哪个桶里有没有真 R_lambda 点。
```

---

## 2. 新 helper

新增：

```text
sum_ab_product_square_bucket_summary(
    lambda_ratios,
    max_denominator,
    extra_conditions=(),
)
```

它只做有限诊断：

```text
relation = sum=A+B
target = lambda + 1
r = numerator / denominator
s = target - r
denominator <= max_denominator
```

只记录：

```text
D 是平方
A_p,B_p 是平方
有两个正有理 roots
```

输出：

```text
bucket_counts
true_member_counts
examples_by_bucket
```

---

## 3. 为什么有 extra_conditions

wl173 的有理 residual guard：

```text
lambda = 535/161
roots = (14/23, 26/7)
```

不在简单整数 lambda 池里。

所以 helper 支持：

```text
extra_conditions=(residual_guard,)
```

普通话说：

```text
把已知危险样本钉进扫描，
防止整数小池看起来太干净。
```

---

## 4. 当前诊断结果

输入：

```text
lambda = 1..15
max_denominator = 20
extra_conditions = 已知 residual guard
```

输出：

```text
bucket_counts = {
  centerline: 230,
  reciprocal: 40,
  residual: 1,
}
```

真成员统计：

```text
true_member_counts = {}
```

代表样本：

```text
centerline:
  lambda = 1
  roots = (1,1)
  pair = (2,2)
  true = False

reciprocal:
  lambda = 7
  roots = (1,7)
  pair = (2,2)
  true = False

residual:
  lambda = 535/161
  roots = (14/23, 26/7)
  pair = (29,29)
  true = False
```

---

## 5. 能说和不能说

可以说：

```text
这个诊断池里三桶都有样本。
目前没有任何桶出现 true_member_pair。
```

不能说：

```text
已经证明 residual 桶没有真点。
已经证明 R_lambda theorem。
```

普通话说：

```text
这是搜索入口，
不是证明出口。
```

---

## 6. 下一步

下一步可以扩大但要有目的：

```text
1. 扩大 residual guard 来源，
   不是单纯扩大整数 lambda。

2. 专门统计 residual 桶的 member_squareclass_pair。

3. 找 residual 桶里是否存在：
   true_member_pair=True
```

如果仍没有真点，尝试证明：

```text
residual bucket => member_squareclass_pair 非 (1,1)
```

也就是：

```text
第三桶可以存在，
但第三桶无法是真 R_lambda。
```

普通话总结：

```text
主线现在变成：
不要消灭第三桶，
要证明第三桶没有真货。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_product_square_bucket_summary_keeps_residual_guard -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```

结果：

```text
1 passed
32 passed
396 passed, 2 warnings
```
