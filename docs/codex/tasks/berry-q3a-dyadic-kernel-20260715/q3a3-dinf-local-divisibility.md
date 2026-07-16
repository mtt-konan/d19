# Q3a3 Exact Local Divisibility Of D_inf

## Outcome

Let `K_varpi=Q_2(i)`, `lambda=1+i`, and

```text
C: y^2=f(t),
f=t^6+(-2-2*i)t^5+(-35-8*i)t^4+(-52-28*i)t^3
  +(19-40*i)t^2+(6+14*i)t-1.
```

With `P_+=(0,1)` and `P_-=(0,-1)` in the reciprocal chart
`x=1/t, z=y/t^3`, the exact result is

```text
[P_+-P_-] is not in 2 J(K_varpi).
```

This is an obstruction for the divisor class, not an evaluation of its
trivial fake squareclass.

## Halving Reduction

Use the split even-degree Mumford representation

```text
E=(u,v:n),
deg(u)=d <= 2,
0 <= n <= 2-d,
```

where the class is represented by
`div(u,v)+n P_+ +(2-d-n)P_--P_+-P_-`. Thus a degree-two class is
`Q_1+Q_2-P_+-P_-`, and the two degree-one cases are `Q-P_+` and `Q-P_-`.

For `d=2`, or for the `n=0` degree-one case, a principal divisor for
`2E-D_inf` has the form `div(w-y)`, with

```text
w=-t^3+r*t^2+s*t+d0,
u monic of degree d,
w^2-f=c*u^2.
```

The leading sign is forced by the two infinity branches. In fact,
`w-y=c*u^2/(w+y)` at `P_-` gives

```text
d=2: div(w-y)=2*div(u)-3*P_+-P_-;
d=1: div(w-y)=2*div(u)+P_--3*P_+.
```

These are exactly `2E-D_inf`, including both infinity points. The function
field pole bounds force every such function to be `w-y` after scaling, so
the identity is necessary, not just a sufficient ansatz. A factor-zero root
cannot be a Weierstrass root: `u^2 | w^2-f` and the squarefreeness of `f`
would contradict a simple root of `f`. Thus no singular or branch division
is hidden in this reduction.

The congruence `v=w mod u` is the exact tangent/Cantor condition for the
finite Mumford divisor; the polynomial divisibility `u^2 | w^2-f` also covers
repeated finite support. No evaluation denominator is inverted at a factor
zero or tangent point.

The remaining degree-one representation `E=Q-P_-` would require a function
with divisor `2Q-P_+-P_-`. The space `L(P_++P_-)` is spanned by `1,t`, so
this is possible only when `Q` is a rational Weierstrass point. The frozen
Q3a2 local factor degrees `(2,4)` give no degree-one factor of `f` over
`K_varpi`, so this branch is absent.

## Degree Zero And One

For `u=1`, coefficient comparison in `w^2-f=c` gives successively

```text
r=1+i,
s=35/2+5*i,
d0=(77+73*i)/2,
```

but the coefficient of `t^2` in `w^2-f` is

```text
(1065+1460*i)/4 != 0.
```

Therefore the possible `3 D_inf=0` branch is impossible. The other
degree-zero classes would require `D_inf=0`; that is excluded by `l(P_-)=1`
(a simple pole cannot give a nonconstant function on this genus-two curve).

For `u=t+a`, the same first three comparisons give

```text
r=1+i,
s=35/2+5*i,
d0=(77+73*i)/2,
c=1065/4+365*i,
a=(1378713+131985*i)/653165.
```

The constant coefficient then equals

```text
(-465740071+634874366*i)/653165 != 0,
```

so the degree-one `Q-P_+` branch is impossible over every characteristic-zero
field containing `i`.

## Degree Two Elimination

For `u=t^2+a*t+b`, coefficient comparison gives the exact system

