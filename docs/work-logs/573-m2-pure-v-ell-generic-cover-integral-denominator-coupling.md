# M2 Pure v_ell Generic-Cover Integral Denominator Coupling

## Question

What global divisibility follows from the prime parameter being an integer on
the generic `wl570` cover?

## Primitive Coordinates

Write

```text
X=q^2=a^2/b^2,
gcd(a,b)=1,
b>0,

tau=m/n,
gcd(m,n)=1,
0<m<n.
```

The `wl570` interval `tau>sqrt(2)-1` gives

```text
Delta=m^2+2*m*n-n^2>0.
```

Homogenizing `ell=L(X,tau)` gives the exact integer equation

```text
H=2*ell*a^2*b^2*Delta,
```

where

```text
H = a^4*m*n
    +2*a^2*b^2*m^2
    +8*a^2*b^2*m*n
    -2*a^2*b^2*n^2
    -4*b^4*m*n.
```

## q-Numerator Support

Reduction modulo `a^2` gives

```text
H == -4*b^4*m*n (mod a^2).
```

Since the right side of the parameter equation is divisible by `a^2`,

```text
a^2 divides 4*b^4*m*n.
```

Using `gcd(a,b)=1` gives the exact necessary condition

```text
a^2 divides 4*m*n.
```

Thus every odd prime power in the numerator of `q` must occur to at least
twice that exponent in exactly one of the coprime integers `m,n`. Only the
visible factor `4` can absorb a dyadic deficit.

## q-Denominator Support

Reduction modulo `b^2` gives

```text
H == a^4*m*n (mod b^2),
```

and therefore

```text
b^2 divides a^4*m*n.
```

Coprimality of `a,b` yields

```text
b^2 divides m*n.
```

Because `m,n` are coprime, the square support of `b` splits uniquely between
them: there are coprime positive `b_m,b_n` with

```text
b=b_m*b_n,
b_m^2 divides m,
b_n^2 divides n.
```

## Delta Divides The Positivity Form

Modulo

```text
Delta=m^2+2*m*n-n^2,
```

the numerator reduces to

```text
H == m*n*K (mod Delta),
K=a^4+4*a^2*b^2-4*b^4.
```

Every common divisor of `Delta` and `m` divides `n^2`, and every common
divisor of `Delta` and `n` divides `m^2`. Since `gcd(m,n)=1`,

```text
gcd(Delta,m*n)=1.
```

The parameter equation has `Delta|H`, hence

```text
Delta divides K.
```

Moreover

```text
K=b^4*(X^2+4*X-4)>0
```

by the exact `wl570` positivity interval. Thus

```text
0<Delta<=K.
```

## Dyadic Boundary

Primitive `m,n` give

```text
v_2(Delta)=0  if m,n have opposite parity,
v_2(Delta)=1  if m,n are both odd.
```

The second line follows from `Delta==2 (mod 4)`. No stronger uniform dyadic
contradiction follows from parameter integrality alone.

## Exact Consequence

The variables of the generic genus-five cover no longer have independent
denominators. Every candidate with `tau!=1/2` must satisfy simultaneously

```text
a^2|4*m*n,
b^2|m*n,
Delta|a^4+4*a^2*b^2-4*b^4.
```

The next gate must combine these global support constraints with one of the
two factored source-square conditions. Repeating standalone local or dyadic
analysis is not progress.

## Boundary

This is an exact denominator-support lemma, not a contradiction. It does not
solve the generic cover, prove `wl535`, identify a Selmer group, or enter M3.
