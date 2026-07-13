# wl589 Mixed D0 Relative 2-Descent Proof Data

## Scope

This checkpoint treats only

~~~text
support=u_3+v_5+w_17|L=3|T=10|d=(15,51,85),  R^2=P_op.
~~~

It constructs D0 data for the mixed fixed cover. It does not edit wl587,
re-enter wl535, run D1 odd-prime filters, classify rational points, or make
a Selmer, rank, Sha, or family-exclusion claim.

The executable certificate is

~~~text
scripts/theory/aa_bb/wl589_mixed_d0_relative_2_descent.py
~~~

with focused tests in

~~~text
tests/theory/aa_bb/test_wl589_mixed_d0_relative_2_descent.py
~~~

## Parameter Base And Source Cover

The parameter base is Spec(Q). The fixed data are

~~~text
L=3, T=10, p=8*L^2-2*T^2=-128,
sqrt(q)=136, q=18496,
e_minus=-p=128, e_pos=2*sqrt(q)=272, e_neg=-2*sqrt(q)=-272,
d=(15,51,85), 15*51*85=255^2.
~~~

The affine complete-d source is

~~~text
X-128 = 15*u0^2
X-272 = 51*u_plus^2
X+272 = 85*u_minus^2.
~~~

Two independent differences are

~~~text
5*u0^2 - 17*u_plus^2 = 48
3*u0^2 - 17*u_minus^2 = -80.
~~~

Parametrize the first conic from the rational point (u0,u_plus)=(8,4).
For the line

~~~text
u_plus = 4 + r*(u0-8)
~~~

the second intersection is

~~~text
D(r) = 17*r^2-5
A(r) = 17*r^2-17*r+5
B(r) = 17*r^2-20*r+5

u0       = 8*A(r)/D(r)
u_plus  = -4*B(r)/D(r).
~~~

The second difference then gives

~~~text
f(r) = 289*r^4 - 408*r^3 + 274*r^2 - 120*r + 25
W^2=f(r)
u_minus = 4*W/D(r).
~~~

The forward function-field map is

~~~text
r = (u_plus-4)/(u0-8),
W = D(r)*u_minus/4.
~~~

At (u0,u_plus)=(8,4), the forward slope is the tangent value r=10/17.
The other point with u0=8, namely (8,-4), is the r=infinity branch.
The inverse formulas therefore cover every finite source point. The source
inverse only requires D(r)!=0, while the t, factor, and fixed-cover polynomial
chart is the smaller open set D(r)*A(r)!=0. Both denominator divisors are
retained as explicit pole branches; D(r)=0 is also the projective boundary
where the affine u coordinates have poles. The tangent and infinity branches
are checked by direct substitution and limits, including both W signs.

The elliptic coordinates and centered-even function are

~~~text
X=128+15*u0^2
Y=255*u0*u_plus*u_minus
Y^2=(X-128)*(X-272)*(X+272)

t = Y/(2*(X-128))
  = -17*B(r)*W/(D(r)*A(r)),
N=(10+t)/2,
M=(10-t)/2.
~~~

The source-side product is an identity on the quartic:

~~~text
(N^2+9)*(M^2+9) = (Z/4)^2,
Z=X/2-t^2.
~~~

## Completion And Divisors

The source quartic has

~~~text
disc(f)=2^14*3^4*5^4*17^2
~~~

and is squarefree, geometrically integral, and genus one. Its two points at
infinity are rational:

~~~text
I_plus  : W/r^2 -> 17
I_minus : W/r^2 -> -17.
~~~

The only poles of t are the four points above D(r)=0 and the four points
above A(r)=0; all are simple. Thus

~~~text
D_t=(t)_infinity,  deg(D_t)=8,
div(D(r))=D_0-2*(I_plus+I_minus),
div(A(r))=D_A-2*(I_plus+I_minus),
D_t ~ 4*(I_plus+I_minus).
~~~

The two factors and their product are

~~~text
F_plus  = N^2+49 = (t^2+20*t+296)/4
F_minus = M^2+49 = (t^2-20*t+296)/4
P_op    = F_plus*F_minus = (t^4+192*t^2+87616)/16.
~~~

For Z_a=(t-a) as a fiber divisor, the zero divisors are

~~~text
div(F_plus)  = Z_{-10+14i}+Z_{-10-14i}-2*D_t
div(F_minus) = Z_{10+14i}+Z_{10-14i}-2*D_t.
~~~

Each Z_a has degree eight and is reduced. The branch divisor of the fixed
cover is

~~~text
B=div(P_op) mod 2
 =Z_{-10+14i}+Z_{-10-14i}+Z_{10+14i}+Z_{10-14i},
deg(B)=32.
~~~

On the finite chart, define

