from typing import Dict
from uuid import UUID
from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.usecases.iupdate_profile_counters_usecase import IUpdateProfileCountersUsecase
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository
from core.results import Result

class UpdateProfileCountersUsecase(IUpdateProfileCountersUsecase):
    def __init__(self, profile_repo: IProfileRepository):
        self.profile_repo = profile_repo

    def execute(self, user_id: UUID, increments: Dict[str, int]) -> Result[ProfileEntity]:
        return self.profile_repo.update_counters(user_id, increments)