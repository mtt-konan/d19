# wl125 — `safe_sieve` coprime guard

日期：2026-06-09

## 1. 本轮问题

审计 H2 指出一个工程安全风险：

```text
classify_reduced_pair(A,B)
```

只对 reduced/coprime `(A,B)` sound，但 wrapper：

```text
run_safe_sieve(A,B)
```

之前没有检查：

```text
gcd(A,B) == 1
```

普通话说：

```text
底层筛子自己说“我只适合互素 pair”，
但外面的入口没有拦住非互素 pair。
```

这不一定已经造成错误 headline，但它会造成危险证书：

```text
非互素 pair 被 coprime-only safe_sieve 记成 terminal no_solution。
```

---

## 2. 具体风险样例

例子：

```text
(A,B) = (6,15)
gcd(A,B) = 3
```

底层 coprime-only 分类会给：

```text
classify_reduced_pair(6,15) = mixed_parity
```

但这个理由在非互素域不成立。

事实上 `(6,15)` 有 concordant：

```text
N = 8
```

所以不能用 coprime mod-12 推论直接拒掉它。

当前后续 full-plane 方法仍能处理它：

```text
run_chain_closure_mod_sieve(6,15) -> no_solution
```

但这必须由 full-plane/gcd-aware 方法给出，而不是由 coprime-only safe_sieve 给出。

---

## 3. 修改

文件：

```text
src/rational_distance/proof_status/methods.py
```

`run_safe_sieve` 现在先检查：

```text
pair_gcd = gcd(A,B)
```

若：

```text
pair_gcd != 1
```

返回：

```text
MethodResult(
    method="safe_sieve",
    outcome="skipped",
    details={
        "classification": "not_reduced_coprime",
        "gcd": pair_gcd,
        "precondition": "gcd(A,B)=1",
    },
)
```

也就是说：

```text
safe_sieve 不再对非互素 pair 给 no_solution。
workflow 会继续跑后续方法。
```

互素输入行为不变：

```text
(1,2) -> no_solution, mixed_parity
(1,5) -> no_solution, odd_odd_wrong_mod4
(1,3) -> pass
```

---

## 4. 新增测试

文件：

```text
tests/test_proof_status.py
```

新增：

```text
TestSafeSieveMethod.test_skips_noncoprime_pair_instead_of_certifying_no_solution
```

检查：

```text
run_safe_sieve(6,15).outcome == "skipped"
classification == "not_reduced_coprime"
gcd == 3
```

新增：

```text
TestWorkflow.test_noncoprime_safe_sieve_skip_does_not_terminate_pipeline
```

检查 workflow 行为：

```text
safe_sieve -> skipped
chain_closure_mod_sieve -> no_solution
```

也就是说，`skipped` 不会终结 pipeline。

---

## 5. 文档同步

更新：

```text
docs/audits/2026-06-07-theory-framework-audit/README.md
docs/audits/2026-06-07-theory-framework-audit/risk-register.md
docs/audits/2026-06-07-theory-framework-audit/branch-status.md
docs/audits/2026-06-07-theory-framework-audit/claim-ledger.md
```

H2 状态从：

```text
safe_sieve wrapper has no coprime guard
```

改为：

```text
mitigated: run_safe_sieve skips non-coprime input
```

仍保留边界：

```text
safe_sieve 的数学 soundness 只在 reduced/coprime input。
非互素 / full-space 仍要靠 gcd-aware 或 full-plane 方法。
```

---

## 6. 能说什么，不能说什么

可以说：

```text
H2 工程边界风险已缓解。
非互素 pair 不会再被 coprime-only safe_sieve 终结为 no_solution。
workflow 会继续后续方法。
```

不能说：

```text
非互素 / full-space 缺口已解决。
safe_sieve 现在对任意 (A,B) sound。
gcd-aware theorem 已经关闭全局问题。
```

这个改动只是防止误用，不是数学证明。

---

## 7. 验证

运行：

```text
uv run pytest tests/test_proof_status.py -q
```

结果：

```text
44 passed
```

本轮属于工程安全清理，目标是防止 reduced/coprime 结论被偷换成 full-space 结论。
