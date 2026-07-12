# M2 Pure v_ell Quartic Character For Split Allocation

## Question

Can the binary allocation of an odd split prime `q ≡ 1 (mod 4)` left open by
`wl565` be constrained by the quartic character of the real-coordinate unit?

## Quartic Sign

Keep

```text
H=alpha^2*M^4-beta^2*N^4.
```

For `q|kappa` with `q ≡ 1 (mod 4)`, `wl565` proves that the normalized value
of `H` is a nonzero quadratic residue modulo `q`. Define its quartic sign

```text
chi_4,q(H)=H^((q-1)/4) in {+1,-1}.
```

The square factor from `g` must be removed first, so this sign is attached to
`H`, not directly to the unnormalized value `F/r`.

## If q Divides alpha

Modulo `q`,

```text
H=-(beta*N^2)^2.
```

Therefore

```text
chi_4,q(H)
 =(-1)^((q-1)/4)*Legendre(beta,q).
```

The first factor is `+1` for `q ≡ 1 (mod 8)` and `-1` for
`q ≡ 5 (mod 8)`.

## If q Divides beta

Modulo `q`,

```text
H=(alpha*M^2)^2,
```

so

```text
chi_4,q(H)=Legendre(alpha,q).
```

These are exact necessary conditions for the two possible sides.

## Complementary-Split Comparison

Fix the allocation of every prime of `kappa/q`, writing its two products as
`alpha_0,beta_0`. The alternatives for `q` predict

```text
q on alpha side:
  chi_4,q(H)=(-1)^((q-1)/4)*Legendre(beta_0,q),

q on beta side:
  chi_4,q(H)=Legendre(alpha_0,q).
```

If these signs differ, the observed quartic sign uniquely chooses the side.
If they agree, quadratic and quartic character information still leaves the
binary allocation unresolved. If the observed sign is the opposite common
sign, both allocations are impossible.

## Exact Failure Point

Quartic character strictly refines `wl565`, but it is not uniformly decisive:
the two predicted signs can coincide. The remaining split allocation is a
finite coupled quartic-character system among the prime factors of `kappa`,
not a collection of independent binary choices.

The next gate must assemble these quartic signs, use the scale/orientation
equation to determine them, or record the resulting finite coupled
quartic-allocation system as the exact unresolved global arithmetic lemma.

## Boundary

This does not assert that the quartic sign is known from `(ell,Q,D)` without
the square-coordinate factorization, solve the coupled allocation system,
solve an orientation, handle the nontrivial real-unit class, prove `wl535`, or
enter M3.
