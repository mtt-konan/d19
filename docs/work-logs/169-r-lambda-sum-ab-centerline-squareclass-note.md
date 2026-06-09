# wl169 — `R_lambda` sum=A+B centerline squareclass note

日期：2026-06-09

## 1. 本轮目标

wl168 看到：

```text
很多非平凡 (u,v) 来自 r=s 的中心线样本。
```

本轮把这条线单独做成 helper 和 proof note。

普通话说：

```text
先把最显眼的一批假象解释掉。
不是证明全局，
而是把中心线这条低维分支讲清楚。
```

---

## 2. 新 helper

新增：

```text
sum_ab_centerline_squareclass_conditions(lambda_ratio)
```

它只处理：

```text
relation = sum=A+B
target = lambda + 1
r = s = (lambda + 1)/2
p = r*s
```

然后复用：

```text
closure_product_square_conditions(...)
```

所以它返回同一套账本：

```text
roots
product_terms_are_squares
member_squareclasses
member_squareclass_pair
true_member_pair
```

---

## 3. 例子

当：

```text
lambda = 3
```

中心线给：

```text
r = s = 2
p = 4
```

结果：

```text
member_squareclasses = (5, 5, 13, 13)
member_squareclass_pair = (5, 13)
true_member_pair = False
```

普通话说：

```text
乘积层面当然会过，
因为 r=s 时两个数一模一样。
但 r^2+1=5 不是平方，
r^2+lambda^2=13 也不是平方。
所以它不是 R_lambda 真点。
```

---

## 4. 奇数整数 lambda 表

若：

```text
lambda = 2n - 1
```

则中心线：

```text
r = s = n
```

于是：

```text
u = squareclass(n^2 + 1)
v = squareclass(n^2 + (2n-1)^2)
```

小表：

```text
lambda=1,  n=1, pair=(2, 2),   true=False
lambda=3,  n=2, pair=(5, 13),  true=False
lambda=5,  n=3, pair=(10, 34), true=False
lambda=7,  n=4, pair=(17, 65), true=False
lambda=9,  n=5, pair=(26,106), true=False
lambda=11, n=6, pair=(37,157), true=False
lambda=13, n=7, pair=(2,218),  true=False
lambda=15, n=8, pair=(65,1),   true=False
```

注意 `pair=(65,1)` 这种情况：

```text
第二边已经是平方类 1，
但第一边不是。
```

所以仍然不是真成员。

---

## 5. 为什么中心线假象多

中心线满足：

```text
r=s
```

因此：

```text
r^2+1 与 s^2+1 完全相同；
r^2+lambda^2 与 s^2+lambda^2 完全相同。
```

所以：

```text
A_p = (r^2+1)(s^2+1)
B_p = (r^2+lambda^2)(s^2+lambda^2)
```

必然是平方。

普通话说：

```text
不是它真的好，
而是同一个坏数乘自己，
看起来当然像平方。
```

这解释了为什么有限扫描里中心线 product-square hit 很多。

---

## 6. 能说和不能说

可以说：

```text
sum=A+B 中心线 product-square 假象已经有本地解释。
r=s 会自动制造 pairwise squareclass equal。
```

不能说：

```text
这证明了全局 R_lambda theorem。
这关闭了所有中心线/中线问题。
这等价于 Yang Ji 的完整中线证明。
```

普通话说：

```text
这只是一个 R_lambda product ledger 里的中心线样板。
它和几何中心线证明有关，
但不是同一份证明。
```

---

## 7. 下一步

有两条自然后续：

```text
1. 写真正的中心线 / A=B / N1=N2 proof note，
   把 Yang Ji 风格翻译成本仓库变量。

2. 在 R_lambda 主线里，
   扫描并分离 r=s 产生的 (u,v)，
   剩下的非中心线 (u,v) 再找模障碍或递降。
```

普通话总结：

```text
中心线方向现在不只是“特殊情况”。
它还能解释 R_lambda product-square 里一批最吵的假阳性。
```

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
