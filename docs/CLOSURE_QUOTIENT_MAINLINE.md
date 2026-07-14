# Closure Quotient Mainline

This document keeps the mathematical architecture of the project. Current
status and eligible directions live in [PROJECT_STATUS.md](./PROJECT_STATUS.md)
and [OPEN_DIRECTIONS.md](./OPEN_DIRECTIONS.md); detailed derivations live in
the [worklog index](./work-logs/README.md).

## Current Boundary

The latest accepted checkpoint is:

```text
wl595_universal_closure_product_g4_route_death
```

It closes only the universal closure-product
Kummer/single-split-prime/denominator mechanism. It is not a Harborth theorem,
family exclusion, Selmer/rank theorem, D2, D5, or M3 result.

The next admissible mathematical input would be a parameter-uniform global
relative 2-descent certificate on the full individual four-factor cover. It
must preserve both `T=A+B` and `T=|A-B|` branches, p=2, denominators, real and
boundary charts, and the complete AA/BB lifts.

## Core Object

For a fixed closure constant `c`, let `M=c-N`. The four original square
conditions are:

```text
NA = N^2 + A^2
NB = N^2 + B^2
MA = M^2 + A^2
MB = M^2 + B^2
```

The four pairwise products give genus-one quotient curves:

```text
AA: y^2 = NA * MA
BB: y^2 = NB * MB
AB: y^2 = NA * MB
BA: y^2 = NB * MA
```

Every full closed point maps to all four quotients. A strict exclusion on one
required quotient can therefore exclude the original nontrivial point, but a
quotient calculation is useful only after its exact pullback and lift
conditions are imposed.

The full-plane closure language uses both:

```text
c_plus  = A + B
c_minus = |A - B|
```

The difference branch is not optional. The diagonal `A=B` case is degenerate
and must be handled separately.

## Finite Certificate

The clean finite certificate is:

```text
AA/BB rank = 0
  -> enumerate torsion
  -> pull back to the quartic
  -> retain only midpoint points
  -> apply the midpoint exclusion theorem
```

For `t=2N-c` and `z=4y`, the even quartic has the form:

```text
z^2 = t^4 + p*t^2 + q
p = 8*L^2 - 2*c^2
q = (c^2 + 4*L^2)^2
```

One elliptic model is:

```text
E: V^2 = X^3 + p*X^2 - 4*q*X - 4*p*q
X = 2*(z + t^2)
V = 2*t*(X+p)
```

The affine reverse map is:

```text
t = V / (2*(X+p))
z = X/2 - t^2
N = (c+t)/2
```

This is a strict finite certificate for the rows with an actual rank-zero
certificate. It is not a family theorem.

## AB/BA Boundary

`AB` and `BA` are not uniform rank-zero exclusion mechanisms. For `c=A+B`,
the structural point `N=A`, `M=B` gives:

```text
(N^2+A^2)*(M^2+B^2) = (2*A*B)^2
```

They remain useful for structural checks and generator data, but not as the
main rank-zero obstruction.

## Ray Ledger

The quotient equations are homogeneous. Scaling by `k` sends:

```text
(A,B,N,y) -> (kA,kB,kN,k^2 y)
```

The natural unit is therefore the primitive ray

```text
lambda = A/B
```

An accepted ray ledger must keep both `c_plus` and `c_minus`, the quotient
certificate, torsion pullback, and midpoint exclusion. A plus-branch result
alone is not a complete ray certificate.

## Selmer Boundary

To turn finite quotient certificates into a family theorem would require:

```text
local image theorems
dyadic local condition
formal lift compatibility
global Selmer dimension bound
rank(E_lambda)=0
```

The current route did not establish that global Selmer bound. The `C_d`,
`M_tail`, AA+BB admissibility, common-source, and relative 2-descent records
remain separate object layers. A point-level obstruction, a fixed-family local
image, or a generic function-field nonsquare does not automatically become a
Selmer statement.

## What Does Not Count

The following are useful diagnostics but are not theorem progress by themselves:

- more certificate or candidate counts;
- larger pair-counting ranges;
- `AB/BA` rank-zero experiments;
- root-number observations without a Selmer lift;
- standalone mod-`p^k` or dyadic tables after the route is exhausted;
- bounded searches that find no point on a residual two-cover.

The project status explicitly separates these diagnostics from strict
certificates and theorem-level claims.

## Reading Route

- [Current status](./PROJECT_STATUS.md)
- [Next research gate](./NEXT_RESEARCH_GATE.md)
- [Open directions](./OPEN_DIRECTIONS.md)
- [Glossary](./GLOSSARY.md)
- [Worklog index](./work-logs/README.md)
- [Canonical script graph](../scripts/README.md)

For the recent AA+BB chain, read the consolidated `491-522`, `523-529`, and
`530-585` histories, then the D4 projection and the protected `wl587`/`wl589`
through `wl592` appendices. `wl594` and `wl595` remain downstream context.
