# Two-Cover Lambda Frontier

## Question

After strict-local-tool pairs are removed, which primitive `lambda=A/B` classes
still require a 2-cover/Selmer obstruction or reviewable no-point certificates?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_two_cover_lambda_frontier.py \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --out results/closure_quotient_two_cover_lambda_frontier.json \
  --strict
```

## Output

```text
status=ok
target_class_count=8
target_pair_count=8
candidate_cover_total=18
selmer_gap_counts={'2': 7, '4': 1}
evidence_level_counts={'bounded-search-no-point-candidate': 8}
family_exclusion_proved_count=0
```

## Interpretation

普通话说：这一步只看 strict local tool 还没有覆盖的 residual 比例类。剩下 8 个
`lambda` 类、18 个 candidate cover：

```text
gap 2: 7 classes
gap 4: 1 class
```

它们都还只是 bounded-search no-point candidate。后续只有两种可接受推进：

- 整族 2-cover / Selmer 障碍；
- 或者每个列出的 cover 都有可审阅的 no-point 证书。

继续延长搜索、增加单个 `(A,B)` 命中，不能算主线进展。

## Boundary

This ledger records the remaining 2-cover/Selmer frontier. It does not prove
that any residual cover has no rational point.
