"""Root conftest — ensures both service packages are importable when running
``python -m pytest apps/runtime/tests apps/control-plane/tests`` from the
repository root.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Allow unsigned requests in test mode (fail-closed in prod)
os.environ.setdefault("CADRIS_ALLOW_UNSIGNED_REQUESTS", "true")
os.environ.setdefault("CADRIS_LOAD_DOTENV", "0")

_REPO = Path(__file__).resolve().parent

for _service_dir in ("apps/control-plane", "apps/runtime", "apps/renderer"):
    _path = str(_REPO / _service_dir)
    if _path not in sys.path:
        sys.path.insert(0, _path)
