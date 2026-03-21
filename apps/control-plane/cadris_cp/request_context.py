from __future__ import annotations

from contextvars import ContextVar

_request_id_var: ContextVar[str | None] = ContextVar("cadris_request_id", default=None)


def set_request_id(value: str) -> None:
    _request_id_var.set(value)


def get_request_id() -> str:
    return _request_id_var.get() or "req_unknown"
