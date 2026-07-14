# Berry Sextic B0 Covering Certificate

## Outcome

`precise_b0_actual_reduction_blocker`

This certificate freezes only the committed degree-6 row

```text
g6(t) = t^6 + (-2-2*i)t^5 + (-35-8*i)t^4 + (-52-28*i)t^3
        + (19-40*i)t^2 + (6+14*i)t - 1
```

over `K=Q(i)`. The two covers are

```text
C_1: v^2=g6(t),       C_i: i*v^2=g6(t),       t in P^1(Q).
```

The covering, models, maps, converses, exceptional fibers, and trivial-point
ledger below are certified. Both twists have actual bad reduction at
`(94*i-169)` and good reduction outside `{(1+i),(94*i-169)}`. Actual dyadic
reduction at `(1+i)` remains unresolved because the fixed-center radial audit
does not classify all Bruhat-Tits-tree directions. No rank, Selmer, Jacobian
decomposition, or bounded-search conclusion is made.

## Models and Geometry

For `d in {1,i}`, put `G(T,S)=S^6*g6(T/S)`. The smooth projective model is
the curve in `P_K(1,3,1)` with coordinates `[T:V:S]` and convention

```text
[T:V:S] ~ [lambda*T:lambda^3*V:lambda*S],
d*V^2=G(T,S).
```

The affine chart `S!=0` is `t=T/S`, `v=V/S^3`, giving `d*v^2=g6(t)`. The
second chart is

```text
x=S/T=1/t,  z=V/T^3,
d*z^2=g6^*(x),
g6^*(x)=1+(-2-2*i)x+(-35-8*i)x^2+(-52-28*i)x^3
         +(19-40*i)x^4+(6+14*i)x^5-x^6.
```

The ordinary plane closure `d*V^2*S^4=G(T,S)` has the singular point
`[0:1:0]`; the weighted model is the smooth projective model. The weighted
ambient singular point is not on the curve. Exact squarefreeness gives
smoothness in both charts. The map and involution are

```text
pi_d([T:V:S])=[T:S],
ι([T:V:S])=[T:-V:S].
```

There are six simple finite branch points, the roots of `g6`; infinity is not
branched. Riemann-Hurwitz gives `2*g-2=-4+6=2`, hence `g=2` for both twists.

At infinity the equation is `d*V^2=1`:

| twist | points above infinity |
|---|---|
| `d=1` | `[1:1:0]`, `[1:-1:0]`, both `K`-rational |
| `d=i` | `[1:+/-sqrt(-i):0]` over `K(sqrt(-i))`, none over `K` |

## Berry Map and Converse

Let

```text
f12(t)=g6(t)*conjugate(g6(t)),
F(A,B)=B^12*f12(A/B)=G(A,B)*conjugate(G(A,B)).
```

Explicitly,

```text
f12(t)=t^12-4*t^11-62*t^10+68*t^9+1647*t^8+4184*t^7
       +2716*t^6-376*t^5+623*t^4-788*t^3+194*t^2-12*t+1.
```

The Berry pullback is the weighted projective genus-5 curve

```text
C_B: W^2=F(A,B),
[A:B:W]~[lambda*A:lambda*B:lambda^6*W].
```

Its map to Berry's fourth-distance surface is the exact homogeneous map
`[A:B:W] -> [X_h(A,B):Y_h(A,B):Z_h(A,B):T_h(A,B):W]` in `P^4`, where
`T_h=B*T_homogeneous_degree_5`; the coordinate forms have no common
projective zero.

For a point on `C_d` with rational base `[T:S]=[A:B]`,

```text
U = epsilon*V*conjugate(V),  epsilon in {+1,-1},
[A:B:W]=[A:B:U].
```

Affinely this is `(t,v) -> (t,epsilon*Norm(v))`. The sign `V -> -V` is the
genus-2 involution and does not change the norm; `epsilon` gives the two Berry
`W` signs.

Conversely, for a rational point on `C_B`, write `t=A/B` with primitive
integers `A,B` and set `G(A,B)=B^6*g6(A/B)`. Then
`G(A,B)*conjugate(G(A,B))=W^2`. A Gaussian prime away from `1+i` dividing
both factors would divide

```text
Res_t(g6,conjugate(g6))=2^40.
```

Thus away from `1+i` only one conjugate factor occurs and its valuation in `G`
is even. At `1+i`, conjugation preserves the valuation and
`v_(1+i)(G*conjugate(G))=2*v_(1+i)(G)` is divisible by four because `W` is
rational. Hence `G` is a unit times a square in `K`; the unit squareclasses
are exactly `{1,i}`. Therefore every affine rational-parameter Berry point
lifts to one of the two twist classes, with `v=V/B^3`. At `B=0`,
`G(A,0)=A^6`, so only `d=1` has `K`-rational points above infinity.

## Inverse Parameter Charts

The exact identities are

```text
X-2Y-Z = t*(Z-X),
-X+3Y+2Z+T = t*(X-Y+T).
```

The denominators factor as

