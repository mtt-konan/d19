# Valuation/global invariant findings (2026-09-09)

## Scope

This note starts from the strict `wl596` divisor-pair system, with
`A=Abar>B=Bbar>0`, `gcd(A,B)=1`,

```text
s=A+B, r=A-B, Delta=s*r,
d_i=Delta/q_i,
a_i=(q_i+d_i)/2, b_i=(q_i-d_i)/2,
U_i^2=a_i^2-A^2=b_i^2-B^2.
```

It does not alter `wl596` or claim a new numbered checkpoint.

## A uniform 2-adic branch reduction

For every finite non-boundary source point, `U_i` is divisible by `4`.

* If `A,B` have opposite parity, then `s,r,Delta,q_i,d_i` are odd. Hence
  `a_i,b_i` have opposite parity. The member among `a_i,b_i` paired with the
  odd base (`A` or `B`) must itself be odd, since an even square minus an odd
  square is `3 (mod 4)`. Its square difference is therefore `0 (mod 8)`.
  Modulo `16`, an odd-square difference can only be `0` or `8`, and a square
  cannot be `8`; hence `U_i^2=0 (mod 16)` and `4|U_i`.

* If `A,B` are both odd, then `Delta` is even and the parity condition
  `q_i=d_i (mod 2)` forces both `q_i,d_i` even. Therefore `a_i,b_i` have the
  same parity. They cannot both be even because `a_i^2-A^2` would be `3
  (mod 4)`, so both are odd. The same odd-square argument gives `4|U_i`.

Consequences for the six closure branches:

1. Opposite-parity `A,B` have odd `s,r`, while every `U_1 +/- U_2` is
   divisible by `4`. Thus **all** finite positive divisor-pair closure
   branches are impossible in this parity class.
2. For primitive odd `A,B`, `gcd(s,r)|2`, so exactly one of `s,r` has
   `v_2=1` and the other has `v_2>=2`. Since `4|(U_1 +/- U_2)`, the branch
   with `v_2(T)=1` is impossible. Only the `T` branch divisible by `4`
   remains. This selects `T=s` or `T=r` from `A,B (mod 4)` without any local
   table.

This is a genuine family-level reduction of the exact divisor-pair set, but
it does not determine the odd squareclass of `q_1q_2` and does not by itself
close the remaining `T` branch.

## Stronger dyadic allocation statement for the surviving class

When `A,B` are both odd, write `q_i=2Q_i`, `d_i=2D_i`. Since `a_i,b_i`
are odd,

```text
Q_i+D_i=a_i odd,
Q_i-D_i=b_i odd.
```

Thus `Q_i,D_i` have opposite parity. Because
`Q_iD_i=Delta/4` and `v_2(s),v_2(r)` are `{1, alpha-1}` with
`alpha=v_2(Delta)`, this forces

```text
v_2(q_i) in {1, alpha-1}.
```

So the surviving branch has only the two endpoint dyadic allocations; the
intermediate dyadic allocations are excluded integrally (stronger than merely
excluding the valuation-middle `Q_2` source branch). If `alpha` is even, both
choices have odd valuation and the `2`-part of `q_1q_2` is automatically a
square. If `alpha` is odd, the remaining dyadic bit is the parity of whether
the two choices agree, and the closure unit equation still has to decide it.

## A potentially useful exact factorization (not yet an invariant)

For each source point, put `n_i=b_i-B>0` away from the `U_i=0` endpoint. Then

```text
U_i^2=n_i(2B+n_i),
(b_i-U_i)(b_i+U_i)=B^2.
```

Likewise, with `m_i=a_i-A`,

```text
U_i^2=m_i(2A+m_i),
(a_i-U_i)(a_i+U_i)=A^2.
```

Hence each individual source square is simultaneously an allocation of the
prime divisors of `A^2` and `B^2`; this is stronger than the original
`q_i d_i=Delta` allocation but does not yet couple `i=1,2` or prove a fixed
squareclass. It may be the correct starting point for a future global
factor-pair/closure argument.

## Checks and boundary

An exhaustive exact enumeration for primitive `A,B<1000` found no nonzero
closure pair, but this is diagnostic only and is not used as proof. The
parity proof includes `U_i=0` as a multiple of `4`; endpoint and projective
charts remain under the existing `wl596` boundary convention. No reciprocity
or Gaussian norm identity was found that fixes the odd part of
`sqf(q_1q_2)`.

## Status

`candidate=dyadic global branch reduction`; `degrees_of_freedom_removed=1`
(the opposite-parity parameter class and one of the two physical `T` branches
are removed). This is partial progress, not a route closure. The unresolved
object is the positive divisor-pair system restricted to odd `A,B`, the
`T` branch with `4|T`, and `v_2(q_i) in {1,alpha-1}`.
