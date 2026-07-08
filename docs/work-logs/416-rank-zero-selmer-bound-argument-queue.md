# Rank-Zero Selmer Bound Argument Queue

## Question

After the transcript fields were split into shared setup, family conclusion, and
package-specific parts, what are the actual proof-writing tasks left?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_rank_zero_selmer_bound_argument_queue.py \
  --field-decomposition results/closure_quotient_rank_zero_selmer_transcript_field_decomposition.json \
  --transcript-bridge results/closure_quotient_rank_zero_selmer_transcript_bridge.json \
  --isogeny-setup-templates results/closure_quotient_rank_zero_selmer_isogeny_setup_templates.json \
  --family-conclusion-templates results/closure_quotient_rank_zero_selmer_family_conclusion_templates.json \
  --out results/closure_quotient_rank_zero_selmer_bound_argument_queue.json \
  --strict
```

## Output

```text
status=ok
primary_remaining_proof_field=selmer_bound_argument
bound_argument_task_count=9
open_bound_argument_task_count=9
kernel_template_reuse_count=3
family_conclusion_target_count=3
selmer_rank_upper_bound_proved_count=0
family_exclusion_proved_count=0
```

## Interpretation

普通话说：现在不是让 Sage 多跑一会儿就算完成。队列已经把真正缺的证明材料列出来：
9 个 package 都需要一段可审阅的 `selmer_bound_argument`。

这 9 个任务复用 3 个 kernel 级模板，并分别指向 3 个 family 结论：`AA`、`AA+BB`、
`BB`。共享的 `local_squareclass_conditions` 和 `isogeny_setup` 已经有模板；还没完成的是
逐 package 的 Selmer bound 论证。

当前仍没有 Selmer rank upper bound、rank-zero 定理或 `lambda` family exclusion。

## Boundary

This is a queue of proof-writing tasks. It does not prove the tasks.
