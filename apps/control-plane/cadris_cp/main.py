from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import settings
from .database import engine
from .errors import AppError
from .exception_handlers import (
    app_error_handler,
    ensure_request_id,
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from .migrations import run_sql_migrations
from .repository import ControlPlaneRepository
from .routers import (
    auth,
    billing,
    dossiers,
    generation,
    missions,
    projects,
    shared,
    templates,
    uploads,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    run_sql_migrations(engine, Path(__file__).resolve().parent.parent / "sql")
    from sqlalchemy.orm import Session as _Session

    # ── Env-var sanity checks ──────────────────────────────────
    if not settings.trusted_proxy_secret and not settings.allow_unsigned_requests:
        logger.warning(
            "CONTROL_PLANE_TRUSTED_PROXY_SECRET not set and "
            "CADRIS_ALLOW_UNSIGNED_REQUESTS is false — all authenticated "
            "requests will be rejected"
        )
    if settings.stripe_secret_key and not settings.stripe_webhook_secret:
        logger.warning(
            "STRIPE_WEBHOOK_SECRET not set — webhook endpoint will reject all events"
        )

    with _Session(engine) as startup_session:
        repo = ControlPlaneRepository(startup_session)
        recovered = repo.recover_stale_runs()
        if recovered:
            logger.info("recovered %d stale agent run(s) at startup", recovered)
    yield


app = FastAPI(title="Cadris Control Plane", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = ensure_request_id(request)
    start = time.perf_counter()
    response: Response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 1)
    response.headers["x-request-id"] = request_id
    logger.info(
        "request completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "request_id": request_id,
        },
    )
    return response


app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# ── Routers ────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(billing.router)
app.include_router(templates.router)
app.include_router(projects.router)
app.include_router(missions.router)
app.include_router(generation.router)
app.include_router(dossiers.router)
app.include_router(uploads.router)
app.include_router(shared.router)


@app.get("/health")
async def healthcheck():
    return {"ok": True}
