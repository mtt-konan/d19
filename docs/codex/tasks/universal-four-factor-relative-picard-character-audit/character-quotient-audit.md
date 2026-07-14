# Universal Four-Factor Relative Picard Character Audit

Status: complete.

This report starts strictly after the accepted scoped result
`low_support_candidate_space_zero`. It will record only the explicitly defined
character-quotient and radical-linear/sign-split candidate universe. It is not
a computation of all `Pic(C)[2]` unless the required pullback, norm, and
2-primary isogeny kernels are actually controlled.

## Accepted Outcome

```text
accepted_outcome=non_base_pullback_candidate_ready
```

The accepted class is a parameter-uniform non-base-pullback unramified
2-cover class. This authorizes only a later descent-design audit. It is not an
obstruction and does not authorize `wl596` automatically.

## Phase 0: Exact Object And Literature Audit

Work over two separate generic fields:

```text
K_plus  = Q(A,B), T=A+B,
K_minus = Q(A,B), T=A-B, with A>B>0 on the real chamber.
```

The minus chart is an algebraic signed chart for the physical target
`T=|A-B|`. Put

```text
P_1=P_A+=(T+t)^2+4*A^2,  P_2=P_A-=(T-t)^2+4*A^2,
P_3=P_B+=(T+t)^2+4*B^2,  P_4=P_B-=(T-t)^2+4*B^2.
```

The generic open excludes

```text
A*B*T*(A^2-B^2)=0
```

and the six pairwise resultants from `wl595`. Equivalently, the eight roots
of the four `P_i` are simple and pairwise distinct. On either positive closure
branch the extra resultant factors are positive, so this is the same smooth
physical open used by `wl594` and the precursor census.

Let `C` be the normalization of `P^1_t` in

```text
K(t)(r_1,r_2,r_3,r_4),  r_i^2=P_i.
```

The four radicands are independent in `K(t)^*/K(t)^{*2}` because each has a
simple zero outside the other three branch sets. Hence `C` is connected,
`deg(C/P^1)=16`, and its deck group is

```text
G=(Z/2)^4,
e_i(r_i)=-r_i, e_i(r_j)=r_j for j!=i.
```

There are eight geometric branch values. Above each there are eight points
of ramification index two, and infinity is unramified because every `P_i` has
even pole order two. Thus

```text
2*g(C)-2=16*(-2)+8*(16/2)=32,
g(C)=17.
```

Divisors below mean Weil divisors on this smooth normalization. A proposed
unramified Kummer class must be represented by `h in K(C)^*` with
`div_C(h)=2D`; a function-field nonsquare without this identity does not
qualify. Parameter constants, base pullbacks, the four factor-radical classes,
and the automatic product class are kept as distinct layers until a stated
quotient removes them.

The reusable theory is:

1. character quotients of a finite abelian cover and the resulting
   quotient-Jacobian isogeny;
2. the even-subset-of-branch-points model for geometric 2-torsion on a
   hyperelliptic curve of even degree;
3. pullback and norm/pushforward on divisor classes;
4. Prym kernels of norm maps.

The current literature archive does not contain a theorem that already
computes these objects for this four-radical cover. Peschmann supplies Kummer
and residual-descent language but explicitly leaves a residual class open;
KSS supplies elliptic homogeneous-space analogies; Ono and
Halbeisen-Hungerbuhler concern the concordant elliptic family and different
special-point conditions. None retains both `T` branches and all four
individual lifts, so none is transferred as an obstruction.

Field boundary:

- over `Kbar`, every branch point is geometric and the usual branch-subset
  description of `Jac(C_S)[2]` applies;
- over `K(i)`, all eight displayed branch points split, but descent from
  `K(i)` to `K` is still required;
- over `K`, complex conjugation exchanges the two roots inside each quadratic
  orbit, so only Galois-invariant classes can be K-rational;
- no statement over `K(i)` alone is a parameter-uniform K-rational class.

## Phase 1: Character Quotient Inventory

For each nonempty `S subset {1,2,3,4}`, define

