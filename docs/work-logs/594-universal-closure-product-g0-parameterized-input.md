# wl594 Universal Closure-Product G0 Parameterized Input

## Scope

This checkpoint encodes the accepted G0 truth-and-novelty audit for the
universal AA/BB closure-product family. It does not create a Kummer,
split-prime, or local-image obstruction and does not select G1.

The exact certificate is:

```text
scripts/theory/aa_bb/wl594_universal_closure_product_g0.py
```

## Exact Centered Products

For a signed centered pair with `N+M=T`, set

```text
t=N-M,
N=(T+t)/2,
M=(T-t)/2.
```

These coordinates satisfy the exact identities

```text
N+M=T,
N-M=t,
T+t=2*N,
T-t=2*M.
```

For `L` equal to `A` or `B`, the existing AA/BB quotient product is

```text
(N^2+L^2)(M^2+L^2) = Q_L(t)/16,
```

where

```text
Q_L(t)
  = ((T+t)^2+4*L^2)*((T-t)^2+4*L^2)
  = t^4 + (8*L^2-2*T^2)*t^2 + (T^2+4*L^2)^2.
```

The cleared square roots are `z_L=4*y_L`, and the product cover is

```text
W^2 = Q_A(t)*Q_B(t),
W = z_A*z_B.
```

For `T=A+B`:

```text
Q_A = t^4 + 2*(A-B)*(3*A+B)*t^2 + (5*A^2+2*A*B+B^2)^2
Q_B = t^4 - 2*(A-B)*(A+3*B)*t^2 + (A^2+2*A*B+5*B^2)^2
```

For `T=|A-B|`, after choosing `A>B>0`:

```text
Q_A = t^4 + 2*(A+B)*(3*A-B)*t^2 + (5*A^2-2*A*B+B^2)^2
Q_B = t^4 + 2*(A+B)*(3*B-A)*t^2 + (A^2-2*A*B+5*B^2)^2
```

## Scale, Smoothness, And Genus

The scale law is

```text
(A,B,T,t) -> k*(A,B,T,t),
Q_L -> k^4*Q_L,
W -> k^4*W.
```

The last law is an identity on the product equation, not a label:

```text
W^2-Q_A*Q_B=0
  => (k^4*W)^2-(k^4*Q_A)*(k^4*Q_B)
     = k^8*(W^2-Q_A*Q_B)=0.
```

After common scale and `A<->B`, the genuine parameter is

```text
lambda=A/B,
lambda>=1.
```

The plus branch has `T/B=lambda+1`; the minus branch has `T/B=lambda-1`
after `A>B`. The boundary `B=0` is excluded and `lambda=1` is degenerate.

The exact identities are

```text
disc(Q_L) = 2^16*L^4*T^4*(T^2+4*L^2)^2

Res(Q_A,Q_B)
  = 2^16*(A^2-B^2)^4
      *(T^2+(A-B)^2)^2*(T^2+(A+B)^2)^2

disc(Q_A*Q_B)
  = 2^64*A^4*B^4*T^8*(A^2-B^2)^8
      *(T^2+4*A^2)^2*(T^2+4*B^2)^2
      *(T^2+(A-B)^2)^4*(T^2+(A+B)^2)^4.
```

For the `x=t^2` quotient, the corresponding exact factors are

```text
disc(f_A) = -2^6*A^2*T^2,
disc(f_B) = -2^6*B^2*T^2,
Res(f_A,f_B)
  = 2^8*(A^2-B^2)^2
      *(T^2+(A-B)^2)*(T^2+(A+B)^2).
```

All algebraic degeneracy factors are retained by the script. On the positive
real domain the smooth product domain is exactly

```text
A>0, B>0, T>0, A!=B.
```

The degree-eight product cover has genus `3`. The involution `t->-t` gives

