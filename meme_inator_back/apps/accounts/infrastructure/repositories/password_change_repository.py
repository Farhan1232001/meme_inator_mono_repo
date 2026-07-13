from uuid import UUID
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction

from core.results import Ok, NotOk, Error, Result
from apps.accounts.domain.irepositories.ipassword_change_repository import (
    IPasswordChangeRepository,
)
from apps.users.infrastructure.models.user_model import UserModel


class PasswordChangeRepository(IPasswordChangeRepository):
    """
    Django ORM implementation for password updates.
    """

    def verify_current_password(
        self,
        *,
        user_id: UUID,
        current_password: str,
    ) -> Result[None]:
        try:
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return NotOk(
                    message="user not found",
                    static_msg="USER_NOT_FOUND",
                    status_code=404,
                )

            if not check_password(current_password, user.password):
                return NotOk(
                    message="current password is incorrect",
                    static_msg="INVALID_PASSWORD",
                    status_code=400,
                )

            return Ok(None)

        except Exception as e:
            return Error(
                message="failed to verify current password",
                exception=e,
            )

    def set_new_password(
        self,
        *,
        user_id: UUID,
        new_password: str,
    ) -> Result[None]:
        try:
            with transaction.atomic():
                updated = UserModel.objects.filter(id=user_id).update(
                    password=make_password(new_password)
                )

                if updated == 0:
                    return NotOk(
                        message="user not found",
                        static_msg="USER_NOT_FOUND",
                        status_code=404,
                    )

                return Ok(None)

        except Exception as e:
            return Error(
                message="failed to set new password",
                exception=e,
            )
