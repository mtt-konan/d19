# AA Family Odd Support Separation

## Question

What does the `AA` odd-prime local-image matrix imply for the global
squareclass support of the three descent coordinates?

## Result

Ignoring the prime `2` and unit signs, the odd-prime support separates as:

```text
kernel_minus_p        odd support only from primes dividing T^2 + 4*L^2
kernel_pos_2sqrt_q    odd support only from primes ell | T with ell == 1 mod 4
kernel_neg_2sqrt_q    odd support only from primes dividing L
```

普通话说：三个 kernel 的“自由素数”分开了。`minus_p` 的自由只来自 `T^2+4L^2`，
`neg_2sqrt_q` 的自由只来自 `L`，`pos_2sqrt_q` 的自由只来自 `T` 里让 `-1` 成为平方的
奇素数。

## Proof

Use the proved `AA` odd-prime local-image matrix:

```text
bad factor              kernel_minus_p      kernel_pos_2sqrt_q                    kernel_neg_2sqrt_q
L                       {1}                 {1}                                   full
T                       {1, -1}             unit classes if -1 nonsquare; full    {1, -1}
T^2 + 4*L^2             full                {1}                                   {1}
```

The coprime-support audit gives, for primitive `A:B`,

```text
gcd(L, T) = 1
gcd(L, T^2 + 4*L^2) = 1
gcd(T, T^2 + 4*L^2) divides 4.
```

So an odd prime belongs to exactly one of the three odd support boxes:
`L`, `T`, or `T^2+4L^2`.

A local image `{1}` forces even valuation at that odd prime. A local image
`{1, -1}` also forces even valuation, because both classes are units. A full
local image imposes no parity restriction. For `kernel_pos_2sqrt_q` at
`ell | T`, the image is full exactly when `-1` is a square in `Q_ell`, i.e.
`ell == 1 mod 4`; otherwise it contains only the two unit classes and again
forces even valuation.

Combining these facts gives the support separation displayed above.

## Consequence

This is a usable input for the next `global_selmer_dimension_bound` attempt.
It does not yet make the Selmer group small: the possible odd support still
has size

```text
omega(T^2 + 4*L^2) + omega({ell | T : ell == 1 mod 4}) + omega(L)
```

before any global relation, dyadic restriction, or family-level rank-zero
argument is applied.

## Boundary

This proves only the odd-prime support separation implied by existing local
image theorems. It does not prove the dyadic local condition, a global Selmer
rank bound, rank zero, root-number exclusion, 2-cover exclusion, or any
lambda-family exclusion.
