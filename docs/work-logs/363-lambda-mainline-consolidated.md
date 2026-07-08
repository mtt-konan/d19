# wl363-wl385, wl408-wl409 — lambda mainline consolidated

## Scope

This file replaces the old route-building logs `wl363` through `wl385`, plus
`wl408` and `wl409`.

## Result

The closure quotient work stopped being a count of separate `(A,B)` hits and
became a `lambda = A/B` mainline.

Current ledger status:

```text
lambda_class_count = 356
rank_zero_class_count = 200
root_number_class_count = 148
two_cover_class_count = 8
covered_class_count = 356
family_exclusion_proved_count = 0
```

Plain meaning: the project has sorted all current primitive ratio classes into
three proof routes. It has not proved any full ratio family impossible.

## What Survived

The useful facts from the replaced logs are:

- Scale does not create a new problem. For fixed primitive `(a,b)`, the quotient
  curves for `(ka,kb)` are the same problem after rescaling.
- The `c_+ = A+B` and `c_- = |A-B|` ledgers move the problem from pair counting
  to ratio classes.
- The route partition is complete for the current ledger: `200 + 148 + 8 = 356`.
- The rank-zero route is the first priority because it compresses 200 classes to
  3 seed groups: `AA`, `AA+BB`, and `BB`.
- Root-number data only sorts hard cases. It is not a no-point proof.
- The two-cover branch is small: 8 classes and 18 candidate covers. It still
  needs a real obstruction or a reviewable no-point certificate.

## Rank-Zero Inputs

The rank-zero branch has these audited inputs:

```text
candidate_class_count = 200
primitive_model_count = 243
model_counts_by_curve = {'AA': 125, 'BB': 118}
rank_zero_seed_groups = {'AA': 82, 'AA+BB': 43, 'BB': 75}
matched_rank_row_count = 275
matched_primitive_model_count = 243
rank_key_counts = {'0/0': 243}
torsion_order_counts = {'4': 243}
root_number_counts = {'1': 243}
```

The 275 rank-zero rows collapse to 243 primitive `class + curve` models. The
forced full 2-torsion comes from the formula

```text
X^3 + pX^2 - 4qX - 4pq = (X+p)(X^2-4q),  q = sqrt_q^2.
```

This explains the torsion pattern. It does not explain rank zero. The missing
piece is a uniform rank-zero theorem, most likely through a 2-isogeny/Selmer
bound.

## Boundary

This consolidation records the current mainline and deletes route-building
bookkeeping. It does not add a no-point certificate, prove rank zero, prove a
Selmer bound, or exclude any full `lambda` family.
