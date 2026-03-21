"""Prompt loading helpers and flow-label constants."""

from __future__ import annotations

from ..prompt_loader import load_prompt

__all__ = [
    "load_prompt",
    "FLOW_LABELS",
    "FLOW_DOSSIER_TITLES",
    "MAX_CYCLES",
    "_prompt_key",
]

MAX_CYCLES = 3

FLOW_LABELS: dict[str, str] = {
    "demarrage": "Demarrage",
    "projet_flou": "Recadrage",
    "pivot": "Pivot",
}

FLOW_DOSSIER_TITLES: dict[str, str] = {
    "demarrage": "Dossier d'execution - Demarrage",
    "projet_flou": "Dossier de recadrage",
    "pivot": "Dossier de pivot",
}


def _prompt_key(flow_code: str, role: str, stage: str) -> str:
    return f"{flow_code}/{role}/{stage}"
