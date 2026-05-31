# wl091 — F.4：精读 Peschmann §7 + 与 d19 mod-p² closure sieve 对比 → A.5 关闭

## 任务

OPEN_DIRECTIONS **F.4**：精读 Peschmann (arXiv:2604.09328) §7(2) 的 "modular search
(45 primes < 200)"，判断能否迁移；**A.5**：据此决定要不要把 safe_sieve 扩到 45 primes
规模。风险预设（wl078-079）：(a,b) mod p² CRT 不能 universal kill，怕重走 path B。

结论先行：**A.5 关闭（不值得做）**。理由有三，全部由实测支撑。

## 一、Peschmann §7 到底筛什么（逐条精读）

PDF p.10 §7 "Computational verification" 三个子项：

- **§7(1)**：对 `1≤b<a≤1000, 1≤n<m≤1000`（coprime + 奇偶过滤，约 10¹¹ 元组）暴力验
  `f1 f2` 从不是完全平方。——纯穷举，不是 sieve。
- **§7(2)**：对 5 个 hard specialisation（generator 全满足 `δ3|δ1` 的 s 值）做 **175,418
  个 lattice point** 的 modular search，用 **45 primes p<200** 检验 `f(P)∈ℚ*²`，0 candidate。
  ——**这是"对固定曲线、在 height box 内枚举候选有理点 P=ΣnᵢGᵢ+T，再用多素数同余判 f(P)
  是否平方"**，是 **per-point** 的平方检测，不是 per-(a,b) 的参数 sieve。它的 d19 类比是
  **方向五 Heegner-height 有界枚举 + 多素数平方过滤**，**不是** safe_sieve。
- **§7(3)**：对每个 (a,b,m,n) 存在 blocker prime `p` 使 `v_p(f1 f2)` 为奇 ⟹ 非平方。
  **没有 universal prime**，blocker 随参数变；且 blocker 总是 `p=2`(11.6%) 或
  `p≡1 (mod 4)`(88.4%)，**从不 p≡3 (mod 4)**（Remark 6.5：每个 fᵢ 是 ℤ[i] 的范数，
  p≡3 (mod 4) 必整除到偶次）。——这才是 per-参数 的局部障碍，是 safe_sieve 的真类比。

**纠正 A.5 的 framing**：A.5 把 §7(2) 当成"45-prime 参数 sieve"是 **category error**。
§7(2) 是 per-point 平方检测；真正对应 safe_sieve 的是 §7(3) blocker prime，而 §7(3)
明说"无 universal prime"——与 wl078-079 同一堵墙。

## 二、d19 现状已经超过 Peschmann 的素数规模

A.5 的前提"safe_sieve 现用 mod 1680 ~5 primes"**已过时**：

- `chain_closure_mod_sieve`(wl040)：mod-p² sieve，`STANDARD` 用 p∈[3,53]（14 primes），
  `EXTENDED` 到 p=97（23 primes）。在 max_hyp=2000 上**单这一筛就砍 99.6% hard_case**。
- `finite_descent_hard_cases.py`(wl037 Layer 1)：N-only 条件 `T≠∅` 已检 **primes p<200**
  （即 Peschmann 的 45-prime 规模）。

所以"扩到 45 primes <200"在 d19 **早已实现**，A.5 的增量近乎为零。

## 三、实测：d19 的筛力来自 closure reflection，而非 Peschmann 式 Gaussian 平方

脚本 `scripts/modular/sieve_killer_prime_class.py`（max_hyp=2000，8220 个过 safe_sieve
的 reduced pair）：

| 指标 | 值 |
|---|---|
| 被 chain_closure mod-p²(p≤97) 砍 | 8190 / 8220（survivors 30） |
| kill reason = **reflection_empty** `T∩((A+B)−T)=∅` | **8190（100%）** |
| kill reason = pure `T_empty`（concordant 平方条件本身） | **0** |
| 最小 killer prime ≡ 3 (mod 4) | **7343（89.7%）**，其中 **p=3 占 7197（88%）** |
| 最小 killer prime ≡ 1 (mod 4) | 847（10.3%） |

**解读**：

1. **100% 的 kill 来自 closure reflection**（apex 约束 `b=A+B−N`），纯 concordant 平方
   条件 `T=∅` 一个都没砍到。d19 的筛力**完全来自 chain 闭合结构**，不是 concordant
   条件本身。
2. **90% 的 killer 是 p≡3 (mod 4)**（p=3 独占 88%）——与 Peschmann §7(3)"blocker 从不
   p≡3 (mod 4)"**正好相反**。不矛盾：Peschmann 的 blocker 是对**纯平方** `f1 f2∈ℚ*²`
   的全局 valuation 判据（Gaussian 范数 ⟹ p≡3 偶次，不能当 blocker）；d19 砍的是
   **closure reflection 的局部 residue 交集**，apex 约束破坏了 Gaussian-范数结构，于是
   p≡3 (mod 4)（尤其 p=3）成了主力 killer。两种机制本质不同、互补。
3. **印证 wl078-079**：即便 p=3 砍掉 88%，仍非 universal（30 survivors，且需更大素数才
   能砍的 pair 真实存在）。"无 universal prime" 在 d19 与 Peschmann 一致成立。

## 四、决策

- **A.5 关闭**：(i) "45-prime 参数 sieve" 在 d19 早已实现（mod-p² p≤97 + finite-descent
  p<200）；(ii) 若照 Peschmann §7(2)/§7(3) 的"纯平方 / Gaussian blocker"思路扩，会**恰好
  丢掉**承担 90% 筛力的 p≡3 (mod 4) 素数（含 p=3），严格更弱；(iii) universal kill 不可能
  （wl078-079 + Peschmann §7(3) 一致）。
- **F.4 关闭（已读懂）**：§7(2) 是 per-point 平方检测（类比方向五 Heegner-height），
  §7(3) 是 per-参数 blocker（类比 safe_sieve，但无 universal prime）。
- **可迁移的真东西**：Peschmann Remark 6.5 的 Gaussian-范数观察提示——若要为 *纯
  concordant 平方条件* 做素数选择，p≡3 (mod 4) 无用；但 d19 的力量在 closure reflection，
  那里 p≡3 (mod 4) 恰恰最有用。这条边界本身值得记入文档，避免日后误删 p=3 这类素数。

## 复现

```bash
PYTHONPATH=src uv run python scripts/modular/sieve_killer_prime_class.py --max-hyp 2000
```

## 参考

- Peschmann, arXiv:2604.09328 §7、Remark 6.5（`docs/literature/pdfs/`，notes
  `docs/literature/notes/peschmann-2604-09328.md`）。
- wl037（finite descent，N-only primes<200）、wl040（chain-closure mod-p² sieve）、
  wl078-079（(a,b) mod p² CRT 非 universal）。
