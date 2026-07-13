# apps/registration/domain/iusecases/ideregistration_verification_usecase.py
from abc import ABC, abstractmethod
from uuid import UUID
from core.results import Result
from apps.registration.domain.entities.deregistration_intent_challenge_entity import DeregistrationIntentChallengeEntity

class IDeregistrationVerificationUsecase(ABC):

    @abstractmethod
    def send_deregistration_email(self, email: str, plain_challenge_code: str) -> Result[None]:
        """Send the challenge code (plain) to the user's email via frontend-bridge instructions."""
        pass

    @abstractmethod
    def verify_challenge(self, challenge_code: str, intent_entity: DeregistrationIntentChallengeEntity) -> Result[UUID]:
        """Verify incoming numeric challenge against the stored entity. Returns Ok(user_id) on success."""
        pass
