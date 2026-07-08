# AA Minus-P Zero-Double-Root Full Image

## Question

After the naive parameters failed, what is the corrected local image for the
`rank-zero-selmer-AA-kernel-minus-p` case at odd primes with

```text
ell | T^2 + 4*L^2?
```

## Result

The corrected package-specific local image is full:

```text
{ squareclasses of x(P) : P in E(Q_ell), x(P) != 0 } = Q_ell*/Q_ell*2.
```

普通话说：这个 zero-double-root 坏素数不再给 `x` 的平方类提供限制。它不是把
reduction-level 的 `{trivial}` 推上来，而是把正确答案改成“全部平方类都可能出现”。

## Proof Shape

Write

```text
d  = T^2 + 4*L^2
s  = 64*L^2
a2 = s - 8*d
a4 = 16*d^2.
```

Then `s` and `a2` are square units, and `a4` is a square.

The package transcript now constructs all four odd-prime squareclasses:

- trivial class: take `x = pi^(2*N)*u` with `N > v(d)` and `u` square;
- both ramified classes: take `x = pi*u`, with `u` square or non-square;
- non-square unit class: use the finite-field character count showing there
  is `x0` non-square with `x0+s` square, then lift `x0` to `Q_ell`.

## Boundary

This proves only the package-specific zero-double-root local image. It does
not prove the dyadic condition, the global Selmer bound, rank zero, or any
lambda-family exclusion. The next mathematical issue is how this full-image
prime contribution affects the Selmer bound argument.
