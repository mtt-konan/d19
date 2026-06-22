# wl269 — wl218 bridge centerline-factor lift ledger

日期：2026-06-22

## 1. 本轮目标

接 wl268。

wl268 把 bridge-square 条件提升到 `p^k`，只记录：

```text
(v_p(C), v_p(E))
```

其中：

```text
C = (t-u)(t+u)(tu-1)(tu+1)
E = bridge 差分里的 extra factor
```

普通话说：

```text
上一轮知道“靠近中线”是一条大管道。
这轮把大管道拆开，看看它到底靠近哪一条中线因子。
```

本轮记录五元组：

```text
(v_p(t-u), v_p(t+u), v_p(tu-1), v_p(tu+1), v_p(E)).
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopeBridgeCenterlineFactorLiftSummary
```

新增 helper：

```text
sum_ab_dual_slope_bridge_centerline_factor_lift_summary(p, k)
```

它和 wl268 使用同一套枚举：

```text
P^1(Z/p^kZ) x P^1(Z/p^kZ)
```

并且同样先筛：

```text
k_x^2+1 square
k_y^2+1 square
```

区别只是把 `C` 拆成四个因子的 valuation。

---

## 3. mod 25 结果

对 `p=5,k=2`：

```text
modulus = 25
projective_class_count = 900
both_bridge_square_classes = 295
```

按：

```text
(max v5(C_i), v5(E))
```

聚合后：

```text
(0,2): 20
(1,0): 112
(1,1): 64
(2,0): 63
(2,1): 16
(2,2): 20
```

其中 `C_i` 分别是：

```text
t-u, t+u, tu-1, tu+1.
```

普通话说：

```text
如果四个中线因子全是 5-adic 单位，E 必须二阶可除。
但只要贴近任意中线因子，E 可以马上变成单位。
```

还出现了交叉管道，例如：

```text
(2,2,0,0,0): 2
(0,0,2,2,0): 2
(0,2,0,2,2): 2
```

普通话说：

```text
“贴近中线”不是一条线，而是四条局部线加少量交叉点。
后续不能只用 v(C) 一刀切。
```

---

## 4. mod 121 结果

对 `p=11,k=2`：

```text
modulus = 121
projective_class_count = 17424
both_bridge_square_classes = 4356
```

按：

```text
(max v11(C_i), v11(E))
```

聚合后：

```text
(0,1): 880
(0,2): 88
(1,0): 2600
(1,1): 400
(2,0): 304
(2,1): 40
(2,2): 44
```

普通话说：

```text
11-adic 情况更松：C 为单位时只强迫 E 至少一阶可除。
一旦贴近中线因子，E 同样可以是单位。
```

同样有交叉管道：

```text
(2,2,0,0,0): 2
(0,0,2,2,0): 2
```

---

## 5. 当前证明状态

可以安全说：

```text
1. wl268 的 C/E 二元账本已经细分成四因子账本；
2. C 为单位的管道仍然指向 E=0 邻域；
3. C 被 p 整除的管道必须拆成：
   t-u = 0,
   t+u = 0,
   tu-1 = 0,
   tu+1 = 0
   四个局部分支；
4. 四个分支还有交叉点，需要单独处理。
```

不能说：

```text
C-near branch 已经关闭。
E-near branch 已经关闭。
sum=A+B 已证明。
全平面倒数定理已证明。
```

---

## 6. 下一步

下一步不要再只看 `v_p(C)`。

应该分四张局部图：

```text
1. t = u + p^a h
2. t = -u + p^a h
3. tu = 1 + p^a h
4. tu = -1 + p^a h
```

分别把 both-bridge-square 的两个平方条件展开。

普通话说：

```text
现在要做的是“沿着四条中线附近放大看”。
如果每条线附近都会被迫落回真正 centerline/E=0，第一分支才可能关上。
```

---

## 7. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_dual_slope_bridge_centerline_factor_lift_splits_centerline_tubes -q
```

结果：

```text
1 passed
```
