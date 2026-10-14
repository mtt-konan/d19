# Equal-Side Compatibility As A Three-Norm System

Updated: 2026-09-14

## Exact discriminant

Let signed rational distances be `a,b,c,d` in the paired order from the
Hadamard model, and set

```text
R = a^2+b^2 = c^2+d^2,
q = a^2-b^2,
r = c^2-d^2.
```

For a square side with `V=L^2`, the exact closure equation is

```text
4*V^2 - 4*R*V + q^2+r^2 = 0.
```

Therefore a rational `V` exists exactly when

```text
h^2 = Delta = R^2-q^2-r^2,
V=(R +/- h)/2.
```

The original metric problem requires the stronger condition that one of
these positive `V` is a rational square, `V=w^2`. A rational discriminant is
not enough.

The discriminant has two symmetric factorizations:

```text
(2*a*b)^2 = r^2+h^2,
(2*c*d)^2 = q^2+h^2.
```

Thus the first lift is already two rational Pythagorean triples sharing the
leg `h`. This is an exact identity, not a finite search pattern.

## Equivalent three-square system

Assume `w != 0` and define

```text
e=q/(2*w), f=r/(2*w).
```

Then the square equation is equivalent to

```text
R = w^2+e^2+f^2,
2*a^2 = (w+e)^2+f^2,
2*b^2 = (w-e)^2+f^2,
2*c^2 = (w+f)^2+e^2,
2*d^2 = (w-f)^2+e^2.
```

The converse is immediate: subtract the first two displayed distance
identities to recover `q=2*w*e`, subtract the latter two to recover
`r=2*w*f`, and subtract the equal-norm identities to recover `R`; then the
original square closure equation follows. Hence this is a reversible
repackaging of all four individual square lifts, not a product-square
projection.

The structure is now visible as **three simultaneous norm layers**:

1. `R` is a sum of three rational squares `w^2+e^2+f^2`;
2. each of four Gaussian norms is twice a rational square;
3. the four Gaussian arguments share the same three coordinates and signs.

For example, the first condition can be written
`N(w+i*sqrt(e^2+f^2))=R`, but the four conditions are more naturally the
norms of `(w+e)+i*f`, `(w-e)+i*f`, `(w+f)+i*e`, and `(w-f)+i*e`.

## Gaussian-square parameterization (conditional)

Over `Q(i)`, each identity

```text
U^2+V^2 = 2*Z^2
```

means `N(U+iV)=N((1+i)Z)^2`. Under the usual coprimality and denominator
conditions that make the Gaussian factors primitive, unique factorization
allows a representation

```text
U+iV = unit*(1+i)*(m+i*n)^2,
```

with rational `m,n`. Applying this to the four signed pairs above would give
four Gaussian square parameters linked by the same `w,e,f`. Establishing the
required common-factor hypotheses and extracting a contradiction is an open
next problem; the representation is not asserted unconditionally for
nonprimitive tuples.

This identifies a possible theoretical direction: a shared-factor or unit
equation in `Z[i]`, rather than independent elliptic searches. The relevant
question is whether four such Gaussian squares can share the Hadamard sign
pattern without forcing `w=0`, `e=0`, `f=0`, or a boundary degeneration.

## Primitive 2-adic parity lemma

Clear denominators in the three-norm system and divide by the common gcd, so
`w,e,f,a,b,c,d` are primitive integers. Reducing the four equations modulo 2
gives

```text
w+e+f = 0 mod 2.
```

Exactly two of `w,e,f` are therefore odd. The patterns with `w` odd are
impossible: for example, if `w,e` are odd and `f` even, the first two
equations force `a,b` even while the last two force `c,d` odd; then
`a^2+b^2` is divisible by 4 but `c^2+d^2` is 2 modulo 4, contradicting the
common value `R`. The other case is symmetric. Hence

```text
w is even, e and f are odd, and a,b,c,d are odd.
```

Now `a^2-b^2` and `c^2-d^2` are divisible by 8. Since

```text
a^2-b^2 = 2*w*e,
c^2-d^2 = 2*w*f,
```

and `e,f` are odd, we obtain `4 | w`. This includes all primitive finite
points of the three-norm model; no positivity or interior assumption is
used. It is a genuine 2-adic restriction on the rational side lift, distinct
from the earlier 5-adic rotation-denominator obstruction.

This lemma does **not** say that no primitive tuple exists: after dividing
the equations by their forced powers of 2, a further odd-part or descent
argument is still required. It also does not imply that `e^2+f^2` is a
square; that would be an additional, generally false inference.

## The two roots and the unique square branch

The three-square identity makes the root structure exact. The two roots of
the fixed-distance quadratic are

```text
V_1 = w^2,
V_2 = R-w^2 = e^2+f^2.
```

For a primitive integer lift, the parity lemma gives `e,f` odd, hence
`e^2+f^2 = 2 mod 8` and `v_2(e^2+f^2)=1`. Therefore `V_2` is never a square
in `Q_2`, while `V_1=w^2` is the actual rational-square side branch. Any
nondegenerate rational solution consequently selects a unique square branch;
the other quadratic root cannot also be a square.

This also shows why the stronger-looking condition `q^2+r^2` square is not
available: in the primitive lift,

```text
q^2+r^2 = 4*w^2*(e^2+f^2)
```

has odd 2-adic valuation. Requiring it to be a square would incorrectly
discard every possible primitive solution. The correct third lift is
`V_1=w^2`, not a square condition on the sum of the two distance differences.

## Strict audit of the lift hierarchy

The integer tuple

```text
(a,b,c,d)=(35,149,101,115)
```

has

```text
R=23426, q=-20976, r=-3024,
h=9982,
V=(R+h)/2=16704,
V'=(R-h)/2=6722.
```

Here `h` is rational and both square-side candidates are rational, but
neither is a rational square. The first discriminant lift therefore passes
while the side-square lift fails. This is a strict finite illustration of
why the third norm layer cannot be dropped; it is not evidence of a uniform
exclusion theorem.

For the earlier full rational rectangle tuple `(20,15,15,20)`, the
discriminant is `625^2-175^2-(-175)^2=625*527`, which is not a square. It
fails already at the first lift, while the `24 x 7` and `24 x 25` rectangles
remain valid because they do not impose `L=M`.

## Exact scope

This result explains the arithmetic location of the equal-side requirement:
it is the demand that one root of the fixed-distance quadratic be a square,
after two shared-leg Pythagorean constraints have already been met. It does
not prove that the third layer is impossible, and it does not claim a new
mathematical theory. A productive next question would be a precise Gaussian
common-factor lemma for the four signed pairs, with all primitive and
exceptional cases stated explicitly. More isolated discriminant examples or
larger searches would not answer that question.

## Verification

The task-local tests verify the quadratic, both discriminant factorizations,
the reversible three-square identities, the strict `(35,149,101,115)` lift
audit, the earlier rectangle discriminant, and the primitive parity lemma.

Verification completed: all 8 task-local exact tests passed with `-n 0`; targeted Ruff passed. No database sweep or broad parameter search was used.
