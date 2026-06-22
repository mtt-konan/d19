# wl271 — wl218 trivial-square tube expansion boundary

日期：2026-06-22

## 1. 本轮目标

接 wl270。

wl270 把四条 `C_i=0` 管道分成两类：

```text
centerline-quartic:
  t-u = 0
  tu+1 = 0

trivial-square:
  t+u = 0
  tu-1 = 0
```

本轮只看两条 trivial-square 管道：

```text
u = -t + h
u = 1/t + h
```

普通话说：

```text
这两条线本身不会被 bridge-square 条件杀掉。
所以要看离开这条线一点点时，平方条件会不会立刻产生新矛盾。
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopeBridgeTrivialTubeExpansion
```

新增 helper：

```text
sum_ab_dual_slope_bridge_trivial_tube_expansions(t)
```

它把 bridge numerator 多项式代入：

```text
u = base + h
```

并返回：

```text
X(h), Y(h), E(h), X(h)-Y(h)
```

的精确有理系数。

---

## 3. 管道 t+u=0

令：

```text
S = (t-1)(t+1)(t^2+1).
```

代入：

```text
u = -t + h
```

常数项为：

```text
X(0) = Y(0) = S^2.
```

一阶差为：

```text
X(h)-Y(h)
  = -8t(t-1)(t+1)(t^2+1) h
    + 4(5t^4-1) h^2
    + ...
```

额外因子：

```text
E(h)
  = (t-1)^2(t+1)^2
    + (-2t^3 - t^2 + 2t - 1) h
    + (t^2+t-1) h^2.
```

普通话说：

```text
在这条管道上，X 和 Y 的共同起点就是一个平方。
如果 h 在某个奇素数 p 下很小，且 S 是 p-adic 单位，
那么 X 和 Y 会自动留在平方邻域里。
```

---

## 4. 管道 tu-1=0

同样令：

```text
S = (t-1)(t+1)(t^2+1).
```

代入：

```text
u = 1/t + h
```

常数项为：

```text
X(0) = Y(0) = S^2 / t^4.
```

一阶差为：

```text
X(h)-Y(h)
  = -8(t-1)(t+1)(t^2+1) h / t
    + 4(5-t^4) h^2
    + ...
```

额外因子：

```text
E(h)
  = -(t-1)^2(t+1)^2 / t^2
    + (t^3+2t^2+t-2)h/t
    + (t^2+t-1) h^2.
```

普通话说：

```text
这条管道也一样，X 和 Y 的共同起点是平方。
所以只靠“接近 tu=1”不能推出 p-adic 矛盾。
```

---

## 5. 对 valuation 路线的影响

这轮给出一个负面但重要的边界：

```text
trivial-square 管道在好素数处是 p-adic 开的。
```

更具体地说，若 `p` 是奇素数，且不除共同平方根的分子/分母，
那么：

```text
v_p(h) > 0
```

会让：

```text
X(h) = square * (1 + p-adically small)
Y(h) = square * (1 + p-adically small)
```

因此 `X(h)`、`Y(h)` 在 `Q_p` 中仍是平方。

普通话说：

```text
这两条管道不是“模数再升一层就会死”的类型。
它们局部真的有厚度。
```

所以原来的 valuation 方案如果只看 bridge-square 条件，不能关闭这两条管道。
下一步必须引入额外信息，例如：

```text
1. 回到 x,y,a,b 全四斜率，而不只看 bridge numerator；
2. 利用正有理参数区间 0<t,u<1 对 u=-t 和 u=1/t 的实数排斥；
3. 找全局有理平方条件，而不是只做 p-adic local square；
4. 或回到原始 A_p/B_p 四平方 valuation，把 lambda 与 p=rs 一起纳入。
```

---

## 6. 当前证明状态

可以安全说：

```text
1. trivial-square 管道的 h 展开已精确记录；
2. 两条管道的 bridge-square 常数项都是非零平方；
3. 这解释了 wl268/wl269 中 C-near 且 E-unit 的局部幸存；
4. 单靠 bridge-square 的 p-adic lifting 不能关闭这两条管道。
```

不能说：

```text
sum=A+B 已证明。
trivial-square 管道已关闭。
全平面倒数定理已证明。
```

---

## 7. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_bridge_trivial_tube_expansions_have_square_base -q
```

结果：

```text
1 passed
```
