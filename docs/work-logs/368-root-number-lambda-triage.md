# Root-Number Lambda Triage

## Question

For the `observed-open` primitive `lambda=A/B` classes, what root-number and
rank-key patterns should guide the next family rank/descent work?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_root_number_lambda_triage.py \
  --rank-jsonl results/mixed_closure_rank_hard_cases_320_torsion_cert.jsonl \
  --rank-jsonl results/mixed_closure_rank_localglobal_residual64_torsion_cert.jsonl \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --out results/closure_quotient_root_number_lambda_triage.json \
  --strict
```

## Output

```text
status=ok
target_class_count=148
target_pair_count=156
family_exclusion_proved_count=0
```

Top root-number patterns:

```text
56 AA:-1|AB:-1|BA:-1|BB:-1
53 AA:-1|AB:1|BA:1|BB:-1
12 AA:1|AB:-1|BA:-1|BB:-1
```

Top rank-key patterns:

```text
49 AA:1/1|AB:2/2|BA:2/2|BB:1/1
37 AA:1/1|AB:1/1|BA:1/1|BB:1/1
14 AA:1/1|AB:3/3|BA:3/3|BB:1/1
```

## Interpretation

普通话说：这一步只处理 148 个 `observed-open` 比例类。它把每个类的四条 quotient
曲线按 root number 和 rank key 分型，方便后续选择整族 rank/descent 问题。

root number 在这里只是分流信号，不是 no-point 证明。后续如果要把某一类排除，仍然需要
严格的 rank 论证、descent 论证、2-cover/Selmer 障碍，或者可审阅的 no-point 证书。

## Boundary

This is a root-number/rank-pattern routing ledger. It proves no lambda-family
exclusion by itself.
