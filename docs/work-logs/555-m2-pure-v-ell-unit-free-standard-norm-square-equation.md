# M2 Pure v_ell Unit-Free Standard Norm-Square Equation

## Question

Can the branch-dependent `eta=i` coordinate systems be replaced by one
uniform, unit-free Gaussian square equation before coupling to a `wl546`
orientation?

## Standard Norm Element

Keep the `wl554` coordinates

```text
E=4*(ell-1)*Q^2*D^2,
F=Q^4+(8-4*ell)*Q^2*D^2-4*D^4.
```

Thus `F=R-E`. Define

```text
Z=F+i*E.
```

The `wl547` element is

```text
delta=E+i*F=i*conjugate(Z).
```

After `wl551` and `wl552`, its class equation is

```text
delta=i*r*gamma^2,
```

where `r` is the positive canonical class from `wl554`. Cancelling `i` and
conjugating gives the uniform equation

```text
Z=r*Gamma^2,
Gamma=conjugate(gamma).
```

There is no remaining Gaussian unit and no mod-8-dependent sign in this
equation.

## Uniform Integer Coordinates

Write `Gamma=a+i*b`. Then

```text
F=r*(a^2-b^2),
E=2*r*a*b.
```

Since `E>0` and `r>0`, every candidate satisfies

```text
a*b>0.
```

The exact positivity identity from `wl553` becomes the single uniform cone

```text
H=r*K_ell(a,b),
K_ell(a,b)=ell*(a^2-b^2)+2*(ell-1)*a*b,
K_ell(a,b)>0.
```

The opposite cone signs in `wl553` came only from using different normalized
coordinates after extracting `-4`; the unnormalized standard element removes
that artifact.

## Dyadic Data In Uniform Coordinates

The earlier branch information is retained:

- if `ell ≡ 5 (mod 8)`, `Gamma` is a `1+i`-unit, `a,b` have opposite parity,
  and `v_2(a*b)=3` because `v_2(E)=4`;
- if `ell ≡ 1 (mod 8)`, `v_(1+i)(Gamma)=2`, so `a,b` are both even and
  `(a/2,b/2)` have opposite parity; moreover `v_2(a*b)=v_2(E)-1>=10`.

These conditions coexist with the same equation `Z=r*Gamma^2`.

## Exact Remaining System

On the trivial real-unit branch, the unresolved `G` square and positivity are
now exactly one unit-free square equation and one cone inequality, with

```text
r=sqf_odd(gcd(ell-1,R)).
```

The next gate must combine this standard equation with one complete `wl546`
integer orientation system. No Gaussian unit or divisor-class choice remains.

## Boundary

This is an exact uniformization, not a solution of the standard square
equation or either orientation. It does not handle the nontrivial real-unit
class, prove `wl535`, or enter M3.
