# Lambda Convergence Priorities

## Question

After proof-seed coverage is in the mainline gate, which lambda route should
be attacked first?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_lambda_convergence_priorities.py \
  --proof-seed-coverage results/closure_quotient_lambda_proof_seed_coverage_audit.json \
  --rank-zero-seeds results/closure_quotient_rank_zero_proof_seeds.json \
  --rank-zero-identity-audit results/closure_quotient_rank_zero_seed_identity_audit.json \
  --rank-zero-invariants results/closure_quotient_rank_zero_certifying_invariants.json \
  --rank-zero-forced-torsion results/closure_quotient_rank_zero_forced_torsion_audit.json \
  --root-number-seeds results/closure_quotient_root_number_proof_seeds.json \
  --two-cover-seeds results/closure_quotient_two_cover_proof_seeds.json \
  --out results/closure_quotient_lambda_convergence_priorities.json \
  --strict
```

## Output

```text
status=ok
lambda_class_count=356
priority_order=['rank_zero', 'root_number', 'two_cover']
family_exclusion_proved_count=0
```

## Interpretation

普通话说：这一步不是证明，而是把下一步收敛顺序定死。

1. 先攻 rank-zero：200 个比例类已经压到 3 个 seed group，243 个 primitive model 的系数恒等式、
   rank-zero invariant、forced full rational 2-torsion 都已通过审计。缺的是整族 rank-zero theorem。
2. 再攻 root-number：148 个比例类分成 21 个 root-number/rank pattern。root number 只能给结构路线，
   不能单独证明无点。
3. 最后攻 two-cover：8 个比例类、7 个 seed group、18 个候选 cover。这里需要 family 2-cover/Selmer
   obstruction，或者逐 cover 的可审阅 no-point certificate。

## Boundary

`convergence_complete=False` and `family_exclusion_proved_count=0`.
This audit rejects search-count growth as progress and does not promote any
lambda family to a proved exclusion.