```text
chi_S(e)=product_{i in S}(-1)^(e_i),
C_S=C/ker(chi_S): y_S^2=product_{i in S}P_i,
y_S=product_{i in S}r_i.
```

The quotient map `pi_S:C->C_S` has degree eight. Write the four geometric
Galois orbits as

```text
O1={-T+2*i*A,-T-2*i*A},  O2={ T+2*i*A, T-2*i*A},
O3={-T+2*i*B,-T-2*i*B},  O4={ T+2*i*B, T-2*i*B}.
```

Each `O_i` is one size-two orbit over `K`; all points split over `K(i)`.
For `r=|S|`, `C_S` has degree-`2r` squarefree right side, branch set
`union_{i in S}O_i`, no infinity branch, and

```text
2*g(C_S)-2=2*(-2)+2*r,
g(C_S)=r-1.
```

The complete inventory is:

| `S` | degree | branch set | genus | `t -> -t` | `A<->B` plus | minus raw |
| --- | ---: | --- | ---: | --- | --- | --- |
| `1` | 2 | `O1` | 0 | `2` | `3` | `4` |
| `2` | 2 | `O2` | 0 | `1` | `4` | `3` |
| `3` | 2 | `O3` | 0 | `4` | `1` | `2` |
| `4` | 2 | `O4` | 0 | `3` | `2` | `1` |
| `12` | 4 | `O1+O2` | 1 | `12` | `34` | `34` |
| `13` | 4 | `O1+O3` | 1 | `24` | `13` | `24` |
| `14` | 4 | `O1+O4` | 1 | `23` | `23` | `14` |
| `23` | 4 | `O2+O3` | 1 | `14` | `14` | `23` |
| `24` | 4 | `O2+O4` | 1 | `13` | `24` | `13` |
| `34` | 4 | `O3+O4` | 1 | `34` | `12` | `12` |
| `123` | 6 | `O1+O2+O3` | 2 | `124` | `134` | `234` |
| `124` | 6 | `O1+O2+O4` | 2 | `123` | `234` | `134` |
| `134` | 6 | `O1+O3+O4` | 2 | `234` | `123` | `124` |
| `234` | 6 | `O2+O3+O4` | 2 | `134` | `124` | `123` |
| `1234` | 8 | `O1+O2+O3+O4` | 3 | `1234` | `1234` | `1234` |

Here `+` in the branch-set column denotes disjoint union. The permutations
behind the table are

```text
sigma_t       =(12)(34),
tau_plus      =(13)(24),
tau_minus_raw =(14)(23).
```

In the signed minus chart, swapping `A,B` also sends `T=A-B` to `-T`, which
gives `tau_minus_raw`. Returning to the physical convention `T=|A-B|` and
reordering to `A>B` supplies the compensating `t -> -t`; the net physical
permutation is `sigma_t*tau_minus_raw=tau_plus`.

The genus inventory is therefore exactly

```text
4 singleton quotients: genus 0,
6 two-factor quotients: genus 1,
4 three-factor quotients: genus 2,
1 four-factor quotient: genus 3,
6*1+4*2+1*3=17=g(C).
```

This dimension equality yields a character-decomposition isogeny, not an
identification of 2-torsion. With

```text
Phi: product_{S!=empty}Jac(C_S) -> Jac(C),  (D_S)->sum pi_S^*D_S,
Psi: Jac(C) -> product_{S!=empty}Jac(C_S),  D->(pi_{S,*}D)_S,
```

character orthogonality gives the rational identities

```text
pi_{S,*}pi_R^*=[8] when S=R and 0 when S!=R,
Psi*Phi=[8],
Phi*Psi=[8] on Jac(C),
```

because the trivial character contributes `Jac(P^1)=0`. Consequently the
isogeny kernels and image cokernels are 2-primary. These identities do not
compute those kernels on geometric or K-rational 2-torsion, so summing the
quotient 2-torsion dimensions would be invalid.

Phase 2 must determine, rather than assume:

1. `ker(Phi)` and `ker(Psi)` as geometric group schemes, Galois modules, and
   K-rational subgroups;