~~~text
J_plus  = 289*B(r)^2*f(r) - 340*B(r)*W*D(r)*A(r) + 296*D(r)^2*A(r)^2
J_minus = 289*B(r)^2*f(r) + 340*B(r)*W*D(r)*A(r) + 296*D(r)^2*A(r)^2.
~~~

Their product reduces to

~~~text
K(r)=J_plus*J_minus
    =83521*B(r)^4*f(r)^2
     +55488*B(r)^2*f(r)*D(r)^2*A(r)^2
     +87616*D(r)^4*A(r)^4.
~~~

K has content 25; its primitive degree-16 polynomial is squarefree. The
fixed square locus has the polynomial model

~~~text
W^2=f(r),  rho^2=K(r),  rho=4*(D(r)*A(r))^2*R.
~~~

The finite polynomial chart has source-open condition D(r)*A(r)!=0. The
normalization retains the four points over D(r)=0 and the four points over
A(r)=0 as unramified points above t-poles.

It is a degree-two cover of the genus-one source with 32 simple branch
points, hence its smooth normalization has genus 17. The simultaneous factor
cover is a distinct generic degree-four biquadratic lift; its two branch sets
are disjoint and its generic genus is 33. The factor cover is not the fixed
cover and is not the Picard square-root torsor.

The branch projection, source, pole, t=0, and factor-zero resultants are all
nonzero where required. The primitive branch discriminant has support

~~~text
{2,3,5,7,17,29,37}.
~~~

## Picard Data

Let O=I_plus and write H=I_plus+I_minus. Since D_t~4H,

~~~text
[D_t-8*O] = 4*[I_minus-I_plus].
~~~

The factor square-root line bundles are

~~~text
L_plus  = O_C(D_t),  L_plus^2=O_C(B_plus),
L_minus = O_C(D_t),  L_minus^2=O_C(B_minus),
~~~

and both have Pic0 class [D_t-8*O].

The fixed-cover branch line bundle satisfies O_C(B)=O_C(4*D_t). Its four
rational Picard square roots are

~~~text
L0=O_C(2*D_t),
L0 tensor eta_minus_p,
L0 tensor eta_pos_2sqrt_q,
L0 tensor eta_neg_2sqrt_q,
~~~

with base Pic0 class [2*D_t-16*O]=8*[I_minus-I_plus].

The binary-quartic invariants are I=14896 and J=-2597888, giving the
Jacobian model

~~~text
v^2=u^3-402192*u+70142976
 = (u-516)*(u-192)*(u+708).
~~~

The rational 2-torsion classes are represented by

~~~text
eta_minus_p       = (u,v)=(192,0),
eta_pos_2sqrt_q   = (u,v)=(516,0),
eta_neg_2sqrt_q   = (u,v)=(-708,0),
eta_0             = 0.
~~~

The identification with the original elliptic model is

~~~text
u=9*X/4-96,  v=27*Y/8,
~~~

which maps the roots 128,272,-272 to 192,516,-708. These are Picard classes
of O_C(B), not the relative constant twists.

The executable checks verify the factorization polynomial, all three root
images, the 729/64 equation scaling, and the y-coordinate scaling 27/8.

## Constant Twists And Completeness

The exact structural support is

~~~text
S={2,3,5,7,17,29,37}.
~~~

For a squareclass d, the bidirectional factor-cover collection is

~~~text
W^2=f(r)
J_plus=d*s_plus^2
J_minus=d*s_minus^2.
~~~

The forward map to the fixed cover is

~~~text
F_plus  = d*(s_plus/(2*D(r)*A(r)))^2
F_minus = d*(s_minus/(2*D(r)*A(r)))^2
R       = d*s_plus*s_minus/(4*D(r)^2*A(r)^2).
~~~

Conversely, at a nonzero rational square-locus point, the product
F_plus*F_minus=R^2 forces the two factor values to have the same sign and
the same valuation parity at every place. Outside S, simple disjoint good
reduction of the two zero divisors and even pole orders force both factor
valuations to be even. Therefore their common squareclass is in Q(S,2).
The cleared variables s_plus and s_minus then recover exactly one of the
displayed factor covers, and rho=d*s_plus*s_minus recovers the fixed cover.
The zero and pole branches are handled separately below.

There are 2^8=256 signed squarefree representatives in Q(S,2). The real
condition forces d>0; the dyadic condition forces d to be odd and d=5 mod 8.
The 16 remaining D0 candidates are

~~~text
5, 21, 29, 37, 85, 357, 493, 629,
3045, 3885, 5365, 22533, 51765, 66045, 91205, 383061.
~~~

No odd bad-prime local filter is applied to this list.

## Real, Dyadic, And Bad Fibers

The source quartic has no real zero and is positive at r=0, so it is
positive on the real line. Both factor values are positive on every finite
real source point. Since

