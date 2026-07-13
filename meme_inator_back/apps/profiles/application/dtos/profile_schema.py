from ninja import Schema
from uuid import UUID
from typing import Optional
from datetime import datetime

from pydantic import ConfigDict


class ProfileSchema(Schema):
    """Full profile schema with all fields."""
    # --- Identity ---
    user_id: UUID
    username: str

    # --- Profile appearance ---
    description: Optional[str] = None
    background_color: Optional[str] = None
    profile_pic_key: Optional[str] = None
    profile_header_img_key: Optional[str] = None
    bg_img_key: Optional[str] = None
    profile_theme_music_key: str

    # --- Presence messages ---
    is_online_msg: Optional[str] = None
    is_offline_msg: Optional[str] = None

    # --- Counters ---
    upload_count: int
    followers_count: int
    following_count: int
    friends_count: int
    likes_given: int
    posts_uploaded: int
    comments_posted: int
    dislikes_given: int

    # --- Timestamps ---
    last_updated: datetime


class ProfileDynamicSchema(Schema):
    """
    Dynamic profile schema that can return any subset of fields.
    Used when the 'fields' parameter is provided.
    """
    # Make all fields optional so any combination works
    user_id: Optional[UUID] = None
    username: Optional[str] = None
    description: Optional[str] = None
    background_color: Optional[str] = None
    profile_pic_key: Optional[str] = None
    profile_header_img_key: Optional[str] = None
    bg_img_key: Optional[str] = None
    profile_theme_music_key: Optional[str] = None
    is_online_msg: Optional[str] = None
    is_offline_msg: Optional[str] = None
    upload_count: Optional[int] = None
    followers_count: Optional[int] = None
    following_count: Optional[int] = None
    friends_count: Optional[int] = None
    likes_given: Optional[int] = None
    posts_uploaded: Optional[int] = None
    comments_posted: Optional[int] = None
    dislikes_given: Optional[int] = None
    last_updated: Optional[datetime] = None

class ProfileMiniDashboardView(Schema):
    """
    shape needed for mini dashboard in menu. 
    """
    user_id: Optional[UUID] = None
    username: Optional[str] = None
    background_color: Optional[str] = None
    profile_pic_key: Optional[str] = None
    is_online_msg: Optional[str] = None
    is_offline_msg: Optional[str] = None
    followers_count: Optional[int] = None
    following_count: Optional[int] = None
    