from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from .database import DATABASE_URL

# Load .env from the control-plane root directory
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


class Settings(BaseModel):
    runtime_url: str = Field(default=os.getenv("CONTROL_PLANE_RUNTIME_URL", "http://127.0.0.1:8001"))
    renderer_url: str = Field(default=os.getenv("CONTROL_PLANE_RENDERER_URL", "http://127.0.0.1:8002"))
    trusted_proxy_secret: str | None = Field(default=os.getenv("CONTROL_PLANE_TRUSTED_PROXY_SECRET", None))
    trusted_proxy_max_skew_seconds: int = Field(
        default=int(os.getenv("CONTROL_PLANE_TRUSTED_PROXY_MAX_SKEW_SECONDS", "300"))
    )
    allowed_origins: list[str] = Field(
        default_factory=lambda: os.getenv(
            "CONTROL_PLANE_ALLOWED_ORIGINS",
            "http://127.0.0.1:3000,http://localhost:3000,http://127.0.0.1:3001,http://localhost:3001",
        ).split(",")
    )
    database_url: str = Field(default=DATABASE_URL)
    uploads_dir: Path = Field(
        default=Path(os.getenv("CONTROL_PLANE_UPLOADS_DIR", Path(__file__).resolve().parent.parent / "data" / "uploads"))
    )
    max_upload_bytes: int = Field(default=int(os.getenv("CONTROL_PLANE_MAX_UPLOAD_BYTES", "5242880")))
    s3_bucket: str | None = Field(default=os.getenv("CONTROL_PLANE_S3_BUCKET", None))
    s3_endpoint: str | None = Field(default=os.getenv("CONTROL_PLANE_S3_ENDPOINT", None))
    openai_api_key: str | None = Field(default=os.getenv("OPENAI_API_KEY", None))

    # Stripe billing
    stripe_secret_key: str | None = Field(default=os.getenv("STRIPE_SECRET_KEY", None))
    stripe_webhook_secret: str | None = Field(default=os.getenv("STRIPE_WEBHOOK_SECRET", None))
    stripe_price_starter: str | None = Field(default=os.getenv("STRIPE_PRICE_STARTER", None))
    stripe_price_pro: str | None = Field(default=os.getenv("STRIPE_PRICE_PRO", None))
    stripe_price_expert: str | None = Field(default=os.getenv("STRIPE_PRICE_EXPERT", None))
    frontend_url: str = Field(default=os.getenv("FRONTEND_URL", "http://localhost:3000"))

    # Resend (for password reset emails)
    resend_api_key: str | None = Field(default=os.getenv("RESEND_API_KEY", None))


settings = Settings()
