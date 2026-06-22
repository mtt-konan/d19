# wl288 — wl218 q-adic generated shadow summary

日期：2026-06-23

## 1. 本轮目标

接 wl287。

wl287 的样本还是手工挑的。本轮把样本来源改成可复跑生成器：

```text
q == 15 mod 16
F(t,u) = 0 mod q
E(t,u) = 0 mod q
lift 到 q^e
找有界正有理代表
再跑 q-adic norm summary
```

普通话说：

```text
之前是拿两颗石子看纹路。
现在先做一个小筛子，自动从同一条 q-adic 影子分支里捞石子。
```

这仍然不是证明。它只是把“p+lambda shadow 到底带不带 3 mod 4 坏素数”
变成可复跑的诊断。

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopeQAdicNormGeneratedSummary
```

新增 helper：

```text
sum_ab_dual_slope_qadic_norm_generated_summary(
    prime=q,
    exponent=e,
    representative_bound=H,
    sample_limit=N,
)
```

它做四件事：

```text
1. 枚举 F=E=0 mod q 的有序根；
2. 逐层 lift 到 q^e；
3. 对每个 residue pair 找小高度正有理代表；
4. 复用 sum_ab_dual_slope_qadic_norm_summary 做 squareclass 统计。
```

实现上只保留能进入现有 dual-slope 正参数 chart 的样本。也就是说：

```text
t > 0, u > 0,
(1-t^2)/(2t) > 0,
(1-u^2)/(2u) > 0,
dual denominator > 0.
```

普通话说：

```text
不只是模 q^2 看起来对；
还要它真的落进当前四平方模型正在看的正斜率区域。
```

---

## 3. q=31 的生成输出

命令：

```bash
PYTHONPATH=src uv run python - <<'PY'
from rational_distance.concordant.rational_ratio import (
    sum_ab_dual_slope_qadic_norm_generated_summary,
)

s = sum_ab_dual_slope_qadic_norm_generated_summary(
    prime=31,
    exponent=2,
    representative_bound=80,
    sample_limit=8,
)
print(s.root_count_mod_prime)
print(s.lift_count)
print(s.lifted_residue_pairs)
print(s.parameter_pairs)
print(s.summary)
PY
```

核心输出：

```text
root_count_mod_prime = 8
lift_count = 8

lifted_residue_pairs =
((46, 362), (46, 369), (188, 362), (188, 369),
 (362, 46), (362, 188), (369, 46), (369, 188))

parameter_pairs =
((61/64, 5/77),
 (5/21, 45/47),
 (20/41, 5/77),
 (20/41, 45/47),
 ...)
```

summary：

```text
sample_count = 8
shadow_prime_balanced_count = 8
recovery_contains_shadow_prime_count = 0
recovery_has_three_mod_four_prime_count = 0
recovery_has_only_two_or_one_mod_four_primes_count = 8
q_norm_valuation_pair_counts = {(2, 2): 8}
```

一个代表样本：

```text
(t,u) = (5/21, 45/47)
v_31(Q(t)), v_31(Q(u)) = (2, 2)

recovery squareclasses:
  236448154  = 2 * 118224077
  23675727721 = 37 * 639884533
```

注意：

```text
31 不在 recovery squareclass 里；
这些 recovery squareclass primes 没有 3 mod 4 素数。
```

---

## 4. q=47,79 的同类探针

同一生成器也跑了 `q=47,79`：

```text
q=47, representative_bound=220, sample_limit=8
root_count_mod_prime = 8
lift_count = 8
sample_count = 8
q_norm_valuation_pair_counts = {(2, 2): 8}
recovery_contains_shadow_prime_count = 0
recovery_has_three_mod_four_prime_count = 0
recovery_has_only_two_or_one_mod_four_primes_count = 8

q=79, representative_bound=260, sample_limit=8
root_count_mod_prime = 8
lift_count = 8
sample_count = 8
q_norm_valuation_pair_counts = {(2, 2): 8}
recovery_contains_shadow_prime_count = 0
recovery_has_three_mod_four_prime_count = 0
recovery_has_only_two_or_one_mod_four_primes_count = 8
```

代表样本：

```text
q=47:
  (t,u) = (17/35, 59/75)
  recovery squareclass primes:
    (41, 197, 833477)
    (2, 6569, 43574317)

q=79:
  (t,u) = (151/176, 37/41)
  recovery squareclass primes:
    (49534091492857)
    (2, 12497, 1403869)
