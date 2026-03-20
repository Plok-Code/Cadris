"""Training data logger — saves every mission run for future fine-tuning.

Stores JSONL files in data/training/ with one line per event:
- mission_start: intake, qualification, plan, model selections
- document: each document with full prompt, model, tokens
- critic: critic scores and reviews per wave
- mission_complete: final state, timing, plan
- feedback: user ratings and corrections

This data is the foundation for training custom models:
- SFT (supervised fine-tuning): prompt → output pairs
- DPO: critic scores as preference signal
- Distillation: Opus/GPT-4.1 outputs to train smaller models
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, UTC
from pathlib import Path

logger = logging.getLogger(__name__)

# Store in project root / data / training
DATA_DIR = Path(__file__).parent.parent.parent.parent / "data" / "training"
DATA_DIR.mkdir(parents=True, exist_ok=True)

EVENTS_FILE = DATA_DIR / "events.jsonl"
FEEDBACK_FILE = DATA_DIR / "feedback.jsonl"


def _append_jsonl(filepath: Path, data: dict) -> None:
    """Append one JSON line to a file."""
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False, default=str) + "\n")
    except Exception as e:
        logger.warning("training_logger write failed: %s", e)


def log_mission_start(
    mission_id: str,
    intake_text: str,
    qualification_questions: list[dict],
    qualification_answers: dict[str, str],
    *,
    plan: str = "free",
) -> None:
    """Log when a mission starts with full intake context."""
    _append_jsonl(EVENTS_FILE, {
        "type": "mission_start",
        "timestamp": datetime.now(UTC).isoformat(),
        "mission_id": mission_id,
        "plan": plan,
        "intake_text": intake_text,
        "qualification_questions": qualification_questions,
        "qualification_answers": qualification_answers,
    })


def log_document(
    mission_id: str,
    doc_id: str,
    agent: str,
    title: str,
    content: str,
    certainty: str,
    wave: int,
    *,
    plan: str = "free",
    model: str = "",
    provider: str = "",
    prompt_sent: str = "",
    attempt: int = 1,
    is_fallback: bool = False,
    elapsed_ms: int = 0,
) -> None:
    """Log each document produced by an agent with full context for fine-tuning."""
    _append_jsonl(EVENTS_FILE, {
        "type": "document",
        "timestamp": datetime.now(UTC).isoformat(),
        "mission_id": mission_id,
        "plan": plan,
        "doc_id": doc_id,
        "agent": agent,
        "title": title,
        "content": content,
        "certainty": certainty,
        "wave": wave,
        "content_length": len(content),
        "model": model,
        "provider": provider,
        "prompt_sent": prompt_sent,
        "attempt": attempt,
        "is_fallback": is_fallback,
        "elapsed_ms": elapsed_ms,
    })


def log_critic(
    mission_id: str,
    wave: int,
    overall_quality: str,
    reviews: list[dict],
    questions_for_user: list[str],
    synthesis: str,
    *,
    plan: str = "free",
    model: str = "",
    provider: str = "",
) -> None:
    """Log critic evaluation — key data for DPO and preference training."""
    _append_jsonl(EVENTS_FILE, {
        "type": "critic",
        "timestamp": datetime.now(UTC).isoformat(),
        "mission_id": mission_id,
        "plan": plan,
        "wave": wave,
        "overall_quality": overall_quality,
        "reviews": reviews,
        "questions_for_user": questions_for_user,
        "synthesis": synthesis,
        "model": model,
        "provider": provider,
    })


def log_mission_complete(
    mission_id: str,
    total_documents: int,
    total_errors: int,
    elapsed_seconds: float,
    *,
    plan: str = "free",
) -> None:
    """Log mission completion with summary stats."""
    _append_jsonl(EVENTS_FILE, {
        "type": "mission_complete",
        "timestamp": datetime.now(UTC).isoformat(),
        "mission_id": mission_id,
        "plan": plan,
        "total_documents": total_documents,
        "total_errors": total_errors,
        "elapsed_seconds": elapsed_seconds,
    })


def log_feedback(
    mission_id: str,
    doc_id: str | None,
    rating: int,
    correction: str = "",
    notes: str = "",
) -> None:
    """Log user feedback on a document or mission."""
    _append_jsonl(FEEDBACK_FILE, {
        "type": "feedback",
        "timestamp": datetime.now(UTC).isoformat(),
        "mission_id": mission_id,
        "doc_id": doc_id,
        "rating": rating,
        "correction": correction,
        "notes": notes,
    })
    logger.info(
        "feedback logged: mission=%s doc=%s rating=%d",
        mission_id, doc_id or "overall", rating,
    )
