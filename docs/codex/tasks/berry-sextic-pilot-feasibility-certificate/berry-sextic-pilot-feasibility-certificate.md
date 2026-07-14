# Berry Sextic Pilot Feasibility Certificate

## Outcome

`berry_sextic_pipeline_ready`

The selected curve has a verified degree-12 genus-5 pullback. For every exact
rational pullback point, the realized Q(i) squareclass of the selected factor
lies in the finite group

```text
<i> = {1, i} in Q(i)^*/Q(i)^{*2}.
```

The next arithmetic obligation is the two-cover support problem

```text
d*v^2 = g6(t),  d in {1,i},  t in P^1(Q),  v in Q(i),
U = +/- Norm_Q(i)/Q(v).
```

This is a finite exact reduction, not a rational-point or rank result.

## Berry Input

The pilot is the degree-6 row visually transcribed from Berry 1990, Appendix
Table 4, printed page 528. The body of Proposition 4.3/4.4 calls the same
displayed table Table 5; this is a paper numbering discrepancy, not a formula
ambiguity. The row is

```text
X = t^6 + 6*t^5 + 29*t^4 + 44*t^3 - 13*t^2 - 2*t - 1
Y = t^6 + 12*t^5 + 21*t^4 - 16*t^3 - 21*t^2 + 4*t - 1
Z = t^6 + 4*t^5 + 7*t^4 + 24*t^3 + 39*t^2 - 12*t + 1
T = 10*t^5 + 40*t^4 + 28*t^3 - 24*t^2 + 10*t.
```

Independent checks are recorded in
`scripts/theory/berry_sextic_pilot.py`: visual transcription provenance and
symbolic substitution into Berry's displayed equations (1) and (2). Berry
also identifies this row as the projection of trope C7 from node 5 (printed
page 521). No other sextic is processed here.

## Exact Pullback

Berry's equations, visually read from printed page 505, are

```text
2*(Y^4 + T^4) + X^4 + Z^4 = 2*(X^2 + Z^2)*(Y^2 + T^2),
U^2 + Y^2 = X^2 + Z^2.
```

The first residual is identically zero. The second gives

```text
U^2 = f12(t)

f12(t) = t^12 - 4*t^11 - 62*t^10 + 68*t^9 + 1647*t^8
          + 4184*t^7 + 2716*t^6 - 376*t^5 + 623*t^4
          - 788*t^3 + 194*t^2 - 12*t + 1.
```

With `t=A/B`, the homogeneous model is

```text
W^2 = F(A,B),  F(A,B)=B^12*f12(A/B).
```

The four degree-6 coordinate forms are basepoint-free: their affine gcd is
1 and `X_h(1,0)=1`. The reduction of `f12` modulo 3 is squarefree, so the
degree-12 model has smooth projective genus `5`. The exact checks also give
`gcd(f12,f12')=1` over Q.

The rational trivial points retained by the projective model are

```text
(t,U)=(0,+/-1),
(A:B:W)=(1:0:+/-1) at infinity.
```

The parameter map has the exact identities

```text
X - 2*Y - Z = t*(Z - X),
-X + 3*Y + 2*Z + T = t*(X - Y + T).
```

Thus `t=(X-2*Y-Z)/(Z-X)` on the generic chart; the second ratio covers
`t=1`. The remaining common denominator is

```text
h(t)=t^4 + 12*t^3 + 22*t^2 - 4*t + 1.
```

The polynomial `h` has no rational root. Its four geometric roots map to the
node `(1:0:1:-1)` and are the only normalization fiber not covered by the
two displayed inverse ratios. Infinity is handled by `F(A,B)`, so there is no
lost parameter chart. Conversely, every rational parameter gives a point on
Berry's surface, and `W^2=F(A,B)` is exactly the fourth-distance equation on
that image.

The retained special strata are:

| parameter | image / exact status |
|---|---|
| `t=0` | node `(1:1:-1:0)` up to sign; `f12=1` |
| `t=1` | node `(1:0:1:1)`; `f12=2^13`, no rational `U` |
| `t=-1` | node `(1:0:-1:1)`; `f12=2^11`, no rational `U` |
| `h(t)=0` | node `(1:0:1:-1)`; `f12=2*Z^2`, no rational parameter |
| `t=infinity` | `(1:1:1:0)`; `F(1,0)=1` |
| `f12(t)=0` | all twelve geometric branch parameters retained; none is rational |

The exact factorization `T=2*t*(5*t^4+20*t^3+14*t^2-12*t+5)` has no other
rational zero. The coordinate-zero and node cases are therefore not silently
discarded.

## Q(i) Factor and Tangency Audit

Put `K=Q(i)`. The exact factor is

```text
g6(t) = t^6 + (-2-2*i)*t^5 + (-35-8*i)*t^4
        + (-52-28*i)*t^3 + (19-40*i)*t^2
        + (6+14*i)*t - 1.
```

