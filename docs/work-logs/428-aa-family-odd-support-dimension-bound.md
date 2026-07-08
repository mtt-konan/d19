# AA Family Odd Support Dimension Bound

## Question

What dimension bound follows from the `AA` odd support separation before
handling units, signs, and the prime `2`?

## Result

Let

```text
D = T^2 + 4*L^2.
```

For primitive `A:B`, the odd-valuation part of the three-kernel Selmer
candidate space has dimension at most

```text
omega_odd(D) + omega_{1 mod 4}(T) + omega_odd(L).
```

Here:

- `omega_odd(n)` counts distinct odd prime divisors of `n`;
- `omega_{1 mod 4}(T)` counts distinct odd primes `ell | T` with
  `ell == 1 mod 4`.

普通话说：只看奇素数的“是否出现一次”这件事，三个 kernel 最多分别从
`D`、`T` 的 `1 mod 4` 部分、`L` 取自由变量。这个数不是最终 Selmer rank，只是下一步
global bound 的奇素数支撑上界。

## Proof

From the support separation:

```text
kernel_minus_p        odd support only from primes dividing D
kernel_pos_2sqrt_q    odd support only from primes ell | T with ell == 1 mod 4
kernel_neg_2sqrt_q    odd support only from primes dividing L
```

The coprime-support facts imply these three odd support sets are disjoint:

```text
gcd(L, T) = 1
gcd(L, D) = 1
gcd(T, D) divides 4.
```

Each allowed odd prime contributes at most one F2 coordinate: the parity of
its valuation in the relevant global squareclass. Since the three allowed
sets are disjoint and assigned to different kernel coordinates, the
odd-valuation part injects into

```text
F2^{omega_odd(D)}
  direct_sum F2^{omega_{1 mod 4}(T)}
  direct_sum F2^{omega_odd(L)}.
```

Therefore its dimension is at most the displayed sum.

## Boundary

This is not a Selmer rank upper bound. It deliberately omits:

- the prime `2`;
- unit and sign squareclasses, including the `{1, -1}` local images;
- global relations among the three kernel coordinates;
- any Mordell-Weil rank, rank-zero, root-number, 2-cover, or lambda-family
  exclusion conclusion.