```

普通话说：

```text
这不是 q=31 的偶然小把戏。
至少 q=31,47,79 的 q^2 影子样本都表现成：
shadow prime 被偶次吸收，恢复平方类只剩 2 和 1 mod 4 素数。
```

新增 summary 字段还把 recovery squareclass primes 按模类分桶：

```text
q=31, sample_limit=8
mod4  = {1: 32, 2: 8}
mod8  = {1: 16, 2: 8, 5: 16}
mod16 = {1: 6, 2: 8, 5: 10, 9: 10, 13: 6}

q=47, sample_limit=8
mod4  = {1: 42, 2: 6}
mod8  = {1: 26, 2: 6, 5: 16}
mod16 = {1: 16, 2: 6, 5: 8, 9: 10, 13: 8}

q=79, sample_limit=8
mod4  = {1: 42, 2: 4}
mod8  = {1: 18, 2: 4, 5: 24}
mod16 = {1: 10, 2: 4, 5: 10, 9: 8, 13: 14}
```

这里按“出现次数”计数，不是按 distinct prime 计数。普通话说：

```text
剩下的奇素数全都在 1 mod 4；
再细分到 mod8，它们只落在 1 或 5。
所以 3 mod 4 的门确实没在这批样本里出现，真正剩下的是：
Gaussian 可吸收的 1 mod 4 素数 + 2-adic parity。
```

---

## 5. 对关键引理的影响

用户原始关键引理希望：

```text
用各 q == 3 mod 4 的赋值，
强制 lambda^2-p^2 的赋值矛盾，
除非 p=lambda。
```

本轮给出的更强边界是：

```text
在 q=31,47,79 的 p+lambda shadow 分支上，
自动生成的 q^2 贴近样本仍然可以让 q 在 Q(t),Q(u) 中偶次出现；
同时 q 不进入恢复平方类；
恢复平方类也可以完全没有 3 mod 4 素数。
```

普通话说：

```text
3 mod 4 赋值像是能找到影子的位置，
但它没能把影子钉死。
这条管道上的坏东西很会把 shadow prime 吸收掉，
然后把剩余障碍转移到 2 和 1 mod 4 素数里。
```

因此，单靠当前形式的 `q == 3 mod 4` 赋值账本，不足以关闭
`p+lambda` shadow。

---

## 6. 现在能说和不能说

可以安全说：

```text
1. p+lambda shadow 已有自动生成样本源；
2. q=31,47,79 的 q^2 正 chart 样本都复现 wl287 的模式；
3. shadow prime q 在 Q(t),Q(u) 中成对偶次出现；
4. recovery squareclass 不含 shadow prime，也不含 3 mod 4 素数；
5. 原来的 3 mod 4 赋值路线在这个分支上还缺最后门闩。
```

不能说：

```text
sum=A+B 已证明；
p+lambda shadow 已关闭；
所有 q == 15 mod 16 都有同样全局 squareclass 模式；
倒数定理已证明。
```

---

## 7. 下一步

证明路线应从“继续期待 3 mod 4 一刀切”改成两条并行问题：

```text
1. Gaussian/norm absorption:
   解释为什么 recovery squareclass 只剩 2 和 1 mod 4 素数时，
   是否会被 Gaussian 角度吸收成已有 dual-slope bridge/cycle。

2. 2-adic 分配:
   如果 3 mod 4 素数不负责关门，
   检查 2-adic parity 是否在 full four-square loop 中强制矛盾。
```

更具体的下一步：

```text
1. 检查 Gaussian bridge/cycle 是否解释这些 1 mod 4 素数；
2. 对剩余 2-adic parity 写独立 ledger；
3. 把关键引理改写为 norm/Gaussian/2-adic 三段式，
   而不是单段 3 mod 4 赋值矛盾。
```

---

## 8. 验证

TDD 过程：

```bash
PYTHONPATH=src uv run pytest \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_norm_generated_summary_expands_shadow_samples \
  -q
```

先红：

```text
ImportError: cannot import name 'sum_ab_dual_slope_qadic_norm_generated_summary'
```

实现后：

```text
1 passed
```

相关测试：

```bash
PYTHONPATH=src uv run pytest \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_norm_ledger_tracks_shadow_squareclasses \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_norm_summary_counts_recovery_prime_patterns \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_norm_generated_summary_expands_shadow_samples \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_norm_generated_summary_tries_multiple_representatives \
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_valuation_ledger_tracks_3_mod_4_boundary \
  tests/test_rational_ratio.py::test_sum_ab_shared_odd_prime_power_lift_summary_tracks_p_shadow \
  -q
```

输出：

```text
6 passed
```
