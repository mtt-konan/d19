# M2 Pure v_ell Denominator Splitting Support

## Question

After standalone local obstructions are exhausted, what genuinely coupled
information do the first two square equations impose on the global
denominator of a rational `wl535` candidate, and does the final square equation
add another obstruction at those denominator places?

## Primitive Denominator Setup

Choose rational square roots `a,c` with

```text
a^2 = ell-q^2,
c^2 = ell*q^2+4.
```

Write

```text
a=A/D,
q=Q/D,
```

with integers `A,Q,D`, `D>0`, and `gcd(A,Q,D)=1`. Then

```text
A^2+Q^2 = ell*D^2.
```

Also `cD` is an integer: a rational number whose square is integral is
integral. Writing `C=cD` gives

```text
C^2 = ell*Q^2+4*D^2.
```

## Denominator Support Theorem

The denominator `D` is odd, is coprime to `ell`, and every prime `r|D`
satisfies

```text
r ≡ 1 (mod 4),
(ell/r)=1,
(r/ell)=1.
```

Equivalently, every denominator prime splits completely in the biquadratic
field

```text
Q(i,sqrt(ell)).
```

Consequently `D mod ell` is a nonzero quadratic residue.

## Proof

Let `r|D`. If `r|Q`, then reducing `A^2+Q^2=ell D^2` modulo `r` also gives
`r|A`, contradicting primitivity. Thus `Q` is an `r`-adic unit; the same
argument makes `A` a unit.

If `r=2`, primitivity forces `A,Q` both odd. Then

```text
A^2+Q^2 ≡ 2 (mod 4),
```

whereas `ell D^2` is divisible by `4`, a contradiction. Hence `D` is odd.

For odd `r`, reduction of the first equation gives

```text
(A/Q)^2 ≡ -1 (mod r),
```

so `r ≡ 1 (mod 4)`.

The case `r=ell` is impossible. In the second equation it would force
`ell|C`, but the two terms on the right have valuations `1` and at least `2`,
so their sum has valuation `1`, contradicting the even valuation of `C^2`.

Now `r != ell`, and reduction of the second equation gives

```text
(C/Q)^2 ≡ ell (mod r),
```

so `(ell/r)=1`. Both primes are `1 mod 4`, hence quadratic reciprocity gives
`(r/ell)=1`. These two squareclasses are exactly complete splitting in the
displayed biquadratic field. Multiplying the residue squareclasses with their
exponents shows that `D mod ell` is a square.

## Exact Local Converse At Denominator Places

This support condition is also the complete local condition at a negative
valuation place. Let `r` be an odd prime with

```text
r ≡ 1 (mod 4),
(ell/r)=1,
r != ell,
```

and let `v_r(q)=-k<0`. Then

```text
ell-q^2
  = (-1)*q^2*(1-ell/q^2),

ell*q^2+4
  = ell*q^2*(1+4/(ell*q^2)).
```

The leading units `-1` and `ell` are squares in `Q_r`, while both
parenthesized factors lie in `1+r^(2k) Z_r` and are squares because `r` is
odd. Thus the first two square roots exist locally.

For the last equation, factor its leading term:

```text
G_ell(q^2)
 = q^8 * (1
     +(16-8ell)/q^2
     +(32ell^2-96ell+72)/q^4
     +(32ell-64)/q^6
     +16/q^8).
```

The parenthesized unit is again in `1+r^(2k) Z_r`, hence is a square. So the
last `G` condition adds no further obstruction at an allowed denominator
prime.

## Exact Boundary

This is a global denominator-support restriction obtained by coupling the
first two square equations across every prime divisor of one common
denominator. It is not a rational solution and not an exclusion theorem.

It also identifies the failure point of denominator-place local analysis:
once a prime splits completely in `Q(i,sqrt(ell))`, all three square equations
are automatically locally compatible at negative valuation. Further progress
must use a global relation among these split primes, the numerator and real
positivity, or a descent/counterexample. No complete Selmer, rank, `Sha`, or
M3 claim is made.
