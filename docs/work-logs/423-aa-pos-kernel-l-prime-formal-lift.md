# AA Pos Kernel L-Prime Formal Lift

## Question

For `rank-zero-selmer-AA-kernel-pos-2sqrt-q`, can one more odd-prime formal
lift case be closed without touching the unstable zero-double-root branch?

## Result

Yes. At odd primes with

```text
ell | L
```

the local image for the tracked coordinate `x` is trivial:

```text
x-class {1}
```

## Proof Shape

The model is

```text
y^2 = x^3 - 8*(T^2 + 8*L^2)*x^2 + 16*T^4*x.
```

Set

```text
a2 = -8*(T^2 + 8*L^2)
a4 = 16*T^4
r  = 4*T^2.
```

For `ell | L`, the element `T` is a unit, so `r` is a square unit. The key
identity is

```text
x^2 + a2*x + a4 = (x - r)^2 - 64*L^2*x.
```

If `x-r` is a unit, the quadratic factor is a square by odd-prime square
lifting, so the curve equation forces `x` to be a square. If `x-r` is not a
unit, then `x` is congruent to the square unit `r`, so `x` is again a square.

## Remaining Odd-Prime Branch

The only odd-prime formal-lift branch still open in this package is

```text
ell | T.
```

Preliminary local checks show this zero-double-root branch depends on the
local squareclass of `-1`; it should not be collapsed into a uniform `{1}`
claim without a separate proof.

## Boundary

This proves only the `ell | L` odd-prime subclaim for this package. It does
not prove the `ell | T` zero-double-root branch, the dyadic condition, the
global Selmer bound, rank zero, or any lambda-family exclusion.
