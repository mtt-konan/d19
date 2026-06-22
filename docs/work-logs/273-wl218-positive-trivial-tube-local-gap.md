# wl273 — wl218 positive trivial-tube local gap

日期：2026-06-22

## 1. 本轮目标

接 wl272。

wl272 说明：

```text
t+u=0
tu-1=0
```

这两条 exact 线本身不在正参数闭环里。

但这还不够。真正要处理的是：

```text
正参数点可以 p-adically 靠近这些线。
```

普通话说：

```text
线本身不是真的，但线附近的同余邻域可能是真的。
如果这些邻域还能通过局部平方检查，单靠一个素数的 valuation 就关不掉。
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopePositiveTrivialTubeLocalWitness
```

新增 helper：

```text
sum_ab_dual_slope_positive_trivial_tube_local_witnesses()
```

它返回两个固定 witness。

这些 witness 不是定理反例；它们只是说明：

```text
正参数 + p-adic tube + Q_p-square
```

仍然不等于：

```text
全局有理平方。
```

---

## 3. t+u 管道 witness

取：

```text
t = 1/4
u = 19/24
```

则：

```text
0<t,u<1
D = 12175/7296 > 0
t+u = 25/24
v_5(t+u)=2
```

反构造得到：

```text
x = 344/2435
y = 2736/2435
```

恢复平方值：

```text
x^2+1 = 6047561/5929225
y^2+1 = 13414921/5929225
```

它们满足：

```text
Q_5 中都是平方；
Q 中都不是平方。
```

普通话说：

```text
这是一个真的正参数点，也真的靠近 t+u=0 的 5-adic 管道。
但它只是假局部成功，不是真有理解。
```

---

## 4. tu-1 管道 witness

取：

```text
t = 1/4
u = 7/8
```

则：

```text
0<t,u<1
D = 225/128 > 0
tu-1 = -25/32
v_5(tu-1)=2
```

反构造得到：

```text
x = 8/105
y = 16/15
```

恢复平方值：

```text
x^2+1 = 11089/11025
y^2+1 = 481/225
```

它们满足：

```text
Q_5 中都是平方；
Q 中都不是平方。
```

普通话说：

```text
这说明 tu≈1 的局部管道同样有正参数幸存点。
但这些点仍然不是真全局四平方闭环。
```

---

## 5. 对证明路线的影响

现在有一个更明确的边界：

```text
positive real domain + one-prime local square tests
```

仍然太弱。

所以不能指望只用：

```text
v_5(t+u) large
or
v_5(tu-1) large
```

来推出矛盾。

普通话说：

```text
5-adic 看起来像平方，不代表真的是有理平方。
下一步必须把所有坏素数的平方类一起看，或者回到原始四平方 identity。
```

---

## 6. 当前证明状态

可以安全说：

```text
1. trivial-square 管道的 exact 线不在正参数域；
2. 但其 5-adic 邻域和正参数域确实有交集；
3. 这些交点能通过 Q_5 的两个恢复平方测试；
4. 它们不能通过全局 Q-square 测试；
5. 因此单素数局部 valuation 路线仍不足以关闭 sum=A+B。
```

不能说：

```text
trivial-square 管道已关闭。
sum=A+B 已证明。
全平面倒数定理已证明。
```

---

## 7. 下一步

下一步有两条更实在的路：

```text
A. 全局平方类路：
   对正参数 trivial-tube 点，记录所有 recovery squareclass primes，
   看是否必然出现某个 q=3 mod 4 的奇 valuation。

B. 原始 identity 路：
   回到 B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2)，
   把四个真成员平方条件同时纳入，而不是只看 bridge-square。
```

普通话说：

```text
下一步不能只盯一个 p-adic 管道。
要么全局数所有平方类，要么回到 lambda,p 的原始恒等式。
```

---

## 8. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_positive_trivial_tube_local_witnesses_show_5adic_gap -q
```

结果：

```text
1 passed
```
