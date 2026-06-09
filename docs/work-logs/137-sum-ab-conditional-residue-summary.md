# wl137 — `sum=A+B` conditional residue summary

日期：2026-06-09

## 1. 本轮问题

wl136 发现：

```text
裸 residue-only 扫描太松。
奇素数单模数高度对称。
2 的幂有结构，但不能直接关掉分支。
```

这轮新增一个条件版 residue helper。

普通话说：

```text
之前是所有余数都放进来。
现在只保留更像真实 Euclid 参数的余数类。
```

---

## 2. 新增 helper

文件：

```text
src/rational_distance/concordant/rational_ratio.py
```

新增：

```text
sum_ab_euclid_conditional_residue_summaries(modulus=M)
```

它返回同一个：

```text
SumAbEuclidResidueSummary
```

但额外筛掉：

```text
gcd(m,n,M) != 1
gcd(u,v,M) != 1
m-n 偶数
u-v 偶数
选中的 slope denominator ≡ 0 mod M
选中的 scaled-term denominator ≡ 0 mod M
重构 other denominator ≡ 0 mod M
重构 failed denominator ≡ 0 mod M
```

注意：

```text
这是条件版诊断。
它不能替代 wl135 的 conservative helper。
```

---

## 3. `mod 24` 结果

新增测试固定：

```text
modulus=24
```

结果：

```text
odd/odd:
  total=24576
  other=16384
  failed=16384
  both=8192
  other_only=8192
  failed_only=8192
  neither=0

odd/even:
  total=16384
  other=0
  failed=0
  both=0
  neither=16384

even/odd:
  total=16384
  other=0
  failed=0
  both=0
  neither=16384

even/even:
  total=24576
  other=16384
  failed=16384
  both=8192
  other_only=8192
  failed_only=8192
  neither=0
```

普通话解释：

```text
在这些条件下，mod 24 直接排除了 mixed orientation。
odd/even 和 even/odd 里，other 和 failed 都不可能同时像平方；
事实上它们连单独像平方的类都没有。
```

这比 wl135 的裸 `mod 8` 信号强很多。

---

## 4. 一个抓到的小坑

实现过程中红灯测试抓到一个重要细节：

```text
分母非零不能检查 denominator == 0。
必须检查 denominator % modulus == 0。
```

因为：

```text
24, 48, 72 在整数里不是 0，
但在 mod 24 下都是 0。
```

这类细节如果写错，就会把不可逆 residue 当成合法类，导致筛子变得不安全。

---

## 5. 能说什么，不能说什么

可以说：

```text
条件版 mod 24 对 mixed orientation 给出强 obstruction 信号。
这支持继续研究 2-adic / mod 24 条件。
```

不能说：

```text
sum=A+B 分支已关闭。
odd/odd 或 even/even 已关闭。
条件版 residue helper 是完整证明。
```

原因：

```text
这是 residue 层诊断。
从 residue obstruction 到整数全证明，还需要严格说明这些条件覆盖了真实 Euclid 参数。
```

---

## 6. 下一步

建议下一步：

```text
1. 写一个 proof note，专门证明：
   primitive Euclid 参数在 mod 24 下会落入 conditional helper 保留的类。

2. 如果第 1 步成立，则 mixed orientation 可以尝试用 mod 24 关闭。

3. 对 odd/odd 和 even/even，继续看因式分解或更强的条件模数。
```

普通话说：

```text
mixed orientation 现在有了像样的突破口。
但真正证明前，必须先把“真实参数一定满足这些 residue 条件”写严谨。
```

---

## 7. 验证

运行：

```text
uv run pytest tests/test_rational_ratio.py::test_sum_ab_euclid_conditional_residue_summaries_apply_primitive_filters -q
uv run pytest tests/test_rational_ratio.py -q
uv run ruff check --select I,E402 src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```

结果：

```text
1 passed
24 passed
All checks passed
```
