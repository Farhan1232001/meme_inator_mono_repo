from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from apps.users.domain.entities.friendship_entity import FriendshipEntity

class IFriendshipRepository(ABC):
    @abstractmethod
    def create(self, friendship: FriendshipEntity) -> FriendshipEntity:
        """Create a new friendship record."""
        raise NotImplementedError

    @abstractmethod
    def get_by_users(self, user_a_id: UUID, user_b_id: UUID) -> Optional[FriendshipEntity]:
        """Retrieve active friendship between two users."""
        raise NotImplementedError

    @abstractmethod
    def list_active_for_user(self, user_id: UUID) -> List[FriendshipEntity]:
        """List all active friends of a user."""
        raise NotImplementedError

    @abstractmethod
    def end_friendship(self, friendship_id: UUID) -> None:
        """Mark a friendship as inactive."""
        raise NotImplementedError

    @abstractmethod
    def exists(self, user_a_id: UUID, user_b_id: UUID) -> bool:
        """Check if an active friendship exists."""
        raise NotImplementedError