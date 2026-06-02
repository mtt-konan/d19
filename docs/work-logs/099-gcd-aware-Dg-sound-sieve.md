# wl099 — gcd-aware 保证除数 $D_g$ + 对任意 (A,B) sound 的闭合筛

## 目标（方向1）

wl098 证了 gcd-aware mod-12 定理（`3|N` 除非 `3|g`；`4|N` 除非 `4|g`）。本 worklog 顺方向1：
在 `3|g` / `4|g` 子类里查更高次幂能否补回丢掉的整除性，并把结论写成一条
**对任意 `(A,B)` sound** 的闭合筛（旧 `safe_sieve` 的非互素推广）。

## 1. prime-level 律到顶（含一个 2-adic 精化）

按 `(v2(g), v3(g))` 分层（非互素 `A<B<=2500`，brute），看 N 的 2-/3-adic 赋值：

- **2-part**：
  - `v2(g)=0`（有奇腿）→ `4|N`，且紧（`min v2(N)=2`）。
  - `v2(g)=1`（最小腿 ≡2 mod4）→ **`8|N`**（`min v2(N)=3`）—— 比主定理的 `4|N` 更强。
  - `v2(g)>=2` → 塌：N 可为奇（odd frac >0），mod 32 也无法补回保证因子。
- **3-part**：`v3(g)=0` → `3|N`（紧）；`v3(g)>=1` → 塌（`v3(g)=1` 仅 ~45% 仍 `3|N`），
  mod 9 / mod 27 无法补回。

**2-adic 精化证明**（`v2(g)=1 ⇒ 8|N`）：最小腿 `C=2C'`（C' 奇），主定理给 `4|N`，写 `N=4m`；
`N²+C²=h² ⇒ 16m²+4C'²=h² ⇒ h=2h'`，`h'²=4m²+C'²`。C' 奇 ⇒ `C'²≡1 mod8`；若 m 奇则
`4m²≡4 mod8`、`h'²≡5 mod8`（非 QR ✗）⇒ m 偶 ⇒ `8|N`。∎

结论：**prime-level 律到顶**，丢掉的层补不回保证整除性（唯一额外收获是 `v2(g)=1` 的 `8|N`）。

## 2. 保证除数 $D_g$ 与 sound 闭合筛

每个 concordant N 被
```
D_g = P2(g) * P3(g),   P2 = {v2=0:4, v2=1:8, v2>=2:1},   P3 = {v3=0:3, v3>=1:1}
```
整除（`g=1→12` 回到 §8.5.1；`g=2→24`）。故任意闭合值 `N_i±N_j` 被 `D_g` 整除，闭合**必须**
`D_g|(A+B)`（sum）或 `D_g||A−B|`（全平面）。实现：`safe_pair_sieve.gcd_aware_kills`，
**对任意 (A,B) sound**。

## 3. 实证（1,802 非互素多-N 对）

- **soundness**：`D_g | N` 零反例（文件 3,779 个 N + brute `A<B<=1200` 9,277 个 N，均 0）。
- **kills vs chain_closure 模 p²**：

| 筛 | 杀数 / 1802 |
|---|---|
| `D_g` 筛（O(1)） | 1138 |
| `chain_closure` 模 p²（full_plane） | 1645 |
| 两者都杀 | 1065 |
| **仅 `D_g` 杀（chain 漏）** | **73** |
| 仅 chain 杀 | 580 |
| 都没杀（落到 GEN-CLOSURE） | 84 |

- `D_g` 取值杀数：`{3:408, 4:367, 8:132, 12:133, 24:98}`。
- `D_g` 筛与 chain 模 p² **互补**：D_g 抓到 73 个 chain 漏掉的；并联后仅 84 个落到穷尽
  GEN-CLOSURE（实际闭合 0）。即**非互素腿的 sound 三段管线**为
  `gcd_aware_kills → chain_closure 模p² → 实际对 GEN-CLOSURE`。

## 文件

- `docs/MATH.md` §8.5.2（2-adic 精化证明 + `D_g` + sound 筛推论）
- `src/rational_distance/concordant/safe_pair_sieve.py`（新增 `guaranteed_divisor`、`gcd_aware_kills`）
- `tests/test_coprime_mod12.py`（+4 测试：D_g soundness / 取值 / `v2=1⇒8|N` / 筛 sound；共 9 passed）
- `scripts/multi_n/gcd_aware_sieve_audit.py`（审计脚本）
