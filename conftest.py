"""Root conftest — ensures both service packages are importable when running
``python -m pytest apps/runtime/tests apps/control-plane/tests`` from the
repository root.
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent

for _service_dir in ("apps/control-plane", "apps/runtime"):
    _path = str(_REPO / _service_dir)
    if _path not in sys.path:
        sys.path.insert(0, _path)
