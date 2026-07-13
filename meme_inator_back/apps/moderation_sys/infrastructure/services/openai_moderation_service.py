# infrastructure/services/openai_moderation_service.py

import base64
import logging
from typing import Any

from openai import OpenAI
from openai.types import ModerationCreateResponse

from apps.moderation_sys.domain.enums.media_type_enums import MediaTypeEnum
from apps.moderation_sys.domain.enums.moderation_enums import ModerationProviderEnum
from apps.moderation_sys.domain.services.moderation_provider import IModerationProvider
from apps.moderation_sys.domain.value_objects.content_to_mod.content_to_moderate import (
    ContentToModerateVo,
)
from apps.moderation_sys.domain.value_objects.moderation_response import (
    ModerationResponseVo,
)

logger = logging.getLogger(__name__)


class OpenAIModerationService(IModerationProvider):
    """
    OpenAI moderation provider implementation.

    Uses:
    - omni-moderation-latest (text + image)
    - text-moderation-latest (text only)
    """

    def __init__(self, api_key: str, model: str = "omni-moderation-latest"):
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def moderate(self, content: ContentToModerateVo) -> ModerationResponseVo:
        try:
            moderation_input = self._build_api_input(content)

            response: ModerationCreateResponse = self._client.moderations.create(
                model=self._model,
                input=moderation_input,
            )

            if not response.results:
                raise ModerationProviderError(
                    "No results returned from moderation API"
                )

            result = response.results[0]

            return ModerationResponseVo(
                provider=ModerationProviderEnum.OPENAI_API,
                model=response.model,
                flagged=result.flagged,
                categories=result.categories.model_dump(),
                category_scores=result.category_scores.model_dump(),
                applied_input_types=getattr(
                    result,
                    "category_applied_input_types",
                    None,
                ),
            )

        except Exception as e:
            logger.exception("OpenAI moderation failed")
            raise ModerationProviderError(
                f"Moderation API call failed: {str(e)}"
            ) from e

    def _build_api_input(self, content: ContentToModerateVo) -> Any:
        """
        Build OpenAI moderation input payload.

        OpenAI accepts:
        - plain string for text moderation
        - multimodal list for image moderation

        Docs:
        https://platform.openai.com/docs/api-reference/moderations/create
        """
        # TEXT
        if content.content_type == MediaTypeEnum.TEXT:
            if not content.text_content:
                raise ModerationProviderError(
                    "TEXT content_type missing text_content"
                )

            return content.text_content.text

        # IMAGE
        if content.content_type == MediaTypeEnum.IMG:
            if not content.image_content:
                raise ModerationProviderError(
                    "IMG content_type missing image_content"
                )

            image = content.image_content

            image_url: str | None = None

            # Remote URL
            if image.image_url:
                image_url = image.image_url

            # Raw bytes -> base64 data URL
            elif image.image_data:
                mime_type = self._infer_image_mime_type(image.format)

                encoded = base64.b64encode(image.image_data).decode("utf-8")

                image_url = (
                    f"data:{mime_type};base64,{encoded}"
                )

            # retrieval_key should already be resolved upstream
            elif image.retrieval_key:
                raise ModerationProviderError(
                    "retrieval_key must be resolved before OpenAI moderation"
                )

            else:
                raise ModerationProviderError(
                    "No usable image source found"
                )

            return [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                }
            ]

        # ----------------------------
        # VIDEO
        # ----------------------------
        if content.content_type == MediaTypeEnum.VIDEO:
            raise ModerationProviderError(
                "OpenAI moderation API does not support video moderation"
            )

        raise ModerationProviderError(
            f"Unsupported content type: {content.content_type}"
        )

    def _infer_image_mime_type(self, image_format: str | None) -> str:
        """
        Convert image format into MIME type.
        """

        if not image_format:
            return "image/jpeg"

        normalized = image_format.lower()

        mapping = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "webp": "image/webp",
        }

        return mapping.get(normalized, "image/jpeg")


class ModerationProviderError(Exception):
    """Custom exception for moderation provider failures."""
    pass