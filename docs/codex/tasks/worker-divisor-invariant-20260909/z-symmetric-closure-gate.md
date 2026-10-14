# Symmetric `z=q_1q_2` Closure Gate

## Result

The six closure equations admit an exact symmetric elimination.  Put

```text
D = S*R,       z = q_1*q_2,       E = q_1^2+q_2^2,
F(q) = ((q^2-S^2)*(q^2-R^2))/(4*q^2).
```

For a closure value `T` (either `S` or `R`), eliminating the two source
roots from `U_1+U_2=T` or `|U_1-U_2|=T` starts from

```text
(T^2-F(q_1)-F(q_2))^2 - 4*F(q_1)*F(q_2) = 0.
```

For the sum branch `T=S`, after clearing denominators this is a quadratic in
`E` with leading coefficient `(z^2-D^2)^2` and linear coefficient

```text
-8*S^2*z^2*(z^2+D^2).
```

Its discriminant factors exactly as

```text
16*z^2 * K_1(z) * K_S(z),

K_1(z) = (z^2-D^2)^2 - 4*D^2*z^2
        = z^4 - 6*D^2*z^2 + D^4,

K_S(z) = (z^2-D^2)^2 - 4*S^4*z^2
        = z^4 - 2*D^2*z^2 - 4*S^4*z^2 + D^4.
```

Therefore every non-boundary closure point supplies the new necessary global
condition

```text
K_1(z)*K_S(z) is an integer square,   z | D^2,   z >= S^2.
```

For the physical difference branch `T=R`, the same formula holds with
`K_S` replaced by

```text
K_R(z) = (z^2-D^2)^2 - 4*R^4*z^2.
```

The two possible values of `E` are

```text
E = [4*T^2*z^2*(z^2+D^2) +/- 2*z*sqrt(K_1*K_T)]/(z^2-D^2)^2.
```

Here `z^2-D^2 != 0` because `z >= S^2 > D=SR`.  To recover the original
pair, one must additionally require `E+2*z` and `E-2*z` to be integer
squares (which in particular makes `E^2-4*z^2` a square) and take

```text
q_{1,2} = (sqrt(E+2*z) +/- sqrt(E-2*z))/2,
```

with integral positive `q_i | D`, `q_i >= S`, parity, and the two original
individual predicates `F(q_i)=U_i^2`.  The sign of
`T^2-F(q_1)-F(q_2)` selects the sum versus difference member of the closure
union.  Thus the elimination is reversible only with these retained source
and positivity conditions.

## Why this is not yet an exclusion

The product-square condition alone has many divisor-supported solutions and
does not imply the individual source squares.  For example, with
`(S,R,D)=(8,6,48)`, both `z=96` and `z=144` divide `D^2` and satisfy
`K_1*K_S` square (`K_S(144)=0`); at `z=96` one branch even gives
`E=320` and `E^2-4z^2=256^2`, but the recovered pair `(q_1,q_2)=(288,32)`
has `F(288)=2982385/144` and `F(32)=3705/16`, so the source-square
predicates fail.  The gate therefore removes the ratio coordinate only after
retaining the exact individual lifts; it is a smaller exact arithmetic
proposition, not a family exclusion or a support theorem.

No frozen `wl596` artifact was changed.  This note is a candidate reopening
input: classify the divisor-supported `z` for which both `K_1K_T` and the
recovered individual `F(q_i)` conditions hold, then evaluate `[z]`.
