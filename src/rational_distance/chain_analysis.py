"""Deprecated stub. Real implementation: rational_distance._legacy.chain_analysis.

Round-2 archive (wl053) moved the chain-fast / EC / parametric era modules
into the _legacy package. This top-level file replaces itself with the
real module so historical imports (including private `_underscore` names)
keep working. New code should import from _legacy.chain_analysis directly.
"""

import sys

from rational_distance._legacy import chain_analysis as _impl

sys.modules[__name__] = _impl
