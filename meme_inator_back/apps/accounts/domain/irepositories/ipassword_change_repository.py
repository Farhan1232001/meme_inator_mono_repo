from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from core.results import Result


class IPasswordChangeRepository(ABC):
    """
    Low-level password operations.
    """

    @abstractmethod
    def verify_current_password(
        self,
        *,
        user_id: UUID,
        current_password: str,
    ) -> Result[None]:
        """
        Ensure provided password matches stored hash.
        """
        raise NotImplementedError

    @abstractmethod
    def set_new_password(
        self,
        *,
        user_id: UUID,
        new_password: str,
    ) -> Result[None]:
        """
        Persist new password hash.
        """
        raise NotImplementedError
