# Q3a1 Dyadic Fake-Kernel Object Boundary

## Outcome

`q3a1_formal_dyadic_setup_only`

This report fixes the dyadic local objects for the selected curve

```text
C_1: v^2=g6(t),  K=Q(i),  L=K[theta]/(g6(theta)).
```

It transports the exact Q2c global rows to the dyadic place and records the
exact branch algebra that is already available. It does not prove or disprove
`D_inf in 2J(K_varpi)`, and it does not claim a complete local fake image or
kernel.

## Dyadic Input

Let

```text
K_varpi = Q_2(i),  varpi=1+i,  v_varpi(varpi)=1,
2=-i*varpi^2,     k_varpi=F_2.
```

The standard local-field squareclass dimension is

```text
dim_F2 K_varpi^*/K_varpi^{*2}=4.
```

No particular four-element basis of this base-field squareclass group is
needed below. The exact B0 dyadic calculation gives

```text
g6(t)=(t+1)^6 mod varpi,
z=t+1,
H(z)=g6(z-1)
    =z^6+(-2*i-8)z^5+(2*i-10)z^4+(-16*i+48)z^3
     +16*i*z^2+(32*i-64)z+32-32*i,
v_varpi(H_0,...,H_6)=(11,10,8,9,3,2,0),
H_5/varpi^2=4*i-1,  H_0/varpi^11=-1.
```

The fixed-center radial forms are

```text
F_r(X)=varpi^(-6*r)*H(varpi^r*X),
v_varpi([X^6]F_r)=0,
v_varpi([X^5]F_r)=2-r,
v_varpi([X^4]F_r)=3-2*r.
```

These are exact fixed-center facts only. They do not produce a basis of the
dyadic algebra squareclasses. The post-B0 unit-square lemma and valuation
partition concern the other twist `C_i`, with `f=(-i)g6`: its finite-chart
branches have valuations `0,6,13,11` for
`v_varpi(z)=0,1,2,>=3`, and its reciprocal chart has normalized value
`1+varpi mod varpi^2`. This proves `C_i(K_varpi)=emptyset`; it is not a
Kummer computation for `C_1`.

## Local Objects

Do not factor `g6` over a p-adic field here. Define the finite local algebra
abstractly by

```text
A_varpi = L tensor_K K_varpi
        = K_varpi[t]/(g6(t)).
```

Its squareclass, diagonal constant, fake, norm, and norm-kernel objects are

```text
W_varpi = A_varpi^*/A_varpi^{*2},
B_varpi = image(K_varpi^*/K_varpi^{*2} -> W_varpi),
F_varpi = W_varpi/B_varpi
          = A_varpi^*/(A_varpi^{*2} K_varpi^*),

Nbar_varpi: F_varpi -> K_varpi^*/K_varpi^{*2},
Nbar_varpi([alpha])=[N_{A_varpi/K_varpi}(alpha)],
H_varpi = ker(Nbar_varpi).
```

The even degree ` [L:K]=6 ` makes `Nbar_varpi` well-defined after quotienting
by diagonal constants. The local fake evaluation map and its two parts are

```text
delta_varpi: J(K_varpi)/2J(K_varpi) -> H_varpi,
I_varpi = im(delta_varpi),
kappa_varpi = ker(delta_varpi).
```

For the selected `C_1`,

```text
D_inf=[P_+-P_-],  P_+=[1:1:0],  P_-=[1:-1:0],
delta_varpi(D_inf)=[1]=0.
```

Thus `D_inf` is in the fake-map kernel as a class in the source quotient, but
the available input does not decide whether that source class is zero, i.e.
whether `D_inf in 2J(K_varpi)`.

## Proved Dimensions and Bases

The exact dimensions and basis data currently available are as follows.

### Dyadic source

The accepted local target calculation gives

```text
dim_F2 J(K_varpi)[2]=1,
dim_F2 J(K_varpi)/2J(K_varpi)
  =[K_varpi:Q_2]*g+dim_F2 J(K_varpi)[2]
  =2*2+1=5.
```

This is a source dimension, not a fake-image dimension. Consequently only the
tautological relation is available:

```text
dim_F2(kappa_varpi)+dim_F2(I_varpi)=5.
```

No value for either summand is claimed. In particular, no lower bound from
`D_inf` is available until its class modulo `2J(K_varpi)` is decided.

