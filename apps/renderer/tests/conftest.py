"""Renderer test configuration — ensure app package is importable."""
from __future__ import annotations

import os
import sys
from pathlib import Path

# The /internal/* endpoints are fail-closed; allow unsigned calls in tests.
os.environ.setdefault("CADRIS_ALLOW_UNSIGNED_REQUESTS", "true")

_renderer_dir = str(Path(__file__).resolve().parent.parent)
if _renderer_dir not in sys.path:
    sys.path.insert(0, _renderer_dir)
