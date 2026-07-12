# M2 Pure v_ell Trivial-Unit Gaussian Double Descent

## Question

Can the remaining Gaussian square in the `wl545` trivial real-quadratic unit
branch be replaced by a finite UFD compatibility condition?

## Primitive Gaussian Factorization

Keep

```text
A^2+Q^2=ell*D^2,
gcd(A,Q,D)=1,
D odd,
gcd(D,ell)=1.
```

The integers `A,Q` have opposite parity, and in fact `gcd(A,Q)=1`. Hence
`A+iQ` and `A-iQ` are coprime in `Z[i]`: a common Gaussian prime would lie
over a common rational divisor, while `1+i` cannot divide an element whose
real and imaginary parts have opposite parity.

Fix the unique sum-of-two-squares orientation

```text
ell=a_0^2+b_0^2,
pi=a_0+i*b_0.
```

Unique factorization and coprimality imply

```text
A+iQ = eta*pi_or_conjugate(pi)*(x+i*y)^2,
x^2+y^2=D,
```

where `eta` is a Gaussian unit. Modulo unit squares, sign changes, conjugation,
and `y -> -y`, there are exactly two essential orientations.

Define

```text
B_pi(x,y)=b_0*(x^2-y^2)+2*a_0*x*y,
R_pi(x,y)=a_0*(x^2-y^2)-2*b_0*x*y.
```

Then the exact alternatives are

```text
Q = +/- B_pi(x,y),
or
Q = +/- R_pi(x,y),
```

with `x^2+y^2=D`. A primitive rational candidate also gives
`gcd(x,y)=1`.

## Couple To The Real-Quadratic Descent

In the trivial unit class from `wl544`,

```text
Q=u*v,
D=abs(u^2-ell*v^2)/4.
```

Thus every candidate lies on one of only two double-descent systems:

```text
u^2-ell*v^2 = +/-4*(x^2+y^2),
u*v = +/-B_pi(x,y),
```

or

```text
u^2-ell*v^2 = +/-4*(x^2+y^2),
u*v = +/-R_pi(x,y).
```

The signs are harmless for conditions depending on `q^2` but are retained in
the exact integer equations.

The primitive parity data from `wl545` also remains:

- if `ell ≡ 5 (mod 8)`, `u,v` are odd and coprime;
- if `ell ≡ 1 (mod 8)`, write `u=2m,v=2n`, where `m,n` are coprime and have
  opposite parity.

## Forward And Converse Scope

The forward implication follows from Gaussian UFD. Conversely, either
quadratic-form orientation, together with `D=x^2+y^2`, reconstructs the other
coordinate of `pi*(x+iy)^2` or `i*pi*(x+iy)^2`, and therefore reconstructs an
integer `A` satisfying `A^2+Q^2=ell D^2`. So the two systems are an exact
replacement for the Gaussian square equation, subject to the displayed
primitive normalization when tracing a primitive candidate.

The remaining equations become

```text
q=Q/D=u*v/(x^2+y^2),
D^8*G_ell((Q/D)^2) square,
ell*Q^4+4*Q^2*D^2-4*ell*D^4>0.
```

## Exact Boundary

This is a genuine double descent: both the real-quadratic norm square and the
Gaussian square have been replaced by two finite quadratic-form compatibility
systems. The only unresolved square is the homogeneous `G_ell` square, still
coupled to positivity.

This work does not solve either orientation, handle the nontrivial unit class,
produce a rational point, prove a family exclusion, establish theorem-level
Selmer/rank/`Sha`, or enter M3.