### Global supported ambient data

Q2c proves, in the fixed column order

```text
zeta4, epsilon_1,...,epsilon_5, S_prime_1,...,S_prime_10,
```

that `V_S` has dimension `16`, the exact supported constant subspace `C_S`
has dimension `4`, and therefore

```text
F_{L,S}=V_S/C_S has dimension 12.
```

Its exact global norm matrix has rank `4`; hence the supported ambient
norm-square kernel has dimension `12`, and its quotient by constants,
`K_{L,S}^N`, has dimension `8`. These are supported ambient/quotient
dimensions only. No dimension of the full `F_L` or full `K_L^N` is inferred.

Q2c also supplies exact global ambient lifts of the two Q2a classes at the
odd prime `(94*i-169)`, namely `epsilon_1` and `epsilon_1+epsilon_4`. The Q2a
basis

```text
(h_varpi,h_nu,h_r,h_u)
```

and its four-dimensional `H_pi` target belong to that odd prime; Q2a also
proves `dim I_pi=2` with local coordinates
`[beta_12]=(0,1,1,0)` and `[beta_r]=(0,0,1,0)`. They cannot be reused as a
dyadic `H_varpi` basis by renaming the uniformizer.

### Still missing at varpi

The following are not certified by the allowed Q3a1 inputs:

```text
dim_F2 W_varpi,
dim_F2 F_varpi,
dim_F2 H_varpi,
```

and there is no certified basis for any of these objects, no dyadic norm
matrix in local squareclass coordinates, and no dyadic local Kummer
evaluation class. Therefore neither `I_varpi` nor `kappa_varpi` is computed.

## Transported Formal Maps

Let `phi_S:F_2^16 -> V_S` be the Q1 ambient coordinate map,
`q_S:V_S -> F_{L,S}` the quotient by `C_S`, and
`j_S:F_{L,S} -> F_L` the natural injection. Completion at `varpi` induces

```text
loc_varpi^fake: F_L -> F_varpi,
loc_varpi^fake([alpha])=[alpha tensor 1],

Lambda_varpi,S
  = loc_varpi^fake o j_S o q_S o phi_S:
    F_2^16 -> F_varpi.
```

For an ambient vector `x`, this is the formal class of the corresponding
Q2c S-unit product in `A_varpi`. The four `M_const` columns map to zero in
`F_varpi`, because they are diagonal constants.

The exact Q2c global norm rows, in the same sixteen-column order, are

```text
M_norm =
  [i]       0000000100000000
  [1+i]     0000001100000000
  [pi]      0000000011001000
  [bar_pi]  0000000000110101.
```

Here `pi=-169+94*i` and `bar_pi=-169-94*i` are the odd support elements from
Q2c; they are not the dyadic uniformizer. Let

```text
c_varpi: K^*/K^{*2} -> K_varpi^*/K_varpi^{*2}
```

be the exact completion squareclass map. The norm rows that can be
transported without choosing a dyadic basis are the formal composite

```text
M_norm,varpi = c_varpi o M_norm,
Nbar_varpi(Lambda_varpi,S(x))
  = M_norm,varpi(x).
```

If a later exact local base-field coordinate map `psi_varpi` is supplied, its
row matrix is `psi_varpi o c_varpi o M_norm`. No rank of this completed row
map is asserted. Likewise, Q2c's displayed `M_loc_H` is an odd-`pi` matrix
and is not a dyadic localization matrix.

## Precise Missing Input

The missing input preventing a complete `H_varpi` basis is one exact
dyadic squareclass/norm certificate for the finite algebra `A_varpi`, giving

1. a certified presentation or basis of `W_varpi=A_varpi^*/A_varpi^{*2}`;
2. the diagonal image `B_varpi` of the four-dimensional base squareclass
   group; and
3. the norm map `W_varpi -> K_varpi^*/K_varpi^{*2}` in those coordinates.

An exact integral-order/filtration or formal local Kummer certificate could
provide this input; no p-adic factorization is supplied or used here. Even
after that basis exists, a separate exact divisor, formal-group, or local
Kummer argument is required to decide `D_inf mod 2` and compute `I_varpi`.

This is a Q3a1 object-and-boundary report only. It does not enter Q3b or Q4,
and it makes no complete local-image, local-kernel, Selmer, rank, or Berry
classification claim.
