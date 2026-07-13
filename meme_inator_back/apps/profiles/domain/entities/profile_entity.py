from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional


@dataclass
class ProfileEntity:
    # --- Identity ---
    user_id: UUID
    username: str 

    # --- Profile appearance ---
    description: Optional[str]
    background_color: Optional[str]
    profile_pic_key: Optional[str]
    profile_header_img_key: Optional[str]
    bg_img_key: Optional[str]
    profile_theme_music_key: str

    # --- Presence messages ---
    is_online_msg: Optional[str]
    is_offline_msg: Optional[str]

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

    # --- Behavior ---
    def to_dict(self):
        """Convert to dict, including None values."""
        return {
            'user_id': str(self.user_id),
            'username': self.username,
            'description': self.description,
            'background_color': self.background_color,
            'profile_pic_key': self.profile_pic_key,
            'profile_header_img_key': self.profile_header_img_key,
            'bg_img_key': self.bg_img_key,
            'profile_theme_music_key': self.profile_theme_music_key,
            'is_online_msg': self.is_online_msg,
            'is_offline_msg': self.is_offline_msg,
            'upload_count': self.upload_count,
            'followers_count': self.followers_count,
            'following_count': self.following_count,
            'friends_count': self.friends_count,
            'likes_given': self.likes_given,
            'posts_uploaded': self.posts_uploaded,
            'comments_posted': self.comments_posted,
            'dislikes_given': self.dislikes_given,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
        }