2. the kernel and image of all relevant `pi_S^*` and `pi_{S,*}` on 2-torsion
   and on the explicitly supported even-divisor classes;
3. the compatibility relations deciding which tuples of quotient classes
   lift to `Jac(C)(K)`;
4. which Galois-invariant branch-subset classes are already factor, base, or
   automatic-product classes;
5. whether a non-base-pullback class survives the 2-primary isogeny kernels.

## Phase 2: Quotient 2-Torsion Modules

For `S` of size `r>=2`, let `B_S=union_{i in S}O_i`. For every even subset
`E subset B_S`, put

```text
D_E=sum_{p in E}W_p-(|E|/2)*(infinity_+ + infinity_-).
```

On `C_S`,

```text
div(product_{p in E}(t-p))=2*D_E,
[D_E]=[D_(E^c)].
```

Consequently

```text
Jac(C_S)[2](Kbar)
  = {even subsets of B_S}/(E~E^c),
dim_F2=2*r-2.
```

Write `O_i={a_i,b_i}` with `a_i` the `+2*i*L` root and put
`o_i=[D_(O_i)]`. The `o_i`, `i in S`, have the one relation
`sum o_i=0`. For an ordering `S={s_1,...,s_r}`, a geometric basis is

```text
o_(s_1),...,o_(s_(r-1)),
v_j=[D_{a_(s_j),a_(s_r)}], 1<=j<r.
```

Complex conjugation swaps `a_i,b_i` simultaneously. A class is fixed when
its subset is fixed or is carried to its complement. The exact invariant
inventory is:

| `|S|` | quotient count | geometric dimension | K-fixed dimension | K-fixed basis type |
| ---: | ---: | ---: | ---: | --- |
| 2 | 6 | 2 | 2 | one `o_i` and `tau_S=[D_{a_i:i in S}]` |
| 3 | 4 | 4 | 2 | two independent whole-orbit classes |
| 4 | 1 | 6 | 4 | `o_1,o_2,o_3,tau_1234` |

The complement-twisted class `tau_S` exists for even `|S|`: conjugation
sends its chosen-one-root-per-orbit subset to the complement. For odd `|S|`,
that subset has odd cardinality and does not define a 2-torsion class.

At the prime two, invariant and anti-invariant eigenspaces do not form a
direct sum because `+1=-1` over `F_2`. The correct data are fixed subspaces
and coinvariants. Quotients exchanged by `sigma_t=(12)(34)` or physical
`tau_plus=(13)(24)` are recorded as pairs in the Phase 1 table. On the stable
genus-one quotients (`12,34` for `sigma_t`; `13,24` for `tau_plus`), the
induced double transposition acts trivially on the full two-dimensional
2-torsion. On `C_1234`, each symmetry has a four-dimensional geometric fixed
subspace, and its intersection with the K-fixed subspace has dimension three.
The raw minus-chart action is `(14)(23)`; restoring `T=|A-B|` gives the same
physical `tau_plus` convention as Phase 1.

### Exact Pullback Kernel

Let `H_S=ker(chi_S)`, the deck group of `pi_S:C->C_S`. Relative inertia is
trivial over `O_i` for `i in S` and is generated by `e_j` over `O_j` for
`j notin S`. For `i in S`,

```text
pi_S^*D_(O_i)=div_C(r_i).
```

Thus the whole-orbit space

```text
R_S=<o_i:i in S>, dim R_S=r-1,
```

lies in the pullback kernel. Conversely, a line bundle killed by pullback
defines an unramified character subcover of `C/C_S`. A character of `H_S` is
unramified exactly when it kills every omitted inertia generator `e_j`,
`j notin S`; these are precisely the `r-1` characters represented by `R_S`.
Therefore

```text
ker(pi_S^*:Jac(C_S)[2](Kbar)->Jac(C)[2](Kbar))=R_S.
```

In particular, the later ramified radical extensions introduce no additional
pullback kernel, and

| `|S|` | `dim Jac(C_S)[2]/R_S` | individual pullback-image dimension |
| ---: | ---: | ---: |
| 2 | 1 | 1 |
| 3 | 2 | 2 |
| 4 | 3 | 3 |