```text
-b^2*c+d0^2+1 = 0
-2*a*b*c+2*s*d0-6-14*i = 0
-a^2*c-2*b*c+2*r*d0+s^2+40*i-19 = 0
-2*a*c+2*r*s-2*d0+52+28*i = 0
r^2-2*s-c+35+8*i = 0
-2*r+2*i+2 = 0.
```

Exact lexicographic elimination over `Q(i)` gives the following necessary
monic equation for `c`:

```text
P(c) = c^10+(-210-68*i)c^9+(16401+12900*i)c^8
 +(-537592-974672*i)c^7+(1926370+37085584*i)c^6
 +(356741044-725661880*i)c^5+(-9952074358+5948878392*i)c^4
 +(106782453448+13561791344*i)c^3
 +(-371183289347-503636744112*i)c^2
 +(-878727109554+2079369073884*i)c
 +(4745893054341+25610622340*i).
```

The exact Sage elimination and the local certificate are reproduced by
`scripts/theory/berry_sextic_q3a3_dinf.sage` and the pure-Python verifier
`scripts/theory/berry_sextic_q3a3_dinf.py`.

## Exact Dyadic Obstruction

Write `v_lambda(lambda)=1` and reduce to `F_2`. Since `P` is monic and
`P(c) mod lambda=(c+1)^10`, any root in `K_varpi` is integral and starts
with `c=1`. In each row below set
`q(z)=P(B+lambda^m*z)/lambda^M`; the displayed `R(z)` is the exact
reduction of `q` modulo `lambda`.

| `B` | `m` | `M` | `R(z)` | consequence |
|---|---:|---:|---|---|
| `1` | 1 | 10 | `z^10` | `z=0` |
| `1` | 2 | 20 | `(z+1)^10` | `z=1` |
| `1+lambda^2` | 3 | 30 | `z^6*(z+1)^4` | two branches |
| `1+lambda^2+lambda^3` | 4 | 34 | `(z+1)^4` | `z=1` |
| `1+lambda^2+lambda^3+lambda^4` | 5 | 36 | `1` | no root |
| `1+lambda^2` | 4 | 36 | `(z+1)^6` | `z=1` |
| `1+lambda^2+lambda^4` | 5 | 42 | `(z+1)^6` | `z=1` |
| `1+lambda^2+lambda^4+lambda^5` | 6 | 46 | `(z+1)^2` | `z=1` |
| `1+lambda^2+lambda^4+lambda^5+lambda^6` | 7 | 48 | `z^2+z+1` | no root in `F_2` |

The third row splits into the two displayed branches. The first branch
terminates at the constant residual `1`; the second terminates at the
irreducible quadratic `z^2+z+1`. Hence `P` has no root in `K_varpi`, and
the degree-two halving identity has no local solution.

This is a finite exact valuation/residue argument from a monic elimination
polynomial. It is not a bounded point search, p-adic stabilization, or
finite-precision factorization.

## Fake-Kernel Consequence

The even-degree function identity

```text
div(t-theta)=2*W_theta-P_+-P_-
```

still gives the fake evaluation `delta_varpi(D_inf)=[1]=0`. The obstruction
above proves that its source class in `J(K_varpi)/2J(K_varpi)` is nonzero.
Therefore the line spanned by `D_inf` is a certified one-dimensional
subspace of `ker(delta_varpi)`. It gives only

```text
dim ker(delta_varpi) >= 1,
dim im(delta_varpi) <= 4
```

from the frozen source dimension `5`; it does not determine the remaining
fake image or the full local kernel.

## Validation

```text
HOME=/private/tmp/d19-sage-home SAGE_TMP_DIR=/private/tmp/d19-sage-tmp \
  sage scripts/theory/berry_sextic_q3a3_dinf.sage
python3 scripts/theory/berry_sextic_q3a3_dinf.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q \
  tests/test_berry_sextic_q3a3_dinf.py -n 1
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/berry_sextic_q3a3_dinf.py \
  tests/test_berry_sextic_q3a3_dinf.py
git diff --check
```
