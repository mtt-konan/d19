# wl587 Pure-u_7 D0 Relative 2-Descent Proof Data

## Scope

This checkpoint treats only

```text
support=u_7|L=7|T=9|d=(7,7,1),  R^2=P_op.
```

It does not process the mixed family, re-enter `wl535`, enter D1, run rank or
finite-search diagnostics, or make a theorem-level Selmer or family-exclusion
claim.

## Parameter Base And Source Cover

The base is `Spec(Q)`. Put

```text
p=230, sqrt(q)=277, q=277^2,
d=(7,7,1).
```

With `u0=u_{-p}`, `u+=u_{+2sqrt(q)}`, and `u-=u_{-2sqrt(q)}`, the affine
complete-d source cover is

```text
X+230 = 7*u0^2,
X-554 = 7*u+^2,
X+554 = u-^2.
```

Equivalently,

```text
u0^2-u+^2=112,
u-^2-7*u0^2=324.
```

Set `r=u0+u+` and `W=2*r*u-`. Since
`(u0-u+)(u0+u+)=112`, every finite source point has `r!=0`. The inverse maps
are

```text
u0=(r^2+112)/(2*r),
u+=(r^2-112)/(2*r),
u-=W/(2*r),
```

on

```text
C: W^2=7*r^4+2864*r^2+87808.
```

The induced elliptic coordinates are

```text
X=7*u0^2-230,
Y=7*u0*u+*u-,
Y^2=(X+230)(X^2-4*277^2).
```

The exact centered-even map is

```text
t=Y/(2*(X+230))
 = W*(r^2-112)/(4*r*(r^2+112)),
N=(9+t)/2,
M=(9-t)/2.
```

All identities, including the source product square, are checked by reduction
modulo the quartic equation in
`scripts/theory/aa_bb/wl587_pure_u7_d0_relative_2_descent.py`.

## Completion, Divisors, And Picard Data

The weighted projective closure of `C` is smooth and geometrically integral;
the source quartic discriminant is

```text
2^28*3^8*7^4*277^2.
```

It has genus one. Let `D_t=(t)_infinity`. Its eight simple points are the two
points over `r=0`, the four points over `r^2+112=0`, and the two points
`I_plus,I_minus` over `r=infinity`.

Define

```text
F_plus=N^2+4=(t^2+18*t+97)/4,
F_minus=M^2+4=(t^2-18*t+97)/4,
P_op=F_plus*F_minus=(t^4-130*t^2+9409)/16.
```

For `Z_a` the fiber divisor of `t=a`, the two factor divisors are

```text
div(F_plus)  = Z_{-9+4i}+Z_{-9-4i}-2*D_t,
div(F_minus) = Z_{ 9+4i}+Z_{ 9-4i}-2*D_t.
```

Each `Z_a` has degree eight and is reduced. The branch divisor is

```text
B=div(P_op) mod 2
 =Z_{-9+4i}+Z_{-9-4i}+Z_{9+4i}+Z_{9-4i},
```

of degree 32. The branch polynomial in the `r`-line is the squarefree degree-16
polynomial

```text
K_branch=f(r)^2*(r^2-112)^4
 -130*f(r)*(r^2-112)^2*(4*r*(r^2+112))^2
 +9409*(4*r*(r^2+112))^4,
```

where `f(r)=7*r^4+2864*r^2+87808`. It is squarefree; each of its roots has
the two points above it on `C`.

The fixed square-locus cover is only

```text
R^2=P_op,
```

with branch divisor `B`. It is not identified with any factor cover. On the
chart `D_t=4*r*(r^2+112)!=0`, define

```text
J_plus  = f(r)*(r^2-112)^2 + 18*W*(r^2-112)*D_t + 97*D_t^2,
J_minus = f(r)*(r^2-112)^2 - 18*W*(r^2-112)*D_t + 97*D_t^2.
```

The explicit constant factor-twist covering for a squareclass `d` is

```text
W^2=f(r),
J_plus=d*s_plus^2,
J_minus=d*s_minus^2.
```

The maps are

```text
F_plus=d*(s_plus/(2*D_t))^2,
F_minus=d*(s_minus/(2*D_t))^2,
R=d*s_plus*s_minus/(4*D_t^2).
```

Conversely, `rho=4*D_t^2*R=d*s_plus*s_minus` gives the polynomial model
`rho^2=K_branch`. The script checks all three cleared-factor identities.

The fixed cover is a degree-two extension of `Q(C)`. Over the geometric
function field, the two factor radicals have disjoint nonempty branch
divisors, so their simultaneous constant-twist schema is generically degree
four. It is therefore a biquadratic lift mapping to the fixed degree-two
cover, not an alternative name for that cover and not the four Picard square
roots of `O_C(B)`.

