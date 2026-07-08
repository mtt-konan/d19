# Rank-Zero Selmer Tangent Squareclass Correction

## Question

Does the odd-prime local-image schema need to remember the tangent squareclass
of the nodal reduction?

## Correction

Yes. The earlier two-schema split was too coarse. The double-root position
alone is not enough:

```text
x*(x-r)^2
x^2*(x-s)
```

The tangent squareclass at the node is also part of the local image problem.
For the current nine odd-prime branches, the corrected grouping is:

```text
tangent squareclass 1  -> 6 branches
tangent squareclass -1 -> 3 branches
```

So the local-image work is now four theorem schemas, not two:

```text
nonzero double root, tangent squareclass 1
nonzero double root, tangent squareclass -1
zero double root, tangent squareclass 1
zero double root, tangent squareclass -1
```

## Boundary

This is a correction to the local-image schema organization. It still does not
prove any local image theorem, local condition, Selmer rank bound, or
lambda-family exclusion.
