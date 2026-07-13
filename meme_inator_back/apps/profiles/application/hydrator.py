from typing import List, Optional, Union
from urllib.parse import urlparse

from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.profiles.domain.entities.profile_light_entity import ProfileLightEntity


class ProfileHydrator:
    """
    Hydrator turns storage-facing data (S3 keys) into client-ready data (URLs).
    
    Assumes ProfilesS3Service interface:
      class ProfilesS3Service:
        def get_public_url_or_signed_url(self, storage_key: str) -> str:
            ...
    
    Converts ProfileEntity/ProfileLightEntity storage keys into client-ready URLs.
    
    Responsibilities:
      - Resolve profile_pic_key, profile_header_img_key, bg_img_key, profile_theme_music_key
      - Return new entity instances (no in-place mutation)
      - Handle both full ProfileEntity and ProfileLightEntity
      - Respect field presence in light entities (only hydrate fields that exist)
    """

    def __init__(self, s3_service):
        """
        :param s3_service: implements
            get_public_url_or_signed_url(storage_key: str) -> str
        """
        self._s3 = s3_service

    def hydrate(self, profile: Union[ProfileEntity, ProfileLightEntity]) -> Union[ProfileEntity, ProfileLightEntity]:
        """
        Hydrate a single profile entity.
        
        Rules:
          - If a value already looks like a URL, leave it untouched
          - If a storage key is missing or empty, skip hydration
          - Always return new instances (entities are immutable)
          - For ProfileLightEntity, only hydrate fields that are present
        """
        if isinstance(profile, ProfileLightEntity):
            return self._hydrate_light(profile)
        return self._hydrate_full(profile)

    def hydrate_many(self, profiles: List[Union[ProfileEntity, ProfileLightEntity]]) -> List[Union[ProfileEntity, ProfileLightEntity]]:
        """Hydrate multiple profile entities."""
        return [self.hydrate(p) for p in profiles]

    # -----------------------
    # Private hydration methods
    # -----------------------
    def _hydrate_full(self, profile: ProfileEntity) -> ProfileEntity:
        """Hydrate a full ProfileEntity."""
        # Create a new instance with hydrated fields
        return ProfileEntity(
            user_id=profile.user_id,
            username=profile.username,
            description=profile.description,
            background_color=profile.background_color,
            profile_pic_url=self._hydrate_key(profile.profile_pic_key),  # Note: field name change
            profile_header_img_url=self._hydrate_key(profile.profile_header_img_key),
            bg_img=self._hydrate_key(profile.bg_img_key),
            profile_theme_music_url=self._hydrate_key(profile.profile_theme_music_key),
            is_online_msg=profile.is_online_msg,
            is_offline_msg=profile.is_offline_msg,
            upload_count=profile.upload_count,
            followers_count=profile.followers_count,
            following_count=profile.following_count,
            friends_count=profile.friends_count,
            likes_given=profile.likes_given,
            posts_uploaded=profile.posts_uploaded,
            comments_posted=profile.comments_posted,
            dislikes_given=profile.dislikes_given,
            last_updated=profile.last_updated,
        )

    def _hydrate_light(self, profile: ProfileLightEntity) -> ProfileLightEntity:
        """Hydrate a ProfileLightEntity, respecting present fields."""
        kwargs = {}
        
        # Only hydrate fields that are present in the light entity
        if profile.has_field('profile_pic_key'):
            kwargs['profile_pic_key'] = self._hydrate_key(profile.profile_pic_key)
        if profile.has_field('profile_header_img_key'):
            kwargs['profile_header_img_key'] = self._hydrate_key(profile.profile_header_img_key)
        if profile.has_field('bg_img_key'):
            kwargs['bg_img_key'] = self._hydrate_key(profile.bg_img_key)
        if profile.has_field('profile_theme_music_key'):
            kwargs['profile_theme_music_key'] = self._hydrate_key(profile.profile_theme_music_key)
        
        # Copy over all other fields
        for field_name in profile._present_fields:
            if field_name not in kwargs and not field_name.endswith('_key'):
                kwargs[field_name] = getattr(profile, field_name)
        
        return ProfileLightEntity(**kwargs)

    def _hydrate_key(self, value: Optional[str]) -> Optional[str]:
        """
        Convert a storage key into a usable URL.

        Returns:
          - None if value is None
          - original value if already a URL
          - resolved URL if value is a storage key
        """
        if not value:
            return value

        if self._looks_like_url(value):
            return value

        return self._s3.get_public_url_or_signed_url(value)

    @staticmethod
    def _looks_like_url(value: str) -> bool:
        """
        Check if a string already appears to be a valid URL.
        """
        try:
            parsed = urlparse(value)
            return bool(parsed.scheme and parsed.netloc)
        except Exception:
            return False