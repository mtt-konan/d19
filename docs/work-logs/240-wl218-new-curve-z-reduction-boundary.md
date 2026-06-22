# wl240 — wl218 new curve z-reduction boundary

日期：2026-06-22

## 1. 本轮目标

继续处理 wl238 / wl239 的新四次曲线：

```text
Y^2 = 5t^4 + 8t^3 - 6t^2 - 8t + 5.
```

普通话说：

```text
上一轮我们把它看成 rank 0 椭圆曲线的入口。
这轮发现它还能再降一层：不是随机四次，而是两个二次平方条件的交集。
```

---

## 2. 关键代换

令：

```text
z = t - 1/t.
```

把四次式除以 `t^2`：

```text
(Y/t)^2
= 5t^2 + 8t - 6 - 8/t + 5/t^2
= 5(t-1/t)^2 + 8(t-1/t) + 4.
```

所以：

```text
(Y/t)^2 = 5z^2 + 8z + 4.
```

另一方面，`z` 真能从有理 `t` 恢复出来，当且仅当：

```text
t^2 - zt - 1 = 0
```

有有理根，即：

```text
z^2 + 4 是有理平方。
```

因此新四次曲线的有理点问题变成：

```text
z^2 + 4          是平方
5z^2 + 8z + 4   是平方.
```

普通话说：

```text
原来要看 t 上的一条四次曲线。
现在可以看 z 上的两个“直角三角形条件”能不能同时成立。
```

边界点：

```text
z=0
```

对应：

```text
t = ±1.
```

---

## 3. 参数化其中一条 conic

若先参数化：

```text
z^2 + 4 = square,
```

从点 `(z,w)=(0,2)` 取斜率 `m`，得到非零分支：

```text
z = -4m / ((m-1)(m+1)).
```

代回第二个平方条件：

```text
5z^2 + 8z + 4 = square
```

得到：

```text
square =
4(m^4 - 8m^3 + 18m^2 + 8m + 1) / ((m-1)^2(m+1)^2).
```

也就是又回到一个 rank-0 型四次：

```text
H^2 = m^4 - 8m^3 + 18m^2 + 8m + 1.
```

若先参数化第二条 conic：

```text
5z^2 + 8z + 4 = square,
```

得到：

```text
z = -4(n-2)/(n^2-5),
```

再代回第一条：

```text
square =
4(n^4 - 6n^2 - 16n + 41)/(n^2-5)^2.
```

也就是：

```text
H^2 = n^4 - 6n^2 - 16n + 41.
```

PARI 对这些四次给出的直接模型不完全相同：

```text
m^4 - 8m^3 + 18m^2 + 8m + 1
  -> [0, 18, 0, -68, 56]

n^4 - 6n^2 - 16n + 41
  -> [0, -6, 0, -164, 1240]
```

但这两个模型同构到同一个最小模型：

```text
[0, 0, 0, -11, 14]
```

普通话说：

```text
z 代换把问题解释清楚了：
难点不是四次式太大，而是两个二次平方条件的交集本身就是一条 genus 1 曲线。
```

---

## 4. mod 3 现象和边界

在有限域 `F_3` 里，同时要求：

```text
z^2 + 4          square
5z^2 + 8z + 4   square
```

会强迫：

```text
z = 0.
```

普通话说：

```text
模 3 看，两个平方条件只留下边界点。
```

但这不能直接升级成 3-adic 递降。

检查 `mod 3^k`：

```text
k=1: live z = {0 mod 3}
k=2: live z = all multiples of 3 mod 9
k=3: live z = all multiples of 3 mod 27
...
```

也就是说：

```text
z 被 3 整除以后，并不会被继续强迫被 9、27、... 整除。
```

普通话说：

```text
mod 3 是一个很漂亮的筛，
但不是一个无限递降证明。
```

---

## 5. 代码入口

新增 helper：

```text
sum_ab_new_curve_z_reduction(t)
```

记录：

```text
z = t - 1/t
original_quartic_value
scaled_quartic_value = original / t^2
z_recovery_square = z^2 + 4
new_curve_square = 5z^2 + 8z + 4
identity_holds
z_recovery_is_square
new_curve_is_square
```

新增测试：

```text
test_sum_ab_new_curve_z_reduction_tracks_two_square_conditions
```

---

## 6. 当前证明状态

可以安全说：

```text
1. 新四次曲线已等价压缩成 z 上两个二次平方条件；
2. z=0 对应 t=±1 边界点；
3. 参数化任一 conic 后，剩余问题仍是 rank-0 型四次；
4. mod 3 在有限域上杀掉所有非零 z，但不是 3-adic 递降。
```

不能说：

```text
新四次曲线已证明只有边界点。
sum=A+B 已关闭。
倒数定理已证明。
```

---

## 7. 下一步

最短下一步不再是原始四次式，而是证明：

```text
z^2 + 4 square
5z^2 + 8z + 4 square
=> z = 0.
```

可选路线：

```text
1. 对 H^2 = n^4 - 6n^2 - 16n + 41 做显式 torsion pullback；
2. 或直接对两个 conic 的交集做 2-descent / elementary descent；
3. 或寻找一个能处理 z 分母退化的全局局部障碍。
```

普通话说：

```text
目标已经比 wl238 短很多：
不用再盯着 x,y,K 三层变量，
先证明这两个 z 平方条件只能给 z=0。
```
