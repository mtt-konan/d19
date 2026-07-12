# M2 Pure v_ell Dyadic Same-Side And Identical k-Allocation

## Question

Does the sole remaining factor `2` transport on the same side under the
`wl575` rotation, making the two complementary `k`-allocations identical?

## Primitive 2-Adic Rotation

For primitive `a,b`, define

```text
e=1  if a is odd,
e=4  if a is even.
```

`wl575` proves

```text
gcd(P,K)=gcd(R1,R2)=e.
```

Put

```text
P0=P/e,
K0=K/e,
S1=R1/e,
S2=R2/e.
```

All four integers are odd. Dividing the scaled rotation by `e` gives

```text
S1*C=P0*A-2*K0*B,
S1*D=2*K0*A+P0*B.
```

Thus over `Z_2` the transformation matrix has odd diagonal entries and even
off-diagonal entries. Its determinant is the unit

```text
S2/S1,
```

by `P0^2+4*K0^2=S1*S2`.

## Valuation-Ordering Lemma

Let a `2`-adic unit matrix have the form

```text
[ odd  even ]
[ even odd  ].
```

If `v_2(A)<v_2(B)`, then the first output coordinate has valuation exactly
`v_2(A)`: its odd-diagonal term has that valuation and its other term has
strictly larger valuation. Both terms in the second output coordinate have
valuation strictly larger than `v_2(A)`. Hence

```text
v_2(C)<v_2(D).
```

The symmetric argument gives

```text
v_2(A)>v_2(B) => v_2(C)>v_2(D).
```

Therefore the transformation preserves which coordinate has the larger
valuation whenever the input valuations differ. Possible cancellation in the
larger coordinate cannot reverse the ordering.

## Apply To The Canonical Class

If `2|k`, then from

```text
A*B=k*U^2,
C*D=k*V^2
```

both valuation sums are odd:

```text
v_2(A)+v_2(B)=1 mod 2,
v_2(C)+v_2(D)=1 mod 2.
```

Thus the two valuations in each pair are unequal. After removing their common
gcd, the side carrying the squarefree factor `2` is exactly the coordinate
with larger valuation. The ordering lemma proves

```text
A-side -> C-side,
B-side -> D-side.
```

So `2` transports same-side. If `2` does not divide `k`, there is no dyadic
allocation to compare.

## Identical Complementary Allocation

`wl577` already proves same-side transport at every odd prime of `k`. Adding
the dyadic result gives the exact identities

```text
alpha=gamma,
beta=delta_0.
```

The two source-square factorizations use one and the same complementary split
of `k`; no allocation variable remains.

## Remaining Magnitude System

The unresolved equations are now only the square magnitudes. With

```text
A=g1*alpha*r1^2,
B=g1*beta*s1^2,
C=g2*alpha*r2^2,
D=g2*beta*s2^2,
alpha*beta=k,
```

the rotation becomes

```text
R1*g2*alpha*r2^2
 =P*g1*alpha*r1^2-2*K*g1*beta*s1^2,

R1*g2*beta*s2^2
 =2*K*g1*alpha*r1^2+P*g1*beta*s1^2.
```

The next gate must attack this common-allocation magnitude system. Any further
side allocation analysis is exhausted.

## Boundary

This proves complete allocation identity, not inconsistency of the remaining
magnitudes. It does not solve the generic cover, prove `wl535`, identify
theorem-level Selmer, or enter M3.