~~~text
N=(10+t)/2, M=(10-t)/2,
~~~

the exact positive AA+BB cone is

~~~text
-10<t<10.
~~~

At 2, the finite source analysis is:

~~~text
r even: f(r)=1 mod 8, so W is odd;
r odd:  f(r)=12 mod 16 and f(r)/4=7 mod 8, impossible for W^2=f(r);
v2(r)<0: the leading term 17^2*r^4 dominates and t is odd.
~~~

The denominator discriminants are disc(D)=340 and disc(A)=-51, whose
2-adic unit classes are both 5; neither denominator branch has a Q2-point.
For every finite or infinite Q2 source point on the chart, t is odd, and

~~~text
4*F_plus  = t^2+20*t+296 = 5 mod 8,
4*F_minus = t^2-20*t+296 = 5 mod 8.
~~~

Therefore [F_plus]=[F_minus]=[5] and [P_op]=[1] in Q2*/Q2*2.

The odd bad-fiber rows are D0 inputs only:

| p | source reduction | primitive branch reduction | status |
|---|---|---|---|
| 3 | (r-1)^2*(r+1)^2 | -(r-1)^4*(r+1)^12 | unevaluated D0 input |
| 5 | -r^2*(r-1)^2 | 2*r^8*(r-2)*(r+1)*(r+2)*(r^2-2r-1)*(r^2+2r-2) | unevaluated D0 input |
| 7 | 2*(r^2-3r+1)*(r^2+2r+2) | -3*r^2*(r-1)^2*(r+3)^2*(r^2-3)^2*(r^2+r-3)^2 | unevaluated D0 input |
| 17 | 2*(r^2+8r+4) | -4 | unevaluated D0 input |
| 29 | -(r^2-2r-1)*(r^2+4r-4) | branch has repeated quadratic factors | unevaluated D0 input |
| 37 | source remains squarefree | branch leading behavior degenerates and has repeated factors | unevaluated D0 input |

The executable certificate retains exact reductions for 29 and 37; the
abbreviated table does not turn those rows into local conclusions. Odd
bad-prime filtering is reserved for D1.

All exceptional branches are retained:

~~~text
r=0:        regular rational points, W=+/-5, t=+/-17;
r=infinity: regular rational points, (u0,u_plus)=(8,-4), t=+/-17;
u0=0:       A(r)=0, four geometric points, simple t poles;
D=0:        four projective boundary points, simple t poles;
u_plus=0:   B(r)=0, four geometric points, t=0, F_plus=F_minus=74;
W=0:        four geometric points, t=0, F_plus=F_minus=74;
F_plus=0:   t=-10+/-14i, 16 geometric points;
F_minus=0:  t=10+/-14i, 16 geometric points;
R=0:        contained in the two factor-zero divisors.
~~~

The D, A, and B discriminants are respectively 340, -51, and 60; f is
irreducible over Q. Thus the nonregular rational branches listed above are
empty. At a t pole the two factors have pole order two and P_op has pole
order four, so the fixed cover is unramified there.

## Exact AA+BB Lift

The two orientation rows are

~~~text
AA: (A,B,L)=(3,7,3), source leg=3, opposite leg=7
BB: (A,B,L)=(7,3,3), source leg=3, opposite leg=7
~~~

Thus both orientations use source leg L=3 and the preserved opposite factor
is 7. The exact common-source lift is equivalent to

~~~text
c in C(Q) on the finite complete-d source, including r=infinity,
R^2=(N^2+49)*(M^2+49),
(N^2+9)*(M^2+9) is a rational square,
-10<t<10.
~~~

The second condition is the fixed square locus, and the third is automatic
from (N^2+9)*(M^2+9)=(Z/4)^2. No individual square condition on either
factor is added.

The consistency point

~~~text
r=10/17, W=15/17, t=17, N=27/2, M=-7/2
~~~

has

~~~text
P_op=226625/16,
~~~

which is not a rational square and it also lies outside the positive cone.
This is a consistency specialization only.

## Verification And Boundary

The strict executable checks pass:

~~~text
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q \
  tests/theory/aa_bb/test_wl589_mixed_d0_relative_2_descent.py
5 passed

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/aa_bb/wl589_mixed_d0_relative_2_descent.py \
  tests/theory/aa_bb/test_wl589_mixed_d0_relative_2_descent.py
All checks passed!

UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run python \
  scripts/theory/aa_bb/wl589_mixed_d0_relative_2_descent.py \
  --out /private/tmp/wl589-mixed.json --strict
status=ok
work_log=wl589
ready=True
violations=[]
~~~

This is a complete D0 proof-data certificate for the fixed mixed cover. It
does not resolve the six odd bad-prime local images, and it does not enter D1.
