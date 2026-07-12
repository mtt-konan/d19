# M2 Pure v_ell Positivity Transfer To The Unit-Class Cone

## Question

How does the remaining real positivity inequality interact with the unique
`eta=i` coordinate equations from `wl552`?

## Positivity Identity

Keep

```text
E=4*(ell-1)*Q^2*D^2,
F=R-E,
R=Q^4+4*Q^2*D^2-4*D^4.
```

The homogenized `wl535` positivity polynomial is

```text
H=ell*Q^4+4*Q^2*D^2-4*ell*D^4.
```

Directly,

```text
H=ell*R-E=(ell-1)*E+ell*F.
```

This transfers positivity from the `(Q,D)` quartic to the two coordinates of
the Gaussian class equation.

## The ell = 5 mod 8 Cone

The `wl552` equations are

```text
E=-2*r*m*n,
F= r*(m^2-n^2),
```

with positive odd squarefree `r`. Since `E>0`, one has `m*n<0`, and

```text
H=r*C_ell(m,n),
C_ell(m,n)=ell*(m^2-n^2)-2*(ell-1)*m*n.
```

Thus the exact positivity condition is

```text
C_ell(m,n)>0.
```

## The ell = 1 mod 8 Cone

After extracting `(1+i)^2` from `gamma`, `wl552` gives

```text
-E/4=-2*r*m*n,
-F/4= r*(m^2-n^2).
```

Equivalently `E=8*r*m*n` and `F=-4*r*(m^2-n^2)`. Hence `m*n>0` and

```text
H=-4*r*C_ell(m,n).
```

The exact positivity condition is now

```text
C_ell(m,n)<0.
```

The class `r` cancels from both sign tests.

## Positivity Alone Is Not An Obstruction

These cones contain parity-compatible integer points uniformly:

- for `ell ≡ 5 (mod 8)`, `(m,n)=(5,-8)` has opposite parity,
  `v_2(m*n)=3`, and

  ```text
  C_ell(5,-8)=41*ell-80>0;
  ```

- for `ell ≡ 1 (mod 8)`, `(m,n)=(1,2^k)` for every `k>=1` has opposite
  parity, positive product, and

  ```text
  C_ell(1,2^k)
    =ell*(1-2^(2k))-2^(k+1)*(ell-1)<0.
  ```

The second family allows arbitrarily large dyadic valuation of `m*n`, so it
is compatible with the high-valuation branch at the level of parity,
valuation, and positivity.

Therefore positivity, even after transfer to the unique unit class, cannot by
itself close either mod-8 branch.

## Next Exact Gate

The remaining obstruction is the simultaneous system: one of the two fixed
`wl546` integer orientations together with both `eta=i` coordinate equations
and the corresponding strict cone inequality above. A valid next step must
use that simultaneous global compatibility, not positivity or dyadic data in
isolation.

## Boundary

The displayed cone witnesses are not solutions of the full coordinate or
orientation equations and are not rational `wl535` points. This work does not
choose `r`, solve either simultaneous system, handle the nontrivial real-unit
class, prove `wl535`, or enter M3.