Direct exact calculation gives

```text
f12 = g6 * conjugate(g6),
Res(g6,conjugate(g6)) = 2^40,
gcd(g6,conjugate(g6)) = 1,
gcd(g6,g6') = gcd(conjugate(g6),conjugate(g6)') = 1.
```

Both factors are irreducible over `K`. Hence there are no common branch roots,
no repeated roots, and no tangency or branch-intersection exception on this
pullback. Since the factors are monic and `f12` is squarefree, there is no
hidden constant or square factor in the factorization.

## Realized Support Proof

Let `A,B` be primitive integers and set

```text
G(A,B)=B^6*g6(A/B).
```

For an exact rational point on the pullback, `W=U*B^6` satisfies

```text
G(A,B)*conjugate(G(A,B)) = F(A,B) = W^2.
```

Here `F(A,B)` is an integer. Since a rational number whose square is an
integer is itself an integer, `W` is an integer. If a rational prime divides
`B`, primitivity gives `G(A,B)=A^6 (mod p)`, so it cannot create an omitted
denominator support prime.

The branch-zero case is absent for rational `A/B`, because `f12` is
irreducible over Q. Otherwise, at any Gaussian prime away from `1+i`, a
common divisor of `G(A,B)` and its conjugate would give a common projective
root of the two homogeneous degree-6 forms and would divide their resultant
`2^40`. Therefore at such a prime only one conjugate factor occurs, and its
valuation in `G(A,B)` is even because the product is the rational square
`W^2`. At `1+i`,

```text
v_(1+i)(G*conjugate(G)) = 2*v_(1+i)(G)
```

while `v_(1+i)(W^2)=4*v_2(W)`, so `v_(1+i)(G)` is even as well. Thus `G` is a
unit times a square in `K`, and
the unit squareclasses are exactly `{1,i}`.

This quantifies over every exact rational pullback point; it does not insert
formal twists. The two genus-2 support equations are `v^2=g6(t)` and
`i*v^2=g6(t)`, with `t` restricted to `P^1(Q)`. For a literal algebraic cover
of the genus-5 curve, use the genus-9 fiber products

```text
d*v^2 = g6(t),
conjugate(d)*w^2 = conjugate(g6)(t),
U = v*w,                 d in {1,i}.
```

They are degree-4 V4 covers of `P^1` with twelve simple branch points. The
genus-2 equations are the smaller exact twist/support obligation; the norm
formula supplies the converse `U=+/-v*conjugate(v)` on rational `t`.

## Quotient and Toolchain Audit

The exact `Q(i)` branch-set stabilizer is trivial. Because `g6` and its
conjugate are irreducible, a PGL2 transformation must preserve or swap the
two factors. In the affine chart `c=0`, the exact Groebner bases force the
preserving transformation to be the identity and force scale zero in the
swapping case. In the `c!=0` chart, both preserving and swapping bases contain
the scale variable, so no invertible transformation occurs. Thus no genuine
nontrivial `Q(i)` base quotient was found.

Sage 10.9 verifies genus 5 and constructs the generic Jacobian, but exposes no
generic rank, decomposition, or Neron-Severi-stabilizer certificate for this
Jacobian. No Magma or mwrank executable is installed. Berry's Neron-Severi
calculation concerns the Kummer surface `S`, not this genus-5 Jacobian.
Accordingly, the factorization above is not reported as a Jacobian split, and
no rank evidence is claimed.

## Literature Boundary

Berry Proposition 4.1 identifies the surface branch divisor as two conjugate
elliptic quartics over `Q(i)`, which is consistent with the exact pulled-back
`g6`/`conjugate(g6)` split. Proposition 4.3 applies to the families generated
by Berry's stated projection procedure. Proposition 4.4 proves the degree-2
and degree-4 exclusions, but explicitly says the degree-6 search found only
the trivial points and supplies no proof. Those results justify the selected
input and its boundary only; they do not prove the two genus-2 obligations or
any statement about the other sextics.

## Files and Validation

- `docs/codex/tasks/berry-sextic-pilot-feasibility-certificate/active-task.md`
- `docs/codex/tasks/berry-sextic-pilot-feasibility-certificate/berry-sextic-pilot-feasibility-certificate.md`
- `scripts/theory/berry_sextic_pilot.py`
- `tests/test_berry_sextic_pilot.py`
- task pointer only in `docs/codex/index.md`

Validated with:

```text
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q tests/test_berry_sextic_pilot.py -n 1
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff format scripts/theory/berry_sextic_pilot.py tests/test_berry_sextic_pilot.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check scripts/theory/berry_sextic_pilot.py tests/test_berry_sextic_pilot.py
git diff --check
```

The focused suite passes. Full pytest was not run. Pre-existing uncommitted
post-wl596 route-audit files and Berry literature note/index changes were
left untouched.
