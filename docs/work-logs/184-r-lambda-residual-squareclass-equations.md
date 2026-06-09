# wl184 — `R_lambda` residual squareclass equations

日期：2026-06-09

## 1. 本轮目标

wl183 说明：

```text
root-grid 到 bound=40 没有触发 watchlist。
唯一 residual 仍是 pair=(29,29)。
```

本轮不继续扩大扫描，而是把 residual 条件方程化。

普通话说：

```text
不要只问“扫到几个假阳性”，
要问“假阳性到底靠什么混过了弱筛”。
```

---

## 2. 新 helper

新增：

```text
sum_ab_residual_squareclass_equations(
    lambda_ratio,
    r,
    s,
)
```

返回：

```text
ResidualSquareclassEquations
```

里面记录：

```text
r^2 + 1
s^2 + 1
r^2 + lambda^2
s^2 + lambda^2
```

以及：

```text
unit_squareclasses
lambda_squareclasses
unit_product_is_square
lambda_product_is_square
all_terms_are_squares
squareclasses_all_trivial
```

---

## 3. 核心等价

对 sum=A+B residual 来说：

```text
r+s = lambda+1
```

弱 product-square 检查看的是：

```text
(r^2+1)(s^2+1) 是否为平方
(r^2+lambda^2)(s^2+lambda^2) 是否为平方
```

普通话说：

```text
它只看两个乘积是不是平方，
不是看四个单项各自是不是平方。
```

squareclass 语言下：

```text
(r^2+1)(s^2+1) 是平方
等价于
r^2+1 和 s^2+1 有同一个 squareclass。

(r^2+lambda^2)(s^2+lambda^2) 是平方
等价于
r^2+lambda^2 和 s^2+lambda^2 有同一个 squareclass。
```

所以 residual 最自然的形式是：

```text
unit_squareclasses = (u,u)
lambda_squareclasses = (v,v)
```

真点要求更强：

```text
u = 1
v = 1
```

---

## 4. 已知 residual

输入：

```text
lambda = 535/161
r = 14/23
s = 26/7
```

得到：

```text
unit_values = (725/529, 725/49)
lambda_values = (295829/25921, 643829/25921)
unit_squareclasses = (29,29)
lambda_squareclasses = (29,29)
unit_product_is_square = True
lambda_product_is_square = True
all_terms_are_squares = False
squareclasses_all_trivial = False
```

普通话说：

```text
这个例子不是四项都过了。
它只是四项都落在同一个非平凡平方类 29 里，
所以两个乘积看起来像平方。
```

---

## 5. toy true 例子

输入：

```text
lambda = 1
r = 3/4
s = 4/3
```

得到：

```text
unit_squareclasses = (1,1)
lambda_squareclasses = (1,1)
all_terms_are_squares = True
squareclasses_all_trivial = True
```

这里会触发 watchlist。

普通话说：

```text
真危险不是“两个乘积是平方”，
而是两个 pair 的 squareclass 都退化成 1。
```

---

## 6. 对主证明的意义

主目标仍是：

```text
若 r,s ∈ R_lambda 且 full-plane closure，
是否必须 s = lambda/r？
```

这轮没有证明。

但它把 residual 分支的证明目标说得更尖：

```text
在 residual 条件下，
证明不可能同时 u=1 且 v=1。
```

或者更强一点：

```text
证明 residual 分支只能产生非平凡 squareclass。
```

普通话说：

```text
我们现在知道弱筛漏洞在哪里：
它把“同一个平方类”误当成了“真平方”。
下一步就是证明 residual 里这个平方类不能变成 1。
```

---

## 7. 可以说 / 不能说

可以说：

```text
已知 residual 的 product-square 通过，
是因为两组单项分别有相同 squareclass。
已知 residual 的 squareclass 是非平凡 29。
```

不能说：

```text
所有 residual 都非平凡。
pair=(1,1) 不可能。
有理比例主定理已经证明。
```

因为：

```text
本轮只是方程 ledger，
不是完整递降或模证明。
```

---

## 8. 下一步

下一步更理论化的方向：

```text
1. 从 r+s=lambda+1 消去 lambda。
2. 令 r^2+1 = u * square，s^2+1 = u * square。
3. 令 r^2+lambda^2 = v * square，s^2+lambda^2 = v * square。
4. 专门研究 u=v=1 是否强迫 rs=lambda。
```

普通话总结：

```text
这轮把“假阳性”改写成了“平方类方程”。
后面要做的不是再看图，
而是攻这个平方类能不能退化成 1。
```

---

## 9. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_residual_squareclass_equations_explain_product_square -q
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
