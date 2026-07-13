# apps/registration/domain/iusecases/icreate_deregistration_intent_usecase.py
from abc import ABC, abstractmethod
from uuid import UUID
from core.results import Result
from apps.registration.domain.entities.deregistration_intent_challenge_entity import DeregistrationIntentChallengeEntity

class ICreateDeregistrationIntentUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID) -> Result[tuple[DeregistrationIntentChallengeEntity, str]]:
        """
        Creates a DeregistrationIntentChallengeEntity and returns (entity, plain_challenge_code)
        Plain challenge code must only be used to email the user; do not persist it.
        """
        ...
