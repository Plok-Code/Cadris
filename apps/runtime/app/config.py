from __future__ import annotations

import os
from typing import Literal

from pydantic import BaseModel, Field


class Settings(BaseModel):
    provider: Literal["local", "openai"] = Field(default=os.getenv("CADRIS_RUNTIME_PROVIDER", "local"))
    openai_model: str = Field(default=os.getenv("CADRIS_OPENAI_MODEL", "gpt-5-mini"))
    openai_api_key: str | None = Field(default=os.getenv("OPENAI_API_KEY"))


settings = Settings()
