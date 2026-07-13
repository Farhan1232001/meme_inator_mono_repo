from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List

from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository

class IProfileEntityFromRepositoryUsecase(ABC):
    """
    Attributes:
        - profile_repo: IProfileRepository
    Convert ORM/dict into ProfileEntity, apply any normalization
    """

    def __init__(self, profile_repo: IProfileRepository) -> None:
        self.profile_repo = profile_repo

    @abstractmethod
    def execute(self, raw: Dict[str, Any]) -> ProfileEntity:
        """Normalize/convert raw repository data into domain ProfileEntity."""
        raise NotImplementedError