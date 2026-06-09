# wl147 — `sum=A+B` same-orientation denominator factorization

日期：2026-06-09

## 1. 本轮问题

wl146 给出 same orientation 的 both-pass 框架，并指出关键量：

```text
P = bc
Q = ad
```

以及：

```text
P-Q
P+Q
```

这轮把 `P±Q` 的因式分解固化成代码 helper。

普通话说：

```text
以后不用再手算 P-Q。
代码直接告诉我们它里面有 nu-mv 这个关键因子。
```

---

## 2. 新增模型

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

新增：

```text
SumAbSameOrientationDenominatorFactorization
sum_ab_same_orientation_denominator_factorization(...)
```

输出：

```text
orientation
other_denominator
failed_denominator
denominator_difference
denominator_sum
nu_minus_mv
difference_factorization
sum_factorization
```

其中：

```text
other_denominator = P = bc
failed_denominator = Q = ad
```

---

## 3. odd/odd 公式

odd orientation：

```text
a = m^2-n^2
b = 2mn
c = u^2-v^2
d = 2uv
```

所以：

```text
P = bc = 2mn(u^2-v^2)
Q = ad = 2uv(m^2-n^2)
```

分解：

```text
P - Q =  2(mu+nv)(nu-mv)
P + Q =  2(mu-nv)(mv+nu)
```

---

## 4. even/even 公式

even orientation：

```text
a = 2mn
b = m^2-n^2
c = 2uv
d = u^2-v^2
```

这会把 odd/odd 的 P,Q 对调。

所以：

```text
P - Q = -2(mu+nv)(nu-mv)
P + Q =  2(mu-nv)(mv+nu)
```

---

## 5. 固定样例

输入：

```text
(m,n) = (4,1)
(u,v) = (7,2)
```

odd/odd：

```text
P = 360
Q = 420
P-Q = -60
P+Q = 780
nu-mv = 1*7 - 4*2 = -1
```

分解：

```text
P-Q = 2 * 30 * (-1)
P+Q = 2 * 26 * 15
```

even/even：

```text
P = 420
Q = 360
P-Q = 60
```

分解：

```text
P-Q = -2 * 30 * (-1)
P+Q = 2 * 26 * 15
```

---

## 6. 为什么 `nu-mv` 重要

如果：

```text
P = Q
```

则：

```text
P-Q = 0
```

正参数下：

```text
mu+nv > 0
```

所以：

```text
nu-mv = 0
```

也就是：

```text
n/u?  更准确地说：nu = mv
```

普通话说：

```text
P=Q 会逼迫两组 Euclid 参数成同一比例。
primitive 情况下，这通常会退化到同一组参数，也就是镜像/互反分支。
```

这和主方向：

```text
s = lambda/r
```

是对齐的。

---

## 7. 能说什么，不能说什么

可以说：

```text
same orientation 的 P±Q 因子现在有代码入口。
P-Q 的关键因子是 nu-mv。
P=Q 会自然导向比例退化。
```

不能说：

```text
both-pass 已推出 P=Q。
same orientation 已关闭。
nu-mv 非零时已经矛盾。
```

---

## 8. 下一步

下一步建议：

```text
1. 假设 both-pass 且 nu-mv != 0。
2. 用两套 (g,r,s) 参数表达 P-Q。
3. 看能否从 P-Q 的因子中抽出更小的 both-pass。
```

普通话说：

```text
真正要打的是 nu-mv 不为 0 的情况。
如果能证明它会导致递降，
same orientation 就会被压到 P=Q / 镜像分支。
```

---

## 9. 验证

运行：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_same_orientation_denominator_factorization_exposes_nu_minus_mv -q
uv run ruff check --select I,E402 src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

结果：

```text
1 passed
All checks passed
```
