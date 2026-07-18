# Berry C_1 B2 Rank And Saturation Boundary

## Outcome

This is an exact partial B2 checkpoint:

~~~
J[2](K) = 0,
2 <= rank J(K) <= 3,
H = <E_+, D_inf> has rank 2,
H is not 2-saturated in J(K).
~~~

Here K=Q(i), C_1: v^2=g6(t), and the only already-certified K-points used
are

~~~
A_+ = [0:i:1],  A_- = [0:-i:1],
P_+ = [1:1:0],  P_- = [1:-1:0].
~~~

The checkpoint does not determine whether the rank is 2 or 3, does not give
a full Mordell-Weil basis, and does not classify rational t.

## Global Branch Algebra And J[2]

Use the exact global branch polynomial

~~~
g6(t) = t^6 + (-2-2*i)t^5 + (-35-8*i)t^4 + (-52-28*i)t^3
        +(19-40*i)t^2 + (6+14*i)t - 1.
~~~

At the global prime

~~~
lambda_13 = (13, i-5),
~~~

the reduction is

~~~
f_13(x) = x^6+x^5+3*x^4+3*x^3+x^2+11*x+12 in F_13[x].
~~~

The exact finite-field irreducibility certificate is

~~~
x^(13^2) mod f_13 = 4*x^5+6*x^4+7*x^3+x^2+10*x+3,
x^(13^3) mod f_13 = 3*x^5+8*x^3+8*x^2+5*x+6,
x^(13^6) mod f_13 = x,

gcd(f_13, x^(13^2)-x) = 1,
gcd(f_13, x^(13^3)-x) = 1.
~~~

Since the prime divisors of 6 are 2 and 3, this is the standard finite-field
irreducibility criterion. Thus f_13 is irreducible of degree 6. The monic
Gauss-lemma lift gives that g6 is irreducible over K. This is a global
branch-algebra argument; no local factorization at (1+i) or (94*i-169) is
used.

Over Kbar, every nonzero element of J[2] is represented by an even subset of
the six finite branch points, modulo complement. Replacing a four-element
subset by its complement, a nonzero class has a representative S of size 2.
If its class is K-rational, Galois sends S to S or its complement. The
complement has size 4, so the size-preserving action forces S to be
Galois-stable. The product of the two corresponding linear factors would then
be a quadratic factor of g6 over K, contradicting irreducibility. Therefore

~~~
J[2](K) = 0.
~~~

The local [2,4] and [1,1,2,2] factor patterns remain local data and do not
enter this global conclusion.

## Structural Point Classes

Set

~~~
E_+   = [A_+-P_+],
E_-   = [A_--P_+],
D_inf = [P_+-P_-].
~~~

Because g6(0)=-1 is nonzero, t has a simple zero at each A_+ and A_-.
It has a simple pole at each even-degree infinity point. Hence the complete
principal divisor relation supported on these four points starts with

~~~
div(t) = A_+ + A_- - P_+ - P_-.
~~~

Consequently

~~~
E_+ + E_- + D_inf = 0.
~~~

There are no other relations among these three classes. The exact
good-reduction certificate below proves that E_+ and D_inf are Z-independent.
Substituting E_-=-E_+-D_inf, any relation

~~~
a*E_+ + b*E_- + c*D_inf = 0
~~~

has a=b=c. Thus all principal-divisor relations in this enumerated four-point
support are exactly the multiples of div(t).

## Rank-Two Lower Bound

Use the split good prime

~~~
lambda_269 = (269, i-82),
82^2+1 = 0 mod 269.
~~~

The displayed model has good reduction there. The exact proof-enabled Sage
certificate gives

~~~
g_269(x) = x^6+103*x^5+116*x^4+73*x^3+236*x^2+78*x+268,
#C_1(F_269)   = 282,
#C_1(F_269^2) = 72430,
#J_1(F_269)   = 75708,
J_1(F_269) ~= Z/3 Z + Z/25236 Z.
~~~

For reproducibility, fixed exact Mumford classes generating this finite group
are

~~~
G_1 = (x^2+96*x+106, 44*x+8),   order 25236,
G_2 = (x^2+54*x+268, 129*x+60), order 3.
~~~

The reductions of the structural classes have the exact coordinates

~~~
E_+   = 14912*G_1 + G_2,
E_-   =  9310*G_1 + G_2,
D_inf =  1014*G_1 + G_2.
~~~

The first two coordinates modulo 3 are therefore

~~~
E_+   -> (2,1),
D_inf -> (0,1)
~~~

in J_1(F_269)/3J_1(F_269) ~= F_3^2; their determinant is 2, nonzero modulo
3.

