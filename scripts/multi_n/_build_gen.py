"""Build the Cython concordant-generation kernel in place.

    uv run python scripts/multi_n/_build_gen.py build_ext --inplace

Produces `_concordant_gen*.so` next to the .pyx. The .so is platform-specific
and intentionally not committed; rebuild it on each machine.
"""

import glob
import shutil
from pathlib import Path

import numpy as np
from Cython.Build import cythonize
from setuptools import Extension, setup

HERE = Path(__file__).resolve().parent

ext = Extension(
    "_concordant_gen",
    ["scripts/multi_n/_concordant_gen.pyx"],
    include_dirs=[np.get_include()],
    extra_compile_args=["-O3"],
)

setup(
    name="_concordant_gen",
    ext_modules=cythonize([ext], language_level="3"),
    script_args=["build_ext", "--inplace"],
)

# setuptools' --inplace may drop the .so under src/ (auto-discovered package);
# move it next to this build script so the scanner can import it.
for so in glob.glob("**/_concordant_gen*.so", recursive=True):
    sop = Path(so).resolve()
    if "build" in sop.parts or sop.parent == HERE:
        continue
    dest = HERE / sop.name
    shutil.move(str(sop), str(dest))
    print(f"moved {so} -> {dest}")

