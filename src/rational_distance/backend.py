"""GPU / array-backend detection for the rational-distance search.

Probes for CuPy (CUDA/ROCm) and PyTorch (ROCm/CUDA) at runtime, falling
back to NumPy (CPU) when neither is available.

Public API
──────────
  detect_backend() → (xp, backend_name, is_gpu)
  _try_cupy()      → cupy module or None
  _try_torch()     → _TorchXP wrapper or None
  _xp_cast(t, dtype) → dtype-cast array, works for numpy/cupy/torch

The _TorchXP class wraps PyTorch so the search code can call a numpy-like
API (xp.array, xp.sqrt, xp.where, …) without knowing about torch internals.
Array objects returned by arithmetic are plain torch tensors; use _xp_cast
to cast them between dtypes in a backend-agnostic way.
"""

from __future__ import annotations

import numpy as np


def _xp_cast(t, dtype):
    """Cast array *t* to *dtype*, compatible with NumPy, CuPy, and PyTorch.

    NumPy / CuPy use  .astype(dtype).
    PyTorch tensors   use  .to(dtype).
    """
    if isinstance(t, np.ndarray):
        return t.astype(dtype)
    if hasattr(t, "to") and not hasattr(t, "astype"):  # PyTorch tensor
        return t.to(dtype)
    return t.astype(dtype)  # CuPy


# ── Backend probes ────────────────────────────────────────────────────────────


def _try_cupy():
    """Return the CuPy module if a GPU device is accessible, else None."""
    try:
        import cupy as cp

        cp.array([1], dtype=cp.int64)  # triggers device init; fails if no GPU
        return cp
    except Exception:
        return None


def _try_torch():
    """Return a _TorchXP namespace if PyTorch ROCm/CUDA is available, else None.

    Wraps torch so callers can use a numpy-like API:
      xp.array(x, dtype=xp.int64)
      xp.sqrt(t)  /  xp.floor(t)  /  xp.any(t)  /  xp.where(cond)
    Raw arithmetic on tensors returns plain torch tensors; cast with _xp_cast.
    """
    try:
        import torch

        if not torch.cuda.is_available():
            return None

        class _TorchXP:
            """Minimal numpy-compatible namespace for torch CUDA/ROCm tensors."""

            def __init__(self, device):
                self._dev = device
                self.int64 = torch.int64
                self.float64 = torch.float64

            # ── Array creation ────────────────────────────────────────────
            def array(self, x, dtype=None):
                t = torch.from_numpy(x) if isinstance(x, np.ndarray) else torch.tensor(x)
                t = t.to(self._dev)
                return t.to(dtype) if dtype is not None else t

            def zeros(self, shape, dtype=None):
                return torch.zeros(shape, dtype=dtype or torch.int64, device=self._dev)

            # ── Math ops ──────────────────────────────────────────────────
            def floor(self, t):
                return torch.floor(t)

            def sqrt(self, t):
                return torch.sqrt(t)

            def any(self, t):
                return bool(t.any())

            def where(self, cond):
                return torch.where(cond)

        dev = torch.device("cuda")
        torch.tensor([1], dtype=torch.int64, device=dev)  # verify device works
        xp = _TorchXP(dev)
        xp._torch = torch
        xp._dev = dev
        return xp
    except Exception:
        return None


# ── Public entry point ────────────────────────────────────────────────────────


def detect_backend() -> tuple:
    """Auto-detect the best available array backend.

    Returns
    -------
    (xp, backend_name, is_gpu)
      xp           — array module (cupy / _TorchXP / numpy)
      backend_name — human-readable string for display
      is_gpu       — True if a real GPU is being used
    """
    cp = _try_cupy()
    if cp is not None:
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
