from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from apps.users.domain.entities.friend_request_entity import FriendRequestEntity



class IFriendRequestRepository(ABC):
    """
    Domain-layer interface for interacting with FriendRequest data.
    Implemented later in the infrastructure layer using Django ORM.
    """

    @abstractmethod
    def create_friend_request(
        self,
        sender_id: UUID,
        receiver_id: UUID,
    ) -> FriendRequestEntity:
        """
        Creates a new friend request. Should throw domain-level exception if
        a duplicate request exists or if users are invalid.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, request_id: UUID) -> Optional[FriendRequestEntity]:
        """
        Fetch a friend request by its ID.
        """
        raise NotImplementedError

    @abstractmethod
    def get_pending_request(
        self,
        sender_id: UUID,
        receiver_id: UUID,
    ) -> Optional[FriendRequestEntity]:
        """
        Retrieve an existing pending request between two users, if any.
        """
        raise NotImplementedError

    @abstractmethod
    def list_received_requests(self, user_id: UUID) -> List[FriendRequestEntity]:
        """
        All friend requests where the user is the receiver.
        """
        raise NotImplementedError

    @abstractmethod
    def list_sent_requests(self, user_id: UUID) -> List[FriendRequestEntity]:
        """
        All friend requests where the user is the sender.
        """
        raise NotImplementedError

    @abstractmethod
    def update_status(
        self,
        request_id: UUID,
        status: str,
    ) -> FriendRequestEntity:
        """
        Update the status of the friend request.
        Allowed: 'pending', 'accepted', 'rejected', 'cancelled'
        """
        raise NotImplementedError

    @abstractmethod
    def delete_request(self, request_id: UUID) -> None:
        """
        Remove the friend request.
        """
        raise NotImplementedError

    @abstractmethod
    def exists_between(self, user1_id: UUID, user2_id: UUID) -> bool:
        """
        Check if any friend request exists between two users (in either direction).
        """
        raise NotImplementedError


    # Maintainance methods
    @abstractmethod
    def expire_old_requests(self) -> int:
        """Mark expired pending requests as EXPIRED and return count."""
        pass