```text
x=t^2,
w=W,
w^2=f_A(x)*f_B(x),
f_L(x)=x^2+(8*L^2-2*T^2)*x+(T^2+4*L^2)^2,
```

which is a genus-one quartic. It has universal midpoint points

```text
x=0,
w=+/-((T^2+4*A^2)*(T^2+4*B^2)).
```

The simultaneous cover

```text
z_A^2=Q_A(t),
z_B^2=Q_B(t)
```

has genus `5` on the smooth parameter domain.

## Forward Image And Boundaries

An exact candidate maps forward by

```text
t=N-M,
W=z_A*z_B,
x=t^2.
```

The converse hierarchy is strict:

1. `x` must be a nonzero positive rational square in the correct interval;
2. `Q_A(t)` and `Q_B(t)` must be individual rational squares;
3. the four original distance-square factors must lift individually.

For positive `N,M` and the two sum branches,

```text
N1+N2=c,
c in {A+B,|A-B|},
|t|<T,
```

with `t= N1-N2`. The midpoint is `t=0`, and `t=+/-T` are endpoint
boundaries with one signed coordinate zero.

Equivalently, for every target `c` in `{A+B,|A-B|}` with `c>0`, the sum
orientation is

```text
N1+N2=c,
T=c,
N=N1,
M=N2,
t=N1-N2,
|t|<T.
```

The physical difference branches are represented by signed coordinates. For
one orientation,

```text
N1-N2=c,
N=N1,
M=-N2,
t=N1+N2>T.
```

The swapped orientation is a separate exact representative:

```text
N2-N1=c,
T=c,
N=N2,
M=-N1,
t=N1+N2>T.
```

In the first orientation `t-T=2*N2`; in the swapped orientation
`t-T=2*N1`, so the strict signed interval follows from `N1,N2>0`. Thus the
same quartic covers both signed difference representatives, but `|t|>T`, not
the positive-sum interval. Both orientations are required independently for
each target `c=A+B` and `c=|A-B|`. When `T=0` and `A=B` on the minus branch,
the sum branch has no positive pair and the quartics become squares; the
physical difference branch is the centerline and is separately degenerate.

The full GEN-CLOSURE quantifier retained by this checkpoint is:

```text
For every exact AA+BB candidate with A,B,N1,N2>0,
{N1+N2, |N1-N2|} intersects {A+B, |A-B|}.
```

Its four branches are `N1+N2=A+B`, `N1+N2=|A-B|`,
`|N1-N2|=A+B`, and `|N1-N2|=|A-B|`; no target or difference orientation
is dropped. The smooth G0 chart adds `A!=B` and `T>0`; the `A=B`, `T=0`
zero-target branch is retained separately as the degenerate case above.

The factor-zero roots are

```text
(T+t)^2+4*L^2=0 -> t=-T+/-2*i*L
(T-t)^2+4*L^2=0 -> t=T+/-2*i*L.
```

Infinity consists of two unramified points on the even-degree product cover.
The elliptic cubic chart `u=(w-h)/x` has a denominator at `x=0`; the midpoint
must be handled outside that chart.

## Novelty Boundary

The accepted outcome is:

```text
exact_parameterized_input_ready
```

This is a genuine parameterized lower-genus forward-obstruction input,
analogous in scope to `wl585`. It is not a proved obstruction.

The whole product cover is locally soluble because the midpoint exists for
every parameter. Also, `[Q_A*Q_B]` is automatically trivial on every exact
AA+BB candidate. These facts do not settle the restricted nonmidpoint image.

No uniform Kummer character, split-prime obstruction, or restricted
local-image theorem is proved here. The next exact G1 obligation must act on
the restricted nonmidpoint image and add uniform square-specialization or
local-image information, retaining the square-`x`, positivity, individual
AA/BB, and full four-factor lifts.

The long-term AA+BB closure objective remains open. No rank table, finite
search, new family, D2, D5, M3, or G1 obligation is executed by this checkpoint.
