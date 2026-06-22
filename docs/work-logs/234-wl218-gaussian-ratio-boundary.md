# wl234 — wl218 Gaussian-ratio boundary

日期：2026-06-22

## 1. 本轮目标

继续推进 `sum=A+B` 分支的 squareclass-ratio 引理：

```text
A/B 是有理平方 => t=u
```

前两轮说明：

```text
z = u - 1/u
```

能把四次式降成二次式，但继续参数化 `z^2+4` 会回到同一个
`A(t,u)/B(t,u)` 问题。

本轮改走 Gaussian / local-symbol 方向。

普通话说：

```text
既然继续换变量会绕圈，就看两个平方和在高斯整数里怎么分解。
如果 A/B 是平方，两个平方和的素因子分配必须高度同步。
```

---

## 2. 两个平方和

沿用：

```text
E = t + u - 2tu - t^2u - tu^2
R = u(1-t^2)
S = t(1-u^2)
```

则：

```text
A = E^2 + R^2
B = E^2 + S^2
```

所以：

```text
A = Norm(E + iR)
B = Norm(E + iS).
```

`A/B` 为有理平方等价于：

```text
Norm((E+iR)/(E+iS)) 是有理平方。
```

---

## 3. Gaussian 比值的实部与虚部

考虑：

```text
(E+iR)/(E+iS)
= ((E+iR)(E-iS)) / B
```

分子实部和虚部为：

```text
X = E^2 + RS
Y = E(R-S)
```

并且：

```text
X^2 + Y^2 = A B.
```

关键因式：

```text
R-S = -(t-u)(tu+1)
```

所以：

```text
Y = E(R-S)
  = (t-u)(tu+1)(t^2u + tu^2 + 2tu - t - u)
```

只差整体符号。

普通话说：

```text
中线 t=u 时，Gaussian 比值是纯实数。
非中线时，虚部一定带着 t-u 这个因子。
```

在正范围：

```text
0<t,u<1
```

有：

```text
tu+1 > 0.
```

而 `E>0` 正是 `lambda>0` 的条件。

所以：

```text
非中线 <=> Y != 0.
```

这给 descent 或局部符号一个明确抓手。

---

## 4. Unit-circle 参数化尝试

若：

```text
A/B = h^2
```

则：

```text
(X + iY)/(hB)
```

在有理单位圆上。

令单位圆参数为 `w`：

```text
Y/X = 2w/(1-w^2).
```

等价方程：

```text
Y(1-w^2) - 2wX = 0.
```

把它看成 `u` 的方程，仍是四次式。判别式有一个大平方因子，但还剩一个
大 quartic；本轮没有把它降成可立即证明的二次或 genus-0 形式。

普通话说：

```text
单位圆参数化能解释结构，但没有直接关门。
它可能适合做 descent，但不是一行证明。
```

---

## 5. Near-miss 的局部素数现象

same-orientation near-miss 小样本继续显示：

```text
失败 squareclass 主要来自 1 mod 4 素数，或含 2 的组合。
```

例子：

```text
(N,P,Q)=(7,24,28)
N^2+P^2 = 25^2
N^2+Q^2 = 833 = 7^2 * 17
失败 squareclass = 17
```

这里：

```text
17 == 1 mod 4.
```

另一个：

```text
(N,P,Q)=(451,780,87)
N^2+P^2 = 17^2 * 53^2
N^2+Q^2 = 2 * 5 * 17^2 * 73
失败 squareclass = 2 * 5 * 73.
```

这再次说明：

```text
只看 q == 3 mod 4 的 valuation 不会抓住主障碍。
```

普通话说：

```text
坏素数不是藏在 3 mod 4 那边。
它们主要藏在 2 和 1 mod 4 的高斯素分裂里。
```

---

## 6. 当前证明边界

可以安全说：

```text
1. A 和 B 是两个 Gaussian norm；
2. Gaussian 比值的虚部精确含有 (t-u)(tu+1)E；
3. 非中线等价于该虚部非零；
4. unit-circle 参数化没有直接降维，但可能可用于 descent；
5. q == 3 mod 4 valuation 不是足够强的关键引理。
```

不能说：

```text
Gaussian 路线已经证明候选引理。
sum=A+B 已关闭。
倒数定理已证明。
```

---

## 7. 下一步

现在更具体的下一步是找 descent 规范量。

候选输入：

```text
X = E^2 + RS
Y = E(R-S)
X^2 + Y^2 = AB
Y = E(R-S)
R-S = -(t-u)(tu+1)
```

若 `A/B = h^2`，则单位圆参数 `w` 存在。需要寻找：

```text
(t,u,h,w) 非中线解
=> 更小的 (t',u',h') 非中线解
```

或证明某个局部 Hilbert symbol 在非中线时必为 `-1`。

普通话说：

```text
现在门把手已经很明确：非中线就是 Gaussian 比值有虚部。
下一步要证明这个虚部不能和“norm 是平方”同时存在，
或者存在就能造出更小反例。
```
