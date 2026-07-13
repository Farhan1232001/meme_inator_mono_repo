# domain/services/content_fetcher/django_content_fetcher.py

import logging
from typing import Tuple, Optional

from apps.moderation_sys.domain.value_objects.content_to_mod.content_to_moderate import ContentToModerateVo
from apps.moderation_sys.domain.enums.media_type_enums import MediaTypeEnum
from apps.moderation_sys.domain.enums.media_src_enum import MediaSourceEnum
from apps.moderation_sys.domain.services.content_fetcher.content_fetcher import (
    IContentFetcher, 
    ContentNotFoundError
)
from core.api_clients.moderation_api_client import ModerationSysApiClient

logger = logging.getLogger(__name__)


class DjangoContentFetcher(IContentFetcher):
    """Fetches both content metadata and raw bytes using Django ORM and external API client."""

    def __init__(self, api_client:ModerationSysApiClient):
        """
        Initialize the content fetcher.
        
        Args:
            api_client: Optional API client for external storage access
        """
        self._api_client = api_client

    # --- Metadata fetching ---
    def fetch_content(self, content_vo: ContentToModerateVo) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Returns (text_content, image_url, video_url).
        
        Raises:
            ValueError: If content source is unsupported
            ContentNotFoundError: If content cannot be retrieved
        """
        if content_vo.content_src == MediaSourceEnum.REQUEST_BODY:
            return self._fetch_from_request_body(content_vo)
        elif content_vo.content_src == MediaSourceEnum.LOCAL_DB:
            return self._fetch_from_local_db(content_vo)
        elif content_vo.content_src == MediaSourceEnum.EXTERNAL_STORAGE:
            return self._fetch_from_external(content_vo)
        else:
            raise ValueError(f"Unsupported content source: {content_vo.content_src}")

    def _fetch_from_request_body(self, content_vo: ContentToModerateVo) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Extract content directly from the request body. No need to extract data from another service."""
        text = None
        image_url = None
        video_url = None
        
        if content_vo.text_content:
            text = content_vo.text_content.text
        if content_vo.image_content:
            image_url = content_vo.image_content.image_url
        if content_vo.video_content:
            video_url = content_vo.video_content.video_url
            
        return text, image_url, video_url

    def _fetch_from_local_db(self, content_vo: ContentToModerateVo) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Fetch content from the local database."""
        try:
            from django.apps import apps
            Post = apps.get_model('your_app', 'Post')  # Adjust to your actual model
            obj = Post.objects.get(id=content_vo.content_id)
            return (
                getattr(obj, 'text', None), 
                getattr(obj, 'image_url', None), 
                getattr(obj, 'video_url', None)
            )
        except Exception as e:
            raise ContentNotFoundError(f"Content {content_vo.content_id} not found in DB: {e}")

    def _fetch_from_external(self, content_vo: ContentToModerateVo) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Fetch content references from external storage."""
        image_url = None
        video_url = None
        
        if content_vo.image_content:
            image_url = content_vo.image_content.retrieval_key or content_vo.image_content.image_url
        if content_vo.video_content:
            video_url = content_vo.video_content.retrieval_key or content_vo.video_content.video_url
            
        return None, image_url, video_url

    # --- Raw bytes fetching (for fingerprinting) ---
    def fetch_bytes(self, content_vo: ContentToModerateVo) -> Optional[bytes]:
        """
        Fetch raw binary content (image/video/text bytes) for fingerprinting.
        
        Returns None if raw bytes are not available.
        """
        if content_vo.content_src == MediaSourceEnum.REQUEST_BODY:
            return self._fetch_bytes_from_request_body(content_vo)
        elif content_vo.content_src == MediaSourceEnum.LOCAL_DB:
            return self._fetch_bytes_from_local_db(content_vo)
        elif content_vo.content_src == MediaSourceEnum.EXTERNAL_STORAGE:
            return self._fetch_bytes_from_external_store(content_vo)
        return None

    def _fetch_bytes_from_request_body(self, content_vo: ContentToModerateVo) -> Optional[bytes]:
        """Get raw bytes from the request body content."""
        if content_vo.content_type == MediaTypeEnum.TEXT:
            content = content_vo.text_content

            if content and content.text:
                return content_vo.text_content.text.encode('utf-8')
            
        elif content_vo.content_type == MediaTypeEnum.IMG:
            content = content_vo.image_content

            if not content: return None
            if content.image_data: return content.image_data
            # Fallback
            if content.image_url: return self._api_client.download_bytes_from_url(content.image_url)
            
        elif content_vo.content_type == MediaTypeEnum.VIDEO:
            content = content_vo.video_content
            if not content: return None
            if content.video_data: return content.video_data
            # Fallback
            if content.video_url: return self._api_client.download_bytes_from_url(content.video_url)
            
        return None

    def _fetch_bytes_from_local_db(self, content_vo: ContentToModerateVo) -> Optional[bytes]:
        """Get raw bytes from local database record."""
        try:
            from django.apps import apps
            Post = apps.get_model('posts', 'Post')
            obj = Post.objects.get(id=content_vo.content_id)
            return getattr(obj, 'raw_data', None)
        except Exception:
            return None

    def _fetch_bytes_from_external_store(
        self,
        content_vo: ContentToModerateVo
    ) -> Optional[bytes]:
        """
        Get raw bytes from external storage.

        Strategy:
        - If URL exists -> download directly from URL
        - Else if retrieval_key exists -> delegate to storage provider client
        - Else -> return None
        """

        if not self._api_client:
            logger.warning(
                "No API client configured for external storage"
            )
            return None

        content_type: MediaTypeEnum = content_vo.get_content_type()

        match content_type:

            # ---------------------------------------------------------
            # IMAGE
            # ---------------------------------------------------------
            case MediaTypeEnum.IMG:

                content = content_vo.image_content

                if not content:
                    logger.warning(
                        "IMG content type but image_content missing"
                    )
                    return None

                # ---------------------------------------------
                # URL-backed external content
                # ---------------------------------------------
                if content.image_url is not None:

                    try:
                        logger.info(
                            f"Downloading image from URL: {content.image_url}"
                        )

                        return self._api_client.download_bytes_from_url(
                            content.image_url
                        )

                    except Exception as e:
                        logger.exception(
                            f"Failed downloading image URL: {e}"
                        )
                        return None

                # ---------------------------------------------
                # Retrieval-key-backed external content
                # ---------------------------------------------
                if content.retrieval_key is not None:

                    try:
                        logger.info(
                            f"Downloading image from retrieval key: "
                            f"{content.retrieval_key}"
                        )

                        return self._api_client.download_bytes_from_storage_key(
                            content.retrieval_key
                        )

                    except Exception as e:
                        logger.exception(
                            f"Failed downloading image from storage key: {e}"
                        )
                        return None

                logger.warning(
                    "Image external content missing both "
                    "image_url and retrieval_key"
                )
                return None

            # ---------------------------------------------------------
            # VIDEO
            # ---------------------------------------------------------
            case MediaTypeEnum.VIDEO:

                content = content_vo.video_content

                if not content:
                    logger.warning(
                        "VIDEO content type but video_content missing"
                    )
                    return None

                # ---------------------------------------------
                # URL-backed external content
                # ---------------------------------------------
                if content.video_url is not None:

                    try:
                        logger.info(
                            f"Downloading video from URL: {content.video_url}"
                        )

                        return self._api_client.download_bytes_from_url(
                            content.video_url
                        )

                    except Exception as e:
                        logger.exception(
                            f"Failed downloading video URL: {e}"
                        )
                        return None

                # ---------------------------------------------
                # Retrieval-key-backed external content
                # ---------------------------------------------
                if content.retrieval_key is not None:

                    try:
                        logger.info(
                            f"Downloading video from retrieval key: "
                            f"{content.retrieval_key}"
                        )

                        return self._api_client.download_bytes_from_storage_key(
                            content.retrieval_key
                        )

                    except Exception as e:
                        logger.exception(
                            f"Failed downloading video from storage key: {e}"
                        )
                        return None

                logger.warning(
                    "Video external content missing both "
                    "video_url and retrieval_key"
                )
                return None

            # ---------------------------------------------------------
            # TEXT
            # ---------------------------------------------------------
            case MediaTypeEnum.TEXT:

                content = content_vo.text_content

                if not content:
                    logger.warning(
                        "TEXT content type but text_content missing"
                    )
                    return None

                return content.text.encode("utf-8")

            # ---------------------------------------------------------
            # UNKNOWN
            # ---------------------------------------------------------
            case _:

                logger.warning(
                    f"Unsupported content type: {content_type}"
                )

                return None