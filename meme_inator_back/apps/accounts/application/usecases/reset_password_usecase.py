# apps/accounts/domain/usecases/reset_password_usecase.py
from datetime import datetime, timedelta, timezone
from uuid import uuid4, uuid7
import secrets

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password

from core.results import Ok, NotOk, Error, Result

from apps.accounts.domain.entities.password_reset_intent_entity import PasswordResetIntentEntity
from apps.accounts.domain.iusecases.ireset_password_usecase import IResetPasswordUsecase
from apps.accounts.domain.irepositories.ipassword_reset_intent_repository import (
    IPasswordResetIntentRepository,
)
from apps.users.domain.irepositories.user_repository import IUserRepository


class ResetPasswordUsecase(IResetPasswordUsecase):
    """
    Two-step password reset:
      1) send_reset_intent(email)
      2) confirm_reset(challenge_code, new_password)
    """

    def __init__(
        self,
        user_repo: IUserRepository,
        reset_intent_repo: IPasswordResetIntentRepository,
    ):
        self._user_repo = user_repo
        self._reset_intent_repo = reset_intent_repo

    # -----------------------------
    # STEP 1: SEND RESET INTENT
    # -----------------------------
    def send_reset_intent(self, *, email: str) -> Result[None]:
        try:
            user = self._user_repo.get_by_email(email)
            if not user:
                # Avoid email enumeration
                return Ok(None)

            # Generate short challenge code
            plain_code = secrets.token_hex(3).upper()  # e.g. "A9F2C1"
            code_hash = make_password(plain_code)

            intent = PasswordResetIntentEntity(
                id=uuid7(),
                user_id=user.id,
                challenge_hash=code_hash,
                expires_at=datetime.now(timezone.utc)
                + timedelta(seconds=settings.PASSWORD_RESET_CHALLANGE_TTL_SECONDS),
                consumed=False,
            )

            repo_result = self._reset_intent_repo.create(intent)
            if isinstance(repo_result, (NotOk, Error)):
                return repo_result

            frontend_url = (
                f"{settings.FRONTEND_URL}/frontend-bridge/reset-password"
            )

            subject = "Reset your password"
            message = (
                f"Your password reset code is:\n\n"
                f"{plain_code}\n\n"
                f"Open the app and go to:\n"
                f"{frontend_url}\n\n"
                "This code expires in 15 minutes."
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )

            return Ok(None)

        except Exception as e:
            return Error(message="failed to send password reset intent", exception=e)

    # -----------------------------
    # STEP 2: CONFIRM RESET
    # -----------------------------
    def confirm_reset(
        self,
        *,
        challenge_code: str,
        new_password: str,
    ) -> Result[None]:
        try:
            intent = self._reset_intent_repo.get_by_challenge(challenge_code)
            if not intent:
                return NotOk(
                    message="Invalid reset challenge",
                    static_msg="INVALID_CHALLENGE",
                    status_code=400,
                )

            if intent.consumed:
                return NotOk(
                    message="Challenge already used",
                    static_msg="CHALLENGE_CONSUMED",
                    status_code=400,
                )

            if intent.expires_at < datetime.now(timezone.utc):
                return NotOk(
                    message="Reset challenge expired",
                    static_msg="CHALLENGE_EXPIRED",
                    status_code=410,
                )

            if not check_password(challenge_code, intent.challenge_hash):
                return NotOk(
                    message="Invalid reset challenge",
                    static_msg="INVALID_CHALLENGE",
                    status_code=400,
                )

            # TODO: Validate password here. 
            # Validate password strength (Django validators)
            # validate_password(new_password)

            user = self._user_repo.get_by_id(intent.user_id)
            if not user:
                return NotOk(
                    message="User not found",
                    static_msg="USER_NOT_FOUND",
                    status_code=404,
                )

            # Update password
            user.set_password(new_password)
            self._user_repo.update(user)

            # Mark intent consumed
            consume_result = self._reset_intent_repo.mark_consumed(intent.id)
            if isinstance(consume_result, (NotOk, Error)):
                return consume_result

            return Ok(None)

        except Exception as e:
            return Error(message="failed to confirm password reset", exception=e)
