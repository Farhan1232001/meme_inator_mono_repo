from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from apps.users.domain.entities.user_entity import UserEntity


class IGetUserByTokenIdUseCase(ABC):
    """Interface for user identity operations."""
    
    @abstractmethod
    def execute(self, user_id: UUID) -> Optional[UserEntity]:
        """Get user by ID."""
        ...
