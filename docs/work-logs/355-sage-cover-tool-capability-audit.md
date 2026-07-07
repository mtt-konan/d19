# Sage Cover Tool Capability Audit

## Question

Can the first rank-zero escalation target `(1625,5643) AA` be pushed to a
cover-level no-point certificate using Sage's built-in genus-one quartic tools?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_sage_cover_tool_capabilities.py \
  --handoff results/mixed_closure_residual_handoffs/priority_005_1625_5643_AA_covers_4_3.json \
  --out results/priority_005_1625_5643_AA_cover_tool_capabilities.json \
  --sage sage \
  --timeout 30 \
  --strict
```

## Output

```text
status=ok
cover_count=2
genus_one_cover_count=2
sage_direct_no_point_capable_count=0
strict_certificate_ready_count=0
recommended_next_tool=magma-or-specialized-cover-descent
```

Per cover:

```text
cover 4: genus=1, has_bounded_rational_points_method=True,
  has_direct_local_solubility_method=False,
  has_direct_two_cover_descent_method=False,
  jacobian_has_rank_method=False,
  jacobian_has_gens_method=False,
  jacobian_has_elliptic_curve_method=False

cover 3: genus=1, has_bounded_rational_points_method=True,
  has_direct_local_solubility_method=False,
  has_direct_two_cover_descent_method=False,
  jacobian_has_rank_method=False,
  jacobian_has_gens_method=False,
  jacobian_has_elliptic_curve_method=False
```

## Interpretation

普通话说：Sage 能把这两个 residual cover 当成 genus-one quartic 曲线，并且有
`rational_points` 这类有界找点接口；但这里没有直接的本地/全局 no-point 证明接口，
也没有能直接对这个 Jacobian 做 rank/gens/descent 的方法。因此这条 cover-level
严格化不该继续靠 Sage 内置一行命令硬推，下一步应转向 Magma 或专门的 cover
descent / Mordell-Weil sieve。

## Boundary

This is a tool-capability audit, not a no-point proof. Missing direct Sage
interfaces and bounded point searches do not prove the residual covers have no
rational point.
