from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from uuid import UUID

from apps.registration.domain.entities.registration_intent_token_entity import RegistrationIntentTokenEntity
from core.results import Result

class ICreateRegistrationIntentTokenUsecase(ABC):
    @abstractmethod
    def execute(self, user_id: UUID) -> Result[RegistrationIntentTokenEntity]:
        """
        Create a registration intent token.
        Tracks a user's intent to register, is delted once user verifies registration via email. 

        Args:
            user_id: The ID of the user.
            expires_at: The datetime when the token expires.
            consumed: Whether the token has been consumed.

        Returns:
            Any: The created registration intent token or relevant result.
        """
        ...