from __future__ import annotations

import os

# Force local provider for tests — must happen before any app import
os.environ.setdefault("CADRIS_RUNTIME_PROVIDER", "local")
os.environ.setdefault("CADRIS_MODEL_PROFILE", "dev")
os.environ.setdefault("CADRIS_TRAINING_ENABLED", "false")

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    return TestClient(app)