```text
Z-X    = -2*(t-1)*h(t),
X-Y+T  =  4*t*h(t),
h(t)  = t^4+12*t^3+22*t^2-4*t+1.
```

The first ratio covers `t=0`, the second covers `t=1`, and both vanish at
the geometric node fiber `h(t)=0`. The polynomial `h` is squarefree and
irreducible over `Q`, so that fiber has no rational parameter. Infinity is
handled by the projective parameter chart and is not lost.

## Exceptional Fibers

The 16 Berry nodes are exactly the four gradient families

```text
A: [1:+/-1:+/-1:0]
B: [1:0:+/-1:+/-1]
C: [0:1:+/-sqrt(2):+/-1]
D: [+/-sqrt(2):1:0:+/-1].
```

The exact fiber audit gives every nonempty node fiber:

| node | parameter fiber |
|---|---|
| `[1:1:1:0]` | `t=infinity` |
| `[1:1:-1:0]` | `t=0` |
| `[1:0:1:1]` | `t=1` |
| `[1:0:-1:1]` | `t=-1` |
| `[1:0:1:-1]` | `h(t)=0` (four geometric parameters) |
| `[0:1:sqrt(2):-1]` | `t=-1-sqrt(2)` |
| `[0:1:-sqrt(2):-1]` | `t=-1+sqrt(2)` |

All other node fibers are empty. The gradient case split and all six
projective minors were checked exactly, including the radical nodes.

The rational special fibers are

```text
t=0:        [-1:-1:1:0]=[1:1:-1:0], f12=1;
t=1:        [1:0:1:1],          f12=2^13;
t=-1:       [1:0:-1:1],         f12=2^11;
t=infinity: [1:1:1:0],          F(1,0)=1;
h(t)=0:     [1:0:1:-1],         f12=2*Z(t)^2.
```

The coordinate-zero fibers are retained:

```text
Y=0: (t-1)(t+1)h(t);
X=0: (t^2+2t-1)(t^4+4t^3+22t^2+4t+1);
T=0: 2t*(5t^4+20t^3+14t^2-12t+5), plus infinity;
Z=0: the six geometric roots of Z(t).
```

The two roots of `t^2+2t-1` are the radical `C`-node fibers. The four roots
of the `X` quartic are nonnode coordinate-zero fibers. The `T` quartic and
the six roots of `Z` are also retained; none has a rational parameter except
`t=0` in `T=0`.

The factor-zero/branch fibers are the six simple roots of `g6` and the six
simple roots of its conjugate. The two factors are irreducible over `K`,
disjoint, and `f12` is irreducible over `Q`; hence no branch parameter is
rational and no collision or tangency is hidden. At a root of `g6`, `v=0` is
the unique ramified point on either twist and its Berry image has `W=0`.

## Finite Place Ledger

Write

```text
varpi=(1+i),
pi=(94*i-169),       Norm(pi)=37397,
pi_bar=(-94*i-169).
```

The exact factorizations are

```text
Disc(g6) = (i-1)^75*(94*i-169),
Disc(conjugate(g6)) = conjugate(Disc(g6)),
Disc(f12) = 2^155*37397,
Res(g6,conjugate(g6)) = 2^40.
```

These give distinct support ledgers:

| role | support over `K` |
|---|---|
| displayed integral `C_1`/`C_i` weighted models | `(1+i)`, `(94*i-169)` |
| Berry genus-5 pullback model | `(1+i)`, `(94*i-169)`, `(-94*i-169)` |
| factor collision/resultant support | `(1+i)` only |
| auxiliary coordinate-fiber separability over `Q` | `2`, `5`, `43`, `53` |

The first row is only the bad support of the displayed integral equations.
Outside it, `2` and `Disc(g6)` are units, so the affine and infinity charts
are smooth for both unit twists. This proves actual good reduction for both
curves at every finite prime outside `{varpi,pi}`.

At `pi`, the reduction is

```text
g6(t)=(t-11745)^2*(t+3615)*(t+9390)*(t^2+6501*t-12218) mod 37397,
```

The double root only diagnoses the displayed equation. The actual badness
claim uses the absolute Igusa invariant audit below, so it does not depend on
the existence of another integral model. At `varpi`, `i=1` in the residue
field and

```text
g6(t) = (t+1)^6 mod (1+i).
```

This proves that the displayed model is singular, but does not decide actual
reduction. Thus the actual curve status is, for both `d=1` and `d=i`,

```text
good proved:  every finite prime outside {varpi,pi}
bad proved:   {pi}
unresolved:   {varpi}.
```

Completeness of the resolved outside set is by the displayed discriminant and
the unit-coefficient smoothness argument. Completeness of the actual bad set is
not claimed because the full dyadic stable-model step remains open.

The last row is deliberately separate: the discriminants of `h`, the `T`
quartic, the `X` quartic, `t^2+2t-1`, and `Z` have prime supports
`{2,43}`, `{2,5}`, `{2}`, `{2}`, and `{2,53}`. These are only collision
supports for optional chart-factor arithmetic, not additional bad places of
the genus-2 curves or the `g6`/`conjugate(g6)` resultant.

