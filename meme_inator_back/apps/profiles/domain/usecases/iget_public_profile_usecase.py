from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from uuid import UUID

from apps.posts.domain.irepositories.iposts_repository import IPostRepository
from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.entities.profile_light_entity import ProfileLightEntity
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository
from core.results import Result

class IGetPublicProfileUsecase(ABC):
    """
    Attributes:
        - profile_repo: IProfileRepository
        - post_repo: IPostRepository
    Returns:
        ProfileViewerEntity (profile as seen by this viewer; viewer_user_id may be None)
    """

    def __init__(self, profile_repo: IProfileRepository) -> None:
        self.profile_repo = profile_repo
    
    @abstractmethod
    def execute_with_user_ids(self, user_id: UUID, viewer_user_id: Optional[UUID] = None, fields: Optional[List[str]] = None) -> Result[ProfileEntity|ProfileLightEntity]:
        """Return profile information tailored to the viewer (permissions, following state, etc.)."""
        ...

    @abstractmethod
    def execute(self, username: str, viewer_user_id: Optional[UUID] = None, fields: Optional[List[str]] = None) -> Result[ProfileEntity|ProfileLightEntity]:
        """Return profile information tailored to the viewer (permissions, following state, etc.)."""
        ...