from __future__ import annotations

import os
from pathlib import Path
from pydantic import BaseModel, Field
from .database import DATABASE_URL


class Settings(BaseModel):
    runtime_url: str = Field(default=os.getenv("CONTROL_PLANE_RUNTIME_URL", "http://127.0.0.1:8001"))
    renderer_url: str = Field(default=os.getenv("CONTROL_PLANE_RENDERER_URL", "http://127.0.0.1:8002"))
    allowed_origins: list[str] = Field(
        default_factory=lambda: os.getenv(
            "CONTROL_PLANE_ALLOWED_ORIGINS",
            "http://127.0.0.1:3000,http://localhost:3000",
        ).split(",")
    )
    database_url: str = Field(default=DATABASE_URL)
    uploads_dir: Path = Field(
        default=Path(os.getenv("CONTROL_PLANE_UPLOADS_DIR", Path(__file__).resolve().parent.parent / "data" / "uploads"))
    )
    max_upload_bytes: int = Field(default=int(os.getenv("CONTROL_PLANE_MAX_UPLOAD_BYTES", "5242880")))
    s3_bucket: str | None = Field(default=os.getenv("CONTROL_PLANE_S3_BUCKET", None))
    s3_endpoint: str | None = Field(default=os.getenv("CONTROL_PLANE_S3_ENDPOINT", None))


settings = Settings()
