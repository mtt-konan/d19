# Closure Quotient Reference

This document preserves the mathematical architecture of the closure-quotient
route. It is reference material, not the default research assignment.
[PROJECT_STATUS.md](./PROJECT_STATUS.md) owns the latest mathematical status;
[NEXT_RESEARCH_GATE.md](./NEXT_RESEARCH_GATE.md) owns task selection.

## Historical Boundary

The former wl596 handoff and subsequent wl597 reduction are indexed in the
[route archive](./archive/RESEARCH_ROUTES.md#hrl-and-divisor-pair-system).
Their exact divisor-pair gap and scoped reopening conditions remain evidence,
not instructions to continue HRL automatically.

The Selmer proof obligations below belong to this particular route. They do
not require an independent proof of the original problem to use Selmer theory.
The architecture and formulas are retained unchanged.

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

For this route's evidence, consult the consolidated `491-522`, `523-529`, and
`530-585` histories, the D4 projection, and the protected `wl587`/`wl589`
through `wl592` appendices as needed. Later results and the unresolved HRL
question are linked from the project status and route archive.
