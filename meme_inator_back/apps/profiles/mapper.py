# apps/profiles/infrastructure/mappers/profile_mapper.py
from typing import Optional, List
from uuid import UUID

from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.entities.profile_light_entity import ProfileLightEntity
from apps.profiles.infrastructure.models.profile_model import ProfileModel


class ProfileMapper:
    """Mapper for converting between ProfileModel and domain entities."""
    
    @staticmethod
    def model_to_entity(profile_model: ProfileModel) -> Optional[ProfileEntity]:
        """
        Map Django ProfileModel instance -> domain ProfileEntity.
        Returns None if the model is None.
        """
        if profile_model is None:
            return None
        
        try:
            # Get username from the user relationship
            username = None
            if profile_model.user and hasattr(profile_model.user, 'user_name'):
                username = profile_model.user.user_name
            else:
                # User relationship is required for ProfileEntity
                return None
            
            return ProfileEntity(
                # --- Identity ---
                user_id=profile_model.user_id,
                username=username,
                
                # --- Profile appearance (Note: these are currently URLs, will be keys after migration) ---
                description=profile_model.description,
                background_color=profile_model.background_color,
                profile_pic_key=profile_model.profile_pic_url,  # Currently URL, will be key
                profile_header_img_key=profile_model.profile_header_img_url,  # Currently URL, will be key
                bg_img_key=profile_model.bg_img,  # Currently URL, will be key
                profile_theme_music_key=profile_model.profile_theme_music_url,  # Currently URL, will be key
                
                # --- Presence messages ---
                is_online_msg=profile_model.is_online_msg,
                is_offline_msg=profile_model.is_offline_msg,
                
                # --- Counters ---
                upload_count=profile_model.upload_count,
                followers_count=profile_model.followers_count,
                following_count=profile_model.following_count,
                friends_count=profile_model.friends_count,
                likes_given=profile_model.likes_given,
                posts_uploaded=profile_model.posts_uploaded,
                comments_posted=profile_model.comments_posted,
                dislikes_given=profile_model.dislikes_given,
                
                # --- Timestamps ---
                last_updated=profile_model.last_updated,
            )
        except AttributeError as e:
            # Log this error in production
            # logger.error(f"Failed to map ProfileModel to ProfileEntity: {e}")
            return None
    
    @staticmethod
    def model_to_light_entity(profile_model: ProfileModel, fields: List[str]) -> Optional[ProfileLightEntity]:
        """
        Map Django ProfileModel instance -> domain ProfileLightEntity with only requested fields.
        Returns None if the model is None.
        """
        if profile_model is None:
            return None
        
        try:
            # Build kwargs dict with only requested fields
            kwargs = {}
            
            # Define field mappings
            field_mapping = {
                # Identity fields
                "user_id": lambda: profile_model.user_id,
                "username": lambda: profile_model.user.user_name if profile_model.user else None,
                
                # Profile appearance
                "description": lambda: profile_model.description,
                "background_color": lambda: profile_model.background_color,
                "profile_pic_key": lambda: profile_model.profile_pic_url,
                "profile_header_img_key": lambda: profile_model.profile_header_img_url,
                "bg_img_key": lambda: profile_model.bg_img,
                "profile_theme_music_key": lambda: profile_model.profile_theme_music_url,
                
                # Presence messages
                "is_online_msg": lambda: profile_model.is_online_msg,
                "is_offline_msg": lambda: profile_model.is_offline_msg,
                
                # Counters
                "upload_count": lambda: profile_model.upload_count,
                "followers_count": lambda: profile_model.followers_count,
                "following_count": lambda: profile_model.following_count,
                "friends_count": lambda: profile_model.friends_count,
                "likes_given": lambda: profile_model.likes_given,
                "posts_uploaded": lambda: profile_model.posts_uploaded,
                "comments_posted": lambda: profile_model.comments_posted,
                "dislikes_given": lambda: profile_model.dislikes_given,
                
                # Timestamps
                "last_updated": lambda: profile_model.last_updated,
            }
            
            # Only include requested fields that exist in the mapping
            for field in fields:
                if field in field_mapping:
                    kwargs[field] = field_mapping[field]()

            entity = ProfileLightEntity(**kwargs)
            entity._requested_fields = fields
            return entity
            
        except AttributeError as e:
            # Log this error in production
            # logger.error(f"Failed to map ProfileModel to ProfileLightEntity: {e}")
            return None
    
    @staticmethod
    def entity_to_model(
        profile_entity: ProfileEntity, 
        existing_model: Optional[ProfileModel] = None,
        user_instance=None
    ) -> Optional[ProfileModel]:
        """
        Map domain ProfileEntity -> Django ProfileModel.
        
        Args:
            profile_entity: The domain entity to map
            existing_model: If provided, update this model; otherwise create new
            user_instance: The UserModel instance to associate with the profile
                          (required for new profiles, optional for updates)
        
        Returns:
            ProfileModel instance or None if user_instance is required but not provided
        """
        if existing_model:
            # Update existing model
            existing_model.description = profile_entity.description
            existing_model.background_color = profile_entity.background_color
            existing_model.profile_pic_url = profile_entity.profile_pic_key
            existing_model.profile_header_img_url = profile_entity.profile_header_img_key
            existing_model.bg_img = profile_entity.bg_img_key
            existing_model.profile_theme_music_url = profile_entity.profile_theme_music_key
            
            existing_model.is_online_msg = profile_entity.is_online_msg
            existing_model.is_offline_msg = profile_entity.is_offline_msg
            
            existing_model.upload_count = profile_entity.upload_count
            existing_model.followers_count = profile_entity.followers_count
            existing_model.following_count = profile_entity.following_count
            existing_model.friends_count = profile_entity.friends_count
            existing_model.likes_given = profile_entity.likes_given
            existing_model.posts_uploaded = profile_entity.posts_uploaded
            existing_model.comments_posted = profile_entity.comments_posted
            existing_model.dislikes_given = profile_entity.dislikes_given
            
            # last_updated is auto_now=True, so don't set it manually
            
            return existing_model
        else:
            # Create new model - user_instance is required
            if user_instance is None:
                return None
            
            return ProfileModel(
                user=user_instance,
                description=profile_entity.description,
                background_color=profile_entity.background_color,
                profile_pic_url=profile_entity.profile_pic_key,
                profile_header_img_url=profile_entity.profile_header_img_key,
                bg_img=profile_entity.bg_img_key,
                profile_theme_music_url=profile_entity.profile_theme_music_key,
                
                is_online_msg=profile_entity.is_online_msg,
                is_offline_msg=profile_entity.is_offline_msg,
                
                upload_count=profile_entity.upload_count,
                followers_count=profile_entity.followers_count,
                following_count=profile_entity.following_count,
                friends_count=profile_entity.friends_count,
                likes_given=profile_entity.likes_given,
                posts_uploaded=profile_entity.posts_uploaded,
                comments_posted=profile_entity.comments_posted,
                dislikes_given=profile_entity.dislikes_given,
                
                # last_updated will be set automatically
            )
    
    @staticmethod
    def entity_to_schema(profile_entity: ProfileEntity):
        """
        Map ProfileEntity to ProfileSchema (if needed).
        Note: This is a convenience method, but you might want to keep this in a separate schema mapper.
        """
        from apps.profiles.application.dtos.profile_schema import ProfileSchema
        
        return ProfileSchema(
            user_id=profile_entity.user_id,
            username=profile_entity.username,
            description=profile_entity.description,
            background_color=profile_entity.background_color,
            profile_pic_url=profile_entity.profile_pic_key,  # Will be hydrated to URL
            profile_header_img_url=profile_entity.profile_header_img_key,  # Will be hydrated to URL
            bg_img=profile_entity.bg_img_key,  # Will be hydrated to URL
            profile_theme_music_url=profile_entity.profile_theme_music_key,  # Will be hydrated to URL
            is_online_msg=profile_entity.is_online_msg,
            is_offline_msg=profile_entity.is_offline_msg,
            upload_count=profile_entity.upload_count,
            followers_count=profile_entity.followers_count,
            following_count=profile_entity.following_count,
            friends_count=profile_entity.friends_count,
            likes_given=profile_entity.likes_given,
            posts_uploaded=profile_entity.posts_uploaded,
            comments_posted=profile_entity.comments_posted,
            dislikes_given=profile_entity.dislikes_given,
            last_updated=profile_entity.last_updated,
        )