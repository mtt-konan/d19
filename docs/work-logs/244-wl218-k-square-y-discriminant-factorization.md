# wl244 — wl218 K-square y-discriminant factorization

日期：2026-06-22

## 1. 本轮目标

接 wl243。

上一轮确认：

```text
K 是平方
R(a,K) 是平方
```

仍然不够，因为真正要先解出有理 `y`。

普通话说：

```text
第二层门能过，不代表人已经进屋。
这一轮直接看第三层门：P=KQ 作为 y 二次方程的判别式。
```

---

## 2. 设置

仍在第一分支：

```text
r+s = lambda+1
```

用斜率变量：

```text
x = r/lambda
y = s/lambda
D = x+y-1
lambda = 1/D
```

剩余 squareclass-ratio 条件是：

```text
P/Q is square
```

其中：

```text
P = x^2 + D^2
Q = y^2 + D^2
```

写成展开式：

```text
P = 2x^2 + 2xy - 2x + y^2 - 2y + 1
Q = x^2 + 2xy - 2x + 2y^2 - 2y + 1
```

固定 `x`，令：

```text
P = K Q.
```

把 `P=KQ` 看成关于 `y` 的二次方程，判别式为：

```text
D_y = -4 I(x,K)
```

其中：

```text
I(x,K)
= K^2x^2 - 2K^2x + K^2
  - 3Kx^2 + 2Kx - K
  + x^2.
```

---

## 3. 新分裂：把 K 写成 k^2

这一轮的新点是：不要只把 `K` 当任意有理数。

原问题要求：

```text
K = k^2.
```

再把 `x` 参数化为勾股斜率：

```text
x = (1-a^2)/(2a).
```

则 `D_y` 精确分裂为：

```text
D_y = - F_-(a,k) F_+(a,k) / a^2
```

其中：

```text
F_-(a,k)
= a^2k^2 - a^2k - a^2
  + 2ak^2 - k^2 - k + 1

F_+(a,k)
= a^2k^2 + a^2k - a^2
  + 2ak^2 - k^2 + k + 1.
```

两个因子作为 `k` 的二次式，有同一个判别式：

```text
Delta(a) = 5a^4 + 8a^3 - 6a^2 - 8a + 5.
```

普通话说：

```text
一旦承认 K 真的是平方，第三层判别式不是一团乱式子，
而是裂成两个互为镜像的二次因子。
这两个因子的共同开关，正是 wl239-wl241 那条新 quartic。
```

---

## 4. 这比 wl243 更靠近核心

wl243 的边界是：

```text
K square + R(a,K) square
```

仍然可能是假阳性。

本轮改成直接记录：

```text
K = k^2
D_y square
```

这是 `P=KQ` 能不能实际解出有理 `y` 的门。

代码 helper：

```text
sum_ab_k_square_y_discriminant_factorization(a, k)
```

记录：

```text
x = (1-a^2)/(2a)
K = k^2
F_-(a,k), F_+(a,k)
D_y
-F_-F_+/a^2 = D_y
Delta(a)
```

测试：

```text
test_sum_ab_k_square_y_discriminant_factorization_splits_layer3
```

---

## 5. 仍然不能宣布证明

这一层仍然有假点。

例如：

```text
a = 1/2
x = 3/4
k = 3
K = 9
```

这时：

```text
D_y = 81/4
```

所以 `P=KQ` 确实能解出有理 `y`。

正根给：

```text
y = 1/4
P/Q = 9.
```

但：

```text
y^2+1 = 17/16
```

不是有理平方。

普通话说：

```text
第三层能解出 y，仍不代表 y 自己是合法直角三角形斜率。
假点还会死在第四层。
```

---

## 6. 小范围检查

为了找结构，只做有限检查，不当证明。

枚举：

```text
1 <= numerator(a) < denominator(a) <= 39
1 <= numerator(k), denominator(k) <= roughly 80/39
```

筛选：

```text
x = (1-a^2)/(2a)
x^2+1 square
D_y square
y > 0
y != x
y^2+1 square
```

结果：

```text
found = 0
```

这只说明当前候选引理仍和有限证据一致。

---

## 7. 下一步

下一刀应直接吃掉 Layer 4：

```text
D_y square
y is a rational root of P=k^2 Q
y^2+1 square
```

目标变成证明：

```text
x=(1-a^2)/(2a), 0<a<1
K=k^2
D_y square
y root
y^2+1 square
=> y=x
```

或者等价地，证明所有非中线 Layer-3 假点都不能通过 `y^2+1`。

普通话说：

```text
现在已经不是 A_p,B_p 那层影子账本了。
我们已经摸到 y 这个真实变量。
剩下要证明的是：能摸到 y 还不够，y 必须也是真勾股；
这一关应当把非中线点全部杀掉。
```

---

## 8. 验证

本轮已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py -q
66 passed

PYTHONPATH=src uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
All checks passed
```

当前仍不能说：

```text
sum=A+B 已证明。
倒数定理已证明。
```

可以说：

```text
sum=A+B 的 squareclass-ratio 路线已从 Layer 2 推进到 Layer 3，
并明确暴露下一步必须处理 Layer 4 的 y^2+1 条件。
```
