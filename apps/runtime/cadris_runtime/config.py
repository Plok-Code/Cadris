from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field, model_validator

logger = logging.getLogger(__name__)

# Load .env from the runtime app directory
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path, override=False)


class Settings(BaseModel):
    provider: Literal["local", "openai", "collaborative"] = Field(
        default=os.getenv("CADRIS_RUNTIME_PROVIDER", "local")
    )
    state_store_url: str | None = Field(
        default=os.getenv("CADRIS_RUNTIME_STATE_DB_URL") or os.getenv("CONTROL_PLANE_DATABASE_URL")
    )
    state_store_dir: Path = Field(
        default=Path(
            os.getenv(
                "CADRIS_RUNTIME_STATE_DIR",
                Path(__file__).resolve().parent.parent / "data" / "mission-state",
            )
        )
    )
    openai_model: str = Field(default=os.getenv("CADRIS_OPENAI_MODEL", "gpt-4.1-nano"))
    openai_api_key: str | None = Field(default=os.getenv("OPENAI_API_KEY"))
    together_api_key: str | None = Field(default=os.getenv("TOGETHER_API_KEY"))
    perplexity_api_key: str | None = Field(default=os.getenv("PERPLEXITY_API_KEY"))
    model_profile: Literal["dev", "prod"] = Field(
        default=os.getenv("CADRIS_MODEL_PROFILE", "dev")
    )
    internal_secret: str | None = Field(
        default_factory=lambda: os.getenv("CADRIS_INTERNAL_SECRET") or None
    )
    allow_unsigned_requests: bool = Field(
        default_factory=lambda: os.getenv("CADRIS_ALLOW_UNSIGNED_REQUESTS", "").lower() == "true"
    )

    @model_validator(mode="after")
    def _warn_missing_api_keys(self) -> Settings:
        """Log warnings at config time if required API keys are missing.

        This surfaces misconfigurations early (at import time) rather than
        failing mid-mission when an agent tries to call the provider.
        """
        if self.model_profile == "prod":
            if not self.internal_secret:
                logger.warning(
                    "CADRIS_INTERNAL_SECRET not set in prod profile — "
                    "runtime endpoints are UNPROTECTED"
                )
            if not self.openai_api_key:
                logger.warning(
                    "OPENAI_API_KEY not set in prod profile — "
                    "paid plan agents will fail"
                )
            if not self.together_api_key:
                logger.warning(
                    "TOGETHER_API_KEY not set in prod profile — "
                    "free plan agents will fail"
                )
        return self


settings = Settings()
