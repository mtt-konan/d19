# wl218 Full-Plane Reciprocal Theorem Goal

> **For agentic workers:** This is a proof-control brief, not an implementation
> plan. Keep intermediate reasoning in notes or worklogs. Do not report a
> theorem as proved until every full-plane branch below is closed by an actual
> argument, not by finite scans.

**Goal:** Prove or rigorously reduce the full-plane `R_lambda` reciprocal
theorem. The theorem is not restricted to points inside a square.

**Plain-language target:** If two rational ratios both pass the two distance
tests, and together they satisfy one of the square-closing linear relations,
then they must be the natural mirror pair `s = lambda/r`.

Plainly: we are allowed to work in the whole plane. The closing condition is
that a sum or a difference of the two distances matches one of the square-side
targets. We do not assume the point is sitting between the two sides of the
square.

**Exact target:**

Let

```text
lambda in Q_{>0}
R_lambda = { r in Q_{>0} : r^2 + 1 and r^2 + lambda^2 are rational squares }.
```

Prove:

```text
If r,s in R_lambda and (r,s) satisfies a full-plane closure relation,
then rs = lambda.
```

The full-plane closure relations are the four relations:

```text
r+s     = lambda + 1
r+s     = |lambda - 1|
|r-s|   = lambda + 1
|r-s|   = |lambda - 1|
```

When `lambda = 1`, the `|lambda-1|` target is zero and gives no positive
sum/difference target.

Scope correction, 2026-06-23:

```text
The theorem is a full-plane statement.
Do not restrict the final statement to points inside the square.
```

Operationally, this means:

```text
Do not assume the geometric point lies in the unit square.
Do not replace GEN-CLOSURE by the single inside-square line.
Use the four full-plane branches as the closure condition.
```

The `sum=A+B` relation is still a useful first subproblem, but only because it
is the cleanest branch and has the most existing notes. In older geometric
language this is the inside-square-looking branch, but it is only Branch 1 of
the full-plane theorem. It is not the whole theorem, and it is not a replacement
for the other three full-plane branches.

Latest requirement adjustment, 2026-06-23:

```text
The active proof target is the full-plane theorem.
The earlier "lock sum=A+B" instruction means "attack Branch 1 first",
not "restrict the theorem to the inside-square case".
After Branch 1 is closed, Branches 2-4 remain mandatory.
```

---

## Current State

The repository already has useful proof-side infrastructure:

```text
wl218: full-plane closure classifier
wl219: full-plane product ledger
wl220-wl222: reciprocal/mirror branch ledgers
```

These are ledgers and diagnostics. They are not yet a proof of the theorem.

The most important existing boundary is:

```text
sum=A+B is only one full-plane branch.
Do not prove that branch and call it the full theorem.
```

The active dangerous branch is:

```text
true-nonreciprocal
```

meaning:

```text
r,s in R_lambda
the chosen full-plane closure relation holds
rs != lambda
```

Finite scans so far have found no `true-nonreciprocal` examples in small pools,
but scans are only alarms. They are not proof.

---

## Product Ledger

For one fixed full-plane relation, let:

```text
T = closure target
p = rs
```

Use sign:

```text
epsilon = -1 for sum relations
epsilon = +1 for diff relations
```

Then the product-level terms are:

```text
A_p = p^2 + epsilon*2p + T^2 + 1
B_p = p^2 + epsilon*2lambda^2 p + lambda^2 T^2 + lambda^4
```

and the key identity is:

```text
B_p - lambda^2 A_p = (lambda^2 - 1)(lambda^2 - p^2).
```

The root discriminants are:

```text
sum relation:  D = T^2 - 4p
diff relation: D = T^2 + 4p
```

Critical warning:

```text
A_p and B_p being rational squares is only a product-level necessary condition.
It does not imply r,s in R_lambda.
```

The actual membership condition is four separate square conditions:

```text
r^2 + 1          square
s^2 + 1          square
r^2 + lambda^2   square
s^2 + lambda^2   square
```

Equivalently, the squareclass pair must be:

```text
(1, 1)
```

not merely two equal nontrivial squareclasses.

Known guard example:

```text
lambda = 535/161
r = 14/23
s = 26/7
```

This satisfies the weak product-square layer in the `sum=A+B` branch but is not
a true member pair:

```text
unit squareclasses   = (29, 29)
lambda squareclasses = (29, 29)
```

Plain-language lesson:

```text
The weak ledger can let in lookalikes. The proof must show that a lookalike
can never become a true pair unless p = lambda.
```

---

## Branches To Close

### Branch 1: `r+s = lambda+1`

This is the original `sum=A+B` branch.

Target:

```text
r,s in R_lambda
r+s = lambda+1
=> rs = lambda
```

Important consequence:

If `rs=lambda`, then:

```text
t^2 - (lambda+1)t + lambda = 0
(t-1)(t-lambda) = 0
```

so `{r,s} = {1, lambda}`. Since `1^2+1 = 2` is not a rational square, this
mirror pair is not a true closure pair. Therefore proving `rs=lambda` in this
branch actually proves that the branch has no true positive closure pair.

