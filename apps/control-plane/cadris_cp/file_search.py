"""OpenAI File Search integration for Cadris uploads.

Handles:
- Creating/reusing a Vector Store per mission
- Uploading files to OpenAI and attaching them to the store
- Querying the store for retrieval (used by runtime agents)

All operations are no-ops when OPENAI_API_KEY is not set.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from openai import OpenAI

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class IndexedFile:
    openai_file_id: str
    vector_store_id: str


@dataclass(slots=True)
class SearchResult:
    input_id: str
    filename: str
    excerpt: str
    score: float
    locator: str | None


class FileSearchClient:
    """Wraps OpenAI Files + Vector Stores APIs."""

    def __init__(self, api_key: str) -> None:
        self._client = OpenAI(api_key=api_key)

    def get_or_create_vector_store(self, mission_id: str) -> str:
        """Return existing vector store for mission, or create one."""
        stores = self._client.vector_stores.list(limit=100)
        for store in stores.data:
            if store.name == f"cadris-{mission_id}":
                return store.id

        store = self._client.vector_stores.create(name=f"cadris-{mission_id}")
        logger.info("Created vector store %s for mission %s", store.id, mission_id)
        return store.id

    def index_file(
        self,
        *,
        mission_id: str,
        file_data: bytes,
        filename: str,
        vector_store_id: str | None = None,
    ) -> IndexedFile:
        """Upload a file to OpenAI and add it to the mission's vector store."""
        vs_id = vector_store_id or self.get_or_create_vector_store(mission_id)

        uploaded = self._client.files.create(
            file=(filename, file_data),
            purpose="assistants",
        )
        logger.info("Uploaded file %s (%s) to OpenAI", uploaded.id, filename)

        self._client.vector_stores.files.create(
            vector_store_id=vs_id,
            file_id=uploaded.id,
        )
        logger.info("Attached file %s to vector store %s", uploaded.id, vs_id)

        return IndexedFile(openai_file_id=uploaded.id, vector_store_id=vs_id)

    def search(
        self,
        *,
        vector_store_id: str,
        query: str,
        max_results: int = 5,
        file_id_to_input_id: dict[str, str] | None = None,
    ) -> list[SearchResult]:
        """Search the vector store and return ranked excerpts.

        Args:
            file_id_to_input_id: Mapping from OpenAI file_id to mission_inputs.id.
                When provided, search results use the correct input_id for citations.
        """
        results = self._client.vector_stores.search(
            vector_store_id=vector_store_id,
            query=query,
            max_num_results=max_results,
        )

        id_map = file_id_to_input_id or {}
        search_results: list[SearchResult] = []
        for item in results.data:
            filename = item.filename or "unknown"
            excerpts: list[str] = []
            for content_block in item.content:
                if content_block.type == "text":
                    excerpts.append(content_block.text)

            excerpt = " ".join(excerpts)[:500] if excerpts else ""
            resolved_id = id_map.get(item.file_id, item.file_id)
            search_results.append(
                SearchResult(
                    input_id=resolved_id,
                    filename=filename,
                    excerpt=excerpt,
                    score=item.score,
                    locator=None,
                )
            )

        return search_results

    def delete_vector_store(self, vector_store_id: str) -> None:
        """Cleanup: delete a vector store (e.g. when mission is deleted)."""
        try:
            self._client.vector_stores.delete(vector_store_id)
        except Exception:  # noqa: BLE001 — best-effort cleanup
            logger.warning("Failed to delete vector store %s", vector_store_id, exc_info=True)
