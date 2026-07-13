# apps/moderation_sys/infrastructure/factories/moderation_provider_factory.py

from django.conf import settings

from apps.moderation_sys.domain.enums.moderation_enums import ModerationProviderEnum
from apps.moderation_sys.domain.services.moderation_provider import IModerationProvider
from apps.moderation_sys.infrastructure.services.openai_moderation_service import OpenAIModerationService

class ModerationProviderFactory:
    """
    Factory responsible for constructing moderation provider implementations.
    """

    @staticmethod
    def create(
        provider: ModerationProviderEnum,
    ) -> IModerationProvider:

        match provider:

            case ModerationProviderEnum.OPENAI_API:
                return OpenAIModerationService(
                    api_key=settings.OPENAI_API_KEY,
                    model="omni-moderation-latest",
                )

            case _:
                raise ValueError(
                    f"Unsupported moderation provider: {provider}"
                )