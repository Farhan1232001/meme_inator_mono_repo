from typing import Dict, Any
from uuid import UUID
from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.usecases.ireplace_my_profile_usecase import IReplaceMyProfileUsecase
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository
from core.results import Result

class ReplaceMyProfileUsecase(IReplaceMyProfileUsecase):
    def __init__(self, profile_repo: IProfileRepository):
        self.profile_repo = profile_repo

    def execute(self, user_id: UUID, full_data: Dict[str, Any]) -> Result[ProfileEntity]:
        return self.profile_repo.replace_my_profile(user_id, full_data)