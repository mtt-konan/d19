"""GPU-accelerated rational-distance search using CuPy or PyTorch.

Backend priority (auto-detected at import time):
  1. CuPy  — nearly identical API to numpy; works with CUDA and ROCm
  2. PyTorch CUDA/ROCm — fallback when CuPy is unavailable
  3. NumPy  — final CPU fallback; still benefits from vectorisation

For AMD Ryzen AI Max+ 392 (ROCm):
  # Ubuntu / Arch, match your ROCm version
  pip install cupy-rocm-6-0        # ROCm 6.x wheels
  # or build from source for ROCm 7.0:
  #   HIP_PATH=/opt/rocm pip install cupy --no-build-isolation

  # PyTorch ROCm fallback (always works):
  pip install torch --index-url https://download.pytorch.org/whl/rocm6.2

For NVIDIA RTX 4090 (CUDA):
  pip install cupy-cuda12x

Design
──────
Unlike parametric_search_fast (multiprocessing), this runs in a *single
process*.  The GPU replaces multi-core CPU parallelism: each triple's
entire (a,b) array is dispatched as one GPU kernel that operates on up to
N_pairs elements simultaneously.

Unified memory on APUs (Ryzen AI Max, Apple M-series with PyTorch MPS)
means transfers are logical, not physical — so even "copy to GPU" is cheap.

int64 safety: tB_max ≈ (scale*r_max)^2 ≈ 4e18 for scale ≈ 600.
Above scale 600 the numpy/cupy int64 path may overflow; a warning is
printed and the caller should switch to the CPU integer path.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction
from math import gcd
from typing import Callable

import numpy as np

from rational_distance.math_utils import primitive_pythagorean_triples
from rational_distance.square import RationalPoint


def _xp_cast(t, dtype):
    """Cast array *t* to *dtype*, compatible with both NumPy (.astype) and
    PyTorch tensors (.to).  CuPy arrays also support .astype."""
    if isinstance(t, np.ndarray):
        return t.astype(dtype)
    # PyTorch tensor (or CuPy array that also has .to):
    if hasattr(t, "to") and not hasattr(t, "astype"):
        return t.to(dtype)
    return t.astype(dtype)  # CuPy

# ── Backend detection ─────────────────────────────────────────────────────────

def _try_cupy():
    """Return CuPy module if a GPU device is accessible, else None."""
    try:
        import cupy as cp
        cp.array([1], dtype=cp.int64)  # triggers device init
        return cp
    except Exception:
        return None


def _try_torch():
    """Return a torch-wrapping namespace if ROCm/CUDA is available, else None."""
    try:
        import torch
        if not torch.cuda.is_available():
            return None

        class _TorchXP:
            """Minimal numpy-compatible wrapper around torch CUDA tensors."""

            def __init__(self, device):
                self._dev = device
                self.int64 = torch.int64
                self.float64 = torch.float64

            # ── Array creation ────────────────────────────────────────────
            def array(self, x, dtype=None):
                if isinstance(x, np.ndarray):
                    t = torch.from_numpy(x)
                else:
                    t = torch.tensor(x)
                t = t.to(self._dev)
                if dtype is not None:
                    t = t.to(dtype)
                return t

            def zeros(self, shape, dtype=None):
                kw = {"dtype": dtype or torch.int64, "device": self._dev}
                return torch.zeros(shape, **kw)

            # ── Math ops ──────────────────────────────────────────────────
            def floor(self, t):
                return torch.floor(t)

            def sqrt(self, t):
                return torch.sqrt(t)

            def any(self, t):
                return bool(t.any())

            def where(self, cond):
                return torch.where(cond)

            # ── .get() helper so caller can call .get() on results ────────
            @staticmethod
            def _wrap(t):
                return _TorchArrayWrapper(t)

        class _TorchArrayWrapper:
            """Wrap a torch tensor so .get() returns a numpy array."""
            def __init__(self, t):
                self._t = t

            def __getitem__(self, idx):
                return _TorchArrayWrapper(self._t[idx])

            def __len__(self):
                return len(self._t)

            def get(self):
                return self._t.cpu().numpy()

            # forward arithmetic operators to underlying tensor
            def __add__(self, o):
                return _TorchArrayWrapper(self._t + (o._t if isinstance(o, _TorchArrayWrapper) else o))
            def __sub__(self, o):
                return _TorchArrayWrapper(self._t - (o._t if isinstance(o, _TorchArrayWrapper) else o))
            def __mul__(self, o):
                return _TorchArrayWrapper(self._t * (o._t if isinstance(o, _TorchArrayWrapper) else o))
            def __eq__(self, o):
                return _TorchArrayWrapper(self._t == (o._t if isinstance(o, _TorchArrayWrapper) else o))
            def __or__(self, o):
                return _TorchArrayWrapper(self._t | (o._t if isinstance(o, _TorchArrayWrapper) else o))
            def __invert__(self):
                return _TorchArrayWrapper(~self._t)
            def __pow__(self, n):
                return _TorchArrayWrapper(self._t ** n)
            def __radd__(self, o):
                return _TorchArrayWrapper(o + self._t)
            def __rsub__(self, o):
                return _TorchArrayWrapper(o - self._t)
            def __rmul__(self, o):
                return _TorchArrayWrapper(o * self._t)
            def astype(self, dtype):
                return _TorchArrayWrapper(self._t.to(dtype))
            def all(self):
                return bool(self._t.all())
            def __bool__(self):
                return bool(self._t)

        dev = torch.device("cuda")
        torch.tensor([1], dtype=torch.int64, device=dev)  # test
        xp = _TorchXP(dev)
        xp._torch = torch
        xp._dev = dev
        return xp
    except Exception:
        return None


def detect_backend() -> tuple:
    """Return (xp, backend_name, is_gpu).

    xp is the array module to use (cupy / torch-wrapper / numpy).
    """
    cp = _try_cupy()
    if cp is not None:
        # Distinguish CUDA vs ROCm via driver info
        try:
            name = cp.cuda.runtime.getDeviceProperties(0)["name"].decode()
        except Exception:
            name = "GPU"
        return cp, f"CuPy — {name}", True

    txp = _try_torch()
    if txp is not None:
        try:
            import torch
            name = torch.cuda.get_device_name(0)
        except Exception:
            name = "GPU"
        return txp, f"PyTorch ROCm/CUDA — {name}", True

    return np, "NumPy (CPU fallback — no GPU found)", False


# ── Core per-triple GPU search ────────────────────────────────────────────────

def _isqrt_gpu(xp, t):
    """Vectorized perfect-square check.  Returns (ok_mask, s_array)."""
    s = _xp_cast(xp.floor(xp.sqrt(_xp_cast(t, xp.float64))), xp.int64)
    ok = (s * s == t) | ((s + 1) * (s + 1) == t)
    return ok, s


def _search_triple_gpu(
    xp,
    p: int, q: int, r: int,
    a_dev, b_dev,
    min_rational: int,
    inside_only: bool = False,
) -> list[dict]:
    """Process one Pythagorean triple entirely on the GPU/array backend.

    a_dev / b_dev are device arrays (cupy / torch-wrapper / numpy).
    Returns raw dicts compatible with _raw_to_point in search.py.
    """
    # Exclude x=1 (a*p == b*r) and y=1 (a*q == b*r) — theorem-required filter
    off = ~((a_dev * p == b_dev * r) | (a_dev * q == b_dev * r))
    if inside_only:
        # x<1 iff a*p < b*r;  y<1 iff a*q < b*r
        off = off & (a_dev * p < b_dev * r) & (a_dev * q < b_dev * r)
    a = a_dev[off]
    b = b_dev[off]
    if len(a) == 0:
        return []

    ar = a * r
    bp = b * p
    bq = b * q
    br = b * r

    tB = (ar - bp) ** 2 + bq ** 2
    tD = (ar - bq) ** 2 + bp ** 2
    tC = (ar - b * (p + q)) ** 2 + (b * (p - q)) ** 2

    okB, sB = _isqrt_gpu(xp, tB)
    okD, sD = _isqrt_gpu(xp, tD)
    okC, sC = _isqrt_gpu(xp, tC)

    cnt = (1
           + _xp_cast(okB, xp.int64)
           + _xp_cast(okD, xp.int64)
           + _xp_cast(okC, xp.int64))
    mask = cnt >= min_rational

    if not xp.any(mask):
        return []

    idx = xp.where(mask)[0]

    # ── Transfer hits back to CPU (hits are rare → cheap) ─────────────────
    def _to_cpu(arr):
        sliced = arr[idx]
        if hasattr(sliced, "get"):          # CuPy
            return sliced.get()
        if hasattr(sliced, "cpu"):          # PyTorch tensor
            return sliced.cpu().numpy()
        return np.asarray(sliced)           # NumPy

    a_hit   = _to_cpu(a)
    b_hit   = _to_cpu(b)
    br_hit  = _to_cpu(br)
    sB_hit  = _to_cpu(sB)
    sD_hit  = _to_cpu(sD)
    sC_hit  = _to_cpu(sC)
    okB_hit = _to_cpu(okB)
    okD_hit = _to_cpu(okD)
    okC_hit = _to_cpu(okC)

    results: list[dict] = []
    seen: set[tuple] = set()

    for i in range(len(a_hit)):
        ai, bi = int(a_hit[i]), int(b_hit[i])
        bri = int(br_hit[i])

        xn, xd = ai * p, bri
        g = gcd(xn, xd); xn //= g; xd //= g
        yn, yd = ai * q, bri
        g = gcd(yn, yd); yn //= g; yd //= g

        key = (xn, xd, yn, yd)
        if key in seen:
            continue
        seen.add(key)

        results.append({
            "x":  (xn, xd),
            "y":  (yn, yd),
            "dA": (ai, bi),
            "dB": (int(sB_hit[i]), bri) if bool(okB_hit[i]) else None,
            "dC": (int(sC_hit[i]), bri) if bool(okC_hit[i]) else None,
            "dD": (int(sD_hit[i]), bri) if bool(okD_hit[i]) else None,
        })

    return results


# ── Public GPU search ─────────────────────────────────────────────────────────

def parametric_search_gpu(
    max_m: int = 80,
    max_k_num: int = 640,
    max_k_den: int = 320,
    min_rational: int = 3,
    progress: bool = True,
    xp=None,
    inside_only: bool = False,
) -> tuple[list[RationalPoint], str]:
    """GPU-accelerated parametric search (single process).

    Returns (points, backend_name).

    Parameters
    ----------
    max_m        : Pythagorean triple generation limit
    max_k_num    : max numerator of k = a/b
    max_k_den    : max denominator of k
    min_rational : minimum rational distances required (3 or 4)
    progress     : show tqdm progress bar
    xp           : override backend (e.g. pass numpy for testing)
    """
    INT64_MAX = 9_223_372_036_854_775_807
    # Rough upper-bound on tB for the given params: (max_k_num * max_r)^2
    # where max_r ≈ 2*max_m^2.  Warn if potentially unsafe.
    approx_max_r = 2 * max_m ** 2
    approx_tB_max = (max_k_num * approx_max_r) ** 2
    if approx_tB_max > INT64_MAX:
        print(
            f"[WARNING] scale may exceed int64 range "
            f"(estimated tB_max ≈ {approx_tB_max:.2e} > {INT64_MAX:.2e}).\n"
            f"          Results above scale ≈ 600 may be incorrect.",
            file=sys.stderr,
        )

    if xp is None:
        xp, backend_name, _ = detect_backend()
    else:
        backend_name = type(xp).__name__

    # Build coprime (a,b) pair arrays once on CPU, then transfer to device
    a_cpu = []
    b_cpu = []
    for b in range(1, max_k_den + 1):
        for a in range(1, max_k_num + 1):
            if gcd(a, b) == 1:
                a_cpu.append(a)
                b_cpu.append(b)
    a_np = np.array(a_cpu, dtype=np.int64)
    b_np = np.array(b_cpu, dtype=np.int64)

    # Upload to device (no-op for numpy or unified-memory APUs)
    a_dev = xp.array(a_np, dtype=xp.int64)
    b_dev = xp.array(b_np, dtype=xp.int64)

    triples = primitive_pythagorean_triples(max_m)

    if progress:
        try:
            from tqdm import tqdm
            it = tqdm(triples, desc="Searching", unit="triple")
        except ImportError:
            it = triples
    else:
        it = triples

    raw: list[dict] = []
    seen_xy: set[tuple] = set()

    for p, q, r in it:
        hits = _search_triple_gpu(xp, p, q, r, a_dev, b_dev, min_rational, inside_only)
        for h in hits:
            key = (h["x"], h["y"])
            if key not in seen_xy:
                seen_xy.add(key)
                raw.append(h)

    # Convert raw dicts → RationalPoint
    def _to_point(d: dict) -> RationalPoint:
        return RationalPoint(
            x=Fraction(*d["x"]),
            y=Fraction(*d["y"]),
            distances=(
                Fraction(*d["dA"]),
                Fraction(*d["dB"]) if d["dB"] else None,
                Fraction(*d["dC"]) if d["dC"] else None,
                Fraction(*d["dD"]) if d["dD"] else None,
            ),
        )

    points = [_to_point(d) for d in raw]
    points.sort(key=lambda pt: (
        -pt.rational_count,
        pt.denominator,
        pt.x,
        pt.y,
    ))
    return points, backend_name
