# rank-zero-selmer-AA-BB-kernel-minus-p

Status: open

## Scope

- family_pattern = AA+BB
- kernel = kernel_minus_p
- candidate_class_count = 43
- model_count = 86

## Symbolic Model

- T = A+B
- L role = A for AA, B for BB; AA+BB requires both sides to close
- kernel_root = -p
- target_a2 = 32*L^2 - 8*T^2
- target_a4 = 16*(T^2 + 4*L^2)^2

## Required Transcript

- statement
- isogeny_setup
- local_squareclass_conditions
- selmer_bound_argument
- rank_zero_conclusion
- review_notes

## Partial Transcript Segments

- `selmer_bound_argument` / `formal_lift_compatibility`
  - status = reviewable-proof
  - proof_path = docs/work-logs/458-aa-bb-minus-p-formal-lift-reviewable-proof.md
  - scope = odd-prime valuation support only
  - summary = The AA+BB odd-prime formal-lift compatibility segment is written as a line-by-line support-collapse proof for the minus-p kernel; the dyadic place, unit/sign classes, the global Selmer bound, and rank zero remain open.
- `local_squareclass_conditions` / `dyadic_opposite_mod4_branch`
  - status = reviewable-proof
  - proof_path = docs/work-logs/460-aa-bb-minus-p-dyadic-opposite-mod4-reviewable-proof.md
  - scope = AA+BB x_minus_p odd-odd opposite-mod-4 branch over {1,-1,2,-2}
  - summary = The AA+BB x_minus_p dyadic opposite-mod-4 branch is written as a line-by-line proof that the Q2 image intersects {1,-1,2,-2} only in {1}; the same-mod-4 branch, Selmer lift, global Selmer bound, and rank zero remain open.
- `local_squareclass_conditions` / `dyadic_same_mod4_local_obstruction`
  - status = reviewable-proof
  - proof_path = docs/work-logs/461-aa-bb-minus-p-dyadic-same-mod4-local-obstruction.md
  - scope = AA+BB x_minus_p odd-odd same-mod-4 branch over {1,-1,2,-2}
  - summary = The AA+BB x_minus_p same-mod-4 dyadic branch is written as a line-by-line local obstruction proof: class 2 is locally admissible on both one-sided models, so the naive one-kernel singleton theorem is false; cross-kernel or Selmer-level compatibility remains necessary.

## Boundary

transcript_status = partial

No Selmer rank upper bound is proved by this file. No rank-zero theorem or lambda-family exclusion is claimed here.