Complex conjugation acts trivially on each quotient `Jac(C_S)[2]/R_S`, since
`c(E)+E` is a union of whole `O_i`. Hence every individual quotient direction
pulls back to a K-rational class on `C`. This proves individual survival; it
does not prove independence between different `S`.

### Uniform Function Representatives

For any even nonempty `J subset S`, define over `K(i)(C)`

```text
E_J={a_i:i in J},
h_J=product_{i in J}(t-a_i),
r_J=product_{i in J}r_i,
s_J=r_J/h_J.
```

Then

```text
c(h_J)=h_J*s_J^2,
c(s_J)=s_J^(-1),
G_(S,J)=h_J*(1+s_J)^2=h_J+c(h_J)+2*r_J in K(C)^*.
```

Its divisor is even and its squareclass is `pi_S^*[D_(E_J)]`. Choosing
`r-1` independent even subsets `J` gives uniform explicit representatives
for the individual image of `C_S`.

A particularly simple representative comes from `S=J={1,2}`. Put

```text
z_A=r_1*r_2,
u_A=t^2-T^2-4*A^2,
H_A=z_A+u_A.
```

The scalar factor two in `G_(12,12)=2*H_A` is irrelevant to the divisor.
The exact identity

```text
(z_A+u_A)*(z_A-u_A)=16*A^2*t^2
```

shows directly that

```text
div_(C_12)(H_A)=2*(W_(0,+)-I_+),
div_C(H_A)=2*pi_12^*(W_(0,+)-I_+).
```

Here `W_(0,+)` is the midpoint point
`(t,z_A)=(0,T^2+4*A^2)`, and `I_+` is the infinity with
`z_A/t^2 -> +1`. The class is nonzero because the cross-orbit subset
`{a_1,a_2}` is outside `R_12=<o_1>`, and the exact pullback-kernel result
proves that it remains nonzero on `C`.

This already gives one concrete parameter-uniform non-base-pullback
unramified class. It is independent of base, factor, and automatic-product
classes: it is not a base function because it contains `z_A`; factor classes
are exactly the killed space `R_12`; and the automatic product is a sum of
factor classes. The formula is valid before specializing `T`, hence on both
`T=A+B` and `T=A-B` branches. Its divisor retains the midpoint and infinity;
endpoints, factor-zero points, cross-collisions, and denominator charts are
units for this divisor rather than silently removed. The arithmetic image
still must retain positive square `x`, real intervals, p=2, primitive/gcd
data, and all four individual lifts.

### Norm Boundary

The pull-push relations are

```text
pi_(S,*)pi_R^*=[8] if S=R and 0 otherwise,
pi_S^*pi_(S,*)=sum_{h in H_S}h_*.
```

Thus every pulled-back quotient 2-torsion class has zero norm to every
character quotient. These identities cannot decide cross-quotient relations,
because `[8]` vanishes on 2-torsion. The still-uncontrolled map is

```text
F: direct_sum_(|S|>=2)(Jac(C_S)[2]/R_S) -> Jac(C)[2](K),
   (x_S) -> sum pi_S^*x_S.
```

Its source has dimension `6*1+4*2+1*3=17`. No claim that `F` is injective or
that these 17 directions are independent is made. This 2-primary isogeny
kernel remains a precise blocker to a complete character-quotient census, but
it does not invalidate the individually proved class `H_A`.

## Phase 3: Radical-Linear Divisor Census

Put `d_ij=r_i-r_j` and `s_ij=r_i+r_j`. The finite multiplicative universe is

```text
U=K^*<t,t-T,t+T,l_plus,l_minus,r_1,r_2,r_3,r_4,
       d_12,s_12,d_13,s_13,d_14,s_14,
       d_23,s_23,d_24,s_24,d_34,s_34>,
l_plus=Delta+T*t, l_minus=Delta-T*t.
```

