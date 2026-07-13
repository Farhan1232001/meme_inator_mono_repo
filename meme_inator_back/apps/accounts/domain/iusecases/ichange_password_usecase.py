from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from core.results import Result


class IChangePasswordUsecase(ABC):
    """
    Authenticated password change.
    """

    @abstractmethod
    def change_password(
        self,
        *,
        user_id: UUID,
        current_password: str,
        new_password: str,
    ) -> Result[None]:
        ...
