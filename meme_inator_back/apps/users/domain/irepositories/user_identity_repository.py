from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from apps.users.domain.entities.user_entity import UserEntity  # Adjust import as needed

class IUserIdentityRepository(ABC):
    """Contract for accessing core user identity data and credentials."""

    @abstractmethod
    def get_user_by_user_id(self, user_id: UUID) -> Optional[UserEntity]:
        ...

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[UserEntity]:
        ...

    @abstractmethod
    def change_username(self, user_id: int, new_username: str) -> bool:
        """Change the username for a user."""
        ...

    @abstractmethod
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """Change the password for a user, verifying the current password."""
        ...