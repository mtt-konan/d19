# M2 Pure v_ell Affine F2 System For Split Allocation

## Question

Do the coupled quartic-sign choices from `wl566` form an explicit solvable
finite system, or an intrinsically nonlinear allocation problem?

## Variables And Fixed Factors

Let `J` be the odd split prime factors of `kappa` whose sides remain undecided
after `wl564`-`wl565`. Put all already assigned dyadic and inert factors into
coprime products

```text
alpha_0,
beta_0.
```

For `q in J`, define

```text
x_q=1 if q|alpha,
x_q=0 if q|beta.
```

Then

```text
alpha=alpha_0*product(q^x_q),
beta =beta_0 *product(q^(1-x_q)).
```

## Additive Character Data

For a nonzero residue `u mod q`, write

```text
[u/q]=(1-Legendre(u,q))/2 in F_2.
```

Define

```text
A_qt=[t/q]                         for t!=q,
a_q=[alpha_0/q],
b_q=[beta_0/q],
d_q=(q-1)/4 mod 2,
z_q=(1-chi_4,q(H))/2.
```

Here `d_q` records the quartic sign of `-1`.

## Linearization

If `x_q=0`, so `q|beta`, `wl566` gives

```text
z_q=a_q+sum_(t!=q) A_qt*x_t.
```

If `x_q=1`, so `q|alpha`, it gives

```text
z_q=d_q+b_q+sum_(t!=q) A_qt*(1-x_t).
```

Over `F_2`, the dependence on the other `x_t` is the same in both cases.
Therefore define

```text
Delta_q=d_q+a_q+b_q+sum_(t!=q) A_qt.
```

Both alternatives are equivalent to the single affine-linear row

```text
Delta_q*x_q + sum_(t!=q) A_qt*x_t = z_q+a_q.
```

Thus the complete split allocation is an affine `F_2` system, not a nonlinear
search through `2^|J|` cases.

## Exact Consequence

For fixed candidate data `(alpha_0,beta_0,z)`, ordinary Gaussian elimination
does exactly one of the following:

- proves the split allocation impossible;
- gives a unique allocation;
- leaves an explicit affine space of allocations.

This matrix is attached to the quartic real-coordinate factorization. It is
not the `wl561` Gaussian norm-character matrix and is not a theorem-level
Selmer matrix.

## Remaining Global Coupling

The right-hand vector `z` still comes from
`H=alpha^2M^4-beta^2N^4`, and the surviving allocations must also satisfy

```text
g*M*N=h*abs(Q*D),
```

the selected `wl556` orientation, the exact real-coordinate equality, and the
strict cone. The next gate must couple the affine solution space to those
integer equations or certify that combined system as the exact unresolved
global lemma.

## Boundary

This does not claim the affine system is always consistent or inconsistent,
determine `z` without the square-coordinate factorization, solve the integer
equations, handle the nontrivial real-unit class, prove `wl535`, identify a
Selmer group, or enter M3.
