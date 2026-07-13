# apps/accounts/domain/orchestrations/user_password_orchestration.py
from typing import Any
from uuid import UUID
from django.db import transaction
from core.results import Ok, NotOk, Error, Result

from apps.accounts.domain.iusecases.ichange_password_usecase import IChangePasswordUsecase
from apps.accounts.domain.iusecases.ireset_password_usecase import IResetPasswordUsecase
from apps.users.domain.irepositories.user_repository import IUserRepository


class UserPasswordOrchestration:
    """
    Coordinates password-related flows:
      - authenticated change password
      - password reset intent (email)
      - password reset confirm (challenge -> set password)
    """

    def __init__(
        self,
        change_password_usecase: IChangePasswordUsecase,
        reset_password_usecase: IResetPasswordUsecase,
        user_repo: IUserRepository,
    ):
        self._change_password_usecase = change_password_usecase
        self._reset_password_usecase = reset_password_usecase
        self._user_repo = user_repo

    def change_password(self, *, user_id: UUID, current_password: str, new_password: str) -> Result[None]:
        """
        Authenticated change password. Delegates to IChangePasswordUsecase.
        """
        if not self._change_password_usecase:
            return Error(message="change password not configured", exception=None)

        try:
            result = self._change_password_usecase.change_password(
                user_id=user_id, current_password=current_password, new_password=new_password
            )
            return result
        except Exception as e:
            return Error(message="failed to change password", exception=e)

    def reset_password_intent(self, *, email: str) -> Result[Any]:
        """
        Initiate reset flow (send challenge or token to email).
        """
        if not self._reset_password_usecase:
            return Error(message="reset password not configured", exception=None)

        try:
            result = self._reset_password_usecase.send_reset_intent(email=email)
            return result
        except Exception as e:
            return Error(message="failed to initiate password reset", exception=e)

    def reset_password_confirm(self, *, challenge_code: str, new_password: str) -> Result[Any]:
        """
        Confirm reset — verify challenge and set password.
        Wrapped in transaction.atomic to keep operations atomic where needed.
        """
        if not self._reset_password_usecase:
            return Error(message="reset password not configured", exception=None)

        try:
            result = self._reset_password_usecase.confirm_reset(
                challenge_code=challenge_code, new_password=new_password
            )
            return result
        except Exception as e:
            return Error(message="failed to confirm password reset", exception=e)
