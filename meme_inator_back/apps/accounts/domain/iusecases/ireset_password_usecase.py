# apps/accounts/domain/iusecases/ireset_password_usecase.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from core.results import Result

class IResetPasswordUsecase(ABC):
    """
    Password reset usecase — two-step:
      1) send_reset_intent(email) -> create and send challenge/token
      2) confirm_reset(challenge_code, new_password) -> verify and set new password
    """

    @abstractmethod
    def send_reset_intent(self, *, email: str) -> Result[Any]:
        """
        Create/reset intent (challenge or token), persist the intent, and email the user.
        Return Ok on success or NotOk/Error.
        """
        raise NotImplementedError

    @abstractmethod
    def confirm_reset(self, *, challenge_code: str, new_password: str) -> Result[Any]:
        """
        Verify the challenge_code (or token) and set the new password for the corresponding user.
        Return Ok on success or NotOk/Error.
        """
        raise NotImplementedError
