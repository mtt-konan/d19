# Center-Line Impossibility Proof Note

Date: 2026-06-09

## Status

The geometric center-line branch is closed by a known theorem:

```text
Yang Ji, "Several special cases of a square problem", arXiv:2105.05250.
```

The paper proves the midline case for a unit square and states that the same
special-case arguments apply to points in the whole plane, not just points
inside the square.

This note records the d19 translation. It does not reprint Yang Ji's full
Fermat descent. The local value is the dictionary:

```text
geometric midline
= A=B or N1=N2
= a+b=2n or |a-b|=2n in closure language
= r=s in the R_lambda sum=A+B ledger
```

普通话说：

```text
中线已经被论文关了。
这里补的是仓库变量翻译，防止后续把同一条线看成几条不同分支。
```

## Source Theorem

Yang Ji's Theorem 2 proves that a point on a square midline cannot have rational
distances to all four vertices. Remark 1 says the special-case theorems are not
restricted to the square interior; they apply to points in the plane.

Source:

```text
https://arxiv.org/abs/2105.05250
```

The proof route in the paper is Fermat infinite descent. In the midline case it
reduces the assumed rational-distance point to an integer equation of the shape:

```text
(a^2 + b^2)^2 + (2ab)^2 = e^2
```

and then descends back to a smaller solution of the same form.

## d19 Coordinates

Use the unit square with vertices:

```text
(0,0), (1,0), (1,1), (0,1)
```

Write a rational point as:

```text
P = (u/L, v/L)
```

with integers `u,v` and `L>0`. After multiplying distances by `L`, the four
corner square conditions become:

```text
u^2       + v^2       = square
(u-L)^2   + v^2       = square
(u-L)^2   + (v-L)^2   = square
u^2       + (v-L)^2   = square
```

d19 usually names the two horizontal legs and two vertical legs as:

```text
A  = |u|
B  = |u-L|
N1 = |v|
N2 = |v-L|
```

Then `N1` and `N2` are concordant values for `(A,B)`.

## Horizontal Midline

Assume the point lies on the horizontal midline:

```text
y = 1/2
```

After choosing `L` even:

```text
v = L/2
N1 = N2 = L/2
```

Write the shared vertical leg as:

```text
N1 = N2 = n
```

Then:

```text
L = 2n
```

The horizontal leg relation is:

```text
A + B = L      if the point is between the two vertical sides
|A - B| = L    if the point is outside that strip
```

So the center-line closure language is exactly:

```text
N1 = N2 = n
A + B = 2n
```

or:

```text
N1 = N2 = n
|A - B| = 2n
```

These are not merely "centerline-like" conditions. They are the geometric
midline in cleared-denominator coordinates.

## Why This Gives a Contradiction

On the horizontal midline, the four distances collapse into two pairs:

```text
A^2 + n^2 = square
B^2 + n^2 = square
```

because the distances to the two left vertices are equal, and the distances to
the two right vertices are equal.

If positive integers `A,B,n` satisfied one of:

```text
A + B = 2n
|A - B| = 2n
```

and both Pythagorean conditions:

```text
A^2 + n^2 = square
B^2 + n^2 = square
```

then the point:

```text
P = (u/(2n), 1/2)
```

could be reconstructed with four rational distances to the square vertices.
For `A+B=2n`, take `0 <= u <= 2n`. For `|A-B|=2n`, take `u` outside the strip.
Concretely, if `A-B=2n`, take `u=A>2n`; if `B-A=2n`, take `u=-A<0`.
The sign only chooses which side of the square the point lies on.

Yang Ji's midline theorem and whole-plane remark rule out this point. Therefore:

```text
No positive center-line solution exists.
```

普通话说：

```text
只要 N1=N2=n，再加 a+b=2n 或 |a-b|=2n，
你就已经把点放在正方形中线上。
如果两条勾股边也都过了，
那就是 Yang Ji 已经排除的点。
```

## Vertical Midline

The vertical midline is the same branch after swapping axes:

```text
x = 1/2
```

In d19 variables this is:

```text
A = B = m
```

The matching closure language becomes:

```text
N1 + N2 = 2m
```

or:

```text
|N1 - N2| = 2m
```

The square conditions are:

```text
m^2 + N1^2 = square
m^2 + N2^2 = square
```

By D4 symmetry this is the same as the horizontal midline. It is also closed by
Yang Ji's theorem.

## Relation To `R_lambda`

The `R_lambda` sum branch scales by `B`:

```text
lambda = A / B
r = N1 / B
s = N2 / B
```

The inside-square center-line relation:

```text
N1 = N2
N1 + N2 = A + B
```

becomes:

```text
r = s
r + s = lambda + 1
```

so:

```text
r = s = (lambda + 1) / 2
```

This is the `sum_ab_centerline_*` branch in `rational_ratio.py`. The recent
quartic and PARI diagnostics study the same geometric midline in normalized
variables. They are useful for a self-contained local proof, but they are not
needed to cite the known geometric closure.

## What This Note Closes

Closed:

```text
A = B
N1 = N2
a+b=2n
|a-b|=2n
r=s with r+s=lambda+1
```

when these describe the square midline and the point is required to have all
four vertex distances rational.

Not closed:

```text
A = kB for k != 1
general rational lambda
non-center full-plane closure
closure-first 3/4 near-miss families
non-coprime full-space gap
```

## How To Use This In Later Work

If a scan reports a center-line hit, do not treat it as a possible Harborth
counterexample. It should be routed to this note and Yang Ji Theorem 2.

If a future proof route tries to generalize to:

```text
A = kB
```

then `k=1` is already closed by this note. For `k != 1`, the proof must use
extra structure, such as Yang Ji's fixed-distance-ratio theorem, new gcd control,
or a new modular/descent argument.

The clean next step is:

```text
make an A=kB coverage table:
k, inside n=k+1, outside n=k-1, Yang Ji prime-pair covered?, open residue classes
```

This turns the center-line proof note into a template instead of a new search
branch.
