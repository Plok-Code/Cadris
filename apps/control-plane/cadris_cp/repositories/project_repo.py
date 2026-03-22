from __future__ import annotations

from sqlalchemy import select

from .base import utc_now
from ..models import ProjectSummary
from ..records import ProjectRecord


class ProjectRepoMixin:
    """Project-related repository methods."""

    def list_projects_for_user(self, user_id: str) -> list[ProjectSummary]:
        statement = (
            select(ProjectRecord)
            .where(ProjectRecord.user_id == user_id)
            .order_by(ProjectRecord.updated_at.desc())
        )
        return [self._to_project_summary(row) for row in self.session.scalars(statement).all()]

    def create_project(self, *, user_id: str, project_id: str, name: str) -> ProjectSummary:
        record = ProjectRecord(
            id=project_id,
            user_id=user_id,
            name=name,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return self._to_project_summary(record)

    def get_project_for_user(self, user_id: str, project_id: str) -> ProjectSummary | None:
        statement = select(ProjectRecord).where(
            ProjectRecord.id == project_id,
            ProjectRecord.user_id == user_id,
        )
        record = self.session.scalar(statement)
        if record is None:
            return None
        return self._to_project_summary(record)

    def update_project_after_mission(
        self,
        *,
        user_id: str,
        project_id: str,
        active_mission_id: str,
        active_mission_status: str,
        mission_delta: int = 0,
    ) -> ProjectSummary:
        # Defense-in-depth: verify ownership even though callers already check
        statement = select(ProjectRecord).where(
            ProjectRecord.id == project_id,
            ProjectRecord.user_id == user_id,
        )
        record = self.session.scalar(statement)
        if record is None:
            from ..errors import AppError
            raise AppError.not_found("project_not_found", "Project not found.")

        record.active_mission_id = active_mission_id
        record.active_mission_status = active_mission_status
        record.mission_count += mission_delta
        record.updated_at = utc_now()
        self.session.commit()
        self.session.refresh(record)
        return self._to_project_summary(record)
