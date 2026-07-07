# Rank-Zero Family Obligations

## Question

After the lambda convergence audit says rank-zero is first, what exactly is
missing before those seeds become family theorems?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_family_obligations.py \
  --convergence-priorities results/closure_quotient_lambda_convergence_priorities.json \
  --rank-zero-seeds results/closure_quotient_rank_zero_proof_seeds.json \
  --primitive-models results/closure_quotient_rank_zero_primitive_models.json \
  --identity-audit results/closure_quotient_rank_zero_seed_identity_audit.json \
  --invariants results/closure_quotient_rank_zero_certifying_invariants.json \
  --forced-torsion results/closure_quotient_rank_zero_forced_torsion_audit.json \
  --out results/closure_quotient_rank_zero_family_obligations.json \
  --strict
```

## Output

```text
status=ok
rank_zero_family_proof_complete=False
rank_zero_family_obligation_count=3
family_exclusion_proved_count=0
```

## Interpretation

普通话说：rank-zero 路线现在不是“再多算一些例子”，而是 3 个整族证明义务：

1. `AA`：82 个比例类、82 个 AA primitive model。
2. `AA+BB`：43 个比例类、86 个 primitive model。
3. `BB`：75 个比例类、75 个 BB primitive model。

这些模型的系数恒等式、观测 rank-zero invariant、forced full rational 2-torsion 都已经通过审计。
但这仍然不是 rank-zero theorem。真正缺的是对每个 seed family 给出 uniform 2-isogeny/Selmer
rank upper bound，或者外部可审阅的 rank-zero theorem certificate。

## Boundary

`rank_zero_family_proof_complete=False` and `family_exclusion_proved_count=0`.
More individual scaled `(A,B)` rank rows are diagnostics only, not family-proof
progress.
