# wl597 HRL Closure Discriminant and Dyadic Branch Reduction

## Scope

This checkpoint reopens the exact `wl596` positive divisor-pair system with
one algebraic projection and one uniform parity lemma. It does not alter the
`wl596` allocation proof and does not claim an exclusion theorem.

Put

```text
S=Abar+Bbar, R=Abar-Bbar>0, D=S*R,
z=q1*q2, E=q1^2+q2^2,
F(q)=((q^2-S^2)(q^2-R^2))/(4*q^2).
```

For a source point, `4*U_i^2=q_i^2+D^2/q_i^2-S^2-R^2`. Eliminating the
two `U_i` from a closure value `T` (`T=S` or `T=R`) gives

```text
(4*T^2-e1-e2)^2=4*e1*e2.
```

After substituting `z` and `E`, this is the quadratic

```text
(z^2-D^2)^2 E^2
 - 8*T^2*z^2*(z^2+D^2) E
 - 4*z^2*(D^4-6*D^2*z^2-8*T^4*z^2+z^4) = 0.
```

Its discriminant factors as

```text
16*z^2*K_1(z)*K_T(z),
K_1(z)=(z^2-D^2)^2-4*D^2*z^2,
K_T(z)=(z^2-D^2)^2-4*T^4*z^2.
```

Therefore every strict point supplies the smaller symmetric gate

```text
K_1(z)*K_T(z) is an integer square,
z | D^2, z >= S^2,
```

with

```text
E=[4*T^2*z^2*(z^2+D^2) +/- 2*z*sqrt(K_1*K_T)]/(z^2-D^2)^2.
```

The projection is reversible only after retaining the exact lifts: `E+2*z`
and `E-2*z` must be integer squares, their roots must recover positive
divisors `q_1,q_2|D` with the parity and `q_i>=S` conditions, and both
individual `F(q_i)` must be integer squares. The sign of
`4*T^2-e1-e2` selects the relevant member of the sum/ordered-difference
closure union. The product-square condition alone is not an obstruction: it
is automatically square on the exact source-square domain and has false
divisor-supported candidates after the individual lifts are removed.

## Uniform dyadic reduction

Every finite source point has `4|U_i`.

If `Abar,Bbar` have opposite parity, then `S,R,q_i,d_i` are odd and
`a_i=(q_i+d_i)/2`, `b_i=(q_i-d_i)/2` have opposite parity. The member paired
with an odd base must be odd, since an even square minus an odd square is
`3 mod 4`. The difference of odd squares is `0` or `8 mod 16`, while a
square cannot be `8 mod 16`; hence `U_i^2=0 mod 16`.

Thus every finite `U_1 +/- U_2` is divisible by `4`, whereas both physical
closure targets `S,R` are odd. The entire opposite-parity parameter class is
removed.

If `Abar,Bbar` are both odd, parity forces `q_i,d_i` even. Then `a_i,b_i`
have the same parity and cannot both be even, so they are both odd; the same
odd-square argument gives `4|U_i`. Exactly one of `S,R` has `v_2=1`, so the
corresponding physical branch is impossible. Only the target divisible by
`4` remains. Writing `q_i=2Q_i,d_i=2D_i`, the oddness of `a_i,b_i` makes
`Q_i,D_i` opposite parity. Hence, with `alpha=v_2(D)`,

```text
v_2(q_i) in {1, alpha-1};
```

all intermediate dyadic allocations are excluded. When `alpha` is even the
dyadic part of `q_1q_2` is automatically a square; when `alpha` is odd one
agreement bit remains.

## Exact status

This is an accepted `precise_smaller_arithmetic_proposition`: it removes the
opposite-parity family, one physical `T` branch in the remaining class, the
two source radicals, and the ordering coordinate from the closure square
condition. It does **not** determine the odd squareclass of `q_1q_2`, classify
the surviving divisor pairs, or imply a Selmer/rank/family theorem.

The executable certificate is
`scripts/theory/aa_bb/wl597_hrl_closure_discriminant.py`, with focused tests
in `tests/theory/aa_bb/test_wl597_hrl_closure_discriminant.py`.

The next exact gate is the surviving odd-`Abar,Bbar` branch: combine the
endpoint dyadic allocation with the symmetric `z,E` gate and the two
individual source-square predicates. No standalone local table or product
squareclass claim is authorized from this checkpoint.
