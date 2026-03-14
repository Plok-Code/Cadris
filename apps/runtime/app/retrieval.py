"""Vector Store retrieval for runtime agents.

Provides a thin wrapper around OpenAI File Search so agents can query
uploaded documents during mission execution.

No-op when OPENAI_API_KEY is absent.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class RetrievalResult:
    file_id: str
    filename: str
    excerpt: str
    score: float
    locator: str | None


class RetrievalClient:
    """Query an OpenAI Vector Store for relevant excerpts."""

    def __init__(self, api_key: str) -> None:
        from openai import OpenAI

        self._client = OpenAI(api_key=api_key)

    def search(
        self,
        *,
        vector_store_id: str,
        query: str,
        max_results: int = 5,
    ) -> list[RetrievalResult]:
        try:
            results = self._client.vector_stores.search(
                vector_store_id=vector_store_id,
                query=query,
                max_num_results=max_results,
            )
        except Exception:
            logger.warning("Vector store search failed for %s", vector_store_id, exc_info=True)
            return []

        output: list[RetrievalResult] = []
        for item in results.data:
            excerpts: list[str] = []
            for block in item.content:
                if block.type == "text":
                    excerpts.append(block.text)

            excerpt = " ".join(excerpts)[:500] if excerpts else ""
            output.append(
                RetrievalResult(
                    file_id=item.file_id,
                    filename=item.filename or "unknown",
                    excerpt=excerpt,
                    score=item.score,
                    locator=None,
                )
            )

        return output


_client: RetrievalClient | None = None


def get_retrieval_client() -> RetrievalClient | None:
    """Return a cached retrieval client, or None if no API key is set."""
    global _client
    if _client is not None:
        return _client

    from .config import settings

    if not settings.openai_api_key:
        return None

    _client = RetrievalClient(settings.openai_api_key)
    return _client


def search_mission_documents(
    *,
    vector_store_id: str,
    query: str,
    max_results: int = 5,
) -> list[RetrievalResult]:
    """Convenience function for agents to search uploaded documents.

    Returns an empty list when OpenAI is not configured.
    """
    client = get_retrieval_client()
    if client is None:
        return []
    return client.search(
        vector_store_id=vector_store_id,
        query=query,
        max_results=max_results,
    )
