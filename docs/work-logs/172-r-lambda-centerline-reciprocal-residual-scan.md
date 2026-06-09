# wl172 — `R_lambda` centerline/reciprocal residual scan

日期：2026-06-09

## 1. 本轮目标

wl171 发现：

```text
剔除 r=s 中心线后，
有限池里剩下的 product-square 假象像 reciprocal orbit。
```

本轮新增：

```text
reciprocal_pair
```

然后扫描：

```text
非 centerline
非 reciprocal
但仍 product-square
```

普通话说：

```text
先把两个最明显的假象桶拿掉，
看看桶外还有没有东西。
```

---

## 2. 新字段

`closure_product_square_conditions(...)` 新增：

```text
reciprocal_pair
```

含义：

```text
roots = (r,s)
rs = lambda
```

也就是：

```text
s = lambda/r
```

普通话说：

```text
两个数互为 lambda 镜像。
```

---

## 3. 测试样本

中心线不是 reciprocal：

```text
lambda = 2
roots = (3/2, 3/2)
product = 9/4
centerline = True
reciprocal_pair = False
```

reciprocal 样本：

```text
lambda = 7
roots = (1, 7)
product = 7
centerline = False
reciprocal_pair = True
member_squareclass_pair = (2,2)
true_member_pair = False
```

普通话说：

```text
(1,lambda) 是镜像闭合点，
但通常不是真有理距离点。
```

---

## 4. 小扫描

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
total product-square hits = 270
centerline hits           = 230
reciprocal noncenter hits = 40
residual hits             = 0
```

普通话说：

```text
这个小池里，
product-square 假象完全被两个桶吃掉：
中心线桶 + reciprocal 桶。
```

---

## 5. 当前能说什么

可以说：

```text
有限池里没有发现第三类 product-square 假象。
```

不能说：

```text
已经证明所有 product-square hit 都只能是 centerline 或 reciprocal。
已经证明 R_lambda translation theorem。
```

普通话说：

```text
这是一个很强的诊断信号，
但还不是证明。
```

---

## 6. 为什么这接近主证明

主目标是：

```text
若 r,s in R_lambda 且满足 closure，
是否必须 s=lambda/r？
```

现在 product-square 假象被分成：

```text
1. centerline: r=s
2. reciprocal: rs=lambda
3. residual: 暂未看到
```

如果能理论证明：

```text
product-square + closure
=> centerline 或 reciprocal
```

再单独排除 centerline 真成员，
就会更接近：

```text
true R_lambda closure => reciprocal
```

普通话说：

```text
我们不是直接证明大结论。
我们先证明假象只有两种形状。
```

---

## 7. 下一步

下一步可以尝试代数化：

```text
sum=A+B:
r+s = lambda + 1
A_p,B_p 是平方
```

问：

```text
是否强迫 r=s 或 rs=lambda？
```

这条比直接处理四个 R_lambda 成员条件弱，
但更可能先拿下。

如果拿下，再加：

```text
centerline 不是 true_member_pair
```

就能把 sum=A+B 分支进一步压到：

```text
reciprocal orbit
```

普通话总结：

```text
现在最像的证明路线是：
先把 product-square 的第三类残差证明不存在。
```

---

## 8. 验证

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
