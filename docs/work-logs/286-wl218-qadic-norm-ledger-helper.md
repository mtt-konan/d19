# wl286 — wl218 q-adic norm ledger helper

日期：2026-06-23

## 1. 本轮目标

接 wl285。

wl285 建议不要再只看单个 q 的 Hensel lift，而要建立全局账本：

```text
Q(t), Q(u), x^2+1, y^2+1
```

一起看。

普通话说：

```text
现在的问题不是“31 这个素数自己会不会死”。
它不会。
问题变成：31 进入 Q(t),Q(u) 后，
其他素数的平方类账能不能一起平。
```

本轮把这个账本做成可复跑 helper。

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopeQAdicNormLedger
```

新增 helper：

```text
sum_ab_dual_slope_qadic_norm_ledger(t, u, prime=q)
```

它记录：

```text
Q(t), Q(u)
v_q(Q(t)), v_q(Q(u))
abs(Q(t)), abs(Q(u)) 的 squareclass
x^2+1, y^2+1 的 squareclass
v_q(x^2+1), v_q(y^2+1)
q 是否已经在恢复平方类中被偶次平衡掉
```

这里：

```text
Q(z) = z^4 - 4z^3 - 6z^2 + 4z + 1.
```

注意 `Q(t)` 是 `Q(sqrt(2))` 的 norm，可以为负数；
所以账本保留带符号值，但 squareclass 用 `abs(Q(t))`。

普通话说：

```text
范数可以带符号。
但平方类账本要看正的 squarefree 代表。
```

---

## 3. TDD 样本

测试样本取贴近 `q=31` 的 `mod 31^2` 分支：

```text
t = 61/77
u = 5/77
q = 31
```

账本输出：

```text
Q(t) = -41888068 / 35153041
Q(u) =  43356476 / 35153041

v_31(Q(t)) = 2
v_31(Q(u)) = 2
```

对应 squareclass：

```text
abs(Q(t)) squareclass = 10897 = 17 * 641
abs(Q(u)) squareclass = 11279
```

恢复平方类：

```text
x^2+1 squareclass = 545050311562
y^2+1 squareclass = 211590847301
```

且：

```text
v_31(x^2+1) = 0
v_31(y^2+1) = 0
31 不出现在两个恢复平方类中
```

普通话说：

```text
31 的影子已经在 Q(t),Q(u) 里成偶次平衡。
真正留下来的障碍转移到了其他素数的平方类上。
```

---

## 4. 对证明路线的影响

可以安全说：

```text
1. q-adic norm shadow 可以被全局账本追踪；
2. 在样本中，shadow prime q=31 不直接出现在恢复平方类；
3. 恢复平方类会出现新的大素数；
4. 单看 q 本身不足以矛盾，必须比较所有 squareclass prime。
```

不能说：

```text
这个 helper 证明了 p+lambda shadow 不可能。
这个样本代表所有 q-adic branch。
sum=A+B 已证明。
倒数定理已证明。
```

普通话说：

```text
我们现在有了秤，但还没称完整个货架。
```

---

## 5. 下一步

下一步可以把 helper 用到一批 q-adic 贴近样本上：

```text
for q == 15 mod16:
  lift F=E=0 branch to q^2 or q^3
  choose rational representatives with bounded denominator
  compute norm/recovery squareclass ledger
  look for universal squareclass transfer pattern
```

特别要检查：

```text
1. recovery squareclass primes 是否总避开 q；
2. 新出现的 primes 是否必须含 3 or 11 mod16；
3. 或者是否总是可由 Gaussian/norm absorption 吸收。
```

这会决定下一步走：

```text
多素数 valuation
```

还是：

```text
Gaussian/norm absorption descent
```

---

## 6. 验证

已按 TDD 跑过：

```bash
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_norm_ledger_tracks_shadow_squareclasses -q
```

先红：

```text
ImportError: cannot import name 'sum_ab_dual_slope_qadic_norm_ledger'
```

实现后变绿：

```text
1 passed
```

相关测试：

```bash
PYTHONPATH=src uv run pytest \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_valuation_ledger_tracks_3_mod_4_boundary \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_norm_ledger_tracks_shadow_squareclasses \
  tests/test_rational_ratio.py::test_sum_ab_shared_odd_prime_power_lift_summary_tracks_p_shadow \
  -q
```

输出：

```text
3 passed
```

格式检查：

```bash
git diff --check -- src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

通过。
