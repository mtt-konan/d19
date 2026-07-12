# M2 Pure v_ell Global Character Matrix And Reciprocity Product

## Question

What is the exact simultaneous system obtained by assembling the normalized
split-prime characters from `wl560`, and what cancellation follows from
quadratic reciprocity?

## Character Matrix

Let `P` be the odd prime divisors of `ell-1`. For `q in P`, put

```text
epsilon_q=min(v_q(ell-1),v_q(R)) mod 2.
```

Then

```text
r=product(q^epsilon_q).
```

Let `T` be the split subset `p ≡ 1 (mod 4)`. At each `p in T`, let

```text
C_p=F_d+j_p*E_d,
j_p^2=-1,
d=min(v_p(ell-1),v_p(R)).
```

The `wl560` condition is

```text
Legendre(C_p,p)=Legendre(r/p^epsilon_p,p)
               =product over q!=p of Legendre(q,p)^epsilon_q.
```

Write quadratic characters additively in `F_2`:

```text
n_p=(1-Legendre(C_p,p))/2,
A_pq=(1-Legendre(q,p))/2.
```

Then the complete split-prime system is

```text
n_p = sum over q!=p of A_pq*epsilon_q  (mod 2),
p in T.
```

The vector `epsilon` is candidate-canonical, not a freely chosen Selmer
class. This is a finite character matrix attached to the standard-square
equation, not a theorem-level Selmer matrix.

## Reciprocity Product On Odd Common Split Primes

Let

```text
S={q in P: epsilon_q=1}.
```

Multiply the character equations only over `p in S intersect T`. For two
distinct split primes `p,q in S intersect T`, quadratic reciprocity gives

```text
Legendre(q,p)=Legendre(p,q),
```

so their two appearances cancel. Therefore

```text
product over p in S intersect T of Legendre(C_p,p)
 = product over p in S intersect T
     product over q in S minus T of Legendre(q,p).
```

Since every `p in T` is `1 mod 4`, the right side may equivalently be written

```text
product over q in S minus T
  product over p in S intersect T of Legendre(p,q).
```

In particular, if the canonical class `r` has no inert prime factor, then

```text
product over p|r of Legendre(C_p,p)=1.
```

## Exact Failure Point

Reciprocity cancels all pairwise interactions among split prime factors of
`r`, but it leaves:

- characters involving inert factors of `r`;
- individual equations at split primes not in `r`;
- the candidate-dependent leading characters `Legendre(C_p,p)`.

Therefore the character matrix does not by itself yield a uniform
contradiction. A strict next step must relate the leading characters `C_p` to
the selected `wl556` orientation and source equations, or exhibit a parameter
subfamily where the reciprocity product has the wrong sign.

## Boundary

This does not assert that every `epsilon` vector occurs, solve the matrix,
produce a rational point, handle the nontrivial real-unit class, prove
`wl535`, identify a Selmer group, or enter M3.
