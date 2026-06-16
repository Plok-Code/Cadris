from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class PromptTemplate:
    key: str
    version: str
    instructions: str


PROMPT_PATHS: dict[str, Path] = {
    # ── Legacy per-flow prompts ──────────────────────────────
    # Demarrage
    "demarrage/supervisor/start": Path("demarrage/supervisor_start.md"),
    "demarrage/supervisor/resume": Path("demarrage/supervisor_resume.md"),
    "demarrage/strategy/core": Path("demarrage/strategy_agent.md"),
    "demarrage/product/core": Path("demarrage/product_agent.md"),
    # Projet flou
    "projet_flou/supervisor/start": Path("projet_flou/supervisor_start.md"),
    "projet_flou/supervisor/resume": Path("projet_flou/supervisor_resume.md"),
    "projet_flou/strategy/core": Path("projet_flou/strategy_agent.md"),
    "projet_flou/product/core": Path("projet_flou/product_agent.md"),
    # Pivot
    "pivot/supervisor/start": Path("pivot/supervisor_start.md"),
    "pivot/supervisor/resume": Path("pivot/supervisor_resume.md"),
    "pivot/strategy/core": Path("pivot/strategy_agent.md"),
    "pivot/product/core": Path("pivot/product_agent.md"),
    # ── Collaborative agent prompts (universal, not per-flow) ─
    "agents/strategy_agent": Path("agents/strategy_agent.md"),
    "agents/product_agent": Path("agents/product_agent.md"),
    "agents/tech_agent": Path("agents/tech_agent.md"),
    "agents/design_agent": Path("agents/design_agent.md"),
    "agents/business_agent": Path("agents/business_agent.md"),
    "agents/consolidation_agent": Path("agents/consolidation_agent.md"),
    "agents/critic_agent": Path("agents/critic_agent.md"),
    "agents/qualifier_agent": Path("agents/qualifier_agent.md"),
}


def prompts_root() -> Path:
    return Path(__file__).resolve().parents[3] / "packages" / "prompts"


def _prompt_reload_enabled() -> bool:
    """Dev-only: re-read prompt files when they change on disk.

    Off by default (prod keeps a permanent cache — a redeploy is required
    after editing a prompt). Set CADRIS_PROMPT_RELOAD_ENABLED=true locally to
    pick up edits without restarting the server.
    """
    return os.getenv("CADRIS_PROMPT_RELOAD_ENABLED", "").lower() in ("true", "1", "yes")


@lru_cache(maxsize=None)
def _load_prompt_cached(key: str, _mtime: float) -> PromptTemplate:
    """Load + parse a prompt. Cache key includes the file mtime so that, when
    reload is enabled, an edited file produces a new key and is re-read."""
    relative_path = PROMPT_PATHS.get(key)
    if relative_path is None:
        raise KeyError(f"Unknown prompt key: {key}")

    raw = (prompts_root() / relative_path).read_text(encoding="utf-8")

    parts = raw.split("---\n", maxsplit=1)
    if len(parts) != 2:
        raise ValueError(
            f"Prompt {key!r} is missing the '---' metadata separator."
        )
    metadata, instructions = parts

    values: dict[str, str] = {}
    for line in metadata.strip().splitlines():
        if ":" not in line:
            continue
        meta_key, meta_value = line.split(":", maxsplit=1)
        values[meta_key.strip()] = meta_value.strip()

    return PromptTemplate(
        key=values.get("key", key),
        version=values.get("version", "v1"),
        instructions=instructions.strip(),
    )


def load_prompt(key: str) -> PromptTemplate:
    """Return a parsed prompt template, cached permanently in prod.

    In dev (CADRIS_PROMPT_RELOAD_ENABLED), the file mtime is folded into the
    cache key so edits take effect without a restart.
    """
    relative_path = PROMPT_PATHS.get(key)
    if relative_path is None:
        raise KeyError(f"Unknown prompt key: {key}")

    mtime = 0.0
    if _prompt_reload_enabled():
        try:
            mtime = (prompts_root() / relative_path).stat().st_mtime
        except OSError:
            mtime = 0.0
    return _load_prompt_cached(key, mtime)


def reload_prompts() -> None:
    """Clear the prompt cache (e.g. from an internal ops/reload endpoint)."""
    _load_prompt_cached.cache_clear()
