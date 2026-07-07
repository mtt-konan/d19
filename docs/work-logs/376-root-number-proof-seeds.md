# Root-Number Proof Seeds

## Question

Can the 148 root-number/rank-structure lambda targets be grouped into fewer
combined proof-seed patterns?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_root_number_proof_seeds.py \
  --triage results/closure_quotient_root_number_lambda_triage.json \
  --out results/closure_quotient_root_number_proof_seeds.json \
  --strict
```

## Output

```text
status=ok
seed_group_count=21
target_class_count=148
target_pair_count=156
family_exclusion_proved_count=0
```

Largest groups:

```text
49 classes, 55 pairs:
root[AA:-1|AB:1|BA:1|BB:-1] rank[AA:1/1|AB:2/2|BA:2/2|BB:1/1]

37 classes, 38 pairs:
root[AA:-1|AB:-1|BA:-1|BB:-1] rank[AA:1/1|AB:1/1|BA:1/1|BB:1/1]

14 classes, 15 pairs:
root[AA:-1|AB:-1|BA:-1|BB:-1] rank[AA:1/1|AB:3/3|BA:3/3|BB:1/1]
```

## Interpretation

普通话说：root-number 路线也不应该逐个比例类讨论。现在 148 个目标类被压成 21 个
combined seed group，前三组已经覆盖 100 个类。

这一步只是在给后续整族 rank/descent 问题分桶。root number 仍然不是 no-point 证明；
rank pattern 也只是当前样本的路由信息。下一步如果要推进这一支，应该优先研究最大的
combined pattern 是否能在 `lambda` 族层面解释，而不是继续加单个 `(A,B)` 搜索。

## Boundary

This groups root-number/rank diagnostic patterns for future lambda-family
routing. It does not prove any no-point or family exclusion theorem.
