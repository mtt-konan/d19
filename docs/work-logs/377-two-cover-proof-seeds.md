# Two-Cover Proof Seeds

## Question

Can the 8 remaining 2-cover/Selmer lambda frontier targets be grouped by their
strict certificate needs?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/summarize_closure_quotient_two_cover_proof_seeds.py \
  --frontier results/closure_quotient_two_cover_lambda_frontier.json \
  --out results/closure_quotient_two_cover_proof_seeds.json \
  --strict
```

## Output

```text
status=ok
seed_group_count=7
target_class_count=8
candidate_cover_total=18
family_exclusion_proved_count=0
```

Groups:

```text
1 class, 2 covers:
curve=AA selmer_gap=2 cover_count=2 rank[AA:0/2|AB:1/1|BA:1/1|BB:1/1]

2 classes, 4 covers:
curve=AA selmer_gap=2 cover_count=2 rank[AA:0/2|AB:1/1|BA:1/1|BB:2/2]

1 class, 2 covers:
curve=AA selmer_gap=2 cover_count=2 rank[AA:0/2|AB:2/2|BA:2/2|BB:1/1]

1 class, 2 covers:
curve=BB selmer_gap=2 cover_count=2 rank[AA:1/1|AB:2/2|BA:2/2|BB:0/2]

1 class, 2 covers:
curve=BB selmer_gap=2 cover_count=2 rank[AA:1/1|AB:3/3|BA:3/3|BB:0/2]

1 class, 2 covers:
curve=BB selmer_gap=2 cover_count=2 rank[AA:2/2|AB:1/1|BA:1/1|BB:0/2]

1 class, 4 covers:
curve=BB selmer_gap=4 cover_count=4 rank[AA:2/2|AB:1/1|BA:1/1|BB:0/2]
```

## Interpretation

普通话说：two-cover 剩余支已经很小，但也因此没有太多可继续压缩的余地。8 个剩余
比例类只能压成 7 个证书需求组，其中只有一组含 2 个类。

这一步的意义是把“还差什么证明”说清楚：

- 可以给出整族 2-cover / Selmer 障碍；
- 或者对每个列出的 cover 给出可审阅 no-point 证书；
- bounded search 的 no-point candidate 仍然不是证明。

所以这条支线的下一步不是继续跑更高搜索界，而是补严格 cover-level 证书或找到整族障碍。

## Boundary

This groups 2-cover frontier targets by future strict certificate needs.
Bounded-search no-point candidates are not no-point proofs.