Arbitrary ratios and products of these generators are included. The
`P_i=r_i^2` factor-zero corrections are explicit square columns. Deck
transformations exchange `d_ij,s_ij` up to sign, and `t -> -t`, both A/B
actions, and Galois conjugation preserve `U`; this proves sufficiency for the
declared radical-linear/sign-split universe only.

Label the 16 K-rational infinity points by

```text
I_epsilon: r_i/t -> epsilon_i, epsilon_i in {+1,-1}.
```

At a collision, `C_ij^=` is the sum of the eight sign points with `r_i=r_j`,
and `C_ij^!=` is the complementary eight-point sum. Similarly define
`I_ij^=` and `I_ij^!=`. The three finite collision fibers are

```text
C_0:  t=0, where pairs 12 and 34 collide,
C_14: t=-Delta/T,
C_23: t= Delta/T.
```

Their specializations are

| branch | `C_14` | `C_23` |
| --- | --- | --- |
| `T=A+B` | `t=B-A` | `t=A-B` |
| `T=A-B` | `t=-(A+B)` | `t=A+B` |

Every zero and pole in the following table has multiplicity one:

| pair | `div(d_ij)` | `div(s_ij)` |
| --- | --- | --- |
| `12` | `C_0^= - I_12^!=` | `C_0^!= - I_12^=` |
| `34` | `C_0^= - I_34^!=` | `C_0^!= - I_34^=` |
| `14` | `C_14^= - I_14^!=` | `C_14^!= - I_14^=` |
| `23` | `C_23^= - I_23^!=` | `C_23^!= - I_23^=` |
| `13` | `I_13^= - I_13^!=` | `I_13^!= - I_13^=` |
| `24` | `I_24^= - I_24^!=` | `I_24^!= - I_24^=` |

There are no other finite zeros or poles. All radical-linear generators are
units at the factor-zero and endpoint fibers. The table follows from

```text
d_12*s_12=d_34*s_34=4*T*t,
d_13*s_13=d_24*s_24=4*Delta,
d_14*s_14=4*l_plus,
d_23*s_23=4*l_minus.
```

In particular,

```text
d_13/s_13=4*Delta/s_13^2,
d_24/s_24=4*Delta/s_24^2,
```

so the tempting constant-difference ratios have even divisors but vanish
after quotienting by K-constants and squares.

For the correction columns, with `F_a` the full unramified fiber and
`I=sum I_epsilon`,

```text
div(t)=F_0-I,
div(t-T)=F_T-I, div(t+T)=F_(-T)-I,
div(l_plus)=F_(-Delta/T)-I,
div(l_minus)=F_(Delta/T)-I,
div(r_i)=R_i-I,
div(P_i)=2*R_i-2*I.
```

Here `R_i` is the sum of the 16 ramification points over the two roots of
`P_i`. This retains factor-zero, midpoint, endpoints, collision, infinity,
and denominator/boundary corrections; denominator charts add no horizontal
support beyond these projective divisors.

### Parity Matrix

Use the 21 columns in the order

```text
d12,s12,d13,s13,d14,s14,d23,s23,d24,s24,d34,s34,
t,t-T,t+T,l_plus,l_minus,r1,r2,r3,r4.
```

The point rows are determined as follows:

- each factor-zero point over `P_i=0` has only column `r_i=1`;
- at `C_0^epsilon`, columns `d12/s12` and `d34/s34` select equality versus
  inequality of the corresponding signs, and `t=1`;
- at `C_14^epsilon`, `d14/s14` select equality versus inequality and
  `l_plus=1`;
- at `C_23^epsilon`, `d23/s23` select equality versus inequality and
  `l_minus=1`;
- at `F_T` only `t-T=1`, and at `F_(-T)` only `t+T=1`;
- at `I_epsilon`, for `ij=12,14,23,34`, `d_ij=1` exactly when the signs
  differ and `s_ij=1` exactly when they agree; all four columns for pairs
  `13,24` are one, as are all five base columns and all four `r_i` columns.

This is an explicit 160-by-21 point matrix: 64 factor-zero rows, 48 collision
rows, 32 endpoint rows, and 16 infinity rows. Row reduction gives

```text
rank_F2=14,
kernel_dimension=7.
```

