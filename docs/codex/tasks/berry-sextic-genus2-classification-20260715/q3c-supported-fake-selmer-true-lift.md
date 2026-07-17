# Berry C_1 Q3c Supported Fake Selmer And True Lift

## Outcome

`q3c_exact_supported_fake_selmer_true_lift_with_universal_boundary_lemma`

The frozen Q3b dyadic map is injective on the supported quotient.  Exact
inversion gives the two intersection classes, and the outside-support theorem
shows that the supported fake 2-Selmer group is:

```text
Sel_fake^S = span_F2 {
  [epsilon_1*epsilon_2*epsilon_4],
  [epsilon_2*epsilon_4]
}
```

The rejected draft is repaired by the universal divisor-evaluation/Kummer
lemma proved below.  The fake-to-true comparison is an exact sequence, not a
dimension heuristic:

```text
0 -> F_2<kappa(D_inf)> -> Sel_2(J/K) -> Sel_fake^S -> 0.
```

Here `Sel_fake^S` means the exact fake target with square norm, local fake
image membership at every finite place in `S_0`, and the unramified local
condition outside `S_0`; it is not the ambient sixteen-dimensional S-unit
space.

The first term is the global/local infinity kernel.  Its nonzero global class
is proved by the frozen local nondivisibility certificate at `varpi`.  The
sequence gives

```text
dim_F2 Sel_2(J/K) = 3,
```

This is a Selmer statement only; it is not a rank, saturation, rational-`t`,
or point-classification result.

The allowed support is

```text
S_0={1+i, 94*i-169}.
```

This is support language, not a claim that both places are bad.  Reduction at
`1+i` remains unresolved; bad reduction at `94*i-169` is proved; every finite
place outside `S_0` is proved good.  The conjugate place `-94*i-169` is good
and is not an additional Selmer place.

## Exact Pullback

Use the frozen Q3b quotient basis

```text
q_1=[epsilon_1],
q_2=[epsilon_2],
q_3=[epsilon_3],
q_4=[epsilon_4],
q_5=[S_prime_5+S_prime_6],
q_6=[S_prime_5+S_prime_8].
```

The Q3b dyadic map is injective on these six quotient coordinates.  Solving
the two exact eight-coordinate equations gives

```text
01111000 <- 110100 = q_1+q_2+q_4,
01100010 <- 010100 = q_2+q_4.
```

Therefore exact ambient representatives modulo `C_S` are

```text
f_1 = epsilon_1*epsilon_2*epsilon_4
    = 0110100000000000,
f_2 = epsilon_2*epsilon_4
    = 0010100000000000.
```

The ambient coordinate order is

```text
zeta4, epsilon_1,...,epsilon_5, S_prime_1,...,S_prime_10.
```

The constants have rank `4`, and adjoining the two representatives gives
rank `6`, so the two classes are independent modulo `C_S`.  Their odd local
coordinates are in the complete image `I_pi`, and their dyadic coordinates
are the two displayed vectors in the complete `I_varpi`.  Since the Q3b
dyadic quotient kernel is zero, no other quotient representative can map to
either displayed local class.

The equivalent basis is

```text
Sel_fake^S = span_F2 { [epsilon_1], [epsilon_2*epsilon_4] }.
```

## Outside-S Support Theorem

Let

```text
K=Q(i),
L=K[theta]/(g6(theta)),
S_0={1+i, 94*i-169} in Spec(O_K).
```

The exact reduction certificate proves good reduction at every finite place
outside `S_0`.  It does not classify the reduction at `1+i`; that place is
retained in `S_0` as an allowed support place.  Bad reduction at
`94*i-169` is proved.  The conservative Q2b ambient support also includes
`-94*i-169`, but this conjugate place is good for `C_1` and is not an extra
Selmer place.

For a finite `v` outside `S_0`, write `O_v` for the valuation ring and
`A_v=O_L tensor O_v`.  The good-reduction and discriminant checks give:

```text
2 is a unit in O_v,
A_v/O_v is finite etale,
J[2], R=Res_(L/K)(mu_2), and Q=R/mu_2 extend over O_v.
```

The integral cohomology diagram has `Br(O_v)[2]=0`.  Since the residue field
is finite, Lang's theorem gives `H^1(O_v,J)=0`, so

```text
J(K_v)/2J(K_v) = image(H^1(O_v,J[2]) -> H^1(K_v,J[2]))
```

and the local fake evaluation of a Kummer class is represented by a unit of
`A_v`.  In particular, its valuations at all primes of `L` above `v` are
even after the common base-constant quotient.

