# M2 Pure v_ell Dyadic Gaussian Squareclass Elimination

## Question

Does the dyadic Gaussian prime `1+i` actually contribute a squareclass to the
finite support in `wl547` on the trivial real-unit branch?

## Statement

For every primitive trivial-unit candidate,

```text
v_(1+i)(delta)
```

is even. More precisely:

```text
ell ≡ 5 (mod 8) => v_(1+i)(delta)=0,
ell ≡ 1 (mod 8) => v_(1+i)(delta)=4.
```

Therefore the squarefree factor `d` in

```text
delta=eta*d*gamma^2
```

never contains `1+i`.

## Unit-q Branch

If `ell ≡ 5 (mod 8)`, `wl545` gives `Q,D` odd. Both

```text
P=-Q^4+(8ell-12)Q^2D^2+4D^4,
R= Q^4+4Q^2D^2-4D^4
```

are odd. Oddness alone does not make the Gaussian valuation exact. Here the
defining forms give the sharper congruences

```text
P ≡ 7 (mod 8),
R ≡ 1 (mod 8).
```

Thus after division by `1+i`, the two coordinates are `(P+R)/2` and
`(R-P)/2`, one even and one odd. Hence the quotient is not divisible by
`1+i` again. Since `delta=(P+iR)/(1+i)`,

```text
v_(1+i)(delta)=0.
```

## High-q-Valuation Branch

If `ell ≡ 1 (mod 8)`, `wl545` gives `v_2(Q)>=3` and `D` odd. Then

```text
P/4 = D^4 + 2^4*z_1,
R/4 = -D^4 + 2^6*z_2
```

for 2-adic integers `z_1,z_2`. In particular

```text
P/4 ≡ 1 (mod 4),
R/4 ≡ 3 (mod 4).
```

After one division by `1+i`, the two Gaussian coordinates have opposite
parity. Therefore

```text
v_(1+i)((P/4)+i(R/4))=1.
```

Because `v_(1+i)(4)=4`, this gives

```text
v_(1+i)(P+iR)=5,
v_(1+i)(delta)=4.
```

The odd quotients prove these valuations are exact; no cancellation can raise
them.

## Refined Finite Support

On the trivial real-unit branch the fixed support from `wl547` is now

```text
S_ell^odd = {
  Gaussian primes over odd p : p|ell-1 and (2/p)=1
}.
```

The candidate-dependent root condition

```text
(Q^2/D^2)^2+4(Q^2/D^2)-4=0 (mod p)
```

still applies. This removes one possible squareclass generator uniformly.

## Boundary

This result applies only to the trivial real-unit branch analyzed in
`wl545`-`wl547`. It does not enumerate or solve the remaining odd classes,
handle the nontrivial real-unit branch, use positivity, prove the full `wl535`
proposition, or enter M3.
