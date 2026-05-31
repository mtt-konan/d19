# Conditional / Empirical Paper — Outline (F.1)

**Status**: skeleton only (wl090). This is the *conditional + empirical* paper that
can be written **now**, without a rigorous proof of Conjecture A1 (which wl084 showed
is not yet proven). It packages the project's proven algebraic results and its
reproducible no-solution certificate library. Model: Peschmann 2604.09328
(`docs/literature/notes/peschmann-2604-09328.md`).

**Honesty rule for this paper**: every numbered *Theorem/Proposition* below must be
something the repo has either proven algebraically or verified exhaustively in a
stated finite range. Everything merely *observed* universally (notably A1) is labeled
**Conjecture / Observation**, never Theorem.

---

## Title (working)

*Concordant elliptic curves and the Harborth (rational-distance unit-square) problem:
algebraic identities, 2-adic obstructions, and a verified no-solution census.*

## Abstract (skeleton)

- Harborth / perfect-square problem → no integer point known with rational distances
  to all four unit-square vertices.
- Reduce to concordant form `E_{A,B}: Y² = X(X+A²)(X+B²)` + a 4-chain closure condition.
- Contributions: (i) two exact 4-chain identities (A, C); (ii) a 2-adic + mod-p²
  necessary-condition sieve that *proves* no-solution for 94.8% of reduced pairs;
  (iii) a structural theorem that every concordant point lies in `2·E(ℚ)`; (iv) a
  reproducible certificate library covering all reduced `(A,B)` up to a stated bound,
  with the residual *hard cases* classified by Mordell–Weil rank; (v) a conditional
  finiteness statement assuming Conjecture A1.

## 1. Introduction

- Harborth conjecture statement; history (Guy, Bremner–Ulas, Peschmann).
- What is known / the perfect-square (rational-distance) variant.
- Our angle: turn the search into a *certified non-existence census* + isolate the
  exact remaining obstruction.
- Summary of contributions and what is **conditional** vs **proven**.

## 2. Reduction to concordant elliptic curves (proven; cite wl034/wl035, MATH.md)

- Derive `E_{A,B}: Y² = X(X+A²)(X+B²)`; the "last two distances rational" ⟺ a
  rational point with `X = N²` and chain closure.
- Define the **4-chain** and **closure** precisely; define reduced `(A,B)`.

## 3. Exact 4-chain identities (Theorem; proven, wl034)

- **Theorem A**: `h₁²+h₃² = h₂²+h₄² = a²+b²+c²+d²`.
- **Theorem C**: `(h₁h₃−h₂h₄)(h₁h₃+h₂h₄) = (d−b)(a−c)(a+c)(b+d)`.
- Proof (algebraic identities). State explicitly that the earlier "blocker-prime"
  argument built on them is **void** (no mod-4 parity constraint) — do not claim an
  obstruction here.

## 4. 2-adic and mod-p² necessary conditions (Theorem; proven sieve, wl036/wl037/wl040)

- The reduced-`(A,B)` 2-adic necessary condition; statement + proof that failing pairs
  have **no solution**.
- chain-closure mod-p² simultaneous sieve (cuts 99.6% of hard cases).
- Finite-descent effective bound: **no chain solution with N ≤ 10⁸** (wl037).
- These are unconditional non-existence results in stated ranges.

## 5. Structural 2-divisibility theorem (Theorem; proven, wl086)

- **Theorem**: for every concordant `N`, the point `Q_N = (N², N·√…)` lies in
  `2·E_{A,B}(ℚ)` (its 2-descent class is trivial), because `(N², N²+A², N²+B²)` are
  all squares.
- Corollary: cycle / multi-N linear relations among the `Q_N` are *fully* explained by
  2-divisibility + coordinate-rank deficit (wl086) — they give **no** new obstruction
  (also K_n hubs, wl089). This delimits why elementary descent cannot finish the proof.

## 6. The no-solution certificate library (empirical, exhaustive in range; wl030/wl036/wl087)

- Pipeline: `safe_sieve` → `factor_concordant` → `rank_zero` (PARI `ellrank`) →
  residual `hard_case`. Cite `scripts/prove_no_solution.py`.
- Census table (by `max_hyp`): #pairs, #proven_no_solution (≈94.8%), #hard_case (≈5%),
  PARI rank exactness (lower==upper, 100%).
- **hard_case rank distribution**: rank1 ≈37%, rank2 ≈48%, rank3 ≈13%, rank4 ≈1%.
- Reproducibility: DB schema, commands, data files.

## 7. Conditional finiteness (Conjecture A1 + consequences)

- **Conjecture A1 (Observation, NOT proven — wl084)**: every k=2 multi-N pair has
  `rank E_{A,B} ≥ 2`; verified universally (1879/1879 at `max_hyp=1M`) but the
  algebraic proof has a gap in the composite-`c` case.
- **Conditional Theorem**: *assuming A1*, [state the no-solution consequence it would
  give for the relevant pair class]. Make the dependency explicit and quantified.
- Be candid: this is the one place the paper is conditional.

## 8. The remaining obstruction & open problems

- What is genuinely left: rank≥2 fiber finiteness — needs Chabauty/Quadratic-Chabauty
  (B.1) or Brauer–Manin (A.4). Cite wl090/F.2 tooling survey (open-source vs Magma).
- Heegner height-bound upgrade would settle ~37% (rank-1) — open height bound.

## 9. Reproducibility appendix

- Code (GitHub), data files, exact commands, software versions (PARI/cypari2, Python).
- Pointers to worklogs for each Theorem.

---

## TODO to turn this into LaTeX

1. Fill §3/§4/§5 proofs from MATH.md + wl034/wl036/wl037/wl040/wl086.
2. Regenerate the §6 census table from the proof_status DB at the chosen `max_hyp`
   (use an existing certified range — **no new long run**).
3. Write §7 conditional statement precisely; cite wl081–wl084 for the gap.
4. Bib: Harborth, Guy, Bremner–Ulas, Ono (concordant forms), Peschmann, Chabauty refs
   (from wl090).
