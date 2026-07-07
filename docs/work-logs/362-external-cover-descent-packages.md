# External Cover-Descent Packages

## Question

Can the residual frontier be exported as concrete external cover-descent task
inputs instead of only saying "use an external tool"?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/export_external_cover_descent_packages.py \
  --frontier-handoff-audit results/mixed_closure_frontier_handoff_audit.json \
  --handoff-dir results/mixed_closure_residual_handoffs \
  --out-dir results/mixed_closure_external_cover_descent_packages \
  --out results/mixed_closure_external_cover_descent_package_index.json \
  --strict
```

Sage sanity check for the first package:

```bash
DOT_SAGE=/private/tmp/d19-dot-sage sage \
  results/mixed_closure_external_cover_descent_packages/priority_005_1625_5643_AA_covers_4_3/sage_cover_task.sage
```

## Output

```text
status=ok
target_count=10
cover_count=23
strict_certificate_ready_count=0
```

The first Sage task file constructs the two genus-one curves for
`(1625,5643) AA`.

## Interpretation

普通话说：现在 10 个 residual frontier 目标、23 个 cover 都有了可复跑导出的
外部任务包。每个包包含：

- `cover_inputs.json`；
- `magma_cover_descent_task.m`；
- `sage_cover_task.sage`；
- `README.md`。

这一步没有产生新的数学证书。它只是把下一步要交给 Magma 或专门 cover descent
工具的输入固定下来，方便后续拿 transcript 回来走 certificate intake。

## Boundary

The generated packages are task inputs. They do not certify that any residual
cover has no rational point.