The Controller independently reconstructed the matrix from the point rules
and obtained the same rank and kernel basis:

```text
d13*s13,
d13*d24,
d13*s24,
d12*s12*d34*s34,
d12*s12*t,
d14*s14*l_plus,
d23*s23*l_minus.
```

The first and the last four entries are constants, squares, or base-principal
relations. The two cross-pair representatives have the same relative class,
because

```text
(d13*s24)/(d13*d24)=s24/d24=4*Delta/d24^2.
```

Therefore the declared radical-linear candidate quotient has exact dimension
one, represented by

```text
H_RL=(r_1-r_3)*(r_2-r_4).
```

Its exact divisor is

```text
div(H_RL)
 =2*sum_(epsilon_1=epsilon_3, epsilon_2=epsilon_4) I_epsilon
 -2*sum_(epsilon_1!=epsilon_3, epsilon_2!=epsilon_4) I_epsilon.
```

Thus it has four double zeros and four double poles, all at infinity. It is
not a constant/base pullback times a square, even over algebraically closed
constants. Indeed the deck involution `sigma=e_1*e_3` sends `H_RL` to
`-H_RL`. If `H_RL=c*f(t)*g^2`, then `(sigma(g)/g)^2=-1`; hence
`sigma(g)/g=+/-i`, but applying `sigma` twice gives `-1=1`, a contradiction.
The unique factor-zero rows also show that multiplying by factor-radical
columns cannot remove this class, while the wl595 product is already the
square `(r_1*r_2*r_3*r_4)^2`.

The class is fixed up to constants and squares by the deck group,
`t -> -t`, plus-branch A/B exchange, and raw or physical minus-branch A/B
exchange. Its norm squareclass to every character quotient is trivial: every
deck conjugate differs from it by a K-constant times a square, and a norm over
an eight-element `H_S` multiplies eight such copies. No claim that it is the
pullback of one particular `C_S` is needed or made.

## Phase 4: Candidate Acceptance

The Controller accepts outcome A:

```text
accepted_outcome=non_base_pullback_candidate_ready
```

Two independently explicit presentations are available:

1. `H_A=z_A+t^2-T^2-4*A^2`, pulled back from `C_12`, with
   `div_C(H_A)=2*pi_12^*(W_(0,+)-I_+)` and exact pullback-kernel proof;
2. `H_RL=(r_1-r_3)*(r_2-r_4)`, the unique nonzero class in the exact
   21-generator radical-linear quotient, with the infinity divisor above.

Both are defined over `K=Q(A,B)` before substituting `T=A+B` or `T=A-B`, so
they are uniform on both physical branches. Both are nonzero modulo squares,
K-constants, base pullbacks, the factor-radical space, and the automatic
product class. The first has controlled pullback from `C_12` and zero norm to
every character quotient; the second has trivial relative norm squareclass
to every quotient and is not asserted to come from one quotient.

The exact survivor count in the declared radical-linear space is one symmetry
class, represented by `H_RL`. The character-quotient source contains 17
labeled individual pullback directions after quotienting each `R_S`, but the
cross-quotient map `F` is still not controlled, so no claim is made that those
directions are mutually independent or distinct from `H_RL`. Outcome A needs
only the rigorously nonzero explicit class, not that unresolved dimension.

The individual AA/BB and complete four-factor lifts are retained because the
classes live on `C` itself. The real intervals, positive square `x=t^2`, p=2,
primitive/gcd and denominator conditions, midpoint, endpoints, collisions,
factor-zero and infinity charts remain mandatory in any later arithmetic
audit. No local or global obstruction has been attempted here.

The exact next task, if separately authorized, is a local/global
descent-design audit for `H_RL` (or the equivalent selected character class)
that preserves all retained branches and lifts. Stop here because outcome A
has been accepted.

```text
later_descent_design_audit_authorized=true
automatic_execution_authorized=false
```

## Theorem Boundary

No family obstruction, Selmer bound, rank theorem, Harborth theorem, D2, D5,
M3, local-image classification, reciprocity argument, or `wl596` has been
proved or authorized by this audit.
