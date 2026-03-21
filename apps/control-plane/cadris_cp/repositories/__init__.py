from .base import BaseRepository
from .user_repo import UserRepoMixin
from .mission_repo import MissionRepoMixin
from .project_repo import ProjectRepoMixin
from .dossier_repo import DossierRepoMixin


class ControlPlaneRepository(
    UserRepoMixin,
    MissionRepoMixin,
    ProjectRepoMixin,
    DossierRepoMixin,
    BaseRepository,
):
    pass


__all__ = ["ControlPlaneRepository"]
