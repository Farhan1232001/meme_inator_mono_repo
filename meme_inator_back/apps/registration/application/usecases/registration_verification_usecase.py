from datetime import datetime, timezone
from uuid import UUID
from django.conf import settings
from django.core.mail import send_mail
from apps.registration.domain.entities.registration_intent_token_entity import RegistrationIntentTokenEntity
from apps.registration.domain.iservices.iregistration_token_service import IRegistrationTokenService
from apps.registration.domain.iusecases.iregistration_verification_usecase import IRegistrationVerificationUsecase
from apps.registration.infrastructure.repositories.registration_intent_token_repository import RegistrationIntentTokenRepository
from core.results import Error, NotOk, Ok, Result


class RegistrationVerificationUsecase(IRegistrationVerificationUsecase):
    """
    Handles sending and verifying registration email tokens.
    """

    def __init__(self, registration_intent_token_repo: RegistrationIntentTokenRepository):
        self._registration_intent_token_repo = registration_intent_token_repo

    def send_verification_email(self, email: str, intent_token: RegistrationIntentTokenEntity) -> None:
        """
        Sends a verification email using the intent token.
        """
        # TODO: For register verification to work, implement front-end bridge
        # LOOK at frontend-verify-registration sequence diagram made in mermaid. 
        verification_url = f"{settings.FRONTEND_URL}/frontend-bridge/verify-registration?token={intent_token.token}"

        subject = "Verify your email"
        message = f"Please click the following link to verify your account:\n{verification_url}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
        )


    def verify_token(self, token: str) -> Result[UUID]:
        result = self._registration_intent_token_repo.get_by_token(token)

        if isinstance(result, (NotOk, Error)):
            return result

        intent = result.value

        if intent.consumed:
            return NotOk(
                message="Token already consumed",
                static_msg="TOKEN_CONSUMED",
                status_code=400,
            )

        if intent.expires_at < datetime.now(timezone.utc):
            return NotOk(
                message="Token expired",
                static_msg="TOKEN_EXPIRED",
                status_code=410,
            )

        # mark consumed
        consume_result = self.registration_repo.mark_consumed(token)
        if isinstance(consume_result, NotOk) or isinstance(consume_result, Error):
            return consume_result

        return Ok(intent.user_id)
