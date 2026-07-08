# AA Family Odd-Prime Local Image Matrix

## Question

After proving the odd-prime formal-lift subclaims for the three `AA` kernel
packages, what local-image matrix should feed the next Selmer-bound step?

## Result

The `AA` family odd-prime input is:

```text
bad factor              kernel_minus_p      kernel_pos_2sqrt_q                    kernel_neg_2sqrt_q
L                       {1}                 {1}                                   full
T                       {1, -1}             unit classes if -1 nonsquare; full    {1, -1}
T^2 + 4*L^2             full                {1}                                   {1}
```

普通话说：三个 kernel 不是各自孤立地工作。`minus_p` 管不住 `T^2+4L^2` 的奇素数，
但两个 square-root kernel 能管住；`neg_2sqrt_q` 管不住 `L` 的奇素数，但另外两个
kernel 能管住。真正需要继续分析的是 `T` 的奇素数，特别是 `-1` 是不是本地平方。

## Consequence

For an odd prime `ell`:

- if `ell | L`, then any odd valuation contribution is visible only in the
  `kernel_neg_2sqrt_q` descent coordinate;
- if `ell | T^2 + 4*L^2`, then any odd valuation contribution is visible only
  in the `kernel_minus_p` descent coordinate;
- if `ell | T`, then `kernel_minus_p` and `kernel_neg_2sqrt_q` allow only the
  unit classes `{1, -1}`, while `kernel_pos_2sqrt_q` is full exactly when
  `-1` is a local square.

This is the first family-level structural input extracted from the package
proofs. It does not yet prove a global Selmer dimension bound: a global
argument still has to show how these one-kernel free contributions interact
with the three-kernel family conclusion.

## Evidence

Package transcript locations:

- `rank-zero-selmer-AA-kernel-minus-p`: odd-prime image summary records
  `{1}`, `{1, -1}`, and full image for `L`, `T`, and `T^2+4L^2`;
- `rank-zero-selmer-AA-kernel-pos-2sqrt-q`: odd-prime summary records `{1}`,
  the `-1`-dependent `T` image, and `{1}`;
- `rank-zero-selmer-AA-kernel-neg-2sqrt-q`: odd-prime summary records full
  image, `{1, -1}`, and `{1}`.

## Boundary

This is a synthesis of proved odd-prime formal-lift inputs. It does not prove
the dyadic local condition, global Selmer bound, rank zero, root-number
exclusion, 2-cover exclusion, or lambda-family exclusion.
