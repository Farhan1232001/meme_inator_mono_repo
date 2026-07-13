from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from uuid import UUID


@dataclass
class ProfileLightEntity:
    """
    Lightweight profile entity for partial responses.
    Contains only the fields that can be requested via the 'fields' parameter.
    """
    # --- Identity ---
    user_id: Optional[UUID] = None
    username: Optional[str] = None

    # --- Profile appearance (these will be keys, hydrated later) ---
    description: Optional[str] = None
    background_color: Optional[str] = None
    profile_pic_key: Optional[str] = None  
    profile_header_img_key: Optional[str] = None  
    bg_img_key: Optional[str] = None  
    profile_theme_music_key: Optional[str] = None  

    # --- Presence messages ---
    is_online_msg: Optional[str] = None
    is_offline_msg: Optional[str] = None

    # --- Counters ---
    upload_count: Optional[int] = None
    followers_count: Optional[int] = None
    following_count: Optional[int] = None
    friends_count: Optional[int] = None
    likes_given: Optional[int] = None
    posts_uploaded: Optional[int] = None
    comments_posted: Optional[int] = None
    dislikes_given: Optional[int] = None
    
    # --- Timestamps ---
    last_updated: Optional[datetime] = None

    # Track which fields are actually set (for hydration)
    _requested_fields: List[str] = field(default_factory=list, repr=False)


    def to_dict(self) -> dict:
        """Return dict with exactly the fields that were set (the requested ones)."""
        return {
            field_name: getattr(self, field_name)
            for field_name in self._requested_fields
        }
