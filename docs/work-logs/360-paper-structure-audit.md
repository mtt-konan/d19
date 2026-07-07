# Paper Structure Audit

## Question

Does the paper note expose the strict result and the residual-open boundary in
an auditable shape?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_paper_structure.py \
  --paper docs/paper/CLOSURE_QUOTIENT_PARTIAL_RESULT.md \
  --claim-audit results/closure_quotient_paper_claim_audit.json \
  --residual-open-frontier-audit results/mixed_closure_residual_open_frontier_audit.json \
  --frontier-strictification-queue results/mixed_closure_frontier_strictification_queue.json \
  --external-certificate-frontier-audit results/mixed_closure_external_cover_certificate_frontier_intake.json \
  --out results/closure_quotient_paper_structure_audit.json \
  --strict
```

## Output

```text
status=ok
matched_section_count=5
matched_claim_count=14
```

## Interpretation

普通话说：这一步不是检查数学证明，而是检查论文稿有没有把该说的话放在纸面上。
它要求论文稿明确包含：

- 不证明 Harborth conjecture 的边界；
- main lemma / certificate rule / certified census / paper path 等章节；
- `275` 个 rank-zero `AA/BB` 证书和 `220` 个严格排除 pair；
- residual `candidate-not-proof` 和 open-frontier 状态；
- external certificate intake 目前覆盖 `10` 个目标、`23` 个 cover，但 `0` 个证书包 ready；
- bounded search 和 external intake 不能当证明的边界。

## Boundary

This is a paper-structure gate. It checks wording and required claim placement;
it does not verify the mathematics.
