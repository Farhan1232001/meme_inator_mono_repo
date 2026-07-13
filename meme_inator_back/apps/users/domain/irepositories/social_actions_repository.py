from abc import ABC, abstractmethod
from typing import List, Optional
from typing_extensions import Literal

from apps.users.domain.entities.friend_request_entity import FriendRequestEntity
from apps.users.domain.entities.user_entity import UserEntity

class ISocialActionsRepository(ABC):
    """Contract for accessing and modifying social data (Following, Friends)."""
    
    # Following
    @abstractmethod
    def follow_user(self, follower_id: int, target_id: int):
        pass

    @abstractmethod
    def unfollow_user(self, follower_id: int, target_id: int):
        pass

    @abstractmethod
    def get_followers(self, user_id: int) -> List[UserEntity]:
        pass

    @abstractmethod
    def get_following(self, user_id: int) -> List[UserEntity]:
        pass
    
    # Friends
    @abstractmethod
    def create_friend_request(self, sender_id: int, receiver_id: int) -> FriendRequestEntity:
        pass

    @abstractmethod
    def get_friend_requests(
        self, 
        user_id: int, 
        type: Literal['incoming', 'outgoing']
    ) -> List['FriendRequestEntity']:
        pass

    @abstractmethod
    def update_friend_request_status(self, request_id: int, status: str) -> Optional[FriendRequestEntity]:
        pass

    @abstractmethod
    def delete_friend_request(self, request_id: int):
        pass

    @abstractmethod
    def remove_friend(self, user_id: int, friend_id: int):
        pass