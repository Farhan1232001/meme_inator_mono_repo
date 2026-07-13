from typing import Optional, Dict, Any, List, Union
from uuid import UUID
from apps.profiles.domain.entities.profile_light_entity import ProfileLightEntity
from core.results import Result
from apps.profiles.domain.entities.profile_entity import ProfileEntity

class IProfileRepository:
    """Interface for profile repository operations."""

    def get_public_profile(
            self, 
            username: str, 
            viewer_user_id: Optional[UUID], 
            fields: Optional[List[str]] = None
        ) -> Result[ProfileEntity|ProfileLightEntity]:
        """Fetch a public profile by username."""
        ...

    def get_my_profile(
            self, 
            user_id: UUID, 
            viewer_user_id: Optional[UUID]
        ) -> Result[ProfileEntity|ProfileLightEntity]:
        """Fetch the profile of the currently authenticated user."""
        ...

    def create_profile(self, user_id: UUID) -> Result[ProfileEntity]:
        """Create a default profile for a user."""
        ...

    def patch_my_profile(self, user_id: UUID, partial_data: Dict[str, Any]) -> Result[ProfileEntity]:
        """Partially update the authenticated user's profile."""
        ...

    def replace_my_profile(self, user_id: UUID, full_data: Dict[str, Any]) -> Result[ProfileEntity]:
        """Fully replace the authenticated user's profile."""
        ...

    def update_counters(self, user_id: UUID, increments: Dict[str, int]) -> Result[ProfileEntity]:
        """Atomically update numeric counters (e.g., followers_count)."""
        ...

    def sync_media(self, user_id: UUID, media_payload: Dict[str, Any]) -> Result[ProfileEntity]:
        """Update media URLs after upload (profile pic, header, etc.)."""
        ...

    def get_profile_posts(self, username: str, cursor: Optional[str] = None, page_size: int = 10) -> Result[Dict[str, Any]]:
        """Fetch paginated posts for a profile."""
        ...

    def get_profile_image_urls(self, user_id: UUID) -> Result[Dict[str, str]]:
        """Get presigned or public URLs for profile images."""
        ...

    def get_user_id_by_username(self, username: str) -> Result[UUID]:
        """Return the user ID for a given username."""
        ...
    
    def get_public_profile_by_user_id(
        self, 
        user_id: UUID, 
        viewer_user_id: Optional[UUID], 
        fields: Optional[List[str]] = None
    ) -> Result[Union[ProfileEntity, ProfileLightEntity]]:
        ...