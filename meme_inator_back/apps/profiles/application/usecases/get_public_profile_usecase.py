# application/usecases/get_public_profile_usecase.py
from typing import List, Optional
from uuid import UUID

from apps.posts.domain.irepositories.iposts_repository import IPostRepository
from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.entities.profile_light_entity import ProfileLightEntity
from apps.profiles.domain.usecases.iget_public_profile_usecase import IGetPublicProfileUsecase
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository
from core.results import Error, NotOk, Ok, Result

class GetPublicProfileUsecase(IGetPublicProfileUsecase):
    def __init__(self, profile_repo: IProfileRepository):
        self.profile_repo = profile_repo
    
    def execute(self, username: str, viewer_user_id: Optional[UUID] = None, fields: Optional[List[str]] = None) -> Result[ProfileEntity|ProfileLightEntity]:
        # Original implementation using username
        try:
            profile = self.profile_repo.get_public_profile(username, viewer_user_id, fields)
            if profile is None:
                return NotOk(
                    message="Profile not found",
                    static_msg="PROFILE_NOT_FOUND",
                    status_code=404
                )
            return Ok(profile)
        except Exception as e:
            return Error(
                message="Failed to get profile",
                static_msg="PROFILE_FETCH_ERROR",
                exception=e,
                status_code=500
            )
    
    def execute_with_user_ids(self, user_id: UUID, viewer_user_id: Optional[UUID] = None, fields: Optional[str] = None) -> Result[ProfileEntity|ProfileLightEntity]:
        try:
            profile = self.profile_repo.get_public_profile_by_user_id(user_id, viewer_user_id, fields)

            if not isinstance(profile, Ok):
                return profile
            
            return profile
        except Exception as e:
            return Error(
                message="Failed to get profile",
                static_msg="PROFILE_FETCH_ERROR",
                exception=e,
                status_code=500
            )