On the chart `r*(r^2+112)!=0`, the square locus has the equivalent polynomial
model

```text
W^2=f(r),
rho^2=K_branch(r),
rho=4*(4*r*(r^2+112))^2*R,
R=rho/(4*(4*r*(r^2+112))^2).
```

The normalization adds exactly the unramified points above the poles of `t`;
the divisor description below gives all of them.

The divisor relations

```text
div(r)=P0_plus+P0_minus-I_plus-I_minus,
div(r^2+112)=Q_sum-2*(I_plus+I_minus)
```

give `D_t ~ 4*(I_plus+I_minus)`. Hence

```text
B ~ 4*D_t,
L0=O_C(2*D_t),
[L0-16*O]=[2*D_t-16*O]
                    =8*[I_plus+I_minus-2*O]
```

in `Pic^0(C)` for `O=(28,2576)`. The factor square-root line bundles are

```text
L_plus=O_C(D_t),  L_plus^2=O_C(B_plus),  [L_plus-8*O]=[D_t-8*O],
L_minus=O_C(D_t), L_minus^2=O_C(B_minus), [L_minus-8*O]=[D_t-8*O].
```

The four square roots of `O_C(B)` are Picard square-root data for the fixed
cover only; they are not the relative constant factor-twist set. They are
represented by

```text
0, [W1-W2], [W1-W3], [W1-W4],
```

where `Wi=(alpha_i,0)` are the four branch points of the source quartic.

The Jacobian has the checked model

```text
v^2=x^3-420615936*x-2153603358720
  =(x-22704)(x+5520)(x+17184),
```

so all four 2-torsion classes are rational. In explicit root notation, write
`z1,z2` for the two roots of `7*z^2+2864*z+87808`, choose
`alpha^2=z1`, `beta=112/alpha`, and put `H=I_plus+I_minus`. The three
nonzero rational classes can be represented by

```text
[W_alpha+W_-alpha-H],
[W_alpha+W_beta-H],
[W_alpha+W_-beta-H].
```

Their doubles are principal from the corresponding quadratic polynomials in
`r`, and Galois permutes each pair or exchanges complementary pairs. This is
the complete rational Picard square-root torsor, not a replacement for the
constant factor coverings above.

The relative constant factor-twist candidates are indexed by `Q(S,2)` for
`S={2,3,5,7,53,97,277}`. The complete candidate set has 256 classes. The
real and 2-adic conditions below leave exactly 16 candidates:

```text
1, 97, 105, 265, 1113, 1385, 5817, 10185,
14681, 25705, 107961, 134345, 564249, 1424057,
1541505, 149525985.
```

The 256 candidates and the 16 real/Q2 survivors are distinct counts. No odd
bad-prime local filter is applied here.

## Local And Exceptional Fibers

At `2`, a source point must have `v2(r)=2`, so `r=4*s` with `s` odd and

```text
W=16*h,
h^2=7*s^4+179*s^2+343 = 1 mod 8.
```

The excluded `v2(r)=1` case gives `f(r)/16=3 mod 8`, while
`v2(r)>=3` gives `f(r)/256=7 mod 8`.

Then `v2(t)<=-2` and
`4*F_plus/t^2`, `4*F_minus/t^2` are both `1 mod 8`. Thus both factors and
`P_op` are 2-adic squares at every finite 2-adic source point with `D_t!=0`.
The denominator-zero branches are handled separately as unramified pole
branches. A constant twist has a 2-adic point only when its class is a
2-adic square.

Over the reals, the source quartic is positive for every real `r`, the two
factors have no real zeros, and `P_op>0` away from its fourth-order poles. The
positive source condition is exactly

```text
N>0 and M>0  <=>  -9<t<9.
```

The complete factor-cover bad-fiber set is `S`. This is checked separately for
`J_plus` and `J_minus`: both factor branch projections equal `K_branch`, both
are squarefree, and both have nonzero source, pole, and `r^2-112` resultants.
The executable structural invariant support of the source/branch
discriminants, leading coefficients, factor-zero resultants, denominator
discriminants, and all factor-specific resultants is exactly
`{2,3,5,7,53,97,277}`. Thus outside `S` each factor branch divisor is reduced
and disjoint from the other factor and from the even pole divisor, rather than
being inferred from the full `K_branch` projection alone.

For a rational source point, properness gives a point over every `Z_p` outside
`S`. At such a prime, a factor zero is simple and belongs to only one factor;
otherwise both factors are units, while a pole of either factor has even order.
If `F_plus*F_minus` is a square, odd valuation at a simple factor zero is
impossible. Therefore both factor valuations are even outside `S`, proving
that the factor squareclass lies in `Q(S,2)`.

