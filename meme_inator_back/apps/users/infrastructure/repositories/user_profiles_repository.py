from typing import Optional
from django.shortcuts import get_object_or_404
from apps.profiles.infrastructure.models.profile_model import ProfileModel
from apps.profiles.domain.entities.profile_entity import ProfileEntity


class UserProfilesRepository:
    """
    Handles data access for Profile details.
    """
    
    def _map_to_profile_entity(self, profile_instance) -> ProfileEntity:
        return ProfileEntity(
            full_name=profile_instance.full_name,
            bio=profile_instance.bio,
            location=profile_instance.location,
            website=profile_instance.website,
            birth_date=profile_instance.birth_date
        )

    def get_profile(self, user_id: str) -> Optional[ProfileEntity]:
        """Retrieves a user's profile details."""
        profile = get_object_or_404(ProfileModel, user__id=user_id)
        return self._map_to_profile_entity(profile)

    def update_profile(self, user_id: str, data: dict) -> ProfileEntity:
        """Updates or creates a user's profile based on the provided data."""
        profile, _ = ProfileModel.objects.update_or_create(
            user_id=user_id,
            defaults=data
        )
        return self._map_to_profile_entity(profile)


