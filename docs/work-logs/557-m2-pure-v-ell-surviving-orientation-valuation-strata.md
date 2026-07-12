# M2 Pure v_ell Surviving-Orientation Valuation Strata

## Question

What exact 2-adic compatibility remains inside the single orientation selected
by `wl556`, once it is coupled to the real-quadratic variables?

## The ell = 5 mod 8 Branch Is Dyadically Exhausted

Here `v_2(b_0)=1`, `x,y` have opposite parity, and the selected form is

```text
R_pi=a_0*(x^2-y^2)-2*b_0*x*y.
```

Its first term is odd and its second term is divisible by `8`, so `R_pi` is
odd. This is exactly the already-required `v_2(Q)=0`; no sharper 2-adic
condition on `x,y` follows. Thus the surviving `R_pi` branch is exhausted at
`2` and must next be attacked globally or at an odd place.

## Exact Valuation Formula In The ell = 1 mod 8 Branch

Put

```text
c=v_2(b_0)>=2,
k=v_2(x*y)>=1,
s=x^2-y^2 (odd).
```

The selected form is

```text
B_pi=b_0*s+2*a_0*x*y.
```

The two summands have valuations `c` and `k+1`. Therefore

```text
v_2(B_pi) = c       if c<k+1,
v_2(B_pi) = k+1     if c>k+1,
v_2(B_pi) >= c+1    if c=k+1.
```

In the equal-valuation case the exact value is determined by the residual odd
sum after factoring `2^c`.

In particular, the necessary condition `v_2(B_pi)>=3` is equivalent to

```text
(c=2 and k=1) or (c>=3 and k>=2).
```

The excluded mixed cases are `(c=2,k>=2)` and `(c>=3,k=1)`, where one
summand has exact valuation two and the other has larger valuation.

## Couple To The Real-Quadratic Product

Write the `wl545` variables as `u=2*mu`, `v=2*nu`, with `mu,nu` coprime and
of opposite parity. Since `Q=u*v`,

```text
v_2(Q)=2+v_2(mu*nu)=v_2(B_pi).
```

Thus the surviving branch splits into the exact valuation strata above, with
the displayed value matched to `2+v_2(mu*nu)`. This is a genuine compatibility
condition between the real-quadratic and Gaussian orientation descents.

## Exact Failure Point

The strata are nonempty: the equal-valuation case can raise `v_2(B_pi)`
arbitrarily through congruence cancellation, while unequal cases realize the
displayed minimum. Hence dyadic valuation matching alone does not close the
`B_pi` branch. Further progress must use an odd/global equation or the full
`wl555` standard square and cone simultaneously.

## Boundary

This does not produce a global solution, prove every stratum globally
nonempty, solve either surviving branch, handle the nontrivial real-unit
class, prove `wl535`, or enter M3.
