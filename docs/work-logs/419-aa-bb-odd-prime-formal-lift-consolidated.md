# wl419-wl430 — AA/BB odd-prime formal lift consolidated

## Scope

This file replaces `wl419` through `wl430`.

## Result

The `AA` odd-prime local-image work no longer looks like 3 unrelated kernel
tasks. It gives one family matrix.

For `AA`, with

```text
T = A+B
L = A
D = T^2 + 4L^2
```

the odd-prime local image input is:

```text
bad factor              kernel_minus_p      kernel_pos_2sqrt_q                    kernel_neg_2sqrt_q
L                       {1}                 {1}                                   full
T                       {1, -1}             unit classes if -1 nonsquare; full    {1, -1}
D                       full                {1}                                   {1}
```

Plain meaning: no single kernel controls every odd prime. The three kernels
cover different bad-prime boxes.

## Corrections Kept

The old attempted shortcut for `AA / kernel_minus_p` at primes `ell | D` was
wrong. The corrected local image there is full:

```text
{ squareclasses of x(P) : P in E(Q_ell), x(P) != 0 } = Q_ell*/Q_ell*2.
```

So primes dividing `T^2 + 4L^2` do not help this kernel. The two square-root
kernels control those primes instead.

For `AA / kernel_pos_2sqrt_q`, the branch `ell | T` splits:

```text
if -1 is not a square:  local image = unit classes
if -1 is a square:      local image = full squareclass group
```

For `AA / kernel_neg_2sqrt_q`, the odd-prime input is:

```text
ell | L                 full image
ell | T                 contained in {1, -1}
ell | T^2 + 4L^2        {1}
```

## Support Consequences

The `AA` odd-valuation support separates as:

```text
kernel_minus_p        only primes dividing T^2 + 4L^2
kernel_pos_2sqrt_q    only primes ell | T with ell == 1 mod 4
kernel_neg_2sqrt_q    only primes dividing L
```

So before units, signs, the prime `2`, and global relations, the odd-support
dimension is at most

```text
omega_odd(T^2 + 4L^2) + omega_{1 mod 4}(T) + omega_odd(L).
```

The `BB` family gets the same statements by replacing `L=A` with `L=B`.

For the `AA+BB` seed group, the two sides intersect. The odd support collapses
to:

```text
kernel_minus_p        no odd-prime support
kernel_neg_2sqrt_q    no odd-prime support
kernel_pos_2sqrt_q    only primes ell | T with ell == 1 mod 4
```

Thus the `AA+BB` odd-support dimension is at most

```text
omega_{1 mod 4}(T).
```

This is why `AA+BB` became the best next rank-zero target.

## Boundary

This consolidation keeps the odd-prime formal-lift conclusions and deletes the
per-branch logs. It does not prove the dyadic local condition, a global Selmer
rank bound, rank zero, or any `lambda` family exclusion.
