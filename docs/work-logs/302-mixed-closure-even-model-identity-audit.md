# wl302 - mixed closure even-model identity audit

日期：2026-07-07

## 一句话结论

`AA/BB rank=0` torsion 回拉引理里的核心代数公式现在有符号审计脚本。

普通话说：论文里用到的中心化四次曲线公式、四次到椭圆曲线的映射、反向映射，不再只靠手写推导；
脚本会用 SymPy 检查恒等式。

## 新增脚本

```text
scripts/theory/audit_mixed_closure_even_model_identities.py
tests/test_mixed_closure_even_model_identity_audit.py
```

命令：

```bash
uv run python scripts/theory/audit_mixed_closure_even_model_identities.py \
  --out results/mixed_closure_even_model_identity_audit.json \
  --strict
```

结果：

```text
wrote even-model identity audit to results/mixed_closure_even_model_identity_audit.json
all_verified=True
```

## 审计的恒等式

### 1. 中心化偶四次

设：

```text
S = A+B
t = 2N-S
z = 4y
```

脚本验证：

```text
16*(N^2+L^2)*((S-N)^2+L^2)
= t^4 + p*t^2 + q
```

其中：

```text
p = 8L^2 - 2S^2
q = (S^2 + 4L^2)^2
```

### 2. 四次到椭圆曲线

对：

```text
z^2 = t^4 + p*t^2 + q
```

脚本验证：

```text
X = 2*(z+t^2)
V = 2*t*(X+p)
```

会落在：

```text
V^2 = X^3 + pX^2 - 4qX - 4pq
```

### 3. 反向公式

脚本验证：

```text
t = V/(2*(X+p))
z = X/2 - t^2
```

在 `X+p != 0` 时把椭圆曲线点送回原四次。

## 边界

这个脚本只审计代数公式：

```text
all_verified=True
```

不表示：

- rank 已认证；
- torsion 枚举已完成；
- residual cover 没有有理点；
- Harborth 猜想已证明。

它只是把 partial result 的主引理公式固定住，防止论文草稿里公式漂移。

## 接入

`audit_closure_quotient_paper_claims.py` 现在也检查：

```text
even_model_identities_verified = 1
```

也就是说，paper-level claim gate 会同时看：

- rank/certificate summary；
- rank-0 certificate audit；
- even-model identity audit；
- residual cover summary；
- BSD 条件诊断。

## 验证

```bash
uv run pytest tests/test_mixed_closure_even_model_identity_audit.py -q
uv run ruff check \
  scripts/theory/audit_mixed_closure_even_model_identities.py \
  tests/test_mixed_closure_even_model_identity_audit.py
```

结果：

```text
3 passed
All checks passed!
```
