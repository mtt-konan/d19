# wl167 — `R_lambda` product-square squareclass equivalence

日期：2026-06-09

## 1. 本轮目标

wl166 已经把 product-square 假象说成：

```text
(r^2+1) 与 (s^2+1) 同 squareclass；
(r^2+lambda^2) 与 (s^2+lambda^2) 同 squareclass。
```

本轮把这个关系直接放进 helper。

普通话说：

```text
乘积是平方，不是什么神秘额外条件。
它基本就在说：
这两个数坏得一样。
```

---

## 2. 新字段

`closure_product_square_conditions(...)` 新增：

```text
product_square_explained_by_pairwise_squareclasses
```

它检查：

```text
product_terms_are_squares
```

是否正好由：

```text
member_squareclasses_pairwise_equal
```

解释。

也就是：

```text
A_p 是平方
<=> r^2+1 与 s^2+1 同 squareclass

B_p 是平方
<=> r^2+lambda^2 与 s^2+lambda^2 同 squareclass
```

---

## 3. 三个样本

### 假点：四项全同非 1

```text
lambda = 535/161
r = 14/23
s = 26/7
member_squareclasses = (29, 29, 29, 29)
```

结果：

```text
product_terms_are_squares = True
member_squareclasses_pairwise_equal = True
product_square_explained_by_pairwise_squareclasses = True
true_member_pair = False
```

### 假点：两对同类

```text
lambda = 2
r = s = 3/2
member_squareclasses = (13, 13, 1, 1)
```

结果：

```text
product_terms_are_squares = True
member_squareclasses_pairwise_equal = True
product_square_explained_by_pairwise_squareclasses = True
true_member_pair = False
```

### 真点：全部 trivial

```text
lambda = 1
r = 3/4
s = 4/3
member_squareclasses = (1, 1, 1, 1)
```

结果：

```text
product_terms_are_squares = True
member_squareclasses_pairwise_equal = True
member_squareclasses_all_trivial = True
true_member_pair = True
```

---

## 4. 小扫描

有限一致性扫描：

```text
lambda = 1..11
relation = sum=A+B
target = lambda + 1
r = small rational with denominator <= 15
s = target - r
```

只看能拆回两个正有理根的点：

```text
checked = 9075
failures = 0
```

含义：

```text
这个有限池里，没有发现
product_terms_are_squares 与 pairwise squareclass equal
不一致的样本。
```

不能说：

```text
有限扫描证明了等价。
有限扫描证明了 R_lambda theorem。
```

---

## 5. 为什么这有用

之前的问题是：

```text
A_p,B_p 是平方，能不能推出 r,s in R_lambda？
```

现在可以改写成：

```text
两对 squareclass 相同，能不能推出两对 squareclass 都是 1？
```

普通话说：

```text
之前我们只知道“乘起来像平方”。
现在我们知道它为什么像平方：
因为两边坏得一样。
接下来要证明的是：
在 closure 条件下，坏得一样是否只能是不坏。
```

这比盯着 `A_p,B_p` 更适合作为证明入口。

---

## 6. 下一步

下一步可以尝试：

```text
设 squareclass(r^2+1) = squareclass(s^2+1) = u
设 squareclass(r^2+lambda^2) = squareclass(s^2+lambda^2) = v
```

然后问：

```text
closure + R_lambda 目标 是否强迫 u=v=1？
```

或者反过来：

```text
若 u 或 v 非 1，
这些假点能否参数化？
是否会触发模障碍或递降？
```

普通话总结：

```text
R_lambda 主线现在更清楚了：
不是从乘积平方直接跳到真成员，
而是先经过 squareclass。
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
30 passed
394 passed, 2 warnings
```
