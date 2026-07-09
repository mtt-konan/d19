# AA+BB Local Solubility Gate

## Question

Using `wl485` as input, is the explicit complete `d`-coordinate cover

```text
d = (3, 3, 1)
```

locally soluble at exactly the scoped places

```text
infinity, 2, 3, 13
```

for

```text
E_L: Y^2=(X+p)*(X^2-4*q)
```

with `AA, A=3, B=1`?

This was intended as only the local-solubility gate. During the local check,
the certificate found was an exact integral point on the cover, so this
work-log also records global solubility for this single `C_d` cover. It does
not draw any Selmer-rank or family conclusion from that point.

## Input Cover

The `wl485` complete `C_d` relations are

```text
X + 40  = 3*u_minus_p^2
X - 104 = 3*u_pos_2sqrt_q^2
X + 104 = u_neg_2sqrt_q^2
```

with independent difference presentation

```text
u_minus_p^2 - u_pos_2sqrt_q^2 = 48
3*u_minus_p^2 - u_neg_2sqrt_q^2 = -64
```

The coordinate order remains

```text
d_minus_p, d_pos_2sqrt_q, d_neg_2sqrt_q.
```

## Local Certificates

### Infinity

The real point

```text
X = 152
u_minus_p = 8
u_pos_2sqrt_q = 4
u_neg_2sqrt_q = 16
```

satisfies

```text
152 + 40 = 3*8^2 = 192
152 - 104 = 3*4^2 = 48
152 + 104 = 16^2 = 256
```

so the cover is locally soluble over `R`.

### 2

The same displayed integer tuple is a `Q_2` local certificate. Since it
satisfies the three `C_d` square relations exactly over `Z`, its reductions are
compatible modulo `2^n` for every `n`; in particular the result artifact
records checks modulo

```text
2, 4, 8, 16, 32.
```

No regular dyadic Hensel minor is claimed or needed for this certificate.

### Global Witness

The displayed tuple is integral, hence it is also a rational point on the
cover. It induces the point

```text
X = 152
Y = 1536
```

on

```text
E_L: Y^2=(X+40)*(X^2-4*2704),
```

because

```text
1536^2 = (152+40)*(152^2 - 4*2704).
```

Therefore the `u_3` candidate is not a Sha-style locally-soluble
globally-pointless obstruction.

### 3

For the normalized equations

```text
F1 = u_minus_p^2 - u_pos_2sqrt_q^2 - 48
F2 = 3*u_minus_p^2 - u_neg_2sqrt_q^2 + 64
```

the residue point

```text
X = 2
u_minus_p = 1
u_pos_2sqrt_q = 1
u_neg_2sqrt_q = 1        mod 3
```

satisfies `F1 = F2 = 0 mod 3`. The Jacobian minor using columns
`u_minus_p, u_neg_2sqrt_q` has determinant

```text
-4*u_minus_p*u_neg_2sqrt_q = -4 = 2 mod 3,
```

which is nonzero. Hensel lifting gives a `Q_3` point.

### 13

For the same normalized equations, the residue point

```text
X = 9
u_minus_p = 8
u_pos_2sqrt_q = 4
u_neg_2sqrt_q = 3        mod 13
```

satisfies `F1 = F2 = 0 mod 13`. The Jacobian minor using columns
`u_minus_p, u_neg_2sqrt_q` has determinant

```text
-4*u_minus_p*u_neg_2sqrt_q = -96 = 8 mod 13,
```

which is nonzero. Hensel lifting gives a `Q_13` point.

## Result

All four scoped places are locally soluble:

```text
local_solubility_summary = locally_soluble_at_all_relevant_places
candidate_survives_local_gate = true
global_solubility_summary = globally_soluble_integral_point_found_during_local_gate
next_gate = route_impact_of_global_point
```

The next gate is to account for the route impact of this global point. That
gate is not entered in this work-log.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl486_local_solubility_gate.json
```

with:

```text
status = ok
work_log = wl486
input_work_log = wl485
relevant_places = ["infinity", "2", "3", "13"]
local_solubility_decided_here = true
local_solubility_summary = locally_soluble_at_all_relevant_places
local_solubility_gate.candidate_survives_local_gate = true
local_solubility_gate.next_gate = route_impact_of_global_point
global_solubility_decided_here = true
global_solubility_summary = globally_soluble_integral_point_found_during_local_gate
obstruction_proved_here = false
candidate_obstruction_refuted_here = true
explicit_c_d_cover_solved_here = true
broad_rank_or_selmer_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
```

## Boundary

This work-log stops after the local-solubility gate and the forced recording of
the integral global witness found there. It does not prove:

- global insolubility of the `d=(3,3,1)` cover,
- a Cassels-Tate or second-descent obstruction,
- an analytic-rank or L-value theorem,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.
