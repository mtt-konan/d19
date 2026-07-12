# M2 Pure v_ell Canonical Rational Class From The Coordinate GCD

## Question

Is the rational squarefree class `r` from `wl551`-`wl553` still an
independent finite choice, or is it determined by the candidate coordinates?

## Odd GCD Parity Of A Gaussian Square

For integers `m,n`, put

```text
X=m^2-n^2,
Y=2*m*n.
```

For every odd prime `p`, the valuation

```text
v_p(gcd(X,Y))
```

is even. Indeed, if `p` divides both `X` and `Y`, then it divides both `m`
and `n`. Removing their common `p`-power contributes an even power to both
coordinates; after that removal at least one coordinate is a `p`-unit, so no
additional common odd power remains.

Consequently, in either normalized `wl552` equation

```text
delta_normalized=i*r*(m+i*n)^2,
```

the parity of the common odd valuation of the real and imaginary coordinates
is exactly the indicator of `p|r`.

## Apply To delta

Recall

```text
E=4*(ell-1)*Q^2*D^2,
F=R-E,
R=Q^4+4*Q^2*D^2-4*D^4.
```

Dividing by `-4` in the `ell ≡ 1 (mod 8)` branch does not change any odd
valuation. Therefore in both branches

```text
r = sqf_odd(gcd(E,F)),
```

where `sqf_odd` retains precisely the odd primes occurring to odd valuation.

Since `gcd(E,F)=gcd(E,R)`, an odd common prime cannot divide `Q` or `D`:

```text
p|Q => R ≡ -4*D^4 (mod p),
p|D => R ≡ Q^4 (mod p).
```

Thus every common odd prime is coprime to `QD`, and

```text
v_p(E)=v_p(ell-1).
```

The canonical formula becomes

```text
r = product over odd p of
      p^[min(v_p(ell-1),v_p(R)) mod 2].
```

Equivalently, `r` is the odd squarefree kernel of `gcd(ell-1,R)`.

## Strict Reduction

The rational class is not a free divisor choice. For fixed `(ell,Q,D)`, it is
uniquely determined by the parity of `gcd(ell-1,R)`. Any simultaneous
orientation/class/cone system may therefore eliminate `r` as an independent
variable and substitute this canonical kernel.

## Boundary

This does not prove that the canonical class equation is soluble or insoluble,
solve an orientation, use the cone to exclude a candidate, handle the
nontrivial real-unit class, prove `wl535`, or enter M3.
