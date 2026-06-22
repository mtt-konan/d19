# wl272 — wl218 positive domain separates exact trivial tubes

日期：2026-06-22

## 1. 本轮目标

接 wl271。

wl271 说明两条 trivial-square 管道：

```text
t+u = 0
tu-1 = 0
```

在 bridge-square 的 p-adic 意义下不是薄点，而是有局部厚度。

本轮补一个容易混淆但很重要的事实：

```text
这些管道的“中心线本身”并不在正参数闭环里。
```

普通话说：

```text
它们会在模 p 里冒出来，
但不是实际正有理参数 t,u 的真分支。
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopeCenterlineFactorPositiveDomainRow
```

新增 helper：

```text
sum_ab_dual_slope_centerline_factor_positive_domain(t)
```

它检查四条 exact 分支：

```text
u=t
u=-t
u=1/t
u=-1/t
```

是否满足双斜率正参数闭环的基本实数条件：

```text
0<t<1
0<u<1
a=(1-t^2)/(2t)>0
b=(1-u^2)/(2u)>0
D=a+b-ab>0
```

其中：

```text
x=b/D
y=a/D
```

需要 `D>0` 才回到正的 `x,y,L`。

---

## 3. 结果

对 `t=1/4`：

```text
t-u:   u=1/4   admissible
t+u:   u=-1/4  not in 0<u<1
tu-1:  u=4     not in 0<u<1, b<0
tu+1:  u=-4    not in 0<u<1
```

所以 exact 分支里，只有：

```text
t=u
```

能进入正参数闭环。

对 `t=1/5`，即使是 `u=t`：

```text
a=b=12/5
D=a+b-ab=-24/25<0
```

也不能进入正的反构造。

普通话说：

```text
中心线也不是每个 t 都合法；
它还要过 D>0 这一关。
```

---

## 4. 对证明路线的影响

现在可以把两件事分开：

```text
exact real branch:
  在正参数域里只剩 t=u，并回到 centerline/Yang Ji。

p-adic tube:
  t+u≈0 或 tu≈1 仍可在模 p 意义下出现，
  但它们不是 exact 正参数分支本身。
```

普通话说：

```text
trivial-square 管道是局部同余现象，不是几何上真的多出两条正分支。
```

这有助于防止后续证明误判：

```text
不能说 t+u=0 或 tu=1 给出真实候选；
只能说它们给出 p-adic 邻域里的幸存方向。
```

---

## 5. 当前证明状态

可以安全说：

```text
1. exact C_i=0 分支在正参数域中只剩 centerline 型；
2. trivial-square 两条线本身不是真正的正参数候选；
3. 但它们的 p-adic 邻域仍然开放，尚未关闭；
4. 因此 sum=A+B 还没有证明完。
```

不能说：

```text
trivial-square 管道已关闭。
sum=A+B 已证明。
全平面倒数定理已证明。
```

---

## 6. 下一步

下一步要处理的是：

```text
正参数点靠近 t+u=0 或 tu=1 的 p-adic 管道，
但不等于这些 exact 线。
```

可走的方向：

```text
1. 回到原始四平方 valuation，让 lambda 与 p=rs 参与；
2. 对 h 展开后的两个 square 方程做全局有理点分析；
3. 用实数区间 0<t,u<1 与 p-adic 接近条件组合，找 height/descent 约束。
```

---

## 7. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_centerline_factor_exact_branches_separate_positive_domain -q
```

结果：

```text
1 passed
```
