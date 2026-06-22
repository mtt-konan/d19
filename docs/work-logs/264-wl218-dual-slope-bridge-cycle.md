# wl264 — wl218 dual-slope bridge cycle ledger

日期：2026-06-22

## 1. 本轮目标

接 wl263。

wl263 已经说明单条 Gaussian bridge：

```text
failed slope F  ->  target dual slope T
k = (F - T)/(TF + 1)
```

会保留失败项的 squareclass。

本轮把两条交叉 bridge 同时放进一个闭环账本。

普通话说：

```text
如果 dual_x, dual_y 已经是好斜率，
那么 generated_x, generated_y 是否也是好斜率，
可以改看两条“角差桥”本身是不是好斜率。
```

这不是证明结束；这是把硬点换成了更小的角差闭环问题。

---

## 2. 记号

令：

```text
dual_x = a = (1 - t^2)/(2t)
dual_y = b = (1 - u^2)/(2u)
D = a + b - ab
x = b/D
y = a/D
```

这里 `a,b` 自动是勾股斜率。真正剩下的要求是：

```text
x^2 + 1 square
y^2 + 1 square
```

定义两条交叉 bridge：

```text
k_x = (x - b)/(bx + 1)   # x -> dual_y
k_y = (y - a)/(ay + 1)   # y -> dual_x
```

因为 `a,b` 已经是好斜率，tangent-subtraction 恒等式给出：

```text
squareclass(k_x^2+1) = squareclass(x^2+1)
squareclass(k_y^2+1) = squareclass(y^2+1)
```

所以：

```text
x,y 都是好斜率
<=>
k_x,k_y 都是好斜率
```

普通话说：

```text
四平方闭环没有消失；
它被挪到了两个角差 k_x,k_y 上。
```

---

## 3. 新 helper

新增 dataclass：

```text
SumAbDualSlopeGaussianBridgeCycle
```

新增 helper：

```text
sum_ab_dual_slope_gaussian_bridge_cycle(t, u)
```

它记录：

```text
x_to_dual_y
y_to_dual_x
generated_slopes = (x, y)
dual_slopes = (dual_x, dual_y)
bridge_ratios = (k_x, k_y)
generated_squareclasses
bridge_squareclasses
generated_pythagorean_flags
bridge_pythagorean_flags
generated_flags_match_bridge_flags
```

新增测试：

```text
test_sum_ab_dual_slope_gaussian_bridge_cycle_reduces_squares_to_bridges
```

固定样例：

```text
t = 1/4
u = 2/7

dual_x = 15/8
dual_y = 45/28
x = 24/7
y = 4

k_x = 357/1276
k_y = 1/4

generated_squareclasses = (1, 17)
bridge_squareclasses    = (1, 17)
```

因此这个样例只是一边好：

```text
x 是好斜率，k_x 也是好斜率；
y 不是好斜率，k_y 也不是好斜率。
```

---

## 4. 一个重要纠偏

原先的自然猜想是：

```text
k_y = t
k_x = u
```

这只在特殊点发生，不是恒等式。

符号检查给出：

```text
k_y - t = 0
```

等价于一个额外多项式因子消失：

```text
2t^3u - t^2u^2 - 2t^2u + t^2
- 2tu^2 - 2tu + 2t + u^2 + 2u - 1 = 0
```

在固定样例 `t=1/4, u=2/7` 中，这个因子确实为零，所以看起来像
`k_y=t`。

但另一边：

```text
k_x - u != 0
```

对应因子为：

```text
t^2u^2 + 2t^2u - t^2
- 2tu^3 + 2tu^2 + 2tu - 2t
- u^2 - 2u + 1
```

在同一样例中等于：

```text
-15/5488
```

普通话说：

```text
单桥回到参数，不是一般规律。
如果证明需要这个现象，必须证明平方约束会强迫对应额外因子消失；
否则这条路不能直接用。
```

---

## 5. 小范围反例优先扫描

运行一个只用于找模式的参数扫描：

```text
1 <= numerator < denominator <= 24
```

结论：

```text
both cross bridges pythagorean: 0
one-side bridge pythagorean:   164
```

注意这不是证明，只是说明：

```text
非中心真闭环没有在小参数池出现；
单边好桥很多，所以单边现象本身不够强。
```

---

## 6. 当前证明状态

可以安全说：

```text
1. dual-slope 四平方闭环已改写成两条 Gaussian cross bridge 同时为好斜率；
2. 样例 t=1/4,u=2/7 只是一边好，不是闭环；
3. k_y=t 不是通用恒等式，只是特殊额外因子消失；
4. 小范围扫描没有发现两条桥同时好的非中心候选。
```

不能说：

```text
sum=A+B 已证明。
全平面倒数定理已证明。
单条 bridge 的 Gaussian absorption 已经排除所有非中心闭环。
```

---

## 7. 下一步

下一步应直接研究：

```text
k_x^2+1 square
k_y^2+1 square
```

在 `t,u` 平面上的共同约束。

最想要的引理是：

```text
k_x,k_y 都是勾股斜率
=> centerline_factor = (t-u)(t+u)(tu-1)(tu+1) = 0
```

在正参数范围内，这会把非退化情况压到：

```text
t = u
```

也就是回到 centerline。

---

## 8. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py -q
PYTHONPATH=src uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
git diff --check
```

结果：

```text
88 passed
All checks passed
git diff --check passed
```
