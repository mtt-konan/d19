# Closure Quotient C-Ratio Coverage

## Question

Given the primitive ray ledger with `c_- = |A-B|`, what does `c_+/c_-` actually
cover, and what does it not cover at the `lambda=A/B` level?

## Command

```bash
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python scripts/theory/audit_closure_quotient_c_ratio_coverage.py \
  --ray-ledger results/closure_quotient_ray_ledger.json \
  --out results/closure_quotient_c_ratio_coverage_audit.json \
  --strict
```

## Output

```text
status=ok
defined_c_ratio_class_count=356
lambda_orientation_gap_class_count=356
lambda_family_exclusion_proved_count=0
```

Additional counts:

```text
input_c_ratio_class_count=356
undefined_c_ratio_class_count=0
orientation_lost_class_count=356
both_orientations_observed_class_count=0
single_orientation_observed_class_count=356
strict_unordered_class_count=200
residual_unordered_class_count=8
open_unordered_class_count=156
no_point_certificate_added_count=0
```

## Interpretation

普通话说：`c_+/c_- = (A+B)/|A-B|` 能识别的是无向比例类 `{A:B, B:A}`。
它看不出 `lambda=A/B` 和 `1/lambda=B/A` 的方向差别。

当前 ledger 里有 356 个 defined `c_+/c_-` class，但每个 class 都只观察到一个有向
ray。因此：

```text
c_+/c_- covers unordered ratio classes: yes, 356 observed classes
c_+/c_- covers oriented lambda classes: no, 356 orientation gaps remain
lambda-family exclusions proved by this audit: 0
```

这正好说明下一步不能继续把 `(A,B)` 数量当进展。`c_+/c_-` 已经把已有 closure
quotient 证据压成无向比例账本；要进入主线，必须转到有向 `lambda=A/B` 的整族结构证明，
或者对剩余类给出可审阅的 no-point certificate。

## Boundary

This audit reorganizes the existing ray ledger. It does not add a no-point
certificate and does not prove any lambda-family exclusion.
