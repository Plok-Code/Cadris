from __future__ import annotations

import mimetypes
import re
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4
import boto3


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
    return cleaned or "upload.bin"


def build_preview(data: bytes, mime_type: str | None) -> str | None:
    if mime_type and not mime_type.startswith("text/") and mime_type not in {
        "application/json",
        "application/xml",
    }:
        return None

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None

    compact = " ".join(text.split())
    if not compact:
        return None
    if len(compact) <= 280:
        return compact
    return f"{compact[:277].rstrip()}..."


@dataclass(slots=True)
class StoredUpload:
    input_id: str
    display_name: str
    mime_type: str
    byte_size: int
    storage_path: str
    preview_text: str | None


class LocalUploadStorage:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir

    def store(self, *, mission_id: str, filename: str, media_type: str | None, data: bytes) -> StoredUpload:
        safe_name = sanitize_filename(filename)
        mission_dir = self.root_dir / mission_id
        mission_dir.mkdir(parents=True, exist_ok=True)

        input_id = f"input_{uuid4().hex[:10]}"
        resolved_media_type = media_type or mimetypes.guess_type(safe_name)[0] or "application/octet-stream"
        target_path = mission_dir / f"{input_id}_{safe_name}"
        target_path.write_bytes(data)

        return StoredUpload(
            input_id=input_id,
            display_name=filename,
            mime_type=resolved_media_type,
            byte_size=len(data),
            storage_path=str(target_path),
            preview_text=build_preview(data, resolved_media_type),
        )

    def download(self, storage_path: str) -> bytes | None:
        path = Path(storage_path)
        if not path.exists():
            return None
        return path.read_bytes()

    def delete_mission_files(self, mission_id: str) -> None:
        """Delete all uploaded files for a mission."""
        mission_dir = self.root_dir / mission_id
        if mission_dir.exists():
            import shutil
            shutil.rmtree(mission_dir, ignore_errors=True)


class S3UploadStorage:
    def __init__(self, bucket_name: str, endpoint_url: str | None = None) -> None:
        self.bucket = bucket_name
        self.s3 = boto3.client('s3', endpoint_url=endpoint_url)

    def store(self, *, mission_id: str, filename: str, media_type: str | None, data: bytes) -> StoredUpload:
        safe_name = sanitize_filename(filename)
        input_id = f"input_{uuid4().hex[:10]}"
        resolved_media_type = media_type or mimetypes.guess_type(safe_name)[0] or "application/octet-stream"

        s3_key = f"missions/{mission_id}/{input_id}_{safe_name}"
        self.s3.put_object(
            Bucket=self.bucket,
            Key=s3_key,
            Body=data,
            ContentType=resolved_media_type
        )

        return StoredUpload(
            input_id=input_id,
            display_name=filename,
            mime_type=resolved_media_type,
            byte_size=len(data),
            storage_path=f"s3://{self.bucket}/{s3_key}",
            preview_text=build_preview(data, resolved_media_type),
        )

    def download(self, storage_path: str) -> bytes | None:
        s3_key = self._extract_key(storage_path)
        if not s3_key:
            return None
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=s3_key)
            return response["Body"].read()
        except self.s3.exceptions.NoSuchKey:
            return None

    def generate_presigned_upload_url(
        self, *, mission_id: str, filename: str, content_type: str, expires_in: int = 3600
    ) -> dict[str, str]:
        safe_name = sanitize_filename(filename)
        input_id = f"input_{uuid4().hex[:10]}"
        s3_key = f"missions/{mission_id}/{input_id}_{safe_name}"

        url = self.s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.bucket,
                "Key": s3_key,
                "ContentType": content_type,
            },
            ExpiresIn=expires_in,
        )
        return {
            "upload_url": url,
            "s3_key": s3_key,
            "input_id": input_id,
            "storage_path": f"s3://{self.bucket}/{s3_key}",
        }

    def generate_presigned_download_url(self, storage_path: str, *, expires_in: int = 3600) -> str | None:
        s3_key = self._extract_key(storage_path)
        if not s3_key:
            return None
        return self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": s3_key},
            ExpiresIn=expires_in,
        )

    def delete_mission_files(self, mission_id: str) -> None:
        """Delete all uploaded files for a mission from S3."""
        prefix = f"missions/{mission_id}/"
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
            objects = response.get("Contents", [])
            if objects:
                self.s3.delete_objects(
                    Bucket=self.bucket,
                    Delete={"Objects": [{"Key": o["Key"]} for o in objects]},
                )
        except Exception:
            pass  # Best-effort cleanup

    @staticmethod
    def _extract_key(storage_path: str) -> str | None:
        if not storage_path.startswith("s3://"):
            return None
        # s3://bucket/key -> key
        without_prefix = storage_path[5:]
        slash_idx = without_prefix.find("/")
        if slash_idx < 0:
            return None
        return without_prefix[slash_idx + 1:]
