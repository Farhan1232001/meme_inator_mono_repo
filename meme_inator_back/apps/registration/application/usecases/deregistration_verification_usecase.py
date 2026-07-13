# apps/registration/domain/usecases/deregistration_verification_usecase.py
from datetime import datetime, timezone
from uuid import UUID
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from core.results import Ok, NotOk, Error, Result

from apps.registration.domain.entities.deregistration_intent_challenge_entity import DeregistrationIntentChallengeEntity
from apps.registration.domain.iusecases.ideregistration_verification_usecase import IDeregistrationVerificationUsecase
from apps.registration.infrastructure.repositories.deregistration_intent_challenge_repository import DeregistrationIntentChallengeRepository

class DeregistrationVerificationUsecase(IDeregistrationVerificationUsecase):
    def __init__(self, challenge_repo: DeregistrationIntentChallengeRepository):
        self._challenge_repo = challenge_repo

    def send_deregistration_email(self, email: str, plain_challenge_code: str) -> Result[None]:
        """
        Sends an email containing the numeric challenge and a frontend-bridge link.
        """
        try:
            frontend_url = f"{settings.FRONTEND_URL}/frontend-bridge/confirm-deregistration"
            subject = "Confirm account deregistration"
            message = (
                f"Your deregistration code is: {plain_challenge_code}\n\n"
                f"Open the app and go to:\n{frontend_url}\n\n"
                "Enter the code in the app to confirm account deregistration."
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            return Ok(None)
        except Exception as e:
            return Error(message="failed to send deregistration email", exception=e)

    def verify_challenge(self, challenge_code: str, intent_entity: DeregistrationIntentChallengeEntity) -> Result[UUID]:
        """
        Verify the numeric code. If valid, mark consumed via repo and return user_id.
        """
        try:
            if intent_entity.consumed:
                return NotOk(message="Challenge already consumed", static_msg="CHALLENGE_CONSUMED", status_code=400)

            if intent_entity.expires_at < datetime.now(timezone.utc):
                return NotOk(message="Challenge expired", static_msg="CHALLENGE_EXPIRED", status_code=410)

            # Compare provided code with stored hash
            ok = check_password(challenge_code, intent_entity.code_hash)
            if not ok:
                return NotOk(message="Invalid challenge code", static_msg="INVALID_CHALLENGE", status_code=400)

            # Mark as consumed via repository
            repo_result = self._challenge_repo.mark_consumed(intent_entity.id)
            if isinstance(repo_result, (NotOk, Error)):
                return repo_result

            return Ok(intent_entity.user_id)

        except Exception as e:
            return Error(message="failed to verify challenge", exception=e)
