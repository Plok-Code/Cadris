"""Module-level singletons shared across routers."""
from __future__ import annotations

from .config import settings
from .file_search import FileSearchClient
from .renderer_client import RendererClient
from .runtime_client import RuntimeClient
from .uploads import LocalUploadStorage, S3UploadStorage

runtime_client = RuntimeClient()
renderer_client = RendererClient()

if settings.s3_bucket:
    upload_storage: LocalUploadStorage | S3UploadStorage = S3UploadStorage(
        settings.s3_bucket, settings.s3_endpoint
    )
else:
    upload_storage = LocalUploadStorage(settings.uploads_dir)

file_search_client: FileSearchClient | None = None
if settings.openai_api_key:
    file_search_client = FileSearchClient(settings.openai_api_key)
