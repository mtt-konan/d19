# Closure Quotient Ray Scale Invariance

## Question

If `(A,B)=d(a,b)`, can the closure quotient work be reduced to the primitive
ray `(a,b)` instead of repeating the same analysis for every scale?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_ray_scale_invariance.py \
  --rank-jsonl results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --rank-jsonl results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --out results/closure_quotient_ray_scale_invariance_audit.json \
  --strict
```

## Output

```text
status=ok
observed_pair_count=384
observed_ray_count=356
multi_scale_ray_count=14
rank_row_count=1536
coefficient_identity_verified_count=1536
coefficient_identity_violation_count=0
rank_key_consistent_group_count=56
rank_key_inconsistent_group_count=0
```

## Interpretation

普通话说：对固定本原比例 `(a,b)`，把它放大成 `(A,B)=d(a,b)` 时，closure quotient
四次曲线只是同一条曲线的尺度版本。变量替换是：

```text
N = d n
y = d^2 y0
```

系数规则是：

```text
coeff_scaled[N^i] = d^(4-i) * coeff_primitive[n^i]
```

所以同一个本原 ray 上，不应该把不同 scale 当成新的数学对象。当前样本里有 14 个
multi-scale ray；四条 quotient 曲线合计 56 个 multi-scale rank-key group，观测 rank key
全部一致。

这一步把后续主线进一步压到本原 `lambda=A/B`。后面研究一个比例类时，重点应放在本原
ray 的结构证明，而不是沿同一 ray 继续增加 scale 样本。

## Boundary

This proves and audits the scaling identity for the stored quotient models. It
does not by itself prove that any lambda class has no closed point.
