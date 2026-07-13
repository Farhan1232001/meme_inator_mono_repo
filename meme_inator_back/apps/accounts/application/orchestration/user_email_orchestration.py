# apps/accounts/domain/orchestrations/user_email_orchestration.py
from typing import Optional, Any
from uuid import UUID
from django.db import transaction
from core.results import Ok, NotOk, Error, Result

from apps.accounts.domain.iusecases.iemail_change_usecase import IEmailChangeUsecase
from apps.users.domain.irepositories.user_repository import IUserRepository


class UserEmailOrchestration:
    """
    Coordinates email-change flows:
      - send change intent (to new email)
      - confirm change (challenge -> persist email)
    """

    def __init__(
        self,
        email_change_usecase: IEmailChangeUsecase,
        user_repo: IUserRepository,
    ):
        self._email_change_usecase = email_change_usecase
        self._user_repo = user_repo

    def change_email_intent(self, *, user_id: UUID, new_email: str) -> Result[Any]:
        """
        Initiate email change: validate user exists (optional) and call usecase to send challenge.
        """
        raise NotImplementedError

    def change_email_confirm(self, *, user_id: UUID, challenge_code: str) -> Result[Any]:
        """
        Confirm email change: verify challenge and update user's email atomically.
        """
        raise NotImplementedError
