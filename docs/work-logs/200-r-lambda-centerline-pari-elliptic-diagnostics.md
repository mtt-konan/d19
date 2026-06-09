# wl200 — centerline PARI elliptic diagnostics

日期：2026-06-09

## 1. 本轮目标

wl199 说明：

```text
继续换参数会得到新的自相似四次式。
```

所以本轮停止绕参数，改问：

```text
PARI 能不能直接把中心线四次曲线转成椭圆曲线？
```

结论：

```text
可以。
而且两个相关四次式都落到 rank 0 的椭圆曲线。
```

普通话说：

```text
中心线终于接上了“列尽有理点”的工具链。
```

---

## 2. 新 helper

新增：

```text
sum_ab_centerline_quartic_pari_diagnostics()
```

返回：

```text
SumAbCenterlineQuarticPARIDiagnostics
```

记录：

```text
available
centerline_model
centerline_rank_bounds
centerline_sha2_lower
centerline_generators
centerline_torsion_order
centerline_small_points
w_parameterized_model
w_parameterized_rank_bounds
w_parameterized_sha2_lower
w_parameterized_generators
w_parameterized_torsion_order
w_parameterized_small_points
proof_status
notes
```

如果 `cypari2` 不可用：

```text
available = False
proof_status = "pari-unavailable"
```

---

## 3. 原中心线四次式

四次式：

```text
Q(t)=t^4+8t^3+18t^2-8t+1
```

PARI：

```text
ellfromeqn(y^2 - Q(x))
```

给出 Weierstrass 模型：

```text
[0, 18, 0, -68, 56]
```

也就是：

```text
Y^2 = X^3 + 18X^2 - 68X + 56
```

PARI 诊断：

```text
ellrank effort 0 -> [0, 0, 0, []]
ellrank effort 1 -> [0, 0, 0, []]
ellrank effort 2 -> [0, 0, 0, []]
torsion order    -> 4
small points     -> (-2,16), (-2,-16), (2,0)
```

普通话说：

```text
这条椭圆曲线 rank 0。
所以有理点全在 torsion 里。
```

---

## 4. W 参数化后的四次式

wl199 的剩余四次式：

```text
R(a)=5a^4-8a^3-6a^2+8a+5
```

PARI：

```text
ellfromeqn(y^2 - R(x))
```

给出：

```text
[0, -6, 0, -164, 1240]
```

也就是：

```text
Y^2 = X^3 - 6X^2 - 164X + 1240
```

PARI 诊断：

```text
ellrank effort 1 -> [0, 0, 0, []]
torsion order    -> 4
small points     -> (6,16), (6,-16), (10,0)
```

普通话说：

```text
换参数后的那条四次曲线也不是随机高秩怪物；
它同样是 rank 0 torsion-only。
```

---

## 5. 这有多强

可以说：

```text
中心线剩余四次曲线已经有 PARI 可识别的椭圆曲线模型。
PARI 认证这两个模型 rank = 0。
有限高度搜索之外，现在有了 rank/torsion 方向。
```

不能说：

```text
centerline 已经严格证明无解。
Q(t) 的有理点已经在本地 proof note 里列尽。
```

原因：

```text
ellfromeqn 给出了模型，
但本轮还没有写出 quartic <-> Weierstrass 的显式双有理映射。
```

普通话说：

```text
我们知道椭圆曲线那边只有 torsion，
但还要把 torsion 点明确拉回到 t 这边，
确认只得到显然点或退化点。
```

---

## 6. 当前 proof status

helper 里记录：

```text
proof_status = "needs-birational-pullback"
```

意思是：

```text
工具证据很强，
但还差最后一段人工可读证明。
```

这符合项目纪律：

```text
不要把计算诊断直接写成定理。
```

---

## 7. 下一步

最直接下一步：

```text
1. 找 PARI/手算的 ellfromeqn 双有理映射。
2. 把椭圆曲线 torsion 点 (-2,±16), (2,0) 拉回 Q(t)。
3. 验证只对应 (t,Y)=(0,±1) 或无效/无穷远点。
4. 写 centerline proof note。
```

如果 PARI 不直接给映射：

```text
手工用基点 (t,Y)=(0,1) 的割线法推 birational map。
```

普通话总结：

```text
中心线现在很接近被关掉：
不是靠模筛，
而是靠 rank 0 椭圆曲线。
但最后一步必须把映射写清楚。
```

---

## 8. 验证

已跑：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_centerline_remaining_quartic_matches_lambda_leg_value -q
```

结果：

```text
1 passed
```

后续还需要跑：

```text
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
uv run pytest tests/test_rational_ratio.py -q
uv run pytest -q
```
