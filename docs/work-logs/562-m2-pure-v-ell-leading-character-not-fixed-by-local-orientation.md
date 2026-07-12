# M2 Pure v_ell Leading Character Not Fixed By Local Orientation

## Question

Can the selected `wl556` Gaussian orientation and the first two source-square
equations determine the leading-character row in `wl561` by purely local
residue analysis?

## Exact Split-Prime Witnesses At p = 13

Work modulo `13` with `ell=1`. Let

```text
f(t)=t^2+4*t-4.
```

There are two exact source-compatible square values:

```text
t=0:  t,1-t,t+4 are squares and f(t)=9 is a square,
t=10: t,1-t,t+4 are squares and f(t)=6 is a nonsquare.
```

Both have `f(t) != 0`, so both lie in the same unit-valuation stratum
`d=0`, `epsilon=0`. Fix the local class `r=1`. Their `wl561` row bits are
opposite:

```text
n_13(t=0)=0,
n_13(t=10)=1.
```

## Compatibility With Either Orientation

Normalize the local norm-one factor `pi_0` to `1`; multiplication by an
arbitrary norm-one `pi_0` only reparametrizes the same norm-one torus, as in
`wl550`. For `q^2=t`, take `q=0` and `q=6` respectively.

For the local `B` orientation

```text
B=2*x*y/(x^2+y^2),
```

exact witnesses are

```text
q=0: (x,y)=(0,1),
q=6: (x,y)=(1,2).
```

For the local `R` orientation

```text
R=(x^2-y^2)/(x^2+y^2),
```

exact witnesses are

```text
q=0: (x,y)=(1,1),
q=6: (x,y)=(1,4).
```

All denominators are nonzero modulo `13`. Thus either surviving orientation
admits source-compatible residues with both possible leading-character bits.

## Exact Failure Point

The leading vector `n` in `wl561` is not a function of the local
source-square conditions, the valuation parity `epsilon`, and the selected
orientation alone. The character equation removes one of the two local
configurations when `r=1`, but the orientation does not predict which row bit
must occur globally.

Therefore another residue-level orientation table cannot close the assembled
matrix. A strict next step must use global integer compatibility among the
orientation equations, the standard square, and positivity, or isolate a
parameter subfamily where the global class fixes a row sign incompatible with
all global lifts.

## Boundary

These finite-field witnesses are counterexamples only to local determinacy;
they are not rational `wl535` points or global integer candidates. This work
does not solve the character matrix, handle the nontrivial real-unit class,
prove `wl535`, or enter M3.
