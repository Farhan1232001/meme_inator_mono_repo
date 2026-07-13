# apps/accounts/domain/iusecases/iemail_change_usecase.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID
from core.results import Result

class IEmailChangeUsecase(ABC):
    """
    Email change usecase — two-step:
      1) send_change_intent(user_id, new_email) -> sends challenge to new email
      2) confirm_change(user_id, challenge_code) -> verifies code and updates email
    """

    @abstractmethod
    def send_change_intent(self, *, user_id: UUID, new_email: str) -> Result[Any]:
        """
        Persist an email-change intent and send a verification challenge to the proposed new email.
        """
        raise NotImplementedError

    @abstractmethod
    def confirm_change(self, *, user_id: UUID, challenge_code: str) -> Result[Any]:
        """
        Verify challenge and update the user's email.
        """
        raise NotImplementedError
