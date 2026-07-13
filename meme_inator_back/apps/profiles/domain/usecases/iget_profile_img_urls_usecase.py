from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List

from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository

class IGetProfileImageUrlsUsecase(ABC):
    """
    Attributes:
        - profile_repo: IProfileRepository
    Behavior:
        returns presigned/accessible URLs (profile_picture, header_image, background_image, music)
    """

    def __init__(self, profile_repo: IProfileRepository) -> None:
        self.profile_repo = profile_repo

    @abstractmethod
    def execute(self, user_id: int) -> Dict[str, str]:
        """Return mapping of media keys -> accessible URLs, e.g. {"profile_picture": "..."}."""
        raise NotImplementedError