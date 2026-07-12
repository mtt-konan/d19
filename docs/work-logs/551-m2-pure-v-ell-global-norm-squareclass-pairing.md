# M2 Pure v_ell Global Norm Squareclass Pairing

## Question

What global restriction does `Norm(delta)=W^2` impose on the odd Gaussian
squarefree factor in the `wl547` class equation, after `wl548`-`wl550` have
exhausted the same-prime local tests?

## Norm Parity

Write the `wl547` element equation as

```text
delta=eta*d*gamma^2,
```

where `eta` is a Gaussian unit class and `d` is Gaussian-squarefree with odd
support. Taking norms gives

```text
W^2=Norm(delta)=Norm(d)*Norm(gamma)^2,
```

because every Gaussian unit has norm one. Therefore

```text
Norm(d) is an integer square.
```

This is a global consequence of the class equation, not another residue test.

## Pairing At Split Primes

For a supported rational prime `p ≡ 1 (mod 4)`, write

```text
p=pi*conjugate(pi).
```

The squarefree factor `d` contains each of `pi,conjugate(pi)` with exponent
zero or one. Their contributions to `Norm(d)` are both `p`. Since
`Norm(d)` is a square, the two exponents must agree. Thus a split prime occurs
in `d` either not at all or as the conjugate pair

```text
pi*conjugate(pi)=p.
```

For a supported `p ≡ 3 (mod 4)`, the Gaussian prime is the rational element
`p` itself and has norm `p^2`, already a square. It too contributes only the
rational factor `p` to `d`.

Consequently, after changing by a Gaussian unit if necessary, every surviving
squarefree factor is a rational squarefree integer:

```text
d=r,
r | rad(ell-1),
```

with prime divisors restricted further by the `wl549` root-square condition.
The class equation is therefore

```text
delta=eta*r*gamma^2,
eta in {1,i} modulo unit squares.
```

## Strict Reduction

Individual conjugate Gaussian primes over a split rational prime are not
independent squareclass generators. The remaining finite classes are indexed
by rational squarefree divisors `r`, plus the two unit classes. This is a
strict global reduction of the `wl547` safe class set whenever a supported
split prime is present.

## Next Exact Gate

Write `gamma=m+i*n`. Since

```text
delta=4*(ell-1)*Q^2*D^2
      + i*(R-4*(ell-1)*Q^2*D^2),
```

the next gate may use the real-coordinate equation, whose left side is
`4*(ell-1)*(QD)^2`, together with one fixed `wl546` orientation and the
rational class `r`. This is the first point at which the global class equation
can interact with the orientation beyond same-prime local compatibility.

## Boundary

This does not decide which rational `r` occurs, solve a class equation, use
positivity, handle the nontrivial real-unit class, prove the full `wl535`
proposition, or enter M3. These rational squareclasses are Gaussian descent
data, not theorem-level Selmer classes.
