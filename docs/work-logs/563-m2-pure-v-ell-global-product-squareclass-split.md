# M2 Pure v_ell Global Product Squareclass Split

## Question

What global integer structure follows by combining the imaginary-coordinate
equation in `wl555` with the selected orientation variables, beyond the local
character matrix exhausted in `wl562`?

## Product Equation

Let `L=ell-1`. The standard square gives

```text
E=2*r*a*b=4*L*Q^2*D^2.
```

Since `r>0` and `a*b>0`, replace `(a,b)` by `(-a,-b)` if necessary and take
`a,b>0`. Put

```text
s=L/r.
```

Then the exact global product equation is

```text
a*b=2*s*(Q*D)^2.
```

## Coprime Squareclass Split

Let

```text
g=gcd(a,b),
a=g*A,
b=g*B,
gcd(A,B)=1.
```

Let `kappa` be the positive squarefree kernel of `2*s`, and write uniquely

```text
2*s=kappa*h^2.
```

The product equation shows that `A*B` and `kappa` have the same rational
squareclass. Since `A,B` are coprime, there are unique coprime squarefree
positive integers `alpha,beta` and positive integers `M,N` such that

```text
alpha*beta=kappa,
A=alpha*M^2,
B=beta*N^2.
```

Cancelling the common squareclass in the product equation gives the exact
scale relation

```text
g*M*N=h*abs(Q*D).
```

Thus the Gaussian-square coordinates are no longer free integers: their
coprime squarefree parts form a finite complementary divisor split of the
candidate-canonical integer `kappa`.

## Remaining Real Coordinate And Cone

The real-coordinate equation becomes

```text
F=r*g^2*(alpha^2*M^4-beta^2*N^4).
```

After dividing the uniform positivity cone by the positive factor `r*g^2`, it
becomes

```text
ell*(alpha^2*M^4-beta^2*N^4)
 +2*L*kappa*M^2*N^2 > 0.
```

The selected `wl556` orientation supplies `Q` and `D=x^2+y^2`, so the full
coupling now contains the explicit global relation

```text
g*M*N=h*abs(Q)*(x^2+y^2).
```

This is a genuine integer factorization constraint invisible to the local row
bits in `wl562`.

## Next Exact Gate

For each complementary divisor split `alpha*beta=kappa`, the surviving branch
is reduced to one quartic-difference equation, one product-scale equation, the
selected `B_pi` or `R_pi` orientation, and the displayed strict inequality.
The next gate must attack one such split uniformly or prove that these split
systems are the exact unresolved global arithmetic lemma.

## Boundary

This does not claim any split is soluble or insoluble, enumerate parameter
samples as proof, solve a surviving orientation, handle the nontrivial
real-unit class, prove `wl535`, or enter M3.
