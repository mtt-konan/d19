# M2 Pure v_ell Dyadic Allocation In The Complementary Split

## Question

Once `wl563` introduces the complementary squarefree factors
`alpha*beta=kappa`, can the prime `2` be assigned to one factor rather than
left as another free divisor split?

## Preliminary Residues

The canonical class `r` is odd and supported at primes `1` or `7 mod 8`, so

```text
r ≡ 1 or 7 (mod 8).
```

Write the `wl563` decomposition as

```text
a=g*alpha*M^2,
b=g*beta*N^2,
A=alpha*M^2,
B=beta*N^2.
```

The coprime integers `A,B` have opposite parity.

## The ell = 5 mod 8 Branch

Here `v_2(ell-1)=2`, so

```text
v_2(2*(ell-1)/r)=3,
2|kappa.
```

The Gaussian coordinates `a,b` have opposite parity and their even member has
valuation three. Thus `g` is odd, the even member of `A,B` is divisible by
`8`, and its square is zero modulo `8`. Also `F ≡ 1 (mod 8)`. From

```text
F=r*g^2*(A^2-B^2)
```

one obtains:

```text
r ≡ 1 (mod 8) => A odd,  B even => 2|beta,
r ≡ 7 (mod 8) => A even, B odd  => 2|alpha.
```

Thus the factor `2` has a unique side in the complementary split.

## The ell = 1 mod 8 Branch

Now `a,b` are both even, but `(a/2,b/2)` have opposite parity, so

```text
v_2(g)=1
```

and `A,B` again have opposite parity. Their even member is divisible by `4`.
The congruence from `wl548` gives `F/4 ≡ 7 (mod 8)`. Dividing

`F=r*g^2*(A^2-B^2)` by `4` therefore gives

```text
r ≡ 1 (mod 8) => A even, B odd,
r ≡ 7 (mod 8) => A odd,  B even.
```

The kernel `kappa` contains `2` exactly when

```text
v_2(2*(ell-1)/r)=1+v_2(ell-1)
```

is odd, equivalently when `v_2(ell-1)` is even. In that case:

```text
r ≡ 1 (mod 8) => 2|alpha,
r ≡ 7 (mod 8) => 2|beta.
```

If `v_2(ell-1)` is odd, `kappa` is odd and neither factor contains `2`; the
same congruences still determine which of `A,B` has an even square multiplier.

## Strict Reduction

Whenever `2|kappa`, the complementary divisor split loses its binary choice
at `2`. The allocation is determined by the mod-8 branch and the canonical
class `r`. This uses the global product split from `wl563`; it is not a return
to the standalone dyadic orientation analysis closed in `wl557`.

## Next Exact Gate

Only the odd prime factors of `kappa` remain to be distributed between
`alpha` and `beta`. The next gate must constrain that odd allocation using the
real-coordinate quartic equation and selected orientation, or identify the
resulting finite split systems as the exact unresolved global lemma.

## Boundary

This does not solve an odd divisor allocation, a quartic split system, or a
surviving orientation; it does not handle the nontrivial real-unit class,
prove `wl535`, or enter M3.
