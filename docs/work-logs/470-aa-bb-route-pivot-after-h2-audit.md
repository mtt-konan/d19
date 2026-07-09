# AA+BB Route Pivot After H2

## Question

After `wl469` refuted `H2_coordinate_equivalence`, what is the next valid
route for the AA+BB rank-zero Selmer line?

## Result

The route must pivot away from the package `x`-coordinate pseudo-container as a
bridge to complete Selmer. The selected next route is:

```text
build_minimal_C_d_local_solubility_matrix
```

This does **not** mean building a large machine immediately. It means the next
proof object must be the complete `d`-coordinate local-solubility ledger for
the 2-covers `C_d`, because `wl469` showed the package `x`-triple collapses
complete `d`-data.

## Why

The old route hoped that

```text
dim_F2 S~ <= 2
```

could bridge to a complete Selmer upper bound. But `wl469` shows:

```text
package x-triple != complete d-coordinate data.
```

Therefore the implication

```text
Sel_2(E_L/Q) subset S~
```

cannot be proved via coordinate equivalence. The route still aimed at a
Selmer upper bound must work directly in complete `d`-coordinates and test
local solubility of `C_d`.

## What Can Be Reused

Reusable as boundary evidence:

```text
wl465: S~ is a pseudo-container, not Sel_2(E_L/Q)
wl468: Sel_2(E_L/Q) subset S~ is not proved
wl469: package x-triple cannot replace complete d-data
```

Reusable only inside the old container:

```text
wl466: sign-tail kill inside S~
wl467: T-tail kill inside S~
dim_F2 S~ <= 2 as a pseudo-container statement
```

Reusable only as templates for the next `d`-matrix:

```text
wl457-wl459 odd-prime support rows, after re-proving them as C_d local rows
wl460-wl462 dyadic computations, after rewriting them in d-coordinates
wl463 point-level collapse, only as a rational-point sanity check
```

Not reusable as a Selmer bridge:

```text
package x-coordinate equivalence
direct transfer of mixed AA+BB common-source rows to all complete Selmer classes
single-curve sample diagnostics as proof of a family bound
```

## Next Lemmas

The next proof stack is:

```text
D0_complete_d_container_definition
D1_relevant_place_support_confinement
D2_local_C_d_row_characterization
D3_torsion_baseline_in_d_coordinates
D4_AA_BB_uniform_matrix_rank_bound
```

The next immediate lemma is `D0`: define the replacement container directly in
complete `d`-coordinates, with the product relation and torsion Kummer baseline
in the same quotient.

## Boundary

This pivot audit does not prove:

- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.

It only selects the next valid route after H2 failed and stops before building
the local matrix.