This is fine, but state it clearly.

Candidate proof route:

1. Use `T=lambda+1`, `epsilon=-1`.
2. Assume all four membership squares.
3. Assume `p != lambda`.
4. Use the identity
   `B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2)`.
5. For primes `q == 3 mod 4`, compare valuations forced by the four individual
   square conditions.
6. Show these valuations force a contradiction unless `p=lambda`.

Do not use only `A_p,B_p` square. That loses the real membership information.

### Branch 2: `r+s = |lambda-1|`

This is a sum relation with the smaller target.

Target:

```text
r,s in R_lambda
r+s = |lambda-1|
=> rs = lambda
```

But note that if `rs=lambda`, the equation may already be impossible or may
force roots from a discriminant branch. Treat separately for `lambda>1` and
`0<lambda<1` if needed.

Candidate proof route:

1. Use `T=|lambda-1|`, `epsilon=-1`.
2. Keep the same product identity.
3. The discriminant is `D=T^2-4p`.
4. Track whether the smaller target makes positivity impossible in subranges.
5. Apply the same squareclass/valuation strategy as Branch 1.

### Branch 3: `|r-s| = lambda+1`

This is a diff relation.

Target:

```text
r,s in R_lambda
|r-s| = lambda+1
=> rs = lambda
```

Candidate proof route:

1. Use `T=lambda+1`, `epsilon=+1`.
2. The discriminant is `D=T^2+4p`.
3. The product identity still has the same right-hand side:
   `(lambda^2-1)(lambda^2-p^2)`.
4. Re-run the valuation argument; do not assume signs from the sum branch carry
   over.

### Branch 4: `|r-s| = |lambda-1|`

This is the second diff relation.

Target:

```text
r,s in R_lambda
|r-s| = |lambda-1|
=> rs = lambda
```

Candidate proof route:

1. Use `T=|lambda-1|`, `epsilon=+1`.
2. If `lambda=1`, this target is zero and positive distinct roots do not give a
   diff branch; centerline belongs to the sum branch.
3. Otherwise apply the diff-form ledger and valuation argument.

---

## Reciprocal/Mirror Branch

The theorem conclusion is `rs=lambda`. Existing wl220-wl222 ledgers show how
the reciprocal/mirror candidates behave in all four relations.

Do not confuse two different claims:

```text
The theorem says closure forces rs=lambda.
It does not say that every rs=lambda pair is itself a valid closed pair.
```

In fact, several reciprocal closure candidates fail because one root is `1`,
or because the discriminant roots have nontrivial squareclasses.

This is useful after the theorem is proved:

```text
full-plane closure => rs=lambda
reciprocal branch ledger => many or all reciprocal closure candidates are not true
```

But the reciprocal ledger alone does not close `true-nonreciprocal`.

---

## What Would Count As A Proof

A valid proof must do one of the following for each of the four branches:

```text
1. derive p=rs=lambda from the four individual membership square conditions; or
2. derive a direct contradiction from p != lambda; or
3. reduce the branch to an explicitly solved curve/local obstruction with all
   rational points accounted for.
```

It is not enough to show:

```text
A_p and B_p are squares;
finite scans have no true-nonreciprocal;
known residuals are nontrivial;
reciprocal candidates fail.
```

Those are supporting facts, not the theorem.

---

## Suggested Next Turn

Start with Branch 1, because it is the cleanest algebraically and has the most
existing notes. Treat this as the first full-plane sub-branch, not as an
inside-square restriction.

Concrete task:

```text
Write a proof note for:

lambda in Q_{>0}, r,s in R_lambda, r+s=lambda+1.
Let p=rs.
Assume p != lambda.
Translate the four individual square conditions into valuations at primes
q == 3 mod 4.
Try to force a contradiction in v_q(lambda^2-p^2), using
B_p - lambda^2 A_p = (lambda^2-1)(lambda^2-p^2).
```

If the valuation route fails, record the exact obstruction:

```text
which prime case survives,
which equality is too weak,
and whether the branch becomes a curve problem instead.
```

Then repeat the same proof skeleton for the three other full-plane branches,
with only `T`, `epsilon`, and discriminant sign changed.

---

## Verification Commands

Use these to keep the code-side ledgers honest while proving:

```bash
PYTHONPATH=src uv run python - <<'PY'
from fractions import Fraction
from rational_distance.concordant.rational_ratio import scan_full_plane_true_closure_relations

for n in (10, 15, 20):
    lambdas = tuple(sorted({Fraction(i, j) for i in range(1, n + 1) for j in range(1, n + 1)}))
    relations = scan_full_plane_true_closure_relations(
        lambda_ratios=lambdas,
        max_numerator=n,
        max_denominator=n,
        branches=("true-nonreciprocal",),
        include_centerline=True,
    )
    print(n, len(lambdas), len(relations))
PY
```

Expected current output:

```text
10 63 0
15 143 0
20 255 0
```

Run unit tests after code changes:

```bash
uv run pytest tests/test_rational_ratio.py -q
uv run ruff check src/rational_distance/concordant/rational_ratio.py tests/test_rational_ratio.py
```
