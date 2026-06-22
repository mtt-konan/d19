# wl293 — wl218 full-plane reciprocal goal closeout

日期：2026-06-23

## 1. 收尾结论

本轮目标没有完成“倒数定理”的证明。

可以安全保留的结论是：

```text
全平面倒数定理仍是四分支命题。
sum=A+B 只是第一分支，不是整个定理。
第一分支也尚未关闭。
```

普通话说：

```text
这次不是证明成功，而是把一条看起来很短的证明路试实了：
单靠 3 mod 4 赋值、单个 q-adic 条件、再加 2-adic 条件，
还不能把剩余影子分支关掉。
```

因此本目标应按“已形成边界和下一步入口”收尾，而不能标记为 proved。

---

## 2. 当前精确命题

固定：

```text
lambda in Q_{>0}
R_lambda = { r in Q_{>0} : r^2+1 和 r^2+lambda^2 都是有理平方 }
```

全平面闭合条件是：

```text
{r+s, |r-s|} intersect {lambda+1, |lambda-1|} nonempty
```

也就是四个分支：

```text
1. r+s   = lambda+1
2. r+s   = |lambda-1|
3. |r-s| = lambda+1
4. |r-s| = |lambda-1|
```

目标定理仍是：

```text
r,s in R_lambda
并且满足上述任一全平面闭合关系
=> rs=lambda
```

`sum=A+B` 对应第 1 支：

```text
r+s = lambda+1
```

它可以优先攻，但不能代替全平面命题。

---

## 3. 本轮已经固定下来的代数账本

对任一固定闭合分支，设：

```text
T = closure target
p = rs
epsilon = -1 for sum relations
epsilon = +1 for diff relations
```

乘积层账本是：

```text
A_p = p^2 + epsilon*2p + T^2 + 1
B_p = p^2 + epsilon*2lambda^2*p + lambda^2*T^2 + lambda^4
```

恒等式：

```text
B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2)
```

但必须保留真成员条件：

```text
r^2+1          square
s^2+1          square
r^2+lambda^2   square
s^2+lambda^2   square
```

普通话说：

```text
A_p 和 B_p 是影子账本。
它们能告诉我们乘积层哪里可能有问题，
但不能代替 r,s 自己真的在 R_lambda 里。
```

---

## 4. sum=A+B 分支当前边界

原希望的关键引理是：

```text
用 q == 3 mod 4 的赋值，
强制 lambda^2-p^2 的赋值矛盾，
除非 p=lambda。
```

现在必须改写。

当前更准确的状态是：

```text
q == 3,11 mod 16:
  shared compensation 分支死亡；

q == 7 mod 16:
  落到 p-lambda shadow；

q == 15 mod 16:
  留下 p+lambda shadow。
```

`p+lambda` shadow 已经被 wl288-wl292 进一步定位为：

```text
E-near q-adic/global problem
```

其中：

```text
q-adic norm generated samples:
  q=31,47,79 都有 8 个 roots mod q 和 8 个 lifts mod q^2；

bridge cycle:
  recovery squareclasses 与 Gaussian bridge squareclasses 对齐；

valuation:
  q^2 出现在 E 和 bridge difference 里，
  不出现在 centerline factors 和 bridge values 里；

2-adic:
  q=31 的样本被杀，
  q=47,79 仍有 Q_2 local-square survivors；

q-adic local square:
  q=47,79 的 Q_2 survivors 同时也通过 Q_q local-square。
```

普通话说：

```text
剩下这条缝不是“局部马上坏掉”的缝。
它更像是一条局部都能走过去、但可能全局走不通的通道。
```

---

## 5. 最新可复跑证据

最新测试覆盖：

```bash
PYTHONPATH=src uv run pytest \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_bridge_local_square_summary_keeps_survivors \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_bridge_2adic_summary_separates_parity_survivors \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_bridge_valuation_summary_tracks_e_near_tube \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_norm_bridge_summary_rewrites_recovery_as_bridges \
  -q
```

收尾时结果：

```text
4 passed
```

lint：

```bash
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

收尾时结果：

```text
All checks passed!
```

whitespace：

```bash
git diff --check -- \
  src/rational_distance/concordant/rational_ratio.py \
  tests/test_rational_ratio.py \
  docs/work-logs/292-wl218-qadic-bridge-local-square-survivors.md \
  docs/work-logs/293-wl218-full-plane-reciprocal-goal-closeout.md
```

收尾时结果：

```text
pass
```

---

## 6. 不能再走回去的说法

不能说：

```text
sum=A+B 已经证明；
倒数定理已经证明；
有限扫描没有反例，所以定理成立；
A_p,B_p 平方等价于 r,s in R_lambda；
单个 q-adic 高阶平方条件会自动杀掉 p+lambda shadow；
2-adic 条件会统一杀掉 E-near tube。
```

可以说：

```text
全平面口径已经纠正；
sum=A+B 是第一分支；
第一分支的硬点已缩到 p+lambda / E-near residual tube；
单素数局部条件已经不足；
下一步必须进入 global squareclass、multi-prime linkage、或 descent/curve argument。
```

---

## 7. 下次最短入口

推荐下一步不要继续只加单素数局部探针。

优先做：

```text
sum_ab_dual_slope_qadic_bridge_global_squareclass_summary(...)
```

对 combined Q_q + Q_2 survivors 记录：

```text
1. bridge squareclasses；
2. 所有分子分母素因子按 mod 4 / mod 8 / mod 16 分桶；
3. 是否总出现另一个 3 mod 4 素数；
4. 是否存在 bridge squareclass = 1 的真平方候选；
5. 每个 bucket 的最小代表。
```

如果没有统一坏素数，下一步就应转向：

```text
E-near survivor -> centerline / z-lemma pullback
```

或：

```text
E-near survivor -> smaller-height E-near survivor
```

普通话说：

```text
接下来要么找“另一个坏素数”；
要么证明这些幸存者会被迫递降回已经能处理的中线。
```

---

## 8. 目标状态

本目标收尾状态：

```text
not proved
not falsified
full-plane scope corrected
Branch 1 reduced to an E-near global/descent problem
Branches 2-4 still mandatory
```

当前处理决定：

```text
暂时放弃“单素数局部赋值 / q-adic bridge 自动关门”这条证明方向。
以后若重启 wl218，应从 global squareclass、multi-prime linkage、
或 descent/curve argument 进入，而不是继续沿着单 q 局部筛子加码。
```

这份 worklog 的作用是防止后续重复把局部筛子当证明。
