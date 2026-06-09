# wl170 — `R_lambda` centerline obstruction ledger

日期：2026-06-09

## 1. 本轮目标

wl169 解释了：

```text
sum=A+B 中心线 r=s=(lambda+1)/2
会自动制造 product-square 假象。
```

本轮给这条线加一个更普通的失败分类：

```text
centerline_obstruction
```

普通话说：

```text
不只说它不是真点，
还说它具体坏在哪一边。
```

---

## 2. 新字段

`closure_product_square_conditions(...)` 新增：

```text
centerline_obstruction
```

只有在：

```text
r = s
```

时才有意义。

取值：

```text
unit-leg    : r^2+1 这一边不是平方
lambda-leg  : r^2+lambda^2 这一边不是平方
both-legs   : 两边都不是平方
None        : 非中心线，或中心线两边都通过
```

普通话说：

```text
unit-leg 是“到单位边距离坏了”；
lambda-leg 是“到 lambda 边距离坏了”。
```

---

## 3. 样本

```text
lambda=3
r=s=2
member_squareclass_pair=(5,13)
centerline_obstruction=both-legs
```

两边都坏：

```text
2^2 + 1 = 5
2^2 + 3^2 = 13
```

都不是平方。

另一个样本：

```text
lambda=15
r=s=8
member_squareclass_pair=(65,1)
centerline_obstruction=unit-leg
```

这里：

```text
8^2 + 15^2 = 289 = 17^2
```

lambda-leg 已经过了。

但：

```text
8^2 + 1 = 65
```

unit-leg 仍然坏，所以不是真成员。

---

## 4. 小表

有限诊断：

```text
lambda = 1..25
sum=A+B centerline
```

分布：

```text
both-legs : 23
unit-leg  : 2
```

前几个样本：

```text
lambda=1,  r=1,    pair=(2,2),     obstruction=both-legs
lambda=2,  r=3/2,  pair=(13,1),    obstruction=unit-leg
lambda=3,  r=2,    pair=(5,13),    obstruction=both-legs
lambda=4,  r=5/2,  pair=(29,89),   obstruction=both-legs
lambda=15, r=8,    pair=(65,1),    obstruction=unit-leg
```

可以说：

```text
这个有限表里没有中心线真成员。
```

不能说：

```text
有限表证明所有 lambda 都没有中心线真成员。
```

---

## 5. 真正的证明问题

sum=A+B 中心线真成员要求：

```text
r = (lambda+1)/2
r^2 + 1        是平方
r^2 + lambda^2 是平方
```

普通话说：

```text
同一个 r 要同时和 1、lambda 两边配成勾股距离。
```

这正是 `r in R_lambda` 的单点问题。

所以中心线 proof note 可以写成：

```text
假设中心线真成员存在。
令 r=(lambda+1)/2。
把两个平方条件写成：
  ((lambda+1)/2)^2 + 1
  ((lambda+1)/2)^2 + lambda^2
都是平方。
再尝试用 Yang Ji / 固定线方法排除。
```

这比之前更清楚，因为 product-square 已经被解释掉了：

```text
product-square 在中心线没有信息量。
真正有信息的是两个单项是否分别为平方。
```

---

## 6. 和全局目标的关系

可以说：

```text
中心线是 R_lambda theorem 的一个低维样板。
它能解释一批 product-square 假阳性。
```

不能说：

```text
关闭中心线就关闭全局。
这个 helper 等价于 Yang Ji 的几何中线证明。
```

普通话总结：

```text
中心线这条路的用处不是直接拿下全局，
而是训练我们把“闭包假象”拆成真正的平方条件。
```

---

## 7. 下一步

下一步可以二选一：

```text
1. 继续证明中心线真成员不存在，
   作为 Yang Ji / 特殊线 proof note 的本地版本。

2. 在扫描里剔除 r=s 中心线样本，
   专看非中心线的 (u,v) 模式。
```

我更倾向于：

```text
先做 2。
```

因为这样能知道中心线假象被剔除后，还剩哪些非平凡模式。

---

## 8. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_centerline_squareclass_conditions_explain_midpoint_hits -q
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```

结果：

```text
1 passed
31 passed
395 passed, 2 warnings
```
