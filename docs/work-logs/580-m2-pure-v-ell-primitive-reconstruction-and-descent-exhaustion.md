# M2 Pure v_ell Primitive Reconstruction And Descent Exhaustion

## Question

Does the primitive linear-form condition add a new equation to the `wl579`
magnitude torsor, or does it reconstruct uniquely and close the descent loop?

## Recover tau From X And z

In normalized `wl570` coordinates,

```text
Abar=X*(tau+2)-2,
Bbar=2*tau-X*(2*tau-1),
z=Bbar/Abar.
```

Solving the linear equation for `tau` gives

```text
tau=T(X,z)
   =[X+2*z*(1-X)]/[X*(z+2)-2].
```

There is no exceptional denominator in the candidate domain. Since `X>1`
and `z>0`,

```text
X*(z+2)-2>2*X-2>0.
```

Thus `(X,z)` uniquely determines `tau`. If the reconstructed value lies in
the exact interval `sqrt(2)-1<tau<1`, it has a unique primitive expression

```text
tau=m/n,
gcd(m,n)=1,
0<m<n.
```

No extra primitive-coordinate branch remains.

## Canonical Squareclass Self-Consistency

Put

```text
Delta=m^2+2*m*n-n^2>0,
k=sqf(2*Delta).
```

Choose the candidate's complementary split `alpha*beta=k` and set

```text
lambda=beta/alpha.
```

As rational squareclasses,

```text
[lambda]=[alpha*beta]=[k]=[2*Delta]=[2*(tau^2+2*tau-1)].
```

The common-allocation magnitude condition is exactly

```text
z/lambda is a rational square,
w/lambda is a rational square,
```

where

```text
w=(2*K+P*z)/(P-2*K*z).
```

## Reconstruct The Source Squares

Since `z=Bbar/Abar`,

```text
Abar*Bbar=Abar^2*z.
```

The first factored source predicate is

```text
p^2=Abar*Bbar/(2*X*(tau^2+2*tau-1)).
```

Here `X` is a rational square, while `z` and
`2*(tau^2+2*tau-1)` have the same squareclass `lambda`. Therefore the right
side is a rational square.

Likewise `w=Dbar/Cbar` gives

```text
Cbar*Dbar=Cbar^2*w,
s^2=Cbar*Dbar/(2*(tau^2+2*tau-1)),
```

and the second right side is a rational square because `w` has the same
squareclass.

Conversely, the two source squares produce the canonical common allocation
and hence `z/lambda`, `w/lambda` square by `wl574`-`wl578`. Thus the
self-consistent `wl579` torsor and the two `wl570` source predicates are
equivalent.

## Strict Orientation Identity

The primitive linear forms also satisfy

```text
Abar*Dbar-Bbar*Cbar
 =2*(tau^2+1)*(X^2+4*X-4)>0.
```

This is exactly the strict ordering `w>z` from `wl579`, not an additional
obstruction.

## Exact Failure Point

The sequence `wl573`-`wl579` is now complete as a descent:

- parameter integrality couples denominators;
- both source squares share one canonical squareclass;
- the scaled rotation makes their allocation identical;
- the magnitude torsor records the remaining common squareclass;
- primitive `(m,n)` reconstructs uniquely from `(X,z)`.

After canonical self-consistency is imposed, this machinery is equivalent to
the `wl570` two-source-square system. No further allocation, valuation, gcd,
or coordinate rewrite can yield progress by itself.

## Next Exact Lemma

The unresolved arithmetic theorem is:

```text
For every odd prime ell congruent 1 mod 4, the self-consistent genus-one
magnitude torsor (equivalently the generic genus-five cover) has no positive
rational point in the exact wl570 interval.
```

A next gate must prove a rational-point obstruction on this family or produce
a strict point. It must not continue the exhausted descent bookkeeping.

## Boundary

This is a route-exhaustion certificate and exact missing lemma, not a proof of
that lemma. It does not prove `wl535`, family exclusion, theorem-level Selmer,
or enter M3.
