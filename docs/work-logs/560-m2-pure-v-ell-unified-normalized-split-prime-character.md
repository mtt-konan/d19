# M2 Pure v_ell Unified Normalized Split-Prime Character

## Question

What is the missing leading character when an odd common valuation puts
`p` into the canonical class `r`, and can all valuation parities be written in
one normalized formula?

## Uniform Normalization

For any odd `p|ell-1`, put

```text
e=v_p(ell-1),
k=v_p(R),
d=min(e,k),
epsilon=d mod 2.
```

By `wl554`, `p|r` exactly when `epsilon=1`. Define

```text
r_p=r/p^epsilon.
```

The standard equation `Z=r*Gamma^2` implies that `Gamma` contains the
rational factor `p^((d-epsilon)/2)`. Dividing by `p^d` gives

```text
Z_d=(F_d+i*E_d)=r_p*Gamma_p^2,
E_d=E/p^d,
F_d=F/p^d.
```

Thus the same normalized equation applies for `d=0`, positive even `d`, and
positive odd `d`. The odd case differs only by removing the single squarefree
factor `p` from `r`.

## Local Character

At inert `p ≡ 3 (mod 4)`, the square norm again makes the condition automatic.
At split `p ≡ 1 (mod 4)`, choose `j^2=-1`. The exact condition is

```text
Legendre((F_d+j*E_d)/r_p,p)=1.
```

The three valuation-order cases are uniformly:

```text
e<k: Legendre(L_e*(-1+j)/r_p,p)=1,
k<e: Legendre((R/p^k)/r_p,p)=1,
e=k: Legendre(L_e*(lambda-1+j)/r_p,p)=1,
```

where

```text
L_e=(ell-1)/p^e,
lambda=(R/p^e)/(4*L_e*Q^2*D^2) mod p.
```

For `d=0`, this recovers `wl558`; for positive even `d`, it recovers `wl559`;
for odd `d`, it supplies the previously missing leading character with
`r_p=r/p`.

## Corrected Place Partition

Every odd `p|ell-1` is now fully classified at the standard-square layer:

- inert primes are automatic after normalization;
- split primes obey the single master character above;
- parity of `d` determines only whether the local prime is removed from `r`
  before evaluating that character.

The next gate is genuinely global: assemble these split-prime equations and
test whether quadratic reciprocity forces a contradiction or leaves an exact
global character obstruction.

## Boundary

This does not solve the assembled system, prove that a valuation pattern is
globally realized, solve an orientation, handle the nontrivial real-unit
class, prove `wl535`, or enter M3.
