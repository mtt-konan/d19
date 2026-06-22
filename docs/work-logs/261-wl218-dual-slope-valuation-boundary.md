# wl261 — wl218 dual slope valuation boundary

日期：2026-06-22

## 1. 本轮目标

接 wl260。

wl260 把四勾股闭环参数化到 `t,u`，并暴露：

```text
(x^2+1) - (y^2+1)
```

带有中心线因子。

本轮给这两个恢复平方值加 prime valuation 账本，尤其看 `q == 3 mod 4` 的素数是否直接抓住失败。

普通话说：

```text
我们已经知道两个恢复值的差长什么样。
现在开始数素数次数：
如果某个恢复值不是平方，是不是会被 3 mod 4 素数立刻抓住？
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopeValuationRow
SumAbDualSlopeValuationLedger
```

新增 helper：

```text
sum_ab_dual_slope_valuation_ledger(t, u)
```

它基于：

```text
sum_ab_dual_slope_parameterization(t, u)
```

记录：

```text
recovery_squareclasses
recovery_squareclass_primes
three_mod_four_recovery_squareclass_primes
primes
three_mod_four_primes
rows_by_prime
```

每个 row 记录：

```text
v_q(x^2+1)
v_q(y^2+1)
v_q((x^2+1)-(y^2+1))
v_q(centerline_factor)
```

普通话说：

```text
这个 helper 是显微镜。
它不证明无解，只告诉我们失败发生在哪些素数上。
```

---

## 3. 样例

取 wl260 的非中心样例：

```text
t = 1/4
u = 2/7
```

反构造：

```text
x = 24/7
y = 4
```

恢复值：

```text
x^2+1 = 625/49 = (25/7)^2
y^2+1 = 17
```

所以：

```text
recovery_squareclasses = (1, 17)
recovery_squareclass_primes = (17,)
three_mod_four_recovery_squareclass_primes = ()
```

也就是说：

```text
失败的 squareclass 是 17，而 17 == 1 mod 4。
```

同时整体支撑里确实有 `3 mod 4` 素数：

```text
three_mod_four_primes = (3, 7)
```

但在 `q=7`：

```text
v_7(x^2+1) = -2
v_7(y^2+1) = 0
```

都是偶数。

普通话说：

```text
这个失败不会被“恢复值里出现 3 mod 4 奇赋值”直接抓住。
坏因子落在 17，和之前 guard 的 29 一样，都是 1 mod 4。
```

---

## 4. 对证明路线的影响

这再次修正用户原第 4 点的使用方式。

不能只写：

```text
看 q == 3 mod 4 的成员项奇赋值，就能排掉所有非中心。
```

因为双斜率恢复层也出现了：

```text
only-1-mod-4 squareclass failure
```

更安全的路线是：

```text
1. 用 valuation 账本定位 3 mod 4 因子；
2. 对 only-1-mod-4 squareclass 用 Gaussian absorption / 双斜率自对偶；
3. 证明非中心若能通过所有四平方，会导致递降或回到 centerline。
```

普通话说：

```text
3 mod 4 仍然重要，但它不是唯一入口。
1 mod 4 坏因子会假装无害，因为它可以写成两个平方。
证明必须把这层也吃掉。
```

---

## 5. 当前边界

可以安全说：

```text
1. 双斜率恢复值已有 prime valuation 账本；
2. 非中心样例的失败 squareclass 是 only-1-mod-4；
3. 这和 earlier Gaussian residual 边界一致。
```

不能说：

```text
dual-slope 非中心闭环已排除。
sum=A+B 已证明。
全平面倒数定理已证明。
```
