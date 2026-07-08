# BB Family Odd-Prime Transport

## Question

Do the proved `AA` odd-prime formal-lift statements have to be rewritten from
scratch for the `BB` family?

## Result

No. The `BB` odd-prime inputs are obtained from the `AA` proofs by the
symbolic substitution

```text
L = A  (AA)   ->   L = B  (BB),
T = A+B       ->   T = A+B.
```

普通话说：`AA` 和 `BB` 在 odd-prime formal lift 这一步没有新的代数内容。证明里
只用到了符号变量 `L`、`T`、以及 `gcd(L,T)=1`、`gcd(L,T^2+4L^2)=1` 这些性质；把
`L` 从 `A` 换成 `B` 就行。

## Evidence

The shared `isogeny_setup` templates already record a single symbolic model per
kernel, with

```text
L_role = A for AA, B for BB; AA+BB requires both sides to close.
```

For the three kernels, the target models are uniformly:

```text
kernel_minus_p:      y^2 = x^3 + (32*L^2 - 8*T^2)*x^2 + 16*(T^2 + 4*L^2)^2*x
kernel_pos_2sqrt_q:  y^2 = x^3 - 8*(T^2 + 8*L^2)*x^2 + 16*T^4*x
kernel_neg_2sqrt_q:  y^2 = x^3 + 16*(T^2 + 2*L^2)*x^2 + 256*L^4*x
```

Every proved `AA` odd-prime transcript only used:

- these symbolic coefficients;
- the partition of odd primes into `L`, `T`, and `T^2 + 4*L^2`;
- the primitive coprime-support facts.

Those statements remain true after replacing `L=A` by `L=B`.

## BB Consequences

So the `BB` family inherits the same odd-prime matrix shape, with `L=B`:

```text
bad factor              kernel_minus_p      kernel_pos_2sqrt_q                    kernel_neg_2sqrt_q
B                       {1}                 {1}                                   full
T                       {1, -1}             unit classes if -1 nonsquare; full    {1, -1}
T^2 + 4*B^2             full                {1}                                   {1}
```

Hence the odd-support separation and odd-support dimension bound transport as:

```text
kernel_minus_p        odd support only from primes dividing T^2 + 4*B^2
kernel_pos_2sqrt_q    odd support only from primes ell | T with ell == 1 mod 4
kernel_neg_2sqrt_q    odd support only from primes dividing B
```

and

```text
dim_F2(odd valuation part) <= omega_odd(T^2 + 4*B^2) + omega_{1 mod 4}(T) + omega_odd(B).
```

## Boundary

This is a transport lemma for the odd-prime formal-lift input. It does not
prove the dyadic local condition, a global Selmer bound, rank zero, or any
root-number / 2-cover / lambda-family exclusion.
