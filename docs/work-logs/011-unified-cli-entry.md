# 工作日志 011 — 统一 CLI 入口

**日期**：2026-04  
**对应提交**：本次提交

---

## 摘要

将两个独立的 CLI 脚本（`search_gpu.py` 和 `search_ec.py`）合并为单一入口 `scripts/search.py`，通过子命令区分搜索方法。

---

## 改动

### 新增
- `scripts/search.py`：统一入口，子命令 `parametric` 和 `ec`

### 删除
- `scripts/search_gpu.py`（功能迁移至 `search.py parametric`）
- `scripts/search_ec.py`（功能迁移至 `search.py ec`）

### 修改
- `docs/IMPLEMENTATION.md`：更新模块结构图
- `README.md`：更新使用示例

---

## 用法对照

| 旧命令 | 新命令 |
|--------|--------|
| `python scripts/search_gpu.py --scale 200 --backend torch` | `python scripts/search.py parametric --scale 200 --backend torch` |
| `python scripts/search_gpu.py --scale 80 --backend numpy` | `python scripts/search.py parametric --scale 80 --backend numpy` |
| `python scripts/search_ec.py --max-m 30` | `python scripts/search.py ec --max-m 30` |

---

## 参数结构

**公共参数**（两个子命令均支持）：
- `--min-rational {3,4}`
- `--inside`
- `--out FILE`
- `--top N`
- `--no-progress`

**parametric 专有**：
- `--scale N`（简写，设置 max_m/max_k_num/max_k_den 比例）
- `--max-m`, `--max-k-num`, `--max-k-den`
- `--backend {auto,numpy,cupy,torch}`
- `--workers N`（CPU 多进程数量）
- `--brute-den N`（附加暴力搜索）
- `--no-dedup-symmetry`

**ec 专有**：
- `--max-m`, `--max-k-num`, `--max-k-den`
- `--max-steps N`（弦切法展开步数）
