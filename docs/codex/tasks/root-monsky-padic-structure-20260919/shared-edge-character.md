# A shared-edge quadratic character obstruction

## Question and outcome

Can the four square Gaussian norms, linked by the same square edges, produce
an obstruction that is stronger than the direct Q_2 square tests?

Yes, at the following precise scope. If a full-plane rational-distance point
has coordinates (X/N,Y/N), N > 0 and gcd(X,Y,N)=1, then **8 divides N**.
The argument couples opposite corners at odd primes to a dyadic character of
primitive Pythagorean triples. It is a necessary condition, not a global
exclusion or an infinite descent. No literature-priority claim is made.

Inputs are the four individual rational distances and the exact square
geometry. No elliptic quotient, product-square relaxation, bounded search,
or archived Selmer/HRL mechanism is used.

## Integer and dyadic normalization

Distance differences imply x,y are rational. After choosing the primitive
common denominator N, each scaled distance R is an integer: R is rational
and R^2 is an integer. Thus all four expressions

    (X-a*N)^2 + (Y-b*N)^2,  a,b in {0,1},

are integer squares. Their square roots need not be assigned signs.

If N were odd, one of the four coordinate pairs would be odd-odd, giving
2 modulo 4. Thus N is even. Primitivity and reduction modulo 4 force X,Y to
have opposite parity. Exchange the axes to make X odd. Reduction modulo 8
then gives 4|Y and 4|(Y-N), hence 4|N.

Conversely, X odd, 4|Y and 4|N make all four expressions 1 modulo 8, hence
squares in Q_2. The restriction proved below is therefore not a consequence
of higher-precision square testing in Q_2 alone.

## Opposite-corner content lemma

Write U=X-a*N, V=Y-b*N and g_ab=gcd(U,V)>0. No coordinate pair is (0,0):
a vertex would have distance N*sqrt(2) to its opposite vertex.

Primitivity implies gcd(g_ab,N)=1. The four contents are also pairwise
coprime: a common prime at two distinct corners divides N and then X,Y.

For any prime p|g_ab, the squared distance to the opposite corner is

    (U+(2*a-1)*N)^2 + (V+(2*b-1)*N)^2 = 2*N^2 mod p.

The prime p is odd because U is odd, and p does not divide N. The opposite
distance is an integer, so 2 is a nonzero square modulo p. Consequently

    p = 1 or 7 mod 8, for every prime dividing any g_ab.

This uses the opposite individual square lift, not merely the product of
the four norm expressions. In particular, for the quadratic character

    chi_2(t) = (-1)^((t^2-1)/8),  t any odd integer,

we have chi_2(g_ab)=1. The character is multiplicative and unchanged by
negating its argument.

## Pythagorean content-character identity

For any integer right triangle U^2+V^2=R^2 with U odd and 4|V, let
g=gcd(U,V)>0. Then

    chi_2(U) * (-1)^(V/4) = chi_2(g).                 (1)

If V=0, g=|U| and (1) is immediate. Otherwise divide by g and use the
primitive Pythagorean parameterization, allowing both coordinate signs:

    U/g = s*(m^2-n^2),   V/g = 2*m*n,
    s in {1,-1}, m odd, n even, gcd(m,n)=1.

The sign of n accommodates negative V. Modulo 8, m^2-n^2 is 1 when 4|n
and 5 when n=2 mod 4. Hence

    chi_2(U/g) = (-1)^(n/2) = (-1)^(m*n/2).

As g is odd, m*n/2=V/(4*g) has the same parity as V/4. Multiplicativity
proves (1). This is an integer-factorization statement; arbitrary Q_2 square
roots do not justify the primitive integer parameterization.

## The boundary character forces 8|N

Define, on odd U and V divisible by 4,

    C(U,V) = chi_2(U) * (-1)^(V/4).

The content lemma and (1) force C=1 at all four corners. In particular,

    chi_2(X) = (-1)^(Y/4) = (-1)^((Y-N)/4).

Therefore N/4 is even, so 8|N. No positivity or interior assumption was
used. The proof also gives the necessary residue conditions

    Y = 0 mod 8  =>  X = 1 or 7 mod 8,
    Y = 4 mod 8  =>  X = 3 or 5 mod 8.

The finite coloring interpretation is exact. If N=4 mod 8, the labels in
corner order (00,10,01,11) are (C,-C,-C,C), so they cannot all be 1. If
8|N, all four labels agree. Thus this particular character cannot turn the
new divisibility into indefinite divisibility by higher powers of 2.

## Scope witnesses and descent boundary

The primitive interior tuple (X,Y,N)=(1,4,12) has norm expressions
(17,137,65,185), all 1 modulo 8. It is Q_2-soluble although 8 does not
divide N. This separates the global character argument from pure Q_2
solubility.

The interior tuple (3,4,24) passes all four content-prime and character
conditions: all contents are 1 and all labels are 1. Its norm expressions
are (25,457,409,841). The first and last are squares, while the other two
are not. Thus the resulting conditions are not sufficient for the original
four-distance problem, and the surviving class is not empty merely as a
class of rational coordinate candidates.

A second issue concerns proposed Gaussian common-factor descent. Dividing
the point Z=X+iY and the square side W=N by the same nonzero Gaussian
factor q gives (Z/q,W/q). Whenever its modulus is rational this preserves
rational distances, but the normalized coordinate is exactly

    (Z/q)/(W/q) = Z/W.

This is a similarity of the same configuration and does not decrease its
primitive unit-square denominator N. It may simplify an integer embedding
of a rotated square, but no repeatable descent follows. A genuine descent
would need a new configuration, preservation of all four individual square
lifts, and a strictly decreasing positive integral height.

## Remaining obligation and verification

The accepted outcome is a uniform necessary denominator and residue
restriction, with an exact explanation of where its character argument
stops. The Monsky analogy now has a concrete content: global factorization
forces four finite labels, while shared edges govern their transport.

There is no constructed invariant that contradicts the surviving 8|N
branch, and no constructed non-similarity descent. The original problem
remains open in this repository. This task does not select an automatic
follow-on or create a numbered mathematical checkpoint.

The proof above is uniform. Task-local tests check the exact residue
certificate, diagonal identity, signed and degenerate Pythagorean cases,
nonprimitive contents, both scope witnesses, and the similarity identity.
Their finite examples are regression checks, not a replacement for proof.

Verification completed: 7 task-local tests and 8 protected equal-side
regression tests passed with -n 0; targeted Ruff passed. Stable mathematical
scripts, prior certificates, and historical task records were not changed.
