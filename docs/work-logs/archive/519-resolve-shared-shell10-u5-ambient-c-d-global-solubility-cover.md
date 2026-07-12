# Resolve Shared Shell-10 u5 Ambient C_d Cover

## Question

Using `wl518` as input, can the only remaining genuinely deferred shell-10
cover family

```text
support = u_5
L = 10
T = 19
d = (5, 5, 1)
```

be classified by either an exact ambient `C_d` point or an exhaustive no-lift
certificate?

This work-log enters only that selected gate. It does not execute shell 11,
does not broaden to a proof-level generalization, does not select a final
obstruction candidate, and does not run broad rank or Selmer diagnostics.

## Inputs

The immediate route input is:

```text
wl518 support-family synthesis after wl517
```

The admissibility filter input is:

```text
wl491 ambient C_d to AA+BB admissibility filter
```

The touched object layers are:

```text
complete d-coordinate ambient C_d cover
wl491 AA+BB admissibility filter
M_tail diagnostic support ledger routing
```

This is not the old package-`x` / `S~` pseudo-container and not a
theorem-level `Sel_2(E_L/Q)` upper-bound argument.

## Cover Resolution

The shared cover equations are:

```text
X + 78 = 5*u_minus_p^2
X - 1522 = 5*u_pos_2sqrt_q^2
X + 1522 = u_neg_2sqrt_q^2
```

An exact rational ambient point is:

```text
X = 1260642/121
u_minus_p = 504/11
u_pos_2sqrt_q = 464/11
u_neg_2sqrt_q = 1202/11
```

The induced point on

```text
V^2 = (X + 78)(X - 1522)(X + 1522)
```

is:

```text
X = 1260642/121
V = 1405474560/1331
```

So the shared shell-10 `u_5` ambient `C_d` cover is globally soluble, not
refuted.

## wl491 Filter

After ambient global solubility is established, `wl491` is applied to the two
mirror entries:

```text
AA_A10_B9_u_5_m_tail_shell10_candidate
BB_A9_B10_u_5_m_tail_shell10_candidate
```

Both are classified as:

```text
globally soluble but not AA+BB-admissible
```

The AA-side entry fails the `BB` common-source square product and also has
`M < 0`. The BB-side entry fails the `AA` common-source square product and
also has `M < 0`.

No AA+BB-admissible point is produced here.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl519_resolve_shared_shell10_u5_ambient_c_d_global_solubility_cover.json
```

with:

```text
status = ok
work_log = wl519
input_work_logs = wl491, wl518
resolved_shell10_deferred_covers_here = true
ambient_globally_soluble_count = 2
ambient_global_solubility_refuted_count = 0
wl491_filter_applied_count = 2
aa_bb_admissible_count = 0
aa_bb_not_admissible_count = 2
shell11_executed_here = false
post_wl519_route_choice_made_here = false
advance_to_wl520 = false
```

## Boundary

This work-log stops after `wl519`. It does not prove:

- a final obstruction candidate;
- a new local/Hilbert row;
- uniform full rank of `M_tail`;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.

The next gap is a separate post-`wl519` route choice. That gate is not entered
here.
