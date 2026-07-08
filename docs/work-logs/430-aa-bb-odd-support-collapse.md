# AA+BB Odd Support Collapse

## Question

What happens to the odd-prime support when the `AA` and `BB` local constraints
must both hold at the same time?

## Result

For the `AA+BB` family, the odd-valuation support collapses to a single
kernel:

```text
kernel_minus_p        no odd-prime support
kernel_neg_2sqrt_q    no odd-prime support
kernel_pos_2sqrt_q    odd support only from primes ell | T with ell == 1 mod 4
```

So the odd-valuation part has dimension at most

```text
omega_{1 mod 4}(T).
```

普通话说：一旦 `AA` 和 `BB` 两边都要同时闭合，前面单边还存在的两个自由盒子会互相冲掉。
奇素数真正还能留下自由变量的，只剩 `kernel_pos_2sqrt_q` 在 `T` 的 `1 mod 4` 素数上。

## Proof

From the `AA` and `BB` transport lemmas:

```text
AA:
  kernel_minus_p        support only from T^2 + 4*A^2
  kernel_pos_2sqrt_q    support only from ell | T with ell == 1 mod 4
  kernel_neg_2sqrt_q    support only from A

BB:
  kernel_minus_p        support only from T^2 + 4*B^2
  kernel_pos_2sqrt_q    support only from ell | T with ell == 1 mod 4
  kernel_neg_2sqrt_q    support only from B
```

The `kernel_pos_2sqrt_q` supports are identical on the two sides, so their
intersection is still

```text
{ell odd : ell | T and ell == 1 mod 4}.
```

For `kernel_neg_2sqrt_q`, the two sides would require an odd prime to divide
both `A` and `B`. Primitive `A:B` gives `gcd(A,B)=1`, so this cannot happen.
Hence the odd-prime support for `kernel_neg_2sqrt_q` is empty.

For `kernel_minus_p`, an odd prime `ell` in the intersection would satisfy

```text
ell | (T^2 + 4*A^2)
ell | (T^2 + 4*B^2).
```

Subtracting gives

```text
ell | 4*(A^2 - B^2) = 4*(A-B)*T.
```

Also `ell` cannot divide `T`, because then `ell | T^2 + 4*A^2` would force
`ell | A`, contradicting `gcd(A,T)=1`. So `ell | A-B`.

Now modulo `ell`, we have `A == B`, hence

```text
T = A+B == 2*A
```

and therefore

```text
T^2 + 4*A^2 == 8*A^2 mod ell.
```

Since `ell` is odd and `gcd(A,B)=1`, we have `ell` not dividing `A`, so
`8*A^2` is non-zero modulo `ell`, contradiction. Thus

```text
gcd_odd(T^2 + 4*A^2, T^2 + 4*B^2) = 1,
```

and the odd-prime support for `kernel_minus_p` is empty as well.

This proves the displayed collapse. Because each remaining odd prime
contributes at most one F2 valuation-parity coordinate, the odd-valuation
dimension is at most `omega_{1 mod 4}(T)`.

## Boundary

This is still not a full Selmer rank upper bound. It does not treat the prime
`2`, unit/sign classes, or global relations beyond the AA-vs-BB odd-prime
intersection. It does not prove rank zero, root-number exclusion, 2-cover
exclusion, or any lambda-family exclusion.