The reductions are explicitly classified: at `2`, `f` and `K_branch` reduce to
`r^4` and `r^16`; at `3`, to `(r^2+1)^2` and `(r^2+1)^8`; at `5` and `53`, the
source stays squarefree while the branch polynomial acquires repeated factors;
at `7`, the leading coefficient degenerates and `f` reduces to `r^2`; at
`97`, source and branch share a quadratic factor; and at `277`, the source has
two doubled linear factors while the branch polynomial remains squarefree.
The odd-prime rows are deliberately unevaluated D0 inputs: no local point or
odd-prime twist survivor is claimed here.

All exceptional branches are retained:

- `r=0` and `r=infinity`: projective source boundary, simple `t` poles;
- `u0=0`, equivalently `r^2+112=0`: four finite points, `X+230=Y=0`, and
  simple `t` poles;
- `u+=0`, equivalently `r^2-112=0`, and `W=0`: `t=0`, with
  `F_plus=F_minus=97/4`;
- `F_plus=0`: 16 simple geometric points at `t=-9+/-4i`;
- `F_minus=0`: 16 simple geometric points at `t=9+/-4i`.
- `R=0`: contained in the two factor-zero branches, hence no rational point.

At every `t` pole both factors have even pole order and `P_op` has pole order
four, so these points are unramified on the normalized `R^2=P_op` cover. The
two factor zero divisors are disjoint, and neither meets a source branch or a
denominator point; the branch polynomial also has nonzero resultant with
`r^2-112`, so the inverse formula used to describe the zero fibers has no
hidden zero-denominator branch.

The rational exceptional branches are all empty: `r=0` would require
`W^2=87808`, infinity would require `sqrt(7)`, `u0=0` would require
`r^2=-112`, `u+=0` would require `r^2=112`, and `W=0` is impossible because
`f(r)>0` for real `r`. The factor-zero quadratics have discriminant `-64`, so
they have no rational `t`. Hence every rational square-locus point is on the
finite factor chart and the factor-cover completeness lemma applies.

## Exact AA+BB Lift

For the `AA` orientation the source leg is `7`; for `BB` it is also `7`, and
the opposite leg is `2`. The exact common-source condition is therefore

```text
c in C(Q), r*(r^2+112)!=0,
R^2=(N^2+4)*(M^2+4),
(N^2+49)*(M^2+49) is a rational square,
-9<t<9.
```

The second source product is automatic on `C`:

```text
(N^2+49)*(M^2+49)=(Z/4)^2,
Z=X/2-t^2.
```

The opposite product condition is exactly `R^2=P_op`. Thus the displayed
conditions are necessary and sufficient for the point-level AA+BB lift used by
`wl491`; no stronger individual-square condition is silently added.

For completeness, let a rational finite square-locus point have nonzero values
`f_plus=F_plus` and `f_minus=F_minus`. Put
`d=[f_plus]` in `Q^*/Q^*2`. Since `f_plus*f_minus=R^2`, the same class is
`[f_minus]`, so there are rational `a_plus,a_minus` with

```text
f_plus=d*a_plus^2,
f_minus=d*a_minus^2,
R=d*a_plus*a_minus.
```

The cleared variables `s_plus=2*D_t*a_plus` and
`s_minus=2*D_t*a_minus` put the point on exactly the `d` factor covering above.
The sign and every prime valuation parity are checked universally by an
exhaustive two-bit truth table: `f_plus*f_minus=R^2` forces the same sign and
the same parity at every prime, so `d in Q(S,2)` after the good-prime
argument. Conversely, any
rational point on one such factor covering reconstructs `F_plus`, `F_minus`,
and `R` by the displayed formulas, hence lies on `R^2=P_op`. The script runs
the universal field-level squareclass implication, both cleared maps, the
factor-specific good-prime checks, and every rational exceptional-branch
exclusion as executable structural checks.

The known `wl505` specialization `(r,W)=(28,2576)` gives
`t=69/4`, `N=105/8`, `M=-33/8`, and

```text
P_op=15172945/4096,
```

which is not a rational square and also fails positivity because `M<0`. This
is only a consistency specialization, not a rational-point classification.

## Verification And Boundary

`ready=True` is emitted only when executable checks pass for the source maps,
the source and fixed-cover normalizations, the two factor radicands, both
factor branch projections and their factor-specific bad-prime support, the
Picard line-bundle separation, the universal bidirectional factor-twist
lemma, the generated 256/16 twist sets, the rational exceptional branches,
and the AA+BB lift.
The focused test asserts those structural checks; the 16 locally surviving
constant classes are candidates only because odd bad-prime filters remain
unevaluated.

This is D0 proof-data construction only. It does not classify rational points
on the genus-seventeen cover, enter D1, or claim a family exclusion.
