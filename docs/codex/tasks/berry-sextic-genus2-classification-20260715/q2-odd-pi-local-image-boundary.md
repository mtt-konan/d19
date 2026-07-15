# Q2 Odd-prime Local-image Boundary at pi

## Outcome

`precise_q2_missing_coordinate_certificate`

This retry does not certify the local Kummer image. The certified inputs prove
the local factor-orbit pattern and the strict dimension target 2, but they do
not emit the local evaluation classes or a local-to-global comparison map.
No 16-coordinate vectors are therefore stated.

The missing data is Q2-specific, not a Magma timeout and not a global
Selmer/rank conclusion.

## Frozen Input

Let

```text
K = Q(i),     pi = (94*i - 169),     p = Norm(pi) = 37397,
K_pi = completion(K, pi),            k = F_p.
```

The residue map is `i -> 1991`, since `94*1991 = 169 mod 37397`. The selected
curve is `C_1: v^2 = g6(t)`. The accepted strict target is

```text
dim_F2 J(K_pi)/2 J(K_pi) = 2.
```

The fixed conservative global fake squareclass order is

```text
zeta4, epsilon_1,...,epsilon_5, S_prime_1,...,S_prime_10,
```

so its dimension is 16. This is the Q1 target

```text
L^*/L^{*2} K^*,  L = K[theta]/(g6(theta)),
```

and is not itself the local quotient `J(K_pi)/2J(K_pi)`.

## Exact Local Quotient

Put

```text
A_pi = K_pi[t]/(g6(t)).
```

For the local fake divisor-evaluation map, the relevant squareclass object is

```text
H_pi = {
  [alpha] in A_pi^*/(A_pi^{*2} K_pi^*) :
  Norm(alpha) is in K_pi^{*2}
}.
```

The diagonal `K_pi^*` quotient is harmless for the norm condition because
`deg(g6)=6` is even. For a degree-zero divisor represented away from the
branch and infinity fibers, the usual evaluation is

```text
delta_pi(D) = [ product (t(P)-theta)^(multiplicity at P) ] in H_pi,
```

with the standard extension over branch and infinity fibers. The local fake
image is `I_pi = delta_pi(J(K_pi))`.

There are two distinct dimensions here:

```text
dim_F2 J(K_pi)/2J(K_pi) = 2       (accepted target),
dim_F2 I_pi <= 2                   (not computed).
```

Q1 records that the even-degree infinity difference `D_inf=[P_+-P_-]` is in
the kernel of the fake evaluation map when the leading coefficient is 1.
The target dimension 2 alone therefore does not prove that the fake image has
dimension 2. A Q2 certificate must either prove that the relevant kernel is
zero locally or compute the image directly.

## Certified Reduction Data

The exact reduction supplied by the B0 certificate is

```text
g6(t) = (t - 11745)^2 (t + 3615) (t + 9390)
       (t^2 + 6501*t + 25179)       mod pi.
```

Equivalently, if `F_1,F_2,F_r,F_u` denote the monic Hensel factors over
`K_pi`, their certified reductions and degrees are

```text
F_1  = t + 3615,                  degree 1,
F_2  = t + 9390,                  degree 1,
F_r  = (t + 25652)^2,             degree 2, ramified branch,
F_u  = t^2 + 6501*t + 25179,      degree 2, residue degree 2.
```

Here `-25652 = 11745 mod 37397`. The discriminant of the displayed
quadratic is `15866 mod 37397`, whose Legendre symbol is `-1`, so the four
local Galois orbits have sizes `1,1,2,2`. The certified local algebra has the
form

```text
A_pi ~= K_pi x K_pi x E_r x E_u,
```

where `E_r/K_pi` is ramified quadratic and `E_u/K_pi` is unramified
quadratic.

The invariant even-subset calculation is exact. With one F_2 bit for each
of the four orbits, even cardinality imposes `e_1 + e_2 = 0`; quotienting by
the all-branch relation removes one more dimension. Thus

```text
4 - 1 - 1 = 2.
```

This recovers the accepted `J(K_pi)[2]` dimension. It is a branch-orbit
calculation, not a calculation of the fake evaluation coordinates.

## Exact Coordinate Parametrization Available

The local branch-orbit divisor classes can be named without guessing
coefficients. Let `D_12` be the invariant branch divisor for the two linear
orbits, and let `D_r` and `D_u` be the divisor classes for the two quadratic
orbits. The only coordinate-free candidates are

```text
beta_12 = delta_pi(D_12),
beta_r  = delta_pi(D_r),
beta_u  = delta_pi(D_u),
```

with the single all-branch relation. Any two independent classes among these
are the only possible two-generator parametrization of the local branch
quotient. This names the candidates, but it is not an explicit squareclass
calculation and it is not a 16-coordinate vector certificate.

The tempting replacement `beta_r=[F_r(theta)]` is not valid: after local
factorization, `F_r(theta)` has a zero component in the `E_r` factor of
`A_pi`, so it is not an element of `A_pi^*`. A valid branch evaluation needs a
limiting/tangent normalization, or an equivalent divisor representative whose
support avoids the branch fibers. That normalization is not in the certified
inputs.

A fixed global vector would require a global lift `beta_tilde in L^*` together with

```text
loc_pi(beta_tilde) = beta in H_pi,
coordinates_S(beta_tilde) in F_2^16.
```

No such lift or equality is present in the certified files.

## Why Completeness Cannot Be Closed

The existing local Magma source only constructs the completion, prints
`Factorization(local_g6)`, and prints target dimensions. Its own header says
that the target lines are theorem inputs, not computed local images. The Sage
source independently checks only the degree pattern `[1,1,2,2]` and does not
evaluate divisors.

The segmented S-unit certificate emits a global power-basis description of
units and support generators. It does not emit any of the following:

1. the coefficient vectors of the four local factors `F_1,F_2,F_r,F_u` in a
   fixed pi-adic precision;
2. the limiting/tangent evaluations of `D_12`, `D_r`, and `D_u` in a fixed
   basis of `H_pi`;
3. the localization matrix from the 16 global basis classes to `H_pi`, or
   global S-unit lifts for two independent local classes;
4. a proof that the infinity kernel `D_inf` is zero in
   `J(K_pi)/2J(K_pi)`, or an equivalent direct proof that two displayed fake
   classes are independent;
5. the divisor/Mumford reduction table needed to show that every finite
   affine neighborhood, the ramified double-root neighborhood, factor-zero
   fibers, and the reciprocal infinity chart reduce to the claimed two
   classes.

The reduction factorization identifies the strata, but it does not supply
their evaluation squareclasses. A dimension count can prove completeness only
after two independent local classes have been certified in the same quotient.
The missing localization and infinity-kernel data cannot be recovered from
the 16 basis labels or from the factor degrees without new computation.

## Focused Boundary Check

`q2_odd_pi_boundary.py` is a pure-Python check of only the exact facts that
are available here: the mod-p factorization, irreducibility of the quadratic
residue factor, the orbit dimension 2, and the fixed global coordinate count
16. It intentionally asserts the boundary status and does not claim a local
image.

Run:

```text
python3 docs/codex/tasks/berry-sextic-genus2-classification-20260715/q2_odd_pi_boundary.py
```

Expected status:

```text
status=precise_q2_missing_coordinate_certificate
mod_pi_factorization=ok
orbit_dimension=2
global_coordinate_dimension=16
```

No Sage, Magma, broad search, field computation, Selmer result, rank result,
or global conclusion is used or claimed.
