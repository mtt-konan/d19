# M2 Pure v_ell Exclude tau=1/2 By Integrality

## Question

Does the exceptional genus-one branch `tau=1/2` from `wl571` contain any
candidate with `ell` an odd prime?

## Reduced Denominator

On this branch,

```text
X=q^2,
ell=X+5-4/X.
```

Write the nonzero rational number `q` in lowest terms as

```text
q=a/b,
gcd(a,b)=1,
b>0.
```

Then

```text
ell
 = (a^4+5*a^2*b^2-4*b^4)/(a^2*b^2).
```

Because `ell` is an integer, reduction modulo `a^2` gives

```text
a^2 divides 4*b^4.
```

Since `gcd(a,b)=1`, this forces

```text
a^2 divides 4.
```

Reduction modulo `b^2` gives

```text
b^2 divides a^4.
```

Coprimality now forces

```text
b^2=1,
b=1.
```

Thus every integral value of `ell` on the exceptional branch has

```text
q^2=a^2 in {1,4}.
```

## Positivity Closes The Branch

The exact `wl570` positivity interval has `X>sigma_ell>1` for every
`ell>=5`. Therefore `q^2=1` is impossible, leaving only

```text
q^2=4.
```

Substitution gives

```text
ell=4+5-4/4=8.
```

This is not an odd prime and in particular is not congruent to `1 mod 4`.
Hence no exact `wl535` candidate can have

```text
tau=1/2.
```

The auxiliary square equations `p^2=5-4/X` and `r^2=X+5` are not needed for
the contradiction. At the sole surviving integral value `X=4` they are in
fact populated (`p^2=4`, `r^2=9`); it is exactly the parameter-primality
condition that fails.

## Exact Consequence

The unique genus-one drop in `wl571` is completely excluded. Every remaining
candidate must satisfy

```text
tau!=1/2
```

and therefore lies on the generic genus-five multiquadratic cover.

## Boundary

This closes only the exceptional `tau=1/2` branch. It does not exclude any
point with `tau!=1/2`, solve the generic genus-five cover, prove all of
`wl535`, identify a Selmer group, or enter M3.
