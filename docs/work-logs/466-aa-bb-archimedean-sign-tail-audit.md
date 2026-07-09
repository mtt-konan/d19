# AA+BB Archimedean Sign-Tail Audit

## Question

After `wl465`, does the real place contribute an independent sign tail to the
AA+BB complete 2-descent pseudo-Selmer container `S~`?

## Result

No. The real local image has one nontrivial sign class, but that class is
already represented by rational 2-torsion. Therefore

```text
epsilon_sign = 0
```

and the pseudo-Selmer dimension ledger improves from

```text
dim_F2 S~ <= 2 + omega_{1 mod 4}(T) + epsilon_sign
```

to

```text
dim_F2 S~ <= 2 + omega_{1 mod 4}(T).
```

This still does **not** force `dim Sel_2(E)=2`, because the
`ell | T, ell == 1 mod 4` tail remains unresolved.

## Root Order

Use the complete 2-descent model

```text
E_L: Y^2 = (X-(-p))*(X-(2*sqrt_q))*(X-(-2*sqrt_q)),
T = A+B,
p = 8*L^2 - 2*T^2,
sqrt_q = T^2 + 4*L^2.
```

The three real roots are ordered as

```text
e_neg   = -2*sqrt_q
e_minus = -p
e_pos   =  2*sqrt_q
```

because

```text
e_minus - e_neg = 4*T^2 > 0,
e_pos - e_minus = 16*L^2 > 0.
```

## Real Sign Image

In the coordinate order

```text
(d_minus_p, d_pos_2sqrt_q, d_neg_2sqrt_q)
```

the product relation allows four sign triples:

```text
(+,+,+), (+,-,-), (-,+,-), (-,-,+).
```

The real curve has points only on the intervals

```text
X > e_pos
e_neg < X < e_minus
```

so the actual real local sign image is only

```text
(+,+,+)
(-,-,+).
```

The two other product-compatible sign classes are killed at the real place.

## Torsion Comparison

The surviving nontrivial class

```text
(-,-,+)
```

is already the sign image of rational 2-torsion, represented by

```text
T_minus_p,
T_neg_2sqrt_q.
```

Thus the real place contributes no new pseudo-Selmer dimension beyond the
torsion baseline:

```text
epsilon_sign = 0.
```

## Remaining Route

The only symbolic tail left in the cheap `S~` ledger is now

```text
omega_{1 mod 4}(T).
```

The next task is to kill or account for the primes

```text
ell | T,
ell == 1 mod 4.
```

This note stops at the sign row. It does not build the `T`-tail argument or
the full `C_d` local matrix.

## Boundary

This audit does not prove:

- `dim Sel_2(E)=2`,
- rank zero,
- `Sha[2]=0`,
- any family exclusion.

It only removes the archimedean sign tail from the AA+BB pseudo-Selmer
dimension ledger.
