# Q2a Local Kummer Generators at pi

## Outcome

This report constructs two explicit classes in the local Kummer image at

```text
pi = (94*i - 169),  p = Norm(pi) = 37397,  F = K_pi.
```

The classes are the tangent-normalized divisor evaluations of the two
F-rational branch divisors

```text
D_12 = B_12 - P_+ - P_-,
D_r  = B_r  - P_+ - P_-.
```

They are independent in the local fake quotient. Since the accepted local
target has

```text
dim_F2 J(F)/2J(F) = 2,
```

they form a basis of the local fake image `I_pi`. This is a local Q2a
certificate only. It does not compute the global 16-coordinate localization
map, a fake Selmer group, a true Selmer group, a rank, or a global point set.

## Local Algebra

Write the certified monic local factors as

```text
f = F_1 F_2 F_r F_u,
F_1 = t + 3615,
F_2 = t + 9390,
F_r mod pi = (t + 25652)^2,
F_u mod pi = t^2 + 6501*t + 25179.
```

The exact factor degrees are `(1,1,2,2)`, with `F_r` ramified quadratic and
`F_u` unramified quadratic. Thus

```text
A_pi = F[t]/(f) ~= F x F x E_r x E_u,
```

where `E_r=F[t]/(F_r)` and `E_u=F[t]/(F_u)`. Let `theta` denote the image of
`t` in the relevant factor.

The residue field is `k=F_p`, and `i` reduces to `1991`. Since
`p=37397 = 5 mod 8`, set

```text
nu = 2,
```

which is a nonsquare unit in `F`. For the ramified factor, choose the
ramified squareclass representative `d_r` in

```text
{pi, 2*pi} modulo F^{*2}
```

that equals the squareclass of `Disc(F_r)`, choose `rho` in `E_r` with
`rho^2=d_r`, and set

```text
varpi = Norm_{E_r/F}(rho) = -d_r.
```

Then `rho` is a uniformizer of `E_r`, `varpi` is a uniformizer of `F`, and
`varpi = -rho^2` is a square in `E_r` because `-1=i^2` in `F`. This gives
the component squareclass bases

```text
F^*/F^{*2}:       [varpi], [nu],
E_r^*/E_r^{*2}:   [rho], [nu].
```

For `E_u`, let `alpha` be the residue class of `theta` with

```text
alpha^2 + 6501*alpha + 25179 = 0
```

in `k_2=F_{p^2}`. Define

```text
eta = theta + 2 in E_u.
```

The exact residue checks are

```text
2^((p-1)/2) = -1 mod p,
Norm_{k_2/k}(alpha+2) = 12181,
12181^((p-1)/2) = -1 mod p,
(alpha+2)^((p^2-1)/2) = -1 in k_2.
```

Therefore `eta` is a nonsquare unit of `E_u`, its norm has squareclass
`[nu]`, and

```text
E_u^*/E_u^{*2}:   [varpi], [eta].
```

The pure-Python test records these exact finite-field calculations.

## An Explicit Basis of H_pi

The local norm-square kernel is

```text
H_pi = ker(A_pi^*/(A_pi^{*2} F^*) -> F^*/F^{*2}).
```

Use component order `(F_1,F_2,E_r,E_u)`. Define four classes

```text
h_varpi = [(1, varpi, rho, 1)],
h_nu    = [(1, nu,    1,   eta)],
h_r     = [(1, 1,     nu,  1)],
h_u     = [(1, 1,     1,   varpi)].
```

Every displayed tuple is an element of `H_pi`. Its norm is respectively
`varpi^2`, `nu^2`, `nu^2`, and `varpi^2`, modulo squares.

These four classes are a basis, not merely a convenient subspace. Indeed,
each of the four local field squareclass groups has dimension 2, so
`A_pi^*/A_pi^{*2}` has dimension 8. The norm map has rank 2 because the two
linear `F` components already map onto `F^*/F^{*2}`. The diagonal `F^*`
quotient has dimension 2 and lies in the norm kernel because the total degree
is 6. Hence

```text
dim_F2 H_pi = 8 - 2 - 2 = 4.
```

For an explicit independence check, write a squareclass before the diagonal
quotient as

```text
(a_1,b_1 ; a_2,b_2 ; c,d ; e,f)
```

in the bases listed above. The norm equations are

```text
a_1 + a_2 + c = 0,
b_1 + b_2 + f = 0.
```

Multiplying by a diagonal class makes `a_1=b_1=0`. The remaining free
coordinates are `a_2,b_2,d,e`, and the four displayed `h` classes are the
standard basis in those coordinates. This also proves that the coordinate
system is a basis of the full `H_pi`, not just of the two classes below.

## Tangent-Normalized Divisor Evaluation

For either monic degree-two factor

