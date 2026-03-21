"""Shared fixtures for control-plane tests.

Uses FastAPI dependency_overrides to inject an in-memory SQLite session.
The StaticPool ensures all connections share the same in-memory database.
"""
from __future__ import annotations

import os
import pytest
from pathlib import Path
from uuid import uuid4
os.environ.setdefault("CADRIS_LOAD_DOTENV", "0")
os.environ.setdefault("CONTROL_PLANE_TRUSTED_PROXY_SECRET", "")

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from cadris_cp.main import app
from cadris_cp.database import get_session
from cadris_cp.migrations import run_sql_migrations

# Create an isolated in-memory SQLite engine for tests.
# StaticPool ensures all connections share the same in-memory DB.
_test_engine = create_engine(
    "sqlite://",
    future=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@event.listens_for(_test_engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


_TestSession = sessionmaker(bind=_test_engine, autoflush=False, autocommit=False, expire_on_commit=False)

# Run migrations on the test engine
_sql_dir = Path(__file__).resolve().parent.parent / "sql"
run_sql_migrations(_test_engine, _sql_dir)


def _get_test_session():
    session = _TestSession()
    try:
        yield session
    finally:
        session.close()


# Override the real get_session with our test one
app.dependency_overrides[get_session] = _get_test_session


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def auth_headers():
    return {"x-cadris-user-id": f"test-{uuid4().hex[:12]}"}
