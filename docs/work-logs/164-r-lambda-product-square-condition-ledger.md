# wl164 — `R_lambda` product-square condition ledger

日期：2026-06-09

## 1. 本轮目标

wl163 说下一步要做：

```text
固定 closure target T。
设 p=rs。
把 r,s in R_lambda 翻译成 T,p,lambda 的平方条件。
```

本轮先不证明 `p=lambda`。

本轮只做一件事：

```text
把必要条件和真实条件放到同一个 helper 里。
```

普通话说：

```text
先把账本摊开。
哪些只是看起来对，
哪些才是真的候选点，
不要混。
```

---

## 2. 新 helper

新增：

```text
closure_product_square_conditions(lambda_ratio, target, product, relation)
```

它返回：

```text
discriminant
discriminant_is_square
roots
product_terms_are_squares
member_square_flags
true_member_pair
```

其中：

```text
product_terms_are_squares
```

只检查：

```text
A_p 是平方
B_p 是平方
```

而：

```text
true_member_pair
```

检查的是更强的真实条件：

```text
r^2+1        是平方
s^2+1        是平方
r^2+lambda^2 是平方
s^2+lambda^2 是平方
```

---

## 3. 公式

sum closure：

```text
r+s = T
p = rs
D = T^2 - 4p
```

difference closure：

```text
|r-s| = T
p = rs
D = T^2 + 4p
```

乘积层面的必要条件仍是：

```text
A_p = p^2 + eps*2p + T^2 + 1
B_p = p^2 + eps*2lambda^2*p + lambda^2*T^2 + lambda^4
```

其中：

```text
eps = -1  对应 sum closure
eps = +1  对应 difference closure
```

并且：

```text
B_p - lambda^2 A_p = (lambda^2 - 1)(lambda^2 - p^2)
```

---

## 4. 一个重要坑

测试样本：

```text
lambda = 535/161
r = 14/23
s = 26/7
T = lambda + 1
p = rs
```

它满足：

```text
r+s = T
D 是平方
A_p 是平方
B_p 是平方
```

但：

```text
r,s 都不在 R_lambda。
member_square_flags = (False, False, False, False)
```

普通话说：

```text
两个坏数相乘，也可能变成平方。
所以 A_p、B_p 是平方，不等于四个单项分别是平方。
```

这就是为什么不能只靠 `p=rs` 的乘积恒等式完成证明。

---

## 5. 当前能说什么

可以说：

```text
closure_product_square_conditions 把三层检查分开了：
1. T,p 能不能拆回有理 r,s；
2. A_p,B_p 是否通过乘积必要条件；
3. r,s 是否真的属于 R_lambda。
```

不能说：

```text
A_p,B_p 是平方 => r,s in R_lambda。
有限测试没见反例 => P0 成立。
```

普通话说：

```text
这轮推进的是证明语言，
不是证明结果。
```

---

## 6. 下一步证明入口

下一步最自然的是：

```text
固定 relation 和 T。
设 D 是平方，令 r,s 从 T,p 恢复。
再把四个 member_square_flags 全为 True 写成变量方程。
```

真正要攻的是：

```text
D square
A_p product square
B_p product square
four individual member squares
```

能不能一起强迫：

```text
p=lambda
```

如果不能直接推，就找更细的障碍：

```text
平方剩余
局部模条件
二次曲线交点
隐藏递降
```

普通话总结：

```text
主线没有变：
还是 R_lambda。
只是现在我们知道，
战场不在 A_p/B_p 两个乘积平方，
而在四个单项平方如何同时成立。
```

---

## 7. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_closure_product_identity_uses_difference_sign -q
uv run pytest tests/test_rational_ratio.py::test_sum_ab_product_square_conditions_do_not_imply_membership -q
uv run pytest tests/test_rational_ratio.py -q
```

结果：

```text
1 passed
1 passed
30 passed
```
