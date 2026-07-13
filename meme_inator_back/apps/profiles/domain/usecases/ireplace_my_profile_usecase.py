from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List

from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository

class IReplaceMyProfileUsecase(ABC):
    """
    Attributes:
        - profile_repo: IProfileRepository
    full replace : missing optional fields are cleared
    """

    def __init__(self, profile_repo: IProfileRepository) -> None:
        self.profile_repo = profile_repo

    @abstractmethod
    def execute(self, user_id: int, profile_data: Dict[str, Any]) -> ProfileEntity:
        """Fully replace profile for user_id and return resulting ProfileEntity."""
        raise NotImplementedError
