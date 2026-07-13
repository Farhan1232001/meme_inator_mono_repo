from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List

from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository

class IPatchMyProfileUsecase(ABC):
    """
    Attributes:
        - profile_repo: IProfileRepository
    partial update : merges fields, preserves unspecified fields
    """

    def __init__(self, profile_repo: IProfileRepository) -> None:
        self.profile_repo = profile_repo

    @abstractmethod
    def execute(self, user_id: int, partial_data: Dict[str, Any]) -> ProfileEntity:
        """Apply partial update and return the updated ProfileEntity."""
        raise NotImplementedError
