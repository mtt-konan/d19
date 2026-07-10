# v_5 L=1 T=5 Function-Field Prototype

## Question

For the single cover family

```text
support=v_5|L=1|T=5|d=(5,1,5)
```

represented in `wl495` by

```text
AA_A1_B4_v_5_m_tail_refresh_candidate
BB_A4_B1_v_5_m_tail_refresh_candidate
```

can the missing `wl527` function-field proof data be supplied as a first
minimal prototype?

This touches only the single cover-family function-field prototype layer. It
does not execute shell 11, compute new supports, touch another cover family,
test new ambient `C_d` solubility, apply `wl491` to a new point, run broad
rank/Selmer diagnostics, use the old package-`x` / `S~` bridge, select a final
obstruction candidate, or claim theorem-level progress.

## Model

The existing `wl495` complete `d`-coordinate equations are:

```text
X - 42 = 5*u_minus_p^2
X - 58 = u_pos_2sqrt_q^2
X + 58 = 5*u_neg_2sqrt_q^2
```

Equivalently:

```text
5*u_minus_p^2 - u_pos_2sqrt_q^2 = 16
u_minus_p^2 - u_neg_2sqrt_q^2 = -20
```

Using the chart

```text
r = u_neg_2sqrt_q + u_minus_p
```

the prototype function field is:

```text
Q(r,y)/(y^2 - (5*r^4 - 264*r^2 + 2000))
```

with maps:

```text
u_minus_p = (r^2 - 20)/(2*r)
u_pos_2sqrt_q = y/(2*r)
u_neg_2sqrt_q = (r^2 + 20)/(2*r)
X = 42 + 5*((r^2 - 20)/(2*r))^2
Y = 5*y*(r^4 - 400)/(8*r^3)
```

The chart excludes at least:

```text
r = 0
r^2 = 20
X+p = 0
```

## Source-Side Maps

The centered-even map gives:

```text
t = Y/(2*(X+p)) = y*(r^2+20)/(4*r*(r^2-20))
N = (5+t)/2
M = (5-t)/2
```

Both selected entries have source leg `L=1`. Therefore the source-side product

```text
(N^2+1)(M^2+1)
```

is certified as the expected square:

```text
(N^2+1)(M^2+1) = (z/4)^2
```

This separates the two source labels:

- `AA_A1_B4`: source product uses `A=1`, opposite product uses `B=4`.
- `BB_A4_B1`: source product uses `B=1`, opposite product uses `A=4`.

By this symmetry, both have the same opposite-leg product:

```text
(N^2+16)(M^2+16)
```

or, in `t`:

```text
((t^2 + 89)^2 - 100*t^2)/16
```

## Certificate

`wl528` proves a function-field nonsquare certificate for the opposite-side
product by a rational specialization:

```text
r = 10
y = 160
u_minus_p = 4
u_pos_2sqrt_q = 8
u_neg_2sqrt_q = 6
X = 122
Y = 960
t = 6
N = 11/2
M = -1/2
```

The script now checks this certificate executably. The specialization is
verified to lie on the quartic, to be smooth, to satisfy the chart/open
denominators, to map to the recorded `wl495` cover point and induced `E`
point, and to give the recorded `t,N,M` and opposite product.

At this smooth nonexceptional specialization where the product is regular and
nonzero:

```text
(N^2+16)(M^2+16) = 12025/16
```

and

```text
12025/16 = 5^2*13*37 / 2^4
```

is not a rational square. Hence the opposite-side product is not a square in
the prototype function field: if it were a square in that function field, then
at this smooth rational point where it is regular and nonzero, its residue
would be a rational square.

This is a nonsquare certificate by specialization, not a full divisor-parity
certificate.

## What Remains Unproved

This prototype does not prove the uniform cover-family obstruction. The exact
remaining gap is:

```text
Need a specialization-survival or divisor-parity argument showing that the
opposite-side squareclass obstruction holds for every nonexceptional rational
point in the required positivity domain.
```

The recorded specialization has:

```text
N = 11/2
M = -1/2
```

so `M` positivity fails at that point. That is separated from the squareclass
nonsquare certificate.

## Result Artifact

```text
results/closure_quotient_rank_zero_aa_bb_wl528_v5_l1_t5_function_field_prototype.json
```

with:

```text
status = ok
work_log = wl528
object_layer = single_cover_family_function_field_prototype
prototype_model_built_here = true
rational_source_side_maps_derived_here = true
N_M_as_function_field_elements_derived_here = true
opposite_side_product_formed_here = true
function_field_nonsquare_certificate_proved_here = true
divisor_parity_certificate_proved_here = false
uniform_specialization_survival_proved_here = false
uniform_cover_family_obstruction_proved_here = false
ready_as_reviewable_single_prototype = true
ready_as_uniform_cover_family_theorem = false
shell11_executed_here = false
new_supports_computed_here = false
new_c_d_solubility_tested_here = false
complete_selmer_upper_bound_proved = false
rank_zero_claimed = false
advance_to_next_cover_family = false
advance_to_next_roadmap_step = false
stop_after_current_task = true
all_function_field_identity_checks_passed = true
all_specialization_certificate_prerequisites_passed = true
```

## Boundary

This work-log stops after this one `v_5|L=1|T=5|d=(5,1,5)` prototype. It does
not prove:

- a uniform cover-family squareclass obstruction;
- a divisor-parity certificate;
- specialization survival over the positivity domain;
- a new local/Hilbert row;
- a new `M_tail` row or uniform `M_tail` full rank;
- ambient solubility for any new `C_d` class;
- AA+BB admissibility for any new point or support;
- a final obstruction candidate;
- a complete Selmer upper bound;
- `dim Sel_2(E)=2`;
- rank zero;
- `Sha[2]=0`;
- any family exclusion theorem.
