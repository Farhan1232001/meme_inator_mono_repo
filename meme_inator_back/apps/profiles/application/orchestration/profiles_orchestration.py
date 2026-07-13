from typing import List, Optional, Dict, Any
from uuid import UUID

from apps.profiles.application.dtos.profile_with_followship_context import ProfileWithFollowshipContext
from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.entities.profile_light_entity import ProfileLightEntity
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository
from apps.profiles.domain.usecases.icreate_user_profile_usercase import ICreateUserProfileUsecase
from apps.profiles.domain.usecases.iget_my_profile_usecase import IGetMyProfileUsecase
from apps.profiles.domain.usecases.iget_profile_img_urls_usecase import IGetProfileImageUrlsUsecase
from apps.profiles.domain.usecases.iget_profile_posts_usecase import IGetProfilePostsUsecase
from apps.profiles.domain.usecases.iget_public_profile_usecase import IGetPublicProfileUsecase
from apps.profiles.domain.usecases.ipatch_my_profile_usecase import IPatchMyProfileUsecase
from apps.profiles.domain.usecases.ireplace_my_profile_usecase import IReplaceMyProfileUsecase
from apps.profiles.domain.usecases.isync_profile_media_usecase import ISyncProfileMediaUsecase
from apps.profiles.domain.usecases.iupdate_profile_counters_usecase import IUpdateProfileCountersUsecase
from apps.users.domain.usecases.followship_usecases.idoes_followship_exist_usecase import IDoesFollowshipExistUsecase
from core.results import Ok, Result



class ProfilesOrchestration:
    """Orchestrates profile-related usecases."""

    def __init__(
        self,
        get_public_profile_usecase: IGetPublicProfileUsecase,
        get_my_profile_usecase: IGetMyProfileUsecase,
        create_profile_usecase: ICreateUserProfileUsecase,
        patch_my_profile_usecase: IPatchMyProfileUsecase,
        replace_my_profile_usecase: IReplaceMyProfileUsecase,
        update_counters_usecase: IUpdateProfileCountersUsecase,
        sync_media_usecase: ISyncProfileMediaUsecase,
        get_profile_posts_usecase: IGetProfilePostsUsecase,
        get_profile_image_urls_usecase: IGetProfileImageUrlsUsecase,
        does_follow_exist_usecase: IDoesFollowshipExistUsecase
    ):
        self._get_public_profile = get_public_profile_usecase
        self._get_my_profile = get_my_profile_usecase
        self._create_profile = create_profile_usecase
        self._patch_my_profile = patch_my_profile_usecase
        self._replace_my_profile = replace_my_profile_usecase
        self._update_counters = update_counters_usecase
        self._sync_media = sync_media_usecase
        self._get_profile_posts = get_profile_posts_usecase
        self._get_profile_image_urls = get_profile_image_urls_usecase
        self._does_follow_exist_usecase = does_follow_exist_usecase

    # --- Actual Orchestration methods --------------------
    def get_profile_with_followship_context(
            self, 
            profile_owner_user_id: UUID,
            viewer_user_id: UUID = None, 
            fields: Optional[List[str]] = None
        ) -> Result[ProfileWithFollowshipContext]:
        # 1. Get the base profile
        profile_result = self._get_public_profile.execute_with_user_ids(
            profile_owner_user_id, 
            viewer_user_id, 
            fields
        ) 
        if not isinstance(profile_result, Ok):
            return profile_result

        # 2. check if 
        is_following = False
        follow_check_result = self._does_follow_exist_usecase.execute(viewer_user_id, profile_owner_user_id)

        if not isinstance(follow_check_result, Ok):
            return follow_check_result
        
        is_following = follow_check_result.value 

        profile = profile_result.value

        # 3. Combine into enriched DTO
        enriched = ProfileWithFollowshipContext(**profile.to_dict(), is_following=is_following)
        return Ok(enriched)


    # --- Usecase wrappers --------------------------------

    def get_public_profile(
            self, 
            username: str, 
            viewer_user_id: Optional[UUID] = None, 
            fields: Optional[str] = None
        ) -> Result[ProfileEntity|ProfileLightEntity]:
        return self._get_public_profile.execute(username, viewer_user_id, fields)

    def get_my_profile(
            self, 
            user_id: UUID, 
            viewer_user_id: Optional[UUID],
            fields: Optional[str] = None
        ) -> Result[ProfileEntity|ProfileLightEntity]:
        return self._get_my_profile.execute(user_id, viewer_user_id, fields)

    def create_profile(self, user_id: UUID) -> Result[ProfileEntity]:
        raise NotImplementedError("This method is deprecated and will be removed. Profile is automatically created when user is created.")

    def patch_my_profile(self, user_id: UUID, partial_data: Dict[str, Any]) -> Result[ProfileEntity]:
        return self._patch_my_profile.execute(user_id, partial_data)

    def replace_my_profile(self, user_id: UUID, full_data: Dict[str, Any]) -> Result[ProfileEntity]:
        return self._replace_my_profile.execute(user_id, full_data)

    def update_counters(self, user_id: UUID, increments: Dict[str, int]) -> Result[ProfileEntity]:
        return self._update_counters.execute(user_id, increments)

    def sync_media(self, user_id: UUID, media_payload: Dict[str, Any]) -> Result[ProfileEntity]:
        return self._sync_media.execute(user_id, media_payload)

    def get_profile_posts(self, username: str, cursor: Optional[str] = None, page_size: int = 10) -> Result[Dict[str, Any]]:
        return self._get_profile_posts.execute(username, cursor, page_size)

    def get_profile_image_urls(self, user_id: UUID) -> Result[Dict[str, str]]:
        return self._get_profile_image_urls.execute(user_id)

    def get_user_id_by_username(self, username: str) -> Result[UUID]:
        # TODO: Have GetUserIdByUsername be its owwn usecase with its own reference to ProfileRepo. 
        # Below is a hacky solution
        # each usecase has access to a profiles repo. just get it from there
        profile_repo = self._get_public_profile.profile_repo
        return profile_repo.get_user_id_by_username(username)