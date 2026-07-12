# M2 Pure v_ell Common Delta-Squareclass Double Split

## Question

Can the two factored source squares be expressed by one canonical squareclass
and exact complementary splits after the denominator coupling in `wl573`?

## Homogeneous Positive Factors

Keep the primitive coordinates from `wl573` and define

```text
A=a^2*m+2*a^2*n-2*b^2*n,
B=a^2*n+2*b^2*m-2*a^2*m,
C=a^2*m+4*b^2*m-2*b^2*n,
D=a^2*n+2*b^2*m+4*b^2*n.
```

The exact `wl570` interval makes all four integers positive, and the source
squares are

```text
p^2=A*B/(2*a^2*b^2*Delta),
s^2=C*D/(2*b^4*Delta).
```

## One Canonical Squareclass

Let `k` be the positive squarefree kernel of `2*Delta` and write uniquely

```text
2*Delta=k*h^2,
h>0.
```

The first source square is equivalent to

```text
A*B=k*U^2
```

for a positive integer `U`. Indeed, forward propagation gives

```text
A*B/k=(a*b*h*p)^2.
```

The left side is an integer rational square, hence an integer square.
Conversely `A*B=k*U^2` reconstructs

```text
p=U/(a*b*h).
```

Exactly the same argument gives

```text
C*D=k*V^2,
s=V/(b^2*h)
```

for a positive integer `V`. Thus both source squares have the same
candidate-canonical squarefree class `k`; it is not a freely chosen descent
class.

## GCD Support Of A,B

Regard `A,B` as linear forms in `(m,n)`. Their coefficient determinant is

```text
R_1=5*a^4-8*a^2*b^2+4*b^4.
```

If `g_1=gcd(A,B)`, standard determinant combinations show

```text
g_1 divides R_1*m,
g_1 divides R_1*n.
```

Since `gcd(m,n)=1`,

```text
g_1 divides R_1.
```

The form `R_1` is strictly positive because its discriminant as a quadratic
in `a^2/b^2` is negative:

```text
R_1=5*(a^2-4*b^2/5)^2+4*b^4/5>0.
```

## GCD Support Of C,D

The corresponding determinant is

```text
R_2=a^4+8*a^2*b^2+20*b^4>0.
```

For `g_2=gcd(C,D)`, the same primitive-linear-form argument gives

```text
g_2 divides R_2.
```

Thus common factors inside either source pair are supported on an explicit
positive quartic independent of `(m,n)`.

## Exact Complementary Splits

Write

```text
A=g_1*A_0,
B=g_1*B_0,
gcd(A_0,B_0)=1.
```

Since `A_0*B_0` has squareclass `k`, there are unique coprime positive
squarefree integers `alpha,beta` and positive integers `r_1,s_1` such that

```text
alpha*beta=k,
A_0=alpha*r_1^2,
B_0=beta*s_1^2.
```

Likewise there are unique coprime squarefree `gamma,delta_0` with

```text
gamma*delta_0=k,
C/g_2=gamma*r_2^2,
D/g_2=delta_0*s_2^2.
```

The two complementary allocations may differ, but they are coupled by the
same canonical `k=sqf(2*Delta)`, while `g_1|R_1` and `g_2|R_2`.

## Next Exact Gate

The generic genus-five cover is reduced to two complementary splits of one
canonical squareclass plus two bounded-gcd quartic supports. The next gate
must compare the two allocations using exact linear relations among
`A,B,C,D`; treating either split independently would repeat an exhausted
allocation route.

## Boundary

This proves a common-squareclass double split, not an inconsistency. It does
not solve the generic cover, prove `wl535`, identify theorem-level Selmer, or
enter M3.
