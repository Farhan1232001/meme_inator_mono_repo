from abc import ABC, abstractmethod
from typing import Dict

from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository


class IUpdateProfileCountersUsecase(ABC):
    """
    Attributes:
        - profile_repo: IProfileRepository
    increments example : {"followers_count": 1, "posts_uploaded": -1}
    """

    def __init__(self, profile_repo: IProfileRepository) -> None:
        self.profile_repo = profile_repo

    @abstractmethod
    def execute(self, user_id: int, increments: Dict[str, int]) -> ProfileEntity:
        """Atomically update numeric counters and return resulting ProfileEntity."""
        raise NotImplementedError