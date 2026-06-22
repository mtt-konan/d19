# wl268 — wl218 bridge prime-power lift ledger

日期：2026-06-22

## 1. 本轮目标

接 wl267。

wl267 只在 `P^1(F_p) x P^1(F_p)` 上看了一阶 residue。结论是：

```text
p=5,11 时，both-bridge-square 且非 centerline 的 residue 全部落到 E=0。
```

本轮往上提升到 `p^2`，记录：

```text
(v_p(C), v_p(E))
```

其中：

```text
C = centerline factor = (t-u)(t+u)(tu-1)(tu+1)
E = bridge 差分的 extra factor.
```

普通话说：

```text
上一轮只知道“模 p 时必须贴着 C=0 或 E=0”。
这轮要看贴得有多深，以及会不会自动越来越深。
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopeBridgePrimePowerLiftSummary
```

新增 helper：

```text
sum_ab_dual_slope_bridge_prime_power_lift_summary(p, k)
```

它枚举局部环上的 projective line：

```text
P^1(Z/p^kZ)
```

使用规范代表：

```text
(x, 1),       x mod p^k
(1, p y),     y mod p^(k-1)
```

并在 `P^1 x P^1` 上记录：

```text
both_bridge_square_classes
valuation_pair_counts[(v_p(C), v_p(E))]
centerline_unit_extra_unit_classes
centerline_unit_min_extra_valuation
```

---

## 3. mod 25 结果

对 `p=5,k=2`：

```text
modulus = 25
projective_class_count = 900
both_bridge_square_classes = 295
```

估值对计数：

```text
(v5(C), v5(E)) = (0,2): 20
(v5(C), v5(E)) = (2,0): 175
(v5(C), v5(E)) = (2,1): 80
(v5(C), v5(E)) = (2,2): 20
```

特别是：

```text
v5(C)=0  =>  v5(E)>=2.
```

普通话说：

```text
如果不贴近中线，那么在 5-adic 意义下必须二阶贴近 E=0。
```

但也看到：

```text
v5(C)=2 且 v5(E)=0
```

大量存在。

普通话说：

```text
如果已经二阶贴近中线，E 可以完全不贴近 0。
所以不能只说“E 一定越来越小”。
```

---

## 4. mod 121 结果

对 `p=11,k=2`：

```text
modulus = 121
projective_class_count = 17424
both_bridge_square_classes = 4356
```

估值对计数：

```text
(v11(C), v11(E)) = (0,1): 880
(v11(C), v11(E)) = (0,2): 88
(v11(C), v11(E)) = (1,0): 2200
(v11(C), v11(E)) = (2,0): 704
(v11(C), v11(E)) = (2,1): 440
(v11(C), v11(E)) = (2,2): 44
```

特别是：

```text
v11(C)=0  =>  v11(E)>=1.
```

这里比 `p=5` 弱一阶，但仍没有 `(0,0)`。

---

## 5. 更高一点的 p=5 观察

对 `p=5,k=3`：

```text
modulus = 125
projective_class_count = 22500
both_bridge_square_classes = 4775
```

估值对计数：

```text
(0,2): 200
(0,3): 100
(2,0): 2000
(3,0): 1575
(3,1): 400
(3,2): 400
(3,3): 100
```

仍然有：

```text
v5(C)=0  =>  v5(E)>=2.
```

但没有提升成：

```text
v5(C)=0  =>  v5(E)>=3.
```

普通话说：

```text
5-adic 管道稳定在“E 至少二阶”，不是自动无限贴近。
所以还需要额外方程或另一个素数一起使用。
```

---

## 6. 当前证明状态

可以安全说：

```text
1. E=0 分支已归约到 centerline/Yang Ji；
2. E!=0 分支在 mod 5/11 一阶无普通非退化余类；
3. prime-power lifting 显示：
   - 若 C 是 5-adic 单位，则 E 至少二阶；
   - 若 C 是 11-adic 单位，则 E 至少一阶；
4. 贴近中线的管道仍然开放，E 可以是单位。
```

不能说：

```text
E!=0 分支已证明无解。
5-adic lifting 已经给出无限递降。
sum=A+B 已证明。
```

---

## 7. 下一步

现在应该分两条管道处理：

```text
A. C 是 p-adic 单位：
   利用 E 的强制可除性，加上 E=0 已归约到 centerline/Yang Ji，
   看能否从 E 的二阶/一阶邻域推出矛盾。

B. C 被 p 整除：
   直接展开 centerline factor 的四个因子
   (t-u),(t+u),(tu-1),(tu+1)，
   看 both-bridge-square 是否强迫向真正 centerline 递降。
```

普通话说：

```text
现在不是一个大门，而是两条窄管道。
下一步要分别证明：贴近 E=0 不行；贴近中线也不行。
```

---

## 8. 验证

已跑：

```text
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_dual_slope_bridge_prime_power_lift_tracks_centerline_extra_factor -q
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_dual_slope_bridge_prime_power_lift_tracks_centerline_extra_factor tests/test_rational_ratio.py::test_sum_ab_dual_slope_bridge_residue_summary_routes_mod5_11_to_extra_factor -q
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py -q
PYTHONPATH=src uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
git diff --check
```

结果：

```text
1 passed
2 passed
92 passed
All checks passed
git diff --check passed
```
