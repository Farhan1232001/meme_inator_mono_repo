from typing import List, Optional
from uuid import UUID
from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.entities.profile_light_entity import ProfileLightEntity
from apps.profiles.domain.usecases.iget_my_profile_usecase import IGetMyProfileUsecase
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository
from core.results import Result

class GetMyProfileUsecase(IGetMyProfileUsecase):
    def __init__(self, profile_repo: IProfileRepository):
        self.profile_repo = profile_repo

    def execute(
            self, 
            user_id: UUID, 
            viewer_user_id: Optional[UUID] = None,
            fields: Optional[List[str]] = None
        ) -> Result[ProfileEntity|ProfileLightEntity]:
        # Delegate directly to repository – it already returns a Result
        return self.profile_repo.get_my_profile(user_id, viewer_user_id, fields)
    