Conversely, a norm-square fake class represented by an `A_v`-unit is in the
unramified kernel and lifts through the integral sequences to the local
Kummer image.  Thus the outside-`S_0` condition is exactly the even-valuation
condition after constants; it is not an assumption that only `pi` and
`varpi` matter.

For a global true Selmer class, the parity outside `S_0` is a pullback of a
parity divisor on `K`.  Because `K=Q(i)` is a PID, multiply by one global
constant to remove that common parity.  The exact class-group certificate
`Cl(L)=1` then removes the remaining even ideal.  The fake class has a
representative in the six-prime `S_0`-unit group.  This proves the support
reduction from the conservative ten-prime Q2b container.

The two surviving representatives `f_1,f_2` are products of global units.
They are therefore units at every good place, including `-94*i-169`; their
global norm-square rows already vanish.  The integral diagram proves their
outside-`S_0` local conditions.  Together with the exact `pi` and `varpi`
conditions above, this proves

```text
Sel_fake^S = W_supported intersect I_varpi
```

with dimension `2`.

## Universal Divisor-Evaluation Lemma

Let `F` be any field of characteristic different from `2`, let `g` be monic
and squarefree of degree `2m`, and let

```text
C: y^2=g(t),
A=F[theta]/(g),
x=1/t, z=y/t^m,
P_+=(x=0,z=+1), P_-=(x=0,z=-1),
D_inf=[P_+-P_-].
```

Put `R=Res_(A/F)(mu_2)` and `Q=R/mu_2`, with the quotient by the diagonal
copy of `mu_2`.  There is an exact sequence of finite etale group schemes

```text
1 -> J[2] --iota--> Q --N--> mu_2 -> 1.
```

The fake divisor evaluation and Kummer map fit into the functorial square

```text
J(F)/2J(F) --kappa_F--> H^1(F,J[2])
     | delta_F                 | iota_*
     v                         v
A^*/(A^{*2}F^*) ----j_F----> H^1(F,Q).
```

The bottom arrow is injective, but it is not asserted to be surjective.  Its
cokernel is controlled by the separate Brauer term in
`1 -> mu_2 -> R -> Q -> 1`.

The two exact sequences are compatible: on a fake representative `alpha` the
map `H^1(F,Q) -> H^1(F,mu_2)` sends `j_F([alpha])` to
`[N_{A/F}(alpha)]`.  This follows directly by choosing square roots of the
coordinates of `alpha` in `A tensor Fbar` and multiplying the resulting sign
cocycle.  Thus a fake class has a cohomological lift through `J[2]` exactly
when its norm is a square.

### Geometric exact sequence and signs

Over `Fbar`, let `Omega` be the roots of `g`, and write `W_alpha` for the
branch point over `alpha`.  For an even subset `S` of `Omega`, set

```text
D_S = [sum_(alpha in S) W_alpha - (|S|/2)(P_+ + P_-)] in J[2],
e_S(alpha) = -1 if alpha in S, +1 otherwise.
```

The map `iota` sends `D_S` to the class of `e_S` in
`{+1,-1}^Omega/{diagonal}`.  This is well-defined because

```text
div(t-alpha)=2W_alpha-P_+-P_-,
div(y)=sum_alpha W_alpha-m(P_++P_-).
```

The second identity identifies `S` and its complement, exactly as the
diagonal sign does.  The norm of `e_S` is `(-1)^|S|`, so its kernel is exactly
the even subsets modulo complements.  This proves exactness and fixes the
sign convention.

### Ordinary finite divisors and the commutative square

For a finite divisor `D` disjoint from the branch points, define

```text
ev(D)_alpha = (t-alpha)(D).
```

If `h` is a rational function, Weil reciprocity and the displayed divisor give

```text
(t-alpha)(div(h))
  = h(div(t-alpha))
  = h(W_alpha)^2/(h(P_+)h(P_-)).
```

The denominator is independent of `alpha`, so `ev(D)` is unchanged in
`A^*/(A^{*2}F^*)` by changing a divisor representative by a principal
divisor.  This defines `delta_F` and descends under the Galois action.

For the cocycle calculation, choose over `Fbar` a divisor `E` and a function
`h` with

```text
div(h)=2E-D.
```

Choose `s` with `s^2=h(P_+)h(P_-)`.  Weil reciprocity gives, for every root,

```text
ev(D)_alpha
 = ( (t-alpha)(E) * s/h(W_alpha) )^2.
```

The resulting square-root vector has Galois sign cocycle equal, modulo its
common diagonal factor, to the sign-vector image under `iota` of the Kummer
cocycle `sigma(E)-E`.  Thus

```text
j_F(delta_F([D])) = iota_*(kappa_F([D])).
```

Changing `E`, `h`, or the divisor representative changes the square root by
an `A`-square or a diagonal `Fbar`-constant, so the cohomology class is
unchanged.  This is the cocycle proof of the square, not an identification of
`H^1(F,Q)` with the fake quotient.  A divisor class is first represented after
a finite separable extension and the resulting equality is Galois invariant,
so the same argument applies to every point of `J(F)/2J(F)`.

### Branch and factor-zero normalization

Let `g=h*k` with `h` monic of degree `r`, and use the even branch divisor

```text
D_h=sum_(h(alpha)=0) W_alpha-(r/2)(P_++P_-).
```

At a root `alpha` of `h`, use the branch parameter `z=y`.  The self-factor
contributes `1/g'(alpha)`, while the other `r-1` roots contribute
`prod_(beta != alpha)(beta-alpha)=(-1)^(r-1)h'(alpha)`.  Since

```text
(t-alpha)/z^2 -> 1/g'(alpha),
h'(alpha)/g'(alpha) = 1/k(alpha),
```

the tangent-normalized evaluation is therefore

```text
beta_h|_{F[theta]/(h)} = (-1)^(r-1)*k(theta)^(-1),
beta_h|_{F[theta]/(k)} = h(theta).
```

This replaces the zero value `h(theta)=0` at a factor-zero component by the
signed unit tangent value `(-1)^(r-1)k(theta)^(-1)`.  It is the limit of the
ordinary divisor formula, so it covers all branch fibers and repeated finite support.  For the
degree-two branch divisors used at `pi`,

```text
N_{A/F}(beta_h)
 = (-1)^(r(r-1))*Res(k,h)/Res(h,k)
 = (-1)^(2(2m-2)) = 1.
```

For the selected base `K=Q(i)`, `-1=i^2`, so the corrected degree-two sign is
also square locally and globally.  It is nevertheless retained in the
universal statement; no real-field sign is discarded.

### Both infinity charts

In either infinity chart,

```text
t-alpha = x^(-1)(1-alpha*x),
x(t-alpha) -> 1,
x^d h(1/x) -> 1
```

for `h` monic of degree `d`.  Thus a finite point `Q` has the normalized
evaluation

```text
delta_F([Q-P_+]) = [1-x(Q)*theta],
delta_F([Q-P_-]) = [1-x(Q)*theta],
```

and both infinity points contribute the same leading value `1`.  In
particular `delta_F(D_inf)=[1]`.  No infinity sign is lost, and no factor-zero
formula divides by a vanishing factor.

### The boundary cocycle

Fix one root `alpha_0` over `Fbar`.  Let `q` be the class in `Q(Fbar)` of the
sign vector with `-1` at `alpha_0` and `+1` at all other roots.  Then

```text
N(q)=-1.
```

With the connecting-map convention
`partial_F(-1)_sigma=sigma(q)q^(-1)`, this cocycle has `-1` at
`alpha_0` and `sigma(alpha_0)`.  Under `iota` it is the class of

```text
W_alpha0 + W_sigma(alpha0) - P_+ - P_-.
```

Put `E_alpha0=[P_+-W_alpha0]`.  The root divisor identity gives

```text
2E_alpha0-D_inf = -div(t-alpha_0),
```

so `E_alpha0` is a half of `D_inf`.  Its Kummer cocycle is

```text
sigma(E_alpha0)-E_alpha0 = W_alpha0-W_sigma(alpha0).
```

The difference between this divisor and the boundary divisor is

```text
2W_sigma(alpha0)-P_+-P_- = div(t-sigma(alpha0)),
```

so the two cocycles are equal in `J[2]`.  Therefore, with no unspecified
scalar or sign,

```text
partial_F(-1) = kappa_F(D_inf).
```

All formulas are defined over `F` and were checked after extension to `Fbar`.
They commute with every field extension and, in particular, with every
completion of a number field.

## Infinity And Exceptional Branches

The curve is even degree with two `K`-rational infinity points `P_+`,`P_-`.
For every root `theta` of `g6`,

```text
div(t-theta)=2*W_theta-P_+-P_-.
```

The leading coefficient is `1`, so the infinity difference
`D_inf=[P_+-P_-]` has fake class `[1]=0`.  At a good finite place the monic
infinity chart is integral and contributes no extra squareclass.  At a branch
or factor-zero fiber, the evaluation uses the tangent normalization

```text
beta_h|_h = -(g6/h)(theta)^(-1),
beta_h|_(g6/h) = h(theta),
```

as in the accepted `pi` certificate.  The Q3b quadratic points have
`t_1 != 0` and `g6(t) != 0`, so they are not hidden branch or infinity cases.
The Q3a3 halving audit treats the degree-zero, degree-one, degree-two,
factor-zero, and both infinity branches explicitly.  No exceptional chart is
discarded in the pullback or support argument.

There is one complex place of `K`, where there is no additional Selmer
condition.

## Fake Versus True Cohomology

Keep the separate exact sequence

```text
1 -> mu_2 -> R -> Q -> 1.
```

Its cohomology gives an injection

```text
F_L=L^*/(L^{*2}K^*) -> H^1(K,Q)
  -> Br(K)[2] -> Br(L)[2].
```

The possible cokernel is

```text
B_K=ker(Br(K)[2] -> Br(L)[2]),
```

and is not another infinity kernel.  If `c` is a global true Selmer class,
its local images are local Kummer classes.  The universal square identifies
their images in `H^1(K_v,Q)` with the fake injection, so the associated class
in `B_K` is zero at every place.  Brauer-Hasse-Noether then gives zero
globally, and `c` has a well-defined global fake image.  Exactness of
`J[2] -> Q -> mu_2` makes its norm square.

Conversely, let `f` be in `Sel_fake^S`.  Its image in `H^1(K,Q)` has trivial
image in `H^1(K,mu_2)` because its norm is a square.  Exactness therefore
gives a global cohomological lift `c` in `H^1(K,J[2])`.  At every place `v`,
choose a local Kummer class `k_v` with fake image `f_v`; this is possible by
the local definition of `Sel_fake^S`.  Then

```text
c_v-k_v in ker(H^1(K_v,J[2]) -> H^1(K_v,Q))
       = image(partial_v).
```

The universal boundary identity gives

```text
image(partial_v) = {0,kappa_v(D_inf)}
                    subset kappa_v(J(K_v)/2J(K_v)).
```

Thus every global cohomological lift of every fake class in `Sel_fake^S` is
locally Kummer.  The map to `Sel_fake^S` is surjective.

## Exact Global Kernel

The relevant long exact segment is

```text
Q(K) -> mu_2(K) --partial_K--> H^1(K,J[2]) -> H^1(K,Q).
```

At `varpi`, the frozen Q3a2/Q3a3 certificate gives injective constant
restriction and local relative factor degrees `2` and `4`.  Hence the local
norm of every local `Q(K_varpi)` point is `+1`.  Since global points map to
local points,

```text
Norm(Q(K)) subset Norm(Q(K_varpi)) = {+1}.
```

The reverse inclusion is the identity, so `Norm(Q(K))={+1}`.  This argument
does not assert the false implication `Q(K)=R(K)/mu_2(K)` globally; only the
norm image is needed.

The exact Q3a3 divisibility certificate proves

```text
D_inf not in 2J(K_varpi).
```

Therefore `kappa_K(D_inf)` is nonzero: a global halving would remain a
halving after completion.  The universal boundary lemma identifies it with
`partial_K(-1)`.  Since `mu_2(K)={+1,-1}` and the norm image is trivial, the
global kernel is exactly

```text
ker(Sel_2(J/K) -> Sel_fake^S)
 = F_2<kappa_K(D_inf)>.
```

Combining this with `dim_F2 Sel_fake^S=2` proves the displayed short exact
sequence and `dim_F2 Sel_2(J/K)=3`.

## Artifacts And Validation

The repaired verifier and focused test are:

```text
scripts/theory/berry_sextic_q3c_fake_selmer.py
tests/test_berry_sextic_q3c_fake_selmer.py
```

The verifier labels the universal theorem `status=proved_lemma` and checks
its finite polynomial, divisor, tangent, reciprocal-chart, resultant, and
sign-cocycle identities exactly.  It composes the frozen Q2/Q3a/Q3b
certificates for the finite input.  These executable checks are evidence for
the recorded algebraic identities; they are not a claim that Python has
mechanized Galois cohomology.

Validation:

```text
python3 scripts/theory/berry_sextic_q3c_fake_selmer.py
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q \
  tests/test_berry_sextic_q3c_fake_selmer.py -n 1
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check \
  scripts/theory/berry_sextic_q3c_fake_selmer.py \
  tests/test_berry_sextic_q3c_fake_selmer.py
git diff --check
```
