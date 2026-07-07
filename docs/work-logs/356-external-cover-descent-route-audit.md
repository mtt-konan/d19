# External Cover Descent Route Audit

## Question

After the Sage cover capability audit, what is the next strict route for the
first rank-zero residual target `(1625,5643) AA`?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_external_cover_descent_route.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --sage-cover-capability-audit results/priority_005_1625_5643_AA_cover_tool_capabilities.json \
  --out results/priority_005_1625_5643_AA_external_cover_descent_route.json \
  --magma magma \
  --strict
```

## Output

```text
status=ok
local_magma_available=False
proof_status=external-tool-gap-open
recommended_next_action=obtain-magma-or-specialized-cover-descent-environment
```

## Interpretation

普通话说：这不是“多跑一会儿”的问题。当前本机没有 Magma；Sage 也已经显示没有
直接 cover-level no-point 证书接口。因此第一目标要继续严格收敛，需要一个能产出
可复查 transcript 的外部 cover descent / Mordell-Weil sieve 环境。

可以升级成证明的只有两类输出：

- 每个目标 cover 都有 no-rational-point certificate；
- 或者源椭圆曲线 rank bounds 被严格闭到 `[0,0]`，然后再通过 torsion-preimage
  audit 排除残余回拉。

不能升级成证明的输出包括：

- bounded point search 没找到点；
- rank bounds 仍是 `[0,2]`；
- local solubility witness；
- Sage 接口存在或不存在；
- 没有 no-point/rank certificate 的 Magma transcript。

## Boundary

This is a route audit, not a no-point proof. It records the external-tool gap
and the acceptance criteria for a future transcript.
