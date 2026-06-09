# wl145 — `sum=A+B` factor-pair parameterization

日期：2026-06-09

## 1. 本轮问题

wl144 已经能判断 reduced factor pair 是否为平方对：

```text
(H-P, H+P) = g(r^2, s^2)
```

这轮把它直接写成参数化三元组：

```text
(g, r, s)
```

并提供还原：

```text
N = g r s
P = g(s^2-r^2)/2
H = g(s^2+r^2)/2
```

普通话说：

```text
现在不只知道两个因子是平方；
还能直接把它们变成一套勾股参数。
```

---

## 2. 新增属性

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

`SumAbSameOrientationSharedLegTerms` 新增：

```text
other_factor_pair_parameterization
failed_factor_pair_parameterization
other_parameterized_shared_numerator
failed_parameterized_shared_numerator
other_parameterized_denominator
failed_parameterized_denominator
other_parameterized_hypotenuse
failed_parameterized_hypotenuse
```

如果对应 square equation 不通过，则返回：

```text
None
```

---

## 3. 固定样例

样例：

```text
N = 105
P = 360
H = 375
```

已有：

```text
(H-P, H+P) = (15,735)
g = 15
reduced = (1,49) = (1^2,7^2)
```

所以参数化：

```text
(g,r,s) = (15,1,7)
```

还原：

```text
N = 15 * 1 * 7 = 105
P = 15 * (49-1) / 2 = 360
H = 15 * (49+1) / 2 = 375
```

failed 项不通过：

```text
failed_factor_pair_parameterization = None
```

---

## 4. 为什么这有用

same orientation 如果 both-pass，则会有两套：

```text
other:  (g1,r1,s1)
failed: (g2,r2,s2)
```

并且同一个 `N` 必须满足：

```text
N = g1 r1 s1 = g2 r2 s2
```

同时：

```text
bc = g1(s1^2-r1^2)/2
ad = g2(s2^2-r2^2)/2
```

普通话说：

```text
如果 other 和 failed 都通过，
那它们给同一个 N 生成两套勾股参数。
下一步就是比较这两套参数能不能同时存在。
```

这正好接向：

```text
递降
P=Q / 镜像分支
s = lambda/r
```

---

## 5. 能说什么，不能说什么

可以说：

```text
通过的 shared-leg 方程现在能直接转成 (g,r,s) 参数化。
```

不能说：

```text
both-pass 已被排除。
same orientation 已关闭。
参数化自动推出镜像。
```

这一步只是把证明要比较的变量显式化。

---

## 6. 下一步

建议下一步写一个 both-pass 假设 note：

```text
假设 other 和 failed 都通过。
引入：
  other:  (g1,r1,s1)
  failed: (g2,r2,s2)

列出：
  g1 r1 s1 = g2 r2 s2
  bc = g1(s1^2-r1^2)/2
  ad = g2(s2^2-r2^2)/2
```

然后对照：

```text
a,b,c,d 来自 same orientation 的 Euclid legs。
```

普通话说：

```text
下一步就是搭“反证用的符号架子”。
```

---

## 7. 验证

运行：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_same_orientation_shared_leg_terms_expose_square_difference -q
uv run ruff check --select I,E402 src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

结果：

```text
1 passed
All checks passed
```
