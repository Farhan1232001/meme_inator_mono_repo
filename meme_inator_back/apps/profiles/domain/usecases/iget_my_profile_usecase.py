from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.entities.profile_light_entity import ProfileLightEntity
from core.results import Result

class IGetMyProfileUsecase(ABC):
    """Interface for fetching the authenticated user's own profile."""

    @abstractmethod
    def execute(
        self, 
        user_id: UUID, 
        viewer_user_id: Optional[UUID] = None,
        fields: Optional[List[str]] = None
        ) -> Result[ProfileEntity|ProfileLightEntity]:
        """Return the profile of the user with the given ID."""
        ...