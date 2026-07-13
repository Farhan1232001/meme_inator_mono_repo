# apps/profiles/infrastructure/repositories/profile_repository.py
from typing import List, Optional, Dict, Any, Union
from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, DatabaseError
from django.utils import timezone

from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.entities.profile_light_entity import ProfileLightEntity
from apps.profiles.domain.irepositories.i_profile_repository import IProfileRepository
from apps.profiles.infrastructure.models.profile_model import ProfileModel
from apps.profiles.mapper import ProfileMapper
from apps.users.infrastructure.models.user_model import UserModel
from core.results import Ok, NotOk, Error, Result


class ProfileRepository(IProfileRepository):
    """Concrete repository using Django ORM."""


    def get_public_profile(
        self, 
        username: str, 
        viewer_user_id: Optional[UUID], 
        fields: Optional[List[str]] = None
    ) -> Result[Union[ProfileEntity, ProfileLightEntity]]:
        try:
            # Username is stored in the associated UserModel
            profile = ProfileModel.objects.select_related('user').get(user__user_name=username)
            
            # If fields are specified, return a light entity with only requested fields
            if fields:
                light_entity = ProfileMapper.model_to_light_entity(profile, fields)
                if light_entity is None:
                    return Error(
                        message="Failed to create light entity",
                        static_msg="MAPPING_ERROR",
                        status_code=500
                    )
                return Ok(light_entity)
            
            # Otherwise return full entity
            entity = ProfileMapper.model_to_entity(profile)
            if entity is None:
                return Error(
                    message="Failed to create entity",
                    static_msg="MAPPING_ERROR",
                    status_code=500
                )
            return Ok(entity)
            
        except ProfileModel.DoesNotExist:
            return NotOk(
                message="Profile not found",
                static_msg="PROFILE_NOT_FOUND",
                status_code=404
            )
        except DatabaseError as e:
            return Error(
                message="Database error",
                static_msg="DB_ERROR",
                exception=e,
                status_code=500
            )

    def get_my_profile(
        self, 
        user_id: UUID, 
        viewer_user_id: Optional[UUID],
        fields: Optional[List[str]] = None
    ) -> Result[Union[ProfileEntity, ProfileLightEntity]]:
        try:
            profile = ProfileModel.objects.select_related('user').get(user_id=user_id)
            
            # If fields are specified, return a light entity with only requested fields
            if fields:
                light_entity = ProfileMapper.model_to_light_entity(profile, fields)
                if light_entity is None:
                    return Error(
                        message="Failed to create light entity",
                        static_msg="MAPPING_ERROR",
                        status_code=500
                    )
                return Ok(light_entity)
            
            # Otherwise return full entity
            entity = ProfileMapper.model_to_entity(profile)
            if entity is None:
                return Error(
                    message="Failed to create entity",
                    static_msg="MAPPING_ERROR",
                    status_code=500
                )
            return Ok(entity)
            
        except ProfileModel.DoesNotExist:
            return NotOk(
                message="Profile not found",
                static_msg="PROFILE_NOT_FOUND",
                status_code=404
            )
        except DatabaseError as e:
            return Error(
                message="Database error",
                static_msg="DB_ERROR",
                exception=e,
                status_code=500
            )

    def create_profile(self, user_id: UUID) -> Result[ProfileEntity]:
        try:
            with transaction.atomic():
                user = UserModel.objects.select_for_update().get(pk=user_id)
                # Idempotency: check if already exists
                if ProfileModel.objects.filter(user=user).exists():
                    return NotOk(
                        message="Profile already exists",
                        static_msg="PROFILE_ALREADY_EXISTS",
                        status_code=409
                    )
                profile = ProfileModel.objects.create(
                    user=user,
                    profile_theme_music_url="",  # default empty
                    last_updated=timezone.now()
                )
                
                # Convert to entity before returning
                entity = ProfileMapper.model_to_entity(profile)
                if entity is None:
                    return Error(
                        message="Failed to create entity from created profile",
                        static_msg="MAPPING_ERROR",
                        status_code=500
                    )
                return Ok(entity)
                
        except UserModel.DoesNotExist:
            return NotOk(
                message="User not found",
                static_msg="USER_NOT_FOUND",
                status_code=404
            )
        except DatabaseError as e:
            return Error(
                message="Database error",
                static_msg="DB_ERROR",
                exception=e,
                status_code=500
            )

    def patch_my_profile(self, user_id: UUID, partial_data: Dict[str, Any]) -> Result[ProfileEntity]:
        try:
            with transaction.atomic():
                profile = ProfileModel.objects.select_for_update().get(user_id=user_id)
                # Map frontend field names to model field names (camelCase to snake_case)
                field_mapping = {
                    "description": "description",
                    "backgroundColor": "background_color",
                    "profilePicUrl": "profile_pic_url",
                    "profileHeaderImgUrl": "profile_header_img_url",
                    "bgImg": "bg_img",
                    "profileThemeMusicUrl": "profile_theme_music_url",
                    "isOnlineMsg": "is_online_msg",
                    "isOfflineMsg": "is_offline_msg",
                }
                for frontend_field, model_field in field_mapping.items():
                    if frontend_field in partial_data:
                        setattr(profile, model_field, partial_data[frontend_field])
                profile.save()
                
                entity = ProfileMapper.model_to_entity(profile)
                if entity is None:
                    return Error(
                        message="Failed to create entity from updated profile",
                        static_msg="MAPPING_ERROR",
                        status_code=500
                    )
                return Ok(entity)
                
        except ProfileModel.DoesNotExist:
            return NotOk(
                message="Profile not found",
                static_msg="PROFILE_NOT_FOUND",
                status_code=404
            )
        except DatabaseError as e:
            return Error(
                message="Database error",
                static_msg="DB_ERROR",
                exception=e,
                status_code=500
            )

    def replace_my_profile(self, user_id: UUID, full_data: Dict[str, Any]) -> Result[ProfileEntity]:
        try:
            with transaction.atomic():
                profile = ProfileModel.objects.select_for_update().get(user_id=user_id)
                # Map and set all fields (if missing, set to None or default)
                profile.description = full_data.get("description")
                profile.background_color = full_data.get("backgroundColor")
                profile.profile_pic_url = full_data.get("profilePicUrl")
                profile.profile_header_img_url = full_data.get("profileHeaderImgUrl")
                profile.bg_img = full_data.get("bgImg")
                profile.profile_theme_music_url = full_data.get("profileThemeMusicUrl", "")
                profile.is_online_msg = full_data.get("isOnlineMsg")
                profile.is_offline_msg = full_data.get("isOfflineMsg")
                # Counters are not replaced via replace (should be updated via counters endpoint)
                profile.save()
                
                entity = ProfileMapper.model_to_entity(profile)
                if entity is None:
                    return Error(
                        message="Failed to create entity from replaced profile",
                        static_msg="MAPPING_ERROR",
                        status_code=500
                    )
                return Ok(entity)
                
        except ProfileModel.DoesNotExist:
            return NotOk(
                message="Profile not found",
                static_msg="PROFILE_NOT_FOUND",
                status_code=404
            )
        except DatabaseError as e:
            return Error(
                message="Database error",
                static_msg="DB_ERROR",
                exception=e,
                status_code=500
            )

    def update_counters(self, user_id: UUID, increments: Dict[str, int]) -> Result[ProfileEntity]:
        try:
            with transaction.atomic():
                profile = ProfileModel.objects.select_for_update().get(user_id=user_id)
                # Map frontend field names to model field names
                field_mapping = {
                    "uploadCount": "upload_count",
                    "followersCount": "followers_count",
                    "followingCount": "following_count",
                    "friendsCount": "friends_count",
                    "likesGiven": "likes_given",
                    "dislikesGiven": "dislikes_given",
                    "postsUploaded": "posts_uploaded",
                    "commentsPosted": "comments_posted",
                }
                for frontend_field, model_field in field_mapping.items():
                    if frontend_field in increments:
                        current = getattr(profile, model_field)
                        setattr(profile, model_field, current + increments[frontend_field])
                profile.save()
                
                entity = ProfileMapper.model_to_entity(profile)
                if entity is None:
                    return Error(
                        message="Failed to create entity from updated counters",
                        static_msg="MAPPING_ERROR",
                        status_code=500
                    )
                return Ok(entity)
                
        except ProfileModel.DoesNotExist:
            return NotOk(
                message="Profile not found",
                static_msg="PROFILE_NOT_FOUND",
                status_code=404
            )
        except DatabaseError as e:
            return Error(
                message="Database error",
                static_msg="DB_ERROR",
                exception=e,
                status_code=500
            )

    def sync_media(self, user_id: UUID, media_payload: Dict[str, Any]) -> Result[ProfileEntity]:
        try:
            with transaction.atomic():
                profile = ProfileModel.objects.select_for_update().get(user_id=user_id)
                if "profilePictureKey" in media_payload:
                    profile.profile_pic_url = media_payload["profilePictureKey"]
                if "headerImageKey" in media_payload:
                    profile.profile_header_img_url = media_payload["headerImageKey"]
                if "backgroundImageKey" in media_payload:
                    profile.bg_img = media_payload["backgroundImageKey"]
                if "themeMusicKey" in media_payload:
                    profile.profile_theme_music_url = media_payload["themeMusicKey"]
                profile.save()
                
                entity = ProfileMapper.model_to_entity(profile)
                if entity is None:
                    return Error(
                        message="Failed to create entity from synced media",
                        static_msg="MAPPING_ERROR",
                        status_code=500
                    )
                return Ok(entity)
                
        except ProfileModel.DoesNotExist:
            return NotOk(
                message="Profile not found",
                static_msg="PROFILE_NOT_FOUND",
                status_code=404
            )
        except DatabaseError as e:
            return Error(
                message="Database error",
                static_msg="DB_ERROR",
                exception=e,
                status_code=500
            )

    def get_profile_posts(self, username: str, cursor: Optional[str] = None, page_size: int = 10) -> Result[Dict[str, Any]]:
        # This should ideally call the posts repository/use case.
        try:
            from apps.posts.infrastructure.models.post_model import PostModel
            
            # TODO: Should delegate getting profile feed to /feeds feature OR /posts feature. 
            user = UserModel.objects.get(user_name=username)
            qs = PostModel.objects.filter(author_id=user.id, is_deleted=False, is_flagged=False).order_by('-created_on')
            posts = list(qs[:page_size])
            
            return Ok({
                "posts": posts,
                "next_cursor": None
            })
            
        except UserModel.DoesNotExist:
            return NotOk(
                message="User not found",
                static_msg="USER_NOT_FOUND",
                status_code=404
            )
        except DatabaseError as e:
            return Error(
                message="Database error",
                static_msg="DB_ERROR",
                exception=e,
                status_code=500
            )

    def get_profile_image_urls(self, user_id: UUID) -> Result[Dict[str, str]]:
        try:
            profile = ProfileModel.objects.get(user_id=user_id)
            return Ok({
                "profilePicUrl": profile.profile_pic_url,
                "profileHeaderImgUrl": profile.profile_header_img_url,
                "bgImg": profile.bg_img,
                "profileThemeMusicUrl": profile.profile_theme_music_url,
            })
            
        except ProfileModel.DoesNotExist:
            return NotOk(
                message="Profile not found",
                static_msg="PROFILE_NOT_FOUND",
                status_code=404
            )
        except DatabaseError as e:
            return Error(
                message="Database error",
                static_msg="DB_ERROR",
                exception=e,
                status_code=500
            )

    def get_user_id_by_username(self, username: str) -> Result[UUID]:
        try:
            user = UserModel.objects.only('id').get(user_name=username)
            return Ok(user.id)
            
        except UserModel.DoesNotExist:
            return NotOk(
                message="User not found",
                static_msg="USER_NOT_FOUND",
                status_code=404
            )
        except DatabaseError as e:
            return Error(
                message="Database error",
                static_msg="DB_ERROR",
                exception=e,
                status_code=500
            )
    

    def get_public_profile_by_user_id(
        self, 
        user_id: UUID, 
        viewer_user_id: Optional[UUID], 
        fields: Optional[List[str]] = None
    ) -> Result[Union[ProfileEntity, ProfileLightEntity]]:
        try:
            # Get profile directly by user_id
            profile = ProfileModel.objects.select_related('user').get(user_id=user_id)
            
            # If fields are specified, return a light entity with only requested fields
            if fields:
                light_entity = ProfileMapper.model_to_light_entity(profile, fields)
                if light_entity is None:
                    return Error(
                        message="Failed to create light entity",
                        static_msg="MAPPING_ERROR",
                        status_code=500
                    )
                return Ok(light_entity)
            
            # Otherwise return full entity
            entity = ProfileMapper.model_to_entity(profile)
            if entity is None:
                return Error(
                    message="Failed to create entity",
                    static_msg="MAPPING_ERROR",
                    status_code=500
                )
            return Ok(entity)
            
        except ProfileModel.DoesNotExist:
            return NotOk(
                message="Profile not found",
                static_msg="PROFILE_NOT_FOUND",
                status_code=404
            )
        except DatabaseError as e:
            return Error(
                message="Database error",
                static_msg="DB_ERROR",
                exception=e,
                status_code=500
            )