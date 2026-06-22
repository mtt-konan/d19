# wl287 — wl218 q-adic norm summary boundary

日期：2026-06-23

## 1. 本轮目标

接 wl286。

wl286 给了单个样本的 q-adic norm ledger。本轮把它扩成小批量 summary，
看 `p+lambda` shadow 附近的恢复平方类是否稳定出现：

```text
q 本身；
3 mod 4 素数；
只有 2 或 1 mod 4 素数。
```

普通话说：

```text
我们不只称一个样本。
现在先称一小篮样本，看秤上有没有稳定模式。
```

---

## 2. 新 helper

新增 dataclass：

```text
SumAbDualSlopeQAdicNormSummary
```

新增 helper：

```text
sum_ab_dual_slope_qadic_norm_summary(parameter_pairs, prime=q)
```

它聚合 `sum_ab_dual_slope_qadic_norm_ledger(...)`，统计：

```text
sample_count
shadow_prime_balanced_count
recovery_contains_shadow_prime_count
recovery_has_three_mod_four_prime_count
recovery_has_only_two_or_one_mod_four_primes_count
q_norm_valuation_pair_counts
examples_by_bucket
```

普通话说：

```text
这个 helper 不证明定理。
它只是把“有没有 3 mod 4 坏素数”这种问题从肉眼看输出，
变成可复跑的账本统计。
```

---

## 3. TDD 样本

测试使用两个贴近 `q=31` 的 `mod 31^2` 分支样本：

```text
(t,u) = (61/77, 5/77)
(t,u) = (20/41, 5/77)
```

summary 输出锁定为：

```text
sample_count = 2
shadow_prime_balanced_count = 2
recovery_contains_shadow_prime_count = 0
recovery_has_three_mod_four_prime_count = 0
recovery_has_only_two_or_one_mod_four_primes_count = 2
q_norm_valuation_pair_counts = {(2,2): 2}
```

普通话说：

```text
这两个样本里，31 在 Q(t),Q(u) 里都是偶次；
恢复平方类里没有 31，也没有 3 mod 4 素数。
剩下的障碍来自 2 和 1 mod 4 素数。
```

---

## 4. 对原关键引理的影响

用户原始希望是：

```text
用各 p == 3 mod 4 的赋值，
强制 lambda^2-p^2 的赋值矛盾。
```

现在对 `p+lambda` shadow 的边界更清楚：

```text
q == 15 mod16 的 shadow prime q 本身是 3 mod 4；
但在这些全局贴近样本里，它不出现在恢复平方类中；
恢复平方类甚至可以完全没有 3 mod 4 素数。
```

普通话说：

```text
3 mod 4 赋值仍然是重要入口，
但在 p+lambda 管道上，它很可能只负责定位影子，
不负责最终关门。
真正的门闩可能在 2 和 1 mod 4 的 norm/Gaussian 分配里。
```

这与 wl234 的旧观察一致：

```text
same-orientation near-miss 的失败 squareclass
经常来自 1 mod 4 素数或含 2 的组合。
```

---

## 5. 当前状态

可以安全说：

```text
1. 已有可复跑 summary 统计 q-adic norm shadow 的恢复平方类模式；
2. q=31 的两个贴近样本都没有恢复平方类里的 3 mod 4 素数；
3. 单靠 3 mod 4 赋值不太可能直接关闭 p+lambda 管道；
4. sum=A+B 仍未证明。
```

不能说：

```text
p+lambda shadow 已关闭。
所有 q==15 mod16 样本都只有 2 或 1 mod4 素数。
原关键引理完全失败。
sum=A+B 已证明。
倒数定理已证明。
```

普通话说：

```text
这不是终点，是转向牌。
```

---

## 6. 下一步

下一步应扩大 summary 的输入来源，而不是手写少量样本。

建议：

```text
1. 生成 q==15 mod16 的 F=E=0 mod q 根；
2. lift 到 q^2；
3. 构造一批正参数有理代表；
4. 跑 sum_ab_dual_slope_qadic_norm_summary；
5. 按 recovery squareclass prime 的 mod4/mod8/mod16 分类。
```

如果继续看到：

```text
recovery_has_three_mod_four_prime_count = 0
```

那证明路线应明确转向：

```text
Gaussian / norm absorption / 2-adic 分配。
```

而不是继续期待 `3 mod 4` 赋值一刀切。

---

## 7. 验证

TDD 过程：

```bash
PYTHONPATH=src uv run pytest tests/test_rational_ratio.py::test_sum_ab_dual_slope_qadic_norm_summary_counts_recovery_prime_patterns -q
```

先红：

```text
ImportError: cannot import name 'sum_ab_dual_slope_qadic_norm_summary'
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
  tests/test_rational_ratio.py::test_sum_ab_dual_slope_valuation_ledger_tracks_3_mod_4_boundary \
  tests/test_rational_ratio.py::test_sum_ab_shared_odd_prime_power_lift_summary_tracks_p_shadow \
  -q
```

输出：

```text
4 passed
```
