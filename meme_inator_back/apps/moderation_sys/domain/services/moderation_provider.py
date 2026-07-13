# domain/services/moderation_provider_interface.py
from abc import ABC, abstractmethod

from apps.moderation_sys.domain.value_objects.moderation_response import ModerationResponseVo
from ..value_objects.content_to_mod.content_to_moderate import ContentToModerateVo


class IModerationProvider(ABC):
    """
    Abstraction for external content moderation services.
    Supports text and image inputs.
    """

    @abstractmethod
    def moderate(self, content: ContentToModerateVo) -> ModerationResponseVo:
        """
        Send content to the moderation API and return a unified result.
        
        Args:
            content: Content to be moderated (text and/or image URL).
            
        Returns:
            ModerationResultVo with flagged status, categories and confidence scores.
            
        Raises:
            ModerationProviderError: If the API call fails.
        """
        ...