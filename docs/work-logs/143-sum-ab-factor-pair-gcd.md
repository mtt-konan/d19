# wl143 — `sum=A+B` factor-pair gcd diagnostics

日期：2026-06-09

## 1. 本轮问题

wl142 已经把通过的 shared-leg 方程写成：

```text
(H-P)(H+P) = N^2
```

这轮继续暴露：

```text
gcd(H-P, H+P)
```

以及约分后的因子对。

普通话说：

```text
不只知道 N^2 拆成两块；
还要知道这两块共享了多少公因子。
```

---

## 2. 新增属性

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

`SumAbSameOrientationSharedLegTerms` 新增：

```text
other_factor_pair_gcd
failed_factor_pair_gcd
other_reduced_factor_pair
failed_reduced_factor_pair
```

如果对应 square equation 不通过，则这些属性返回：

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

因子对：

```text
(H-P, H+P) = (15, 735)
```

gcd：

```text
gcd(15,735) = 15
```

约分：

```text
(15,735) / 15 = (1,49)
```

所以：

```text
other_factor_pair_gcd = 15
other_reduced_factor_pair = (1,49)
```

failed 项不通过：

```text
failed_factor_pair_gcd = None
failed_reduced_factor_pair = None
```

---

## 4. 为什么这有用

如果：

```text
(H-P)(H+P)=N^2
```

且：

```text
g = gcd(H-P, H+P)
```

那么：

```text
H-P = gR
H+P = gS
RS = N^2 / g^2
```

普通话说：

```text
g 把两个因子共同的部分剥掉；
剩下的 R,S 更接近“互素因子”。
如果 R,S 互素，而乘积又是平方，
那 R 和 S 往往必须各自是平方。
```

这正是标准勾股参数化/递降证明常用的入口。

---

## 5. 当前能说什么

可以说：

```text
shared-leg 通过项现在能直接给出 gcd 和 reduced factor pair。
```

不能说：

```text
reduced factor pair 一定互素。
same orientation 已关闭。
已经推出 R,S 各自为平方。
```

原因：

```text
是否互素还要看 N、P、H 的奇偶和 gcd 结构。
```

---

## 6. 下一步

下一步建议：

```text
1. 对 factor pair 继续记录：
   gcd(reduced_left, reduced_right)

2. 判断什么时候 reduced pair 互素。

3. 若互素，则尝试写：
   reduced_left = r^2
   reduced_right = s^2

4. 把 P = (H+P - (H-P))/2
   反推回 bc 或 ad。
```

普通话说：

```text
下一步就是把“一个平方拆成两个因子”
推进成“两个互素因子各自是平方”。
如果能做到，就很像递降证明了。
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