## Actual Reduction Audit

At `pi` use the Kohel absolute Igusa invariant

```text
j1=(23671901*i+580427774)/37397.
```

Since `94*1991=169 mod 37397`, the residue map at
`pi=(94*i-169)` sends `i` to `1991`. The numerator of `j1` therefore has
residue

```text
580427774+23671901*1991 = 15271 mod 37397,
```

which is nonzero. The denominator `37397=pi*pi_bar` has `pi`-valuation one,
so `v_pi(j1)=-1`. The criterion used here is the odd-residue-characteristic
integral-invariant necessity: if a genus-2 curve has good reduction and `2` is
invertible, its hyperelliptic quotient and branch divisor give, locally, an
integral binary sextic with unit discriminant. Integral Igusa-Clebsch
polynomials divided by this unit discriminant give integral absolute
invariants. Since `37397>5`, this applies at `pi`. Therefore both `C_1` and
`C_i` have actual bad reduction at `pi`, independently of the displayed
repeated-root model.

The other two exact Kohel invariants are

```text
j2=(-157525606640*i-91084807952)/37397,
j3=(-53747630344*i-24975272704)/37397.
```

The twist `i*v^2=g6` is `v^2=(-i)*g6`. Scaling a binary sextic by `-i`
changes the weighted Igusa-Clebsch invariants by their weights but leaves the
absolute invariants unchanged. Hence the `pi` obstruction is identical for
the two twists.

At `varpi`, all three displayed absolute invariants are integral because
`37397` is a `varpi`-unit. This integrality is not a good-reduction
certificate in residue characteristic two. The current exact calculation is
only the following fixed-center radial audit. Put `pi=1+i`, so
`2=-i*pi^2` and `pi^4=-4`, and shift `z=t+1`:

```text
H(z)=g6(z-1)
    =z^6+(-2*i-8)z^5+(2*i-10)z^4+(-16*i+48)z^3
     +16*i*z^2+(32*i-64)z+32-32*i,
v_pi(H_0,...,H_6)=(11,10,8,9,3,2,0),
H_5/pi^2=4*i-1,   H_0/pi^11=-1.
```

For the fixed center `z=0`, the checked radial forms are

```text
F_r(X)=pi^(-6*r)*H(pi^r*X),
v_pi([X^6]F_r)=0,
v_pi([X^5]F_r)=2-r,
v_pi([X^4]F_r)=3-2*r.
```

The Sage audit verifies the displayed valuations, the radial square
congruence obstructions for `r=1,0,-1`, the residual singular forms for
`r<=-2`, and the unit-square obstruction for the radial `i`-twist. These are
valid fixed-center computations only.

They do not classify all quotient lattices. In a general coordinate change
`M=k1*diag(pi^r,1)*k2`, the right factor `k2` acts on the original branch
sextic. The branch set is not known to be stabilized by `PGL2(O_(varpi))`, so
the radial integer `r` does not determine the center or direction. In
particular, the existing calculation does not cover all finite centers,
nonradial Bruhat-Tits directions, or their projective infinity charts.

Therefore no actual reduction conclusion is drawn at `varpi` for either
twist, and no conclusion is drawn about whether the `i`-twist changes the
answer. The exact smallest remaining B0 blocker is:

```text
Classify every quotient P^1 lattice over K_(1+i), including all
Bruhat-Tits-tree directions and centers after the right PGL2(O_(varpi))
factor, with a finite stopping proof; then construct or obstruct the
corresponding smooth proper generalized model for both twists, including
the infinity charts.
```

This is a stable-model classification gap, not a software-capability claim
and not evidence of bad reduction from the singular displayed sextic.

## Current Trivial Rational-Parameter Ledger

The currently certified entries, without a claim that no other points exist,
are:

| twist | parameter | points |
|---|---|---|
| `C_1` | `t=0` | `v=+/-i` |
| `C_1` | `t=infinity` | `[1:+/-1:0]` |
| `C_i` | `t=0` | none over `K`, since `v^2=i` |
| either twist | `t=+/-1` | none, since `f12(1)=2^13`, `f12(-1)=2^11` are not squares |
| `C_i` | `t=infinity` | none over `K`, since `V^2=-i` |

The positive `C_1` entries map to the Berry points `(0,U)=(0,+/-1)` and
`(infinity,U)=(infinity,+/-1)` after the independent Berry sign choice.

## B0 Boundary

The proof-data scripts are `scripts/theory/berry_sextic_b0.py` and
`scripts/theory/berry_sextic_b0_reduction.sage`; focused tests are
`tests/test_berry_sextic_b0.py`. The covering/model, maps, converses,
exceptional fibers, and trivial ledger are certified, but B0 remains blocked
by `actual_reduction_at_(1+i)_unresolved`. The exact blocker is the missing
full Bruhat-Tits-tree quotient-lattice/stable-model classification for both
twists. B1 does not begin until that is resolved.
