# AA+BB Explicit C_d Cover Equation Instantiation

## Question

Using `wl484` as input, what are the concrete complete `d`-coordinate
`C_d` cover equations for the `AA, A=3, B=1` candidate

```text
d = (3, 3, 1)
```

with support `u_3`?

This is an equation-instantiation audit only. It does not decide local or
global solubility.

## Candidate Data

The curve is

```text
E_L: Y^2=(X+p)*(X^2-4*q)
```

with

```text
side = AA
A = 3
B = 1
L = 3
T = 4
sqrt_q = 52
p = 40
q = 2704
```

The complete `d`-coordinate order remains

```text
d_minus_p, d_pos_2sqrt_q, d_neg_2sqrt_q
```

and the candidate is

```text
d_minus_p       = 3
d_pos_2sqrt_q   = 3
d_neg_2sqrt_q   = 1
```

## Root Data

The roots are

```text
e_minus = -p         = -40
e_pos   =  2*sqrt_q  =  104
e_neg   = -2*sqrt_q  = -104
```

## X-Coordinate Relations

For variables

```text
X, u_minus_p, u_pos_2sqrt_q, u_neg_2sqrt_q
```

the complete `d`-coordinate relations are

```text
X - e_minus = d_minus_p*u_minus_p^2
X - e_pos   = d_pos_2sqrt_q*u_pos_2sqrt_q^2
X - e_neg   = d_neg_2sqrt_q*u_neg_2sqrt_q^2
```

so for this candidate:

```text
X + 40  = 3*u_minus_p^2
X - 104 = 3*u_pos_2sqrt_q^2
X + 104 = u_neg_2sqrt_q^2
```

## Difference Equations

The three complete difference equations are

```text
d_minus_p*u_minus_p^2 - d_pos_2sqrt_q*u_pos_2sqrt_q^2
  = e_pos - e_minus

d_minus_p*u_minus_p^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2
  = e_neg - e_minus

d_pos_2sqrt_q*u_pos_2sqrt_q^2 - d_neg_2sqrt_q*u_neg_2sqrt_q^2
  = e_neg - e_pos
```

Instantiated:

```text
3*u_minus_p^2 - 3*u_pos_2sqrt_q^2 = 144
3*u_minus_p^2 - u_neg_2sqrt_q^2   = -64
3*u_pos_2sqrt_q^2 - u_neg_2sqrt_q^2 = -208
```

The first two are an independent presentation:

```text
3*u_minus_p^2 - 3*u_pos_2sqrt_q^2 = 144
3*u_minus_p^2 - u_neg_2sqrt_q^2   = -64
```

Equivalently, after dividing the first equation by `3`:

```text
u_minus_p^2 - u_pos_2sqrt_q^2 = 48
3*u_minus_p^2 - u_neg_2sqrt_q^2 = -64
```

The third difference is dependent:

```text
(minus_minus_neg) - (minus_minus_pos):
  -64 - 144 = -208.
```

## Next-Gate Checklist

The relevant places remain exactly

```text
infinity, 2, 3, 13
```

The next gate should check local solubility narrowly at these places:

- `infinity`: decide real solubility of the instantiated two-equation cover, or
  equivalently the three real `X`-coordinate square relations.
- `2`: run a direct `Q_2` solubility check for the full cover in the ordinary
  even-`sqrt_q` stratum, not merely the prior squareclass row.
- `3`: run a direct `Q_3` solubility check at the active odd `L`-prime.
- `13`: run a direct `Q_13` solubility check at the odd `sqrt_q`-prime.

No item in this checklist is decided here.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl485_explicit_cd_cover_equation_instantiation.json
```

with:

```text
status = ok
work_log = wl485
input_work_log = wl484
explicit_c_d_cover.candidate_id = AA_A3_B1_u_3_complete_d_candidate
explicit_c_d_cover.two_independent_equations =
  [
    "3*u_minus_p^2 - 3*u_pos_2sqrt_q^2 = 144",
    "3*u_minus_p^2 - u_neg_2sqrt_q^2 = -64"
  ]
relevant_places = ["infinity", "2", "3", "13"]
equation_instantiation_only = true
local_solubility_decided_here = false
global_solubility_decided_here = false
obstruction_proved_here = false
explicit_c_d_cover_solved_here = false
broad_rank_or_selmer_diagnostics_run = false
complete_selmer_upper_bound_proved = false
dim_sel2_eq_2_claimed = false
rank_zero_claimed = false
sha2_trivial_claimed = false
family_exclusion_proved_count = 0
old_package_x_coordinate_collapse_used = false
```

## Boundary

This work-log stops after writing the explicit equations and the local checklist.
It does not prove:

- local solubility or local insolubility at `infinity`, `2`, `3`, or `13`,
- global solubility or global insolubility,
- a Cassels-Tate or second-descent obstruction,
- an analytic-rank or L-value theorem,
- a complete Selmer upper bound,
- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion theorem.
