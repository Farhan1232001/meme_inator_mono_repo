from abc import ABC, abstractmethod
from uuid import UUID


class IRegistrationTokenService(ABC):
    """
    Responsible for creating, validating, and consuming
    one-time registration confirmation tokens.
    """

    @abstractmethod
    def create_token(self, user_id: UUID) -> str:
        """
        Create a one-time registration token for a user.
        """
        raise NotImplementedError

    @abstractmethod
    def validate_token(self, token: str) -> UUID:
        """
        Validate a token and return the associated user_id.

        Raises:
            InvalidTokenError
            ExpiredTokenError
        """
        raise NotImplementedError

    @abstractmethod
    def consume_token(self, token: str) -> None:
        """
        Mark a token as used so it cannot be reused.
        """
        raise NotImplementedError

    @abstractmethod
    def revoke_tokens_for_user(self, user_id: UUID) -> None:
        """
        Revoke all active registration tokens for a user.
        """
        raise NotImplementedError
