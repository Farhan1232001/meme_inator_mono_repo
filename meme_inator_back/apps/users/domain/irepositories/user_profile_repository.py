from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from apps.profiles.domain.entities.profile_entity import ProfileEntity


class IUserProfileRepository(ABC):
    """Contract for accessing and modifying user profile details."""

    @abstractmethod
    def get_profile_model(self, user_id: str) -> Optional[ProfileEntity]:
        ...

    @abstractmethod
    def create_profile_model(self, profile: ProfileEntity) -> ProfileEntity:
        ...