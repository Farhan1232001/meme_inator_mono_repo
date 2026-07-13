from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List

from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository

class ISyncProfileMediaUsecase(ABC):
    """
    Attributes:
        - profile_repo: IProfileRepository
    Used when pushing image upload results (S3 keys) into profile and persistent store
    """

    def __init__(self, profile_repo: IProfileRepository) -> None:
        self.profile_repo = profile_repo

    @abstractmethod
    def execute(self, user_id: int, media_payload: Dict[str, Any]) -> ProfileEntity:
        """
        media_payload might look like:
        { "profile_picture_key": "s3://bucket/key.jpg", "header_image_key": "..." }
        """
        raise NotImplementedError
