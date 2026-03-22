from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from pydantic import BeforeValidator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load local .env BEFORE any other module import, so that database.py
# (and others) can read env vars set in .env.
# Tests opt out with CADRIS_LOAD_DOTENV=0 for hermetic runs.
if os.getenv("CADRIS_LOAD_DOTENV", "1") != "0":
    load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)

# Import AFTER load_dotenv so DATABASE_URL picks up .env values.
from .database import DATABASE_URL  # noqa: E402


def _parse_origins(v: str | list[str]) -> list[str]:
    if isinstance(v, list):
        return v
    return [s.strip() for s in v.split(",") if s.strip()]


def _default_uploads_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "uploads"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="",  # no prefix — env var names are explicit per field
        env_file=None,  # already loaded above via load_dotenv
        extra="ignore",
    )

    runtime_url: str = Field(default="http://127.0.0.1:8001", alias="CONTROL_PLANE_RUNTIME_URL")
    renderer_url: str = Field(default="http://127.0.0.1:8002", alias="CONTROL_PLANE_RENDERER_URL")
    trusted_proxy_secret: str | None = Field(default=None, alias="CONTROL_PLANE_TRUSTED_PROXY_SECRET")
    allow_unsigned_requests: bool = Field(default=False, alias="CADRIS_ALLOW_UNSIGNED_REQUESTS")
    trusted_proxy_max_skew_seconds: int = Field(default=60, alias="CONTROL_PLANE_TRUSTED_PROXY_MAX_SKEW_SECONDS")

    allowed_origins: Annotated[list[str], BeforeValidator(_parse_origins)] = Field(
        default="http://127.0.0.1:3000,http://localhost:3000,http://127.0.0.1:3001,http://localhost:3001",
        alias="CONTROL_PLANE_ALLOWED_ORIGINS",
    )
    database_url: str = Field(default=DATABASE_URL)
    uploads_dir: Path = Field(default_factory=_default_uploads_dir, alias="CONTROL_PLANE_UPLOADS_DIR")
    max_upload_bytes: int = Field(default=5_242_880, alias="CONTROL_PLANE_MAX_UPLOAD_BYTES")
    s3_bucket: str | None = Field(default=None, alias="CONTROL_PLANE_S3_BUCKET")
    s3_endpoint: str | None = Field(default=None, alias="CONTROL_PLANE_S3_ENDPOINT")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    # Stripe billing
    stripe_secret_key: str | None = Field(default=None, alias="STRIPE_SECRET_KEY")
    stripe_webhook_secret: str | None = Field(default=None, alias="STRIPE_WEBHOOK_SECRET")
    stripe_price_starter: str | None = Field(default=None, alias="STRIPE_PRICE_STARTER")
    stripe_price_pro: str | None = Field(default=None, alias="STRIPE_PRICE_PRO")
    stripe_price_expert: str | None = Field(default=None, alias="STRIPE_PRICE_EXPERT")
    frontend_url: str = Field(default="http://localhost:3000", alias="FRONTEND_URL")

    # Resend (for password reset emails)
    resend_api_key: str | None = Field(default=None, alias="RESEND_API_KEY")


settings = Settings()
