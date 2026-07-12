# M2 Pure v_ell Dyadic Selection Of The Gaussian Orientation

## Question

After `wl555`, do both `wl546` Gaussian orientations still survive the exact
dyadic data, or can one orientation be selected uniformly in each mod-8
branch?

## Canonical Sum-Of-Two-Squares Convention

Choose the representation

```text
ell=a_0^2+b_0^2
```

with `a_0` odd and `b_0` even. Then:

- if `ell ≡ 5 (mod 8)`, `v_2(b_0)=1`;
- if `ell ≡ 1 (mod 8)`, `v_2(b_0)>=2`.

Since `D=x^2+y^2` is odd, `x,y` have opposite parity. Therefore
`x^2-y^2` is odd and `x*y` is even.

## Parity Of The Two Orientations

Recall

```text
B_pi=b_0*(x^2-y^2)+2*a_0*x*y,
R_pi=a_0*(x^2-y^2)-2*b_0*x*y.
```

The first expression is always even. The second is always odd: its first term
is odd and its second term is even. Hence

```text
B_pi is even,
R_pi is odd.
```

## Exact Branch Selection

`wl545` gives:

- if `ell ≡ 5 (mod 8)`, `Q` is odd, so only

  ```text
  Q=+/-R_pi(x,y)
  ```

  can occur;

- if `ell ≡ 1 (mod 8)`, `v_2(Q)>=3`, so the odd `R_pi` orientation is
  impossible and only

  ```text
  Q=+/-B_pi(x,y)
  ```

  can occur, with the additional exact condition `v_2(B_pi)>=3`.

Thus the two `wl546` orientations are not simultaneous alternatives after
the dyadic branch is known. Each branch has exactly one possible orientation.

## Remaining Coupled Systems

Combine the selected orientation with

```text
u^2-ell*v^2=+/-4*(x^2+y^2),
u*v=Q,
F+i*E=r*(a+i*b)^2,
r=sqf_odd(gcd(ell-1,R)),
ell*(a^2-b^2)+2*(ell-1)*a*b>0.
```

The `ell ≡ 5 (mod 8)` system uses `R_pi`; the `ell ≡ 1 (mod 8)` system uses
`B_pi`. Only harmless signs remain. This is the first strict elimination of a
complete `wl546` orientation.

## Boundary

This does not solve either surviving branch, remove the signs, handle the
nontrivial real-unit class, prove the full `wl535` proposition, or enter M3.
