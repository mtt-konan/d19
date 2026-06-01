# wl098 — gcd-aware mod-12 定理 + 1,802 非互素对完整验证

## 背景

wl097 证了**互素腿** mod-12 定理：`gcd(A,B)=1 ⇒ 每个 concordant N 被 12 整除`。
随后（框架澄清）确认 coprime-`(A,B)` **并非 WLOG**——最小反例只保证
`gcd(A,B,N₁,N₂)=1`，非互素 `(A,B)` 半空间从未进过解析筛（§8.6）。

本 worklog 做两件事：
1. 把 wl056 的 **1,802 个非互素多-N 对**（hyp≤2000）第一次喂给**实际对**判定器，量化 §8.6；
2. 把 wl097 推广成**适用于任意 `(A,B)`** 的 gcd-aware mod-12 定理。

## 1. 非互素对的完整验证（判定器无需重写）

脚本 `scripts/multi_n/gcd_aware_mod12_check.py`，对 1,802 个非互素对用
`exact_concordant_pair`（完整分解、**不约化**）取 concordant 集后查判定器：

| 检查 | 结果 |
|---|---|
| `exact_concordant_pair` vs wl056 扫描集 | **0 mismatch** → 判定器对非互素精确 |
| 实际对 GEN-CLOSURE 闭合（完整集，四关系） | **0 / 1802** → 这些非互素对全闭合不了 |
| `chain_closure` 模 p²（full_plane，sound） | **1645 / 1802 (91.3%)** 被 sound-杀，157 落下 |
| `safe_sieve`（仅信息，对非互素 unsound） | 按奇偶会拒 499（472 mixed + 27 odd-odd），**无 mod-12 依据**；本样本里那 499 个实际也都没闭合 |

**结论**：`chain_closure` + 实际对 GEN-CLOSURE 对非互素**开箱即用、sound**；
覆盖了 partner-BFS 漏掉的 94% 非互素多-N 对（wl056 覆盖率仅 6.1%），第一次给出
「这 1,802 个非互素对无反例」的完整声明。穷举更新只需：删生成器 gcd/even 过滤
+ 非互素对绕过 `safe_sieve`。

## 2. gcd-aware mod-12 定理（MATH §8.5.2）

把 wl097 的 mod-3 / mod-8 论证按「g 是否含 3、是否含 4」重做：

> 设 `g=gcd(A,B)`。则 `3∤g ⇒ 3|N`，`4∤g ⇒ 4|N`。
> 故 `3∤g 且 4∤g ⇒ 12|N`；`g=1` 即 wl097。

证明（初等）：
- **3-部分**：平方数 mod 3∈{0,1}，`N²+A²=□`⇒`3|N 或 3|A`，同理 `3|N 或 3|B`；
  `3∤N`⇒`3|A 且 3|B`⇒`3|g`。逆否即 `3∤g⇒3|N`。
- **4-部分**：`4∤g`⇒存在腿 C 有 `v₂(C)≤1`。
  - C 奇：`C²≡1 (mod 8)`，mod-8 逼出 `4|N`（同 wl097）。
  - `C≡2 (mod 4)`：`C²≡4 (mod 16)`，平方数 mod 16∈{0,1,4,9}，逐 N 类型只剩 `N≡0 (mod 4)` 可行 ⇒ `4|N`。

边界：`(6,15)` g=3（3|g，N=8 不被 3 整除）、`(8,20)` g=4（4|g，N=15 奇）。

**推论（非互素腿二分）**：g 与 12 互素（含 g=2,5,7,10,11…）时 12|N 仍成立 ⇒ 闭合仍需
12|(A+B) 或 12||A−B|，与互素腿同障碍；真正松绑的只有 `3|g 或 4|g` 子类。§8.6 硬区缩小到后者。

## 3. 实证

- wl056 文件：1,802 对 / 3,779 个 N，逐 N 断言 **0 反例**。
- 独立 brute 重扫 `A<B≤1200`：8,371 对 / 9,277 个 N，**0 反例**。
- 回归测试 `tests/test_coprime_mod12.py`：新增 `test_gcd_aware_mod12_law`、
  `test_gcd_aware_recovers_coprime_special_case`，全套 7 passed，ruff clean。

## 文件

- `docs/MATH.md` §8.5.2（定理 + 证明 + 推论）
- `scripts/multi_n/gcd_aware_mod12_check.py`（验证脚本）
- `tests/test_coprime_mod12.py`（+2 测试）
