"""
Rational distance to unit square vertices.

Modules:
  math_utils    – rational arithmetic helpers (rational_sqrt, primitive triples)
  square        – unit-square distance checker & RationalPoint type
  backend       – GPU/array-backend detection (CuPy, PyTorch, NumPy)
  search        – CPU search strategies (parametric fast, brute-force, dedup)
  search_gpu    – GPU-accelerated search (single process, vectorised)
"""
