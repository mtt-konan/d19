# AA+BB Theorem-Candidate Bridge Audit

## Question

After `wl467` proved the cheap AA+BB pseudo-container ledger

```text
dim_F2 S~ <= 2,
```

can that statement be promoted to a rigorous complete 2-Selmer upper bound?

## Result

No. The bridge is not proved.

The current valid statement is only:

```text
dim_F2 S_tilde_AA_BB <= 2
```

for the AA+BB common-source pseudo-Selmer upper-bound container. The relevant
theorem-level object would be:

```text
Sel_2(E_L/Q)
```

for the complete full-rational-2-torsion curve

```text
E_L: Y^2 = (X+p)*(X^2 - 4*q),
```

with `L=A` on the AA side and `L=B` on the BB side.

The missing implication is:

```text
Sel_2(E_L/Q) subset S_tilde_AA_BB.
```

That inclusion has not been proved. Therefore `S~ <= 2` is not yet a complete
Selmer upper-bound theorem.

## What Is Proved

The prior audits establish the following scoped ledger:

```text
wl465: S~ is an AA+BB common-source pseudo-container, not a full Selmer group.
wl466: the archimedean sign tail contributes no dimension beyond torsion.
wl467: the ell | T, ell == 1 mod 4 tail is killed inside S~.
```

Thus the cheap container has no remaining symbolic non-torsion tail:

```text
dim_F2 S~ <= 2.
```

This is still a statement about `S~`, not about every complete 2-cover class in
`Sel_2(E_L/Q)`.

## Required Hypotheses Still Needed

To promote the theorem candidate, the bridge would need:

```text
H1_complete_selmer_object
  Fix the theorem object as Sel_2(E_L/Q) for each AA or BB side, not S~ and not
  sampled single-curve diagnostics.

H2_coordinate_equivalence
  Prove the complete-descent d-coordinates and the three package x-coordinates
  define equivalent squareclass data for every Selmer class, including torsion
  representatives and exceptional root cases.

H3_uniform_local_containment
  For every place v and every complete 2-cover C_d locally soluble over Q_v,
  prove its translated x-data satisfies the constraints used to define S~.

H4_mixed_rows_upgrade
  Upgrade wl457-wl459 from AA+BB mixed common-source support rows to valid
  constraints on all complete Selmer classes, or prove that every relevant
  Selmer class is represented by such a common-source class.

H5_dimension_and_torsion_identification
  After Sel_2(E_L/Q) subset S~ is proved, identify the two-dimensional torsion
  baseline inside the same ambient quotient and verify dim_F2 S~ <= 2 there.
```

## Formal Gaps

The exact remaining gaps are:

```text
1. No proved inclusion Sel_2(E_L/Q) subset S_tilde_AA_BB.
2. wl457-wl459 are still mixed AA+BB common-source rows, not complete local
   matrix rows.
3. The full C_d local-solubility matrix has not been built or shown redundant
   for all Selmer classes.
4. The killed T-tail and sign-tail remove symbolic tails only inside S~.
5. Therefore dim_F2 S~ <= 2 is not yet a rigorous upper bound for
   dim_F2 Sel_2(E_L/Q).
```

## Result Artifact

The machine-checkable bridge audit is:

```text
results/closure_quotient_rank_zero_aa_bb_theorem_bridge.json
```

with:

```text
s_tilde_is_valid_upper_bound_for_complete_selmer = false
complete_selmer_upper_bound_proved = false
theorem_candidate_promotable = false
selmer_rank_upper_bound_proved_count = 0
family_exclusion_proved_count = 0
rank_zero_claimed = false
sha2_trivial_claimed = false
```

## Boundary

This bridge audit does not prove:

- `dim Sel_2(E)=2`,
- a rank upper bound,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.

It stops after the theorem-candidate bridge audit and does not move to
finite-ledger or all-lambda coverage.