At good reduction with residue characteristic 269 != 3, the reduction kernel
is a pro-269 group, so multiplication by 3 is an automorphism of the kernel.
Reduction therefore induces an injection on the 3-quotient. Any global
relation a*E_+ + b*D_inf=0 forces 3|a,b. Since the accepted good-prime
specialization certificate gives J_1(K)_tors=0, the relation can be divided
by 3; iteration forces a=b=0. Hence

~~~
rank <E_+,D_inf> = 2.
~~~

This is an exact reduction certificate for independence, not a bounded search
for points on C_1.

## Selmer Rank Upper Bound

The accepted Q3c input gives

~~~
dim_F2 Sel_2(J/K) = 3.
~~~

Keep the Kummer and Tate-Shafarevich terms separate:

~~~
0 -> J(K)/2J(K) -> Sel_2(J/K) -> Sha(J/K)[2] -> 0.
~~~

The accepted torsion result is J(K)_tors=0; the global calculation above also
proves J[2](K)=0. Thus

~~~
dim_F2 J(K)/2J(K) = rank J(K).
~~~

It follows exactly that

~~~
3 = rank J(K) + dim_F2 Sha(J/K)[2],
2 <= rank J(K) <= 3.
~~~

No vanishing of Sha(J/K)[2] is inferred.

## Exact 2-Saturation Consequence

At a finite affine point the accepted Q3c divisor-evaluation formula is

~~~
delta([Q-P_+]) = [t(Q)-theta].
~~~

For both A_+ and A_-, t(Q)=0, so the finite evaluation is `[-theta]`.
The reciprocal infinity-chart formula `[1-x(Q)*theta]` is not applicable at
these points because `x=1/t` is undefined. The exact power-basis element

~~~
beta = ((1+3*i)/64)*theta^5 + ((5-5*i)/64)*theta^4
       +((-3-63*i)/32)*theta^3 + ((5-139*i)/32)*theta^2
       +((117-69*i)/64)*theta + (1+27*i)/64
~~~

satisfies `beta^2=-i*theta` modulo `g6(theta)`. Hence

~~~
[-theta] = [(-i)*beta^2] = [1] in L^*/(L^{*2}K^*).
~~~

This is an exact finite-chart squareclass certificate, not a substitution of
the reciprocal formula. Therefore

~~~
delta(E_+) = delta(E_-) = [1].
~~~

The accepted Q3c exact sequence has kernel

~~~
ker(Sel_2(J/K) -> Sel_fake^S) = F_2<kappa(D_inf)>,
kappa(D_inf) != 0.
~~~

Therefore each of kappa(E_+) and kappa(E_-) is either 0 or kappa(D_inf).
Applying the principal relation gives exactly one of E_+ and E_- zero Kummer
class. Equivalently, one of

~~~
E_+       or       E_+ + D_inf
~~~

is twice a K-rational Jacobian point. The alternative is exact but the current
accepted inputs do not identify which branch.

Let H=<E_+,D_inf>. Since H is free of rank 2, H/2H has dimension 2, while its
image in J(K)/2J(K) has dimension 1. Thus

~~~
H is not 2-saturated in J(K).
~~~

This is a proved failure of saturation, not an unresolved saturation claim.
It does not increase the rank: the missing half lies in H tensor Q.

## First Missing Implication And Next Gate

The first missing implication is not dim Sel_2=3 => rank=3; that implication
is false without controlling Sha(J/K)[2]. The structural classes prove only
the rank-two lower bound, and they are not yet a saturated generating
subgroup.

The smallest next arithmetic obligation is:

~~~
decide whether E_+ or E_++D_inf has a K-rational half, construct that half
exactly, and 2-saturate the resulting rank-two subgroup;
then decide rank 2 versus rank 3 by an independent exact rank obstruction
or a third independent K-rational Jacobian class.
~~~

An odd-index saturation or full Mordell-Weil basis claim is also not supplied
by the present data.

## Chabauty Boundary

The genus is 2, while the certified rank is at least 2. The ordinary
Mordell-Weil Chabauty hypothesis over K is rank J(K)<2, so it is not met.
No alternative rational-t method has been set up with its theorem hypotheses.
B3 and rational-t classification remain closed.

## Exact Artifacts

The exact verifiers are:

~~~
scripts/theory/berry_sextic_b2_rank_boundary.py
scripts/theory/berry_sextic_b2_rank_boundary.sage
tests/test_berry_sextic_b2_rank_boundary.py
~~~

The Python verifier checks the finite-field irreducibility certificate,
principal relation data, accepted torsion/Selmer inputs, and the serialized
good-reduction coordinates. The Sage verifier runs with proof.all(True) and
reconstructs the degree-6 branch reduction, finite-field Jacobian group, fixed
Mumford generators, and all three class coordinates.
