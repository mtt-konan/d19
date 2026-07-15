# Q1 Fake 2-Descent Object Hierarchy

## Selected Curve

For the selected pilot

~~~text
C_1: v^2=g6(t),  K=Q(i),  deg(g6)=6,
L=K[theta]/(g6(theta)),
~~~

the exact fake divisor-evaluation quotient is

~~~text
F_L = L^*/(L^{*2} K^*)
    = (L^*/L^{*2}) / im(K^*/K^{*2} -> L^*/L^{*2}).
~~~

The quotient by constants and the norm-square condition are different
operations. Q1 defines both operations and keeps them as separate objects.

## Ambient S-Unit Coordinates

Let S_L be the conservative support above 2 and 37397, and let
U_{L,S} be the S-unit group. The segmented class/unit/S-unit certificate
supplies

~~~text
U_{L,S} ~= C4 x Z^15.
~~~

Define the supported ambient squareclass space

~~~text
V_S = image(U_{L,S}/U_{L,S}^2 -> L^*/L^{*2}).
~~~

With the fixed basis

~~~text
zeta4, epsilon_1,...,epsilon_5, S_prime_1,...,S_prime_10,
~~~

this gives an ambient coordinate identification

~~~text
phi_S: F_2^16 -> V_S.
~~~

The number 16 is therefore only the dimension of the conservative ambient
S-unit coordinate space. It is not the dimension of F_L, not the dimension
of V_S/C_S, not the dimension of a norm kernel, and not a Selmer result.
The ambient space is a supported candidate container; no claim is made here
that its quotient or any local condition has been computed.

## Exact Constant Quotient

Let the constant subspace inside the ambient space be

~~~text
C_S = V_S intersect im(K^*/K^{*2} -> L^*/L^{*2}).
~~~

The supported image of the exact fake target is then

~~~text
F_{L,S} = V_S/C_S,
q_S: V_S -> F_{L,S}.
~~~

It injects into F_L. This definition uses the intersection with the full
constant image; it does not infer C_S from the sixteen basis labels. The
class [i]=[zeta4] is a known constant class in C_S, but the coordinate
matrix and rank of C_S have not been computed.

In particular, the exact target is not replaced by the ambient space:

~~~text
V_S  -- quotient by C_S -->  F_{L,S}  -->  F_L.
~~~

No dimension for F_L or F_{L,S} is claimed.

## Norm-Square Kernel

Because [L:K]=6 is even, the norm descends through the constant quotient:

~~~text
barN_L: F_L -> K^*/K^{*2},
barN_L([alpha]) = [N_{L/K}(alpha)].
~~~

This is well-defined: multiplying alpha by a square changes the norm by a
square, while multiplying it by k in K^* changes the norm by k^6, also a
square in K^*/K^{*2}.

The norm-square subspace is a separate object:

~~~text
K_L^N = ker(barN_L: F_L -> K^*/K^{*2}),
V_S^N = {v in V_S: N_{L/K}(alpha_v) in K^{*2}},
K_{L,S}^N = q_S(V_S^N) = F_{L,S} intersect K_L^N.
~~~

The global norm matrix still missing from the ambient coordinates is

~~~text
M_norm: F_2^16 -> K^*/K^{*2},
M_norm(e_j) = [N_{L/K}(alpha_j)],
~~~

where alpha_j is the fixed S-unit lift of the j-th ambient basis vector.
No rank or kernel dimension for this matrix is asserted.

## Even-Degree Infinity Kernel

The smooth even-degree projective model has two K-rational points at
infinity, P_+ and P_-. Over L, for the branch point W_theta above a
root theta,

~~~text
div(t-theta) = 2*W_theta - P_+ - P_-.
~~~

Thus the image of

~~~text
D_inf = [P_+ - P_-] in J(K)/2J(K)
~~~

lies in the kernel of the even-degree fake divisor-evaluation map. This is a
kernel inclusion only. It does not assert that D_inf is nonzero in
J(K)/2J(K), that it is nonzero torsion in J(K), or that it generates the
full fake-map kernel.

The standard infinity evaluation is the leading-coefficient class. Here the
leading coefficient is 1, so

~~~text
delta_fake(D_inf) = [1] = 0 in F_L.
~~~

The zero vector

~~~text
(0,...,0) in F_2^16
~~~

is only the ambient coordinate vector of the representative [1] in V_S.
It is not a coordinate vector for the fake target F_L.

## Local Fake Quotient at pi

For

~~~text
pi = (94*i-169),  K_pi = completion(K, pi),
A_pi = L tensor_K K_pi = K_pi[t]/(g6(t)),
~~~

the local fake quotient is

~~~text
F_pi = A_pi^*/(A_pi^{*2} K_pi^*).
~~~

Its norm map and norm-square kernel are

~~~text
barN_pi: F_pi -> K_pi^*/K_pi^{*2},
barN_pi([alpha]) = [N_{A_pi/K_pi}(alpha)],
H_pi = ker(barN_pi).
~~~

The local fake image is the separate object

~~~text
I_pi = delta_pi(J(K_pi)/2J(K_pi)) subset H_pi.
~~~

The accepted local quotient target is

~~~text
dim_F2 J(K_pi)/2J(K_pi) = 2,
~~~

but this does not compute F_pi, H_pi, or I_pi, and it does not imply
dim_F2(I_pi)=2. No local basis, local generator, tangent normalization, or
local evaluation class is supplied by Q1.

## Global-to-Local Localization

The completion map L -> A_pi induces the exact localization map

~~~text
loc_pi^fake: F_L -> F_pi,
loc_pi^fake([alpha]) = [alpha tensor 1].
~~~

On the ambient coordinates its supported form is

~~~text
Lambda_pi,S = loc_pi^fake o q_S o phi_S:
                F_2^16 -> F_pi.
~~~

Norm compatibility is

~~~text
barN_pi(Lambda_pi,S(v))
  = loc_pi^K(barN_L(q_S(phi_S(v))))
~~~

so the supported global norm-square kernel maps into H_pi. This defines the
map; it does not provide its matrix. The localization matrix still missing
for Q2 is

~~~text
M_loc_pi(e_j) = loc_pi^fake(q_S(phi_S(e_j))).
~~~

No local coordinate basis is chosen, so no local generators are invented.

## Q2 Missing Data

The strict Q2 arithmetic inputs still missing are:

1. M_const: the coordinate image of global constants inside V_S, needed to
   form the quotient V_S/C_S in the fixed ambient coordinates.
2. M_norm: the global norm matrix from the sixteen ambient columns to
   K^*/K^{*2}, needed to identify the supported norm-square kernel.
3. M_loc_pi: the localization columns at pi, expressed in a certified
   local fake quotient (or equivalent certified global lifts of independent
   local classes).

The local quotient and its norm kernel are defined abstractly above, but no
local basis or local norm-coordinate matrix is supplied. The Q2 report must
still provide tangent-normalized branch evaluations, complete local image
coverage, and the comparison with these global maps.

## Strict Proof Boundary

This Q1 correction proves the object hierarchy and exact formulas only. It
does not compute a norm matrix, a constant-quotient rank, a localization
matrix, a local Kummer image, a fake Selmer group, a true Selmer group, a rank
bound, saturation, rational t-values, or Berry-point reconstruction. It does
not modify or reopen Q2, and it makes no claim about any other Berry sextic.

Focused validation:

~~~text
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q tests/test_berry_sextic_q1.py -n 1
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run ruff check scripts/theory/berry_sextic_q1.py tests/test_berry_sextic_q1.py
git diff --check
~~~