```text
h in {h_12=F_1 F_2, h_r=F_r},
k_h = f/h,
```

let `B_h` be the sum of the two Weierstrass points over the roots of `h`.
The even-degree divisor is

```text
D_h = B_h - P_+ - P_-.
```

It is `F`-rational, and

```text
div(h(t)) = 2*B_h - 2*P_+ - 2*P_- = 2*D_h,
```

so `D_h` is a valid 2-torsion class. In even-degree Mumford notation this is
the branch pair `(u,v)=(h,0)` with the explicit two-infinity correction.

The divisor-evaluation formula is the following element of `A_pi^*`:

```text
beta_h|_{F[t]/(h)} = k_h(theta)^(-1),
beta_h|_{F[t]/(k_h)} = h(theta).
```

For a root `s` of `h`, use the branch local parameter `z=v`. Since
`v^2=f(t)`,

```text
(t-s)/z^2 -> 1/f'(s),
h'(s)/f'(s) = 1/k_h(s).
```

This is exactly the first line of the formula. At a component outside the
roots of `h`, the value is the product of the two nonzero factors and is
`h(theta)` because `deg(h)=2`.

The norm condition is also exact, not only a residue check. If `Res` denotes
the monic resultant, then

```text
Norm_{A_pi/F}(beta_h)
 = Res(k_h,h) / Res(h,k_h)
 = 1,
```

because `deg(h)=2` and `deg(k_h)=4`. Thus the tangent-normalized element is
already in the norm-square kernel before passing to squareclasses.

The formula is a unit normalization at every factor-zero branch. In
particular, for `h=F_r`, the naive `F_r(theta)` vanishes in `E_r` and is not
allowed; the tangent value is `k_r(theta)^(-1)`, whose reduction is nonzero.
The same replacement handles the two linear branch fibers for `h=h_12`.
The other components are nonzero because the four exact local factors are
pairwise coprime over `F`; the residue table below makes the unit property
visible even at the ramified double-root reduction. At `P_+` and `P_-`, all
factors are monic, so the leading-coefficient evaluation is `1` at both
infinities. No unrecorded infinity scalar is introduced.

## The Two Classes and Coordinates

Use `alpha` as above in the residue field of `E_u`. Reducing the two
tangent-normalized elements gives the following exact table, in component
order `(F_1,F_2,E_r,E_u)`:

```text
                 F_1          F_2          E_r              E_u
beta_12       20701        11446        27640        592 + 6504*alpha
beta_r        29324        18457         8588       37107 + 7406*alpha
```

All entries are nonzero. The square/nonsquare bits in the corresponding
local field components are

```text
bits(beta_12) = (0,1,1,1),
bits(beta_r)  = (0,0,1,0).
```

The exact norm residues are both `1`. After the diagonal gauge with the first
component equal to `1`, the coordinates in the basis

```text
(h_varpi, h_nu, h_r, h_u)
```

are

```text
[beta_12] = (0,1,1,0) = h_nu + h_r,
[beta_r]  = (0,0,1,0) = h_r.
```

The two coordinate rows have rank 2 over `F_2`, so the two classes are
independent in `H_pi`. Since they are divisor evaluations, their source
classes are independent modulo `2J(F)`: a relation in `J(F)/2J(F)` would
give the same relation in `H_pi`.

For completeness, the third branch-pair divisor satisfies

```text
D_12 + D_r + D_u = div(v),
```

so its local class is the product of the first two. The residue calculation
indeed gives `[beta_u]=h_nu`, consistent with
`beta_u=beta_12*beta_r` in the squareclass quotient.

## Completeness Boundary

The two independent classes give a 2-dimensional subspace of the local fake
image `I_pi`. The accepted arithmetic input gives

```text
dim_F2 J(F)/2J(F) = 2.
```

Because the fake evaluation map factors through `J(F)/2J(F)`, its image has
dimension at most 2. Therefore these two classes force

```text
dim_F2 I_pi = 2,
I_pi = span_F2{beta_12,beta_r}.
```

This completes the local fake image, not the 4-dimensional ambient kernel
`H_pi`. It also does not assert that the fake map has zero kernel on all of
`J(F)/2J(F)` independently; the two displayed image classes already provide
the needed lower bound, and the accepted source dimension supplies the upper
bound.

## Focused Validation

The exact finite-field and coordinate check is:

```text
UV_CACHE_DIR=/private/tmp/d19-uv-cache uv run pytest -q \
  tests/test_berry_sextic_q2a_local_kummer_generators.py -n 1
```

It reconstructs the certified residue factorization, checks the irreducible
quadratic, verifies the two tangent-value tables and norm residues, and
checks the rank-2 coordinate matrix. It does not use Sage, Magma, p-adic
factorization, broad search, or global 16-coordinate localization.
