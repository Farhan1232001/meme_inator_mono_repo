from abc import ABC, abstractmethod
from uuid import UUID

from apps.registration.domain.entities.registration_intent_token_entity import RegistrationIntentTokenEntity
# Assuming the original imports are available in the environment
# from apps.registration.domain.services.iregistration_token_service import IRegistrationTokenService
# from apps.users.domain.repositories.user_repository import IUserRepository

class IRegistrationVerificationUsecase(ABC):
    """
    Interface for the Registration Verification Usecase.
    Defines the contract for sending verification emails and verifying tokens.
    """

    # The __init__ method is typically not included in an interface in Python,
    # as the interface defines behavior, not implementation details or dependencies.
    # Concrete classes will define their own constructors.

    @abstractmethod
    def send_verification_email(self, email: str, intent_token: RegistrationIntentTokenEntity) -> None:
        """
        Abstract method to generate a token and send a verification email.
        """
        ...

    @abstractmethod
    def verify_token(self, token: str) -> UUID:
        """
        Abstract method to validate the token and mark the user as verified.
        """
        ...

