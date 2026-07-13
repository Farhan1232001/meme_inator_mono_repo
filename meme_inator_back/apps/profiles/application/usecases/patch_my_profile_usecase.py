from typing import Dict, Any
from uuid import UUID
from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.usecases.ipatch_my_profile_usecase import IPatchMyProfileUsecase
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository
from core.results import Result

class PatchMyProfileUsecase(IPatchMyProfileUsecase):
    def __init__(self, profile_repo: IProfileRepository):
        self.profile_repo = profile_repo

    def execute(self, user_id: UUID, partial_data: Dict[str, Any]) -> Result[ProfileEntity]:
        # Repository expects the partial data (already in camelCase as sent from frontend)
        return self.profile_repo.patch_my_profile(user_id, partial_data)