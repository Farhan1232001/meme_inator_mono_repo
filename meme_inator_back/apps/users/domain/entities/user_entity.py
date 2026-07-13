from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime,  timezone
from typing import Optional, Dict, Any
from uuid import UUID

from apps.profiles.domain.entities.profile_entity import ProfileEntity
from apps.users.domain.entities.followship_entity import FollowShipEntity
from apps.users.domain.entities.friend_request_entity import FriendRequestEntity
from apps.users.domain.entities.friendship_entity import FriendshipEntity



@dataclass
class UserEntity:
    id: UUID
    username: str
    email: str

    is_online: bool = False
    # Now attribute of an Entitlement
    # is_pro_user: bool = False
    is_verified: bool = False
    is_banned: bool = False
    
    date_joined: datetime = datetime.now(timezone.utc) # == created_at

    profile: Optional[ProfileEntity] = None
    is_soft_deleted: bool = False

    # --- Behaviors ---
    def follow(self, target: UserEntity) -> FollowShipEntity:
        raise NotImplemented

    def unfollow(self, target: UserEntity) -> bool:
        raise NotImplemented

    def is_following(self, target: UserEntity) -> bool:
        raise NotImplemented

    def block(self, target: UserEntity) -> None:
        raise NotImplemented

    def unblock(self, target: UserEntity) -> None:
        raise NotImplemented

    def send_friend_request(
        self,
        target: UserEntity,
        message: Optional[str] = None,
    ) -> FriendRequestEntity:
        raise NotImplemented
    def accept_friend_request(
        self,
        request: FriendRequestEntity,
    ) -> FriendshipEntity:
        raise NotImplemented

    def reject_friend_request(self, request: FriendRequestEntity) -> None:
        raise NotImplemented

    def get_followers_count(self) -> int:
        raise NotImplementedError

    def get_following_count(self) -> int:
        raise NotImplementedError

    def get_public_profile(self) -> ProfileEntity:
        raise NotImplemented

    def soft_delete(self, reason: Optional[str] = None) -> None:
        raise NotImplemented

    def restore_from_soft_delete(self) -> None:
        raise NotImplemented

    def set_is_online(self, is_online: bool) -> None:
        self.is_online = is_online

    def verify(self, verified_by: Optional[UUID] = None) -> None:
        raise NotImplemented

    def ban(self, reason: Optional[str] = None) -> None:
        raise NotImplemented

    def unban(self) -> None:
        raise NotImplemented

