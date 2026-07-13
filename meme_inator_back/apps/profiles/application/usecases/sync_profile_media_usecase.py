from typing import Dict, Any
from uuid import UUID
from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.usecases.isync_profile_media_usecase import ISyncProfileMediaUsecase
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository
from core.results import Result

class SyncProfileMediaUsecase(ISyncProfileMediaUsecase):
    def __init__(self, profile_repo: IProfileRepository):
        self.profile_repo = profile_repo

    def execute(self, user_id: UUID, media_payload: Dict[str, Any]) -> Result[ProfileEntity]:
        return self.profile_repo.sync_media(user_id, media_payload)