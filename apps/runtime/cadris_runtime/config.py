from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field

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


settings = Settings()
