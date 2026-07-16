# Q3a3 Dyadic Fake-Kernel Exact Sequence

## Outcome

`q3a3_exact_fake_kernel`

For

```text
K=Q_2(i),
A=K[t]/(g6)=E_2 x E_4,
[E_2:K]=2, [E_4:K]=4,
```

the exact even-degree fake descent sequence proves

```text
ker(delta_varpi)=<D_inf>,
dim_F2 ker(delta_varpi)=1,
dim_F2 I_varpi=4.
```

This closes Q3a3 without guessing three more point classes.  It uses the
accepted Q3a2 injective diagonal restriction and the accepted exact theorem
`D_inf not in 2J(K)`.

## Group-Scheme Sequence

Put

```text
R = Res_(A/K)(mu_2),
Q = R/mu_2,
```

where the denominator is the diagonal copy of `mu_2`.  Since `deg(g6)=6` is
even, the norm on `R` is trivial on the diagonal and descends to `Q`.  The
root-subset description of two-torsion gives the exact sequence

```text
1 -> J[2] -> Q --Norm--> mu_2 -> 1.
```

Over a separable closure, `R` is the six-dimensional sign space.  Quotienting
by the all-sign vector gives dimension five, and the product-of-signs row has
rank one.  Its four-dimensional kernel is exactly the even root subsets
modulo complements, hence `J[2]`.

Taking `K`-points and first cohomology gives

```text
Q(K) --Norm--> mu_2(K) --partial--> H^1(K,J[2])
     --> H^1(K,Q).
```

The Kummer map embeds `J(K)/2J(K)` in `H^1(K,J[2])`.  To compare the following
map with fake evaluation, also use

```text
1 -> mu_2 -> R -> Q -> 1.
```

Its cohomology sequence gives an injection

```text
A^*/(A^{*2}K^*) -> H^1(K,Q).
```

The possible following Brauer term is a cokernel of this injection, not an
extra kernel.  In fact, for the present even-degree local algebra it is
nonzero: the nontrivial class in `Br(K)[2]` restricts trivially to both
even-degree factors.  It must therefore be kept explicit rather than silently
identifying all of `H^1(K,Q)` with the fake quotient.

What is needed here is the exact descent commutative square

```text
J(K)/2J(K)  --Kummer-->  H^1(K,J[2])
     |                         |
 delta_fake                   inclusion_*
     |                         |
A^*/(A^{*2}K^*) ---------> H^1(K,Q).
```

The bottom arrow is the injection above.  To check commutativity directly,
work over a separable closure and label the six roots by `omega`.  The
functions `t-omega` satisfy

```text
div(t-omega)=2*W_omega-P_+-P_-.
```

If `E` is a half of a rational degree-zero divisor class, the cocycle
`sigma(E)-E` is its Kummer class.  Evaluating the six functions on twice `E`
and applying Weil reciprocity gives exactly the six sign coordinates of the
image of that cocycle in `R/mu_2`; changing `E`, the divisor representative,
or the common infinity normalization changes the result by an `A`-square or
a diagonal `K`-constant.  This is precisely the class of the accepted
divisor evaluation in `A^*/(A^{*2}K^*)`.  Hence the square commutes, including
the two infinity points.

Consequently, if an actual divisor class has trivial fake evaluation, its
Kummer class maps to zero in `H^1(K,Q)`.  Exactness then places it in

```text
mu_2(K) / Norm(Q(K)).
```

No assertion that all of `H^1(K,Q)` is untwisted is used.

## Exact K-Point Term

There is one possible subtlety: `Q(K)` need not equal
`R(K)/mu_2(K)` if a nonsquare constant becomes a square in `A`.  The exact
sequence for `1 -> mu_2 -> R -> Q -> 1` shows that the obstruction is exactly

```text
ker(K^*/K^{*2} -> A^*/A^{*2}).
```

Q3a2 computes the base squareclass dimension as four and the diagonal image
rank as four.  Hence this restriction kernel is zero and

```text
Q(K)=R(K)/mu_2(K).
```

The two accepted local factors are fields of relative degrees `2` and `4`,
so

```text
R(K)=mu_2(E_2) x mu_2(E_4) = {+/-1}^2.
```

Modulo the diagonal signs, `Q(K)` has one nonzero sign class.  Its norm is

```text
(-1)^2*(+1)^4=+1
```

(and the other representative gives the same result).  Thus

```text
Norm(Q(K))={+1},
dim_F2 mu_2(K)/Norm(Q(K))=1.
```

Consequently the fake map on `J(K)/2J(K)` has kernel dimension at most one.

## Realized Kernel And Image

The accepted Q3a3 divisibility certificate proves

```text
D_inf=[P_+-P_-] not in 2J(K).
```

Its fake evaluation is trivial because the leading coefficient is `1`.
Therefore `D_inf` realizes the unique nonzero cohomological kernel class:

```text
ker(delta_varpi)=<D_inf>.
```

Finally, the accepted source dimension is five, so rank-nullity gives

```text
dim_F2 I_varpi = 5-1 = 4.
```

The earlier Q3a3c point and Mumford searches are not used as proof.  Their
uncertified apparent rank-four vectors are discarded, and the unreviewed
factor-zero payload is not retained.  This result is local to Q3a.  It makes
no Q3b-Q4, global Selmer, rank, Berry-classification, or D19 mainline claim.
