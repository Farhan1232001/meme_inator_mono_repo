from abc import ABC, abstractmethod
from typing import Optional

from apps.users.domain.entities.user_entity import UserEntity


class IGetUserByUsernameUseCase(ABC):
    """Interface for user identity operations."""
    
    @abstractmethod
    def execute(self, username: str) -> Optional[UserEntity]:
        """Get user by username."""
        ...
    