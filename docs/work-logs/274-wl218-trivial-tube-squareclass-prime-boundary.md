# wl274 — wl218 trivial-tube squareclass prime boundary

日期：2026-06-22

## 1. 本轮目标

接 wl273。

wl273 给出两个正参数 witness：

```text
t=1/4, u=19/24   near t+u=0 in Q_5
t=1/4, u=7/8     near tu=1 in Q_5
```

它们都满足：

```text
0<t,u<1,
D>0,
recovery values are Q_5-squares,
recovery values are not Q-squares.
```

本轮追问：

```text
这些“不是真平方”的障碍来自哪些素数？
有没有 q == 3 mod 4 的奇 valuation？
```

普通话说：

```text
如果坏素数里有 3 mod 4，我们还能沿用户原始 valuation 引理走。
如果坏素数全是 1 mod 4，说明这一层太弱，抓不到目标中的 3 mod 4 矛盾。
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopePositiveTrivialTubeSquareclassLedger
```

新增 helper：

```text
sum_ab_dual_slope_positive_trivial_tube_squareclass_ledgers()
```

它对 wl273 的两个 witness 记录：

```text
recovery squareclasses
squareclass primes
one_mod_four_squareclass_primes
three_mod_four_squareclass_primes
```

---

## 3. t+u 管道 witness

对：

```text
t=1/4, u=19/24
```

恢复值：

```text
x^2+1 = 6047561/5929225
y^2+1 = 13414921/5929225
```

平方类：

```text
6047561 = 13 * 173 * 2689
13414921 = 13 * 17 * 101 * 601
```

坏素数集合：

```text
13, 17, 101, 173, 601, 2689
```

全部都是：

```text
1 mod 4.
```

没有 `3 mod 4` 坏素数。

---

## 4. tu-1 管道 witness

对：

```text
t=1/4, u=7/8
```

恢复值：

```text
x^2+1 = 11089/11025
y^2+1 = 481/225
```

平方类：

```text
11089 = 13 * 853
481 = 13 * 37
```

坏素数集合：

```text
13, 37, 853
```

也全部都是：

```text
1 mod 4.
```

没有 `3 mod 4` 坏素数。

---

## 5. 对证明路线的影响

这说明：

```text
bridge recovery layer 的 Q-square failure
不一定会暴露 q == 3 mod 4 的奇 valuation。
```

普通话说：

```text
在这一层，失败可以完全藏在 1 mod 4 素数里。
所以不能只靠 “找 3 mod 4 坏素数” 来证明 bridge recovery 不是全局平方。
```

这不是说用户原始目标中的 `q == 3 mod 4` 引理没戏。
它只说明：

```text
该引理不能直接套在 bridge recovery x^2+1, y^2+1 这一层。
```

下一步必须回到更完整的对象：

```text
r^2+1,
s^2+1,
r^2+lambda^2,
s^2+lambda^2,
B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2).
```

普通话说：

```text
要抓 3 mod 4 矛盾，不能只看 x,y 恢复平方。
要把 lambda 和 p=rs 拉回来。
```

---

## 6. 当前证明状态

可以安全说：

```text
1. 两个正参数 trivial-tube local witness 的全局 squareclass 已记录；
2. 它们的 squareclass obstruction 全在 1 mod 4 素数；
3. bridge recovery 层不能直接提供 q==3 mod 4 矛盾；
4. sum=A+B 仍未证明。
```

不能说：

```text
原始 q==3 mod 4 valuation 引理失败。
sum=A+B 已证明。
全平面倒数定理已证明。
```

---

## 7. 下一步

下一步建议切回原始变量：

```text
lambda = 1/D
r = x/D
s = y/D
p = rs
```

对 wl273 witness 记录完整四平方项：

```text
r^2+1,
s^2+1,
r^2+lambda^2,
s^2+lambda^2.
```

然后看它们的 squareclass primes 是否出现 `3 mod 4`。

普通话说：

```text
如果完整四平方项出现 3 mod 4 坏素数，
那就说明用户原始引理应该作用在 r,s,lambda 层，而不是 x,y bridge 层。
```

---

## 8. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_positive_trivial_tube_squareclass_ledgers_are_one_mod_four -q
```

结果：

```text
1 passed
```
