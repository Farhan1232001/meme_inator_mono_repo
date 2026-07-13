from uuid import UUID
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.conf import settings

from apps.registration.domain.iservices.iregistration_token_service import (
    IRegistrationTokenService,
)


class RegistrationTokenService(IRegistrationTokenService):
    """
    Stateless registration token service using Django signing.
    """

    def __init__(self) -> None:
        self.signer = TimestampSigner(
            salt="registration",
        )
        self.max_age_seconds = getattr(
            settings,
            "REGISTRATION_TOKEN_TTL_SECONDS",
            600,  # 10 minutes default
        )

    def create_token(self, user_id: UUID) -> str:
        """
        Create a signed, timestamped token containing the user_id.
        """
        return self.signer.sign(str(user_id))

    def validate_token(self, token: str) -> UUID:
        """
        Validate token and return user_id.
        """
        try:
            unsigned_value = self.signer.unsign(
                token,
                max_age=self.max_age_seconds,
            )
            return UUID(unsigned_value)

        except SignatureExpired:
            raise ValueError("Registration token has expired")

        except BadSignature:
            raise ValueError("Invalid registration token")

    def consume_token(self, token: str) -> None:
        """
        No-op for stateless implementation.

        Token consumption requires persistence.
        """
        return None

    def revoke_tokens_for_user(self, user_id: UUID) -> None:
        """
        No-op for stateless implementation.

        Revocation requires persistence.
        """
        return None
