import hashlib
from typing import Optional
from uuid import UUID
from django.db import transaction

from apps.moderation_sys.domain.enums.media_src_enum import MediaSourceEnum
from apps.moderation_sys.domain.enums.media_type_enums import MediaTypeEnum
from apps.moderation_sys.domain.enums.storage_src_enum import StorageLocationEnum
from apps.moderation_sys.domain.irepositories.blob_storage_repository import IBlobStorageRepository, ContentBlobReference
from apps.moderation_sys.domain.value_objects.content_to_mod.content_to_moderate import ContentToModerateVo
from apps.moderation_sys.infrastructure.models.content_blob_model import ContentBlobModel

class DjangoBlobStorageRepository(IBlobStorageRepository):
    """Infrastructure repository for storing and retrieving content blobs."""

    @transaction.atomic
    def store(self, content_vo: ContentToModerateVo, raw_bytes: Optional[bytes]) -> ContentBlobReference:
        """Store content blob, using deduplication and metadata extraction similar to _get_or_create_content_blob."""
        content_type = content_vo.content_type
        content_src = content_vo.content_src

        # --- Extract raw bytes, storage key, mime type, and file format based on content type/source ---
        blob_data = None
        storage_key = ""
        mime_type = "application/octet-stream"
        file_format = None
        file_size = 0
        external_storage_url = None
        external_storage_key = None
        external_storage_provider = None

        match content_type:
            case MediaTypeEnum.TEXT:
                text_vo = content_vo.text_content
                raw_bytes_local = text_vo.text.encode('utf-8')
                blob_data = raw_bytes_local
                mime_type = "text/plain"
                file_format = 'txt'
                file_size = len(raw_bytes_local)
                storage_key = ""
            case MediaTypeEnum.IMG:
                img_vo = content_vo.image_content
                file_format = img_vo.format or "jpeg"
                match content_src:
                    case MediaSourceEnum.REQUEST_BODY:
                        raw_bytes_local = img_vo.image_data
                        blob_data = raw_bytes_local
                        storage_key = ""
                        mime_type = f"image/{file_format}"
                        file_size = len(raw_bytes_local) if raw_bytes_local else 0
                    case MediaSourceEnum.LOCAL_DB | MediaSourceEnum.EXTERNAL_STORAGE:
                        raw_bytes_local = None
                        blob_data = None
                        storage_key = img_vo.retrieval_key or img_vo.image_url or ""
                        mime_type = f"image/{file_format}"
                        file_size = 0
            case MediaTypeEnum.VIDEO:
                vid_vo = content_vo.video_content
                file_format = vid_vo.format or "mp4"
                match content_src:
                    case MediaSourceEnum.REQUEST_BODY:
                        raw_bytes_local = vid_vo.video_data
                        blob_data = raw_bytes_local
                        storage_key = ""
                        mime_type = f"video/{file_format}"
                        file_size = len(raw_bytes_local) if raw_bytes_local else 0
                    case MediaSourceEnum.LOCAL_DB | MediaSourceEnum.EXTERNAL_STORAGE:
                        raw_bytes_local = None
                        blob_data = None
                        storage_key = vid_vo.retrieval_key or vid_vo.video_url or ""
                        mime_type = f"video/{file_format}"
                        file_size = 0
            case _:
                raw_bytes_local = raw_bytes if raw_bytes is not None else None
                blob_data = raw_bytes_local
                file_size = len(raw_bytes_local) if raw_bytes_local else 0

        # --- Deduplication hash ---
        hash_input = blob_data if blob_data is not None else storage_key.encode("utf-8")
        content_hash = hashlib.sha256(hash_input).digest()

        # --- Determine external storage references ---
        if content_src == MediaSourceEnum.EXTERNAL_STORAGE:
            if content_type == MediaTypeEnum.IMG and content_vo.image_content:
                img_vo = content_vo.image_content
                if img_vo.image_url:
                    external_storage_url = img_vo.image_url
                elif img_vo.retrieval_key:
                    external_storage_key = img_vo.retrieval_key
                    external_storage_provider = "s3"
            elif content_type == MediaTypeEnum.VIDEO and content_vo.video_content:
                vid_vo = content_vo.video_content
                if vid_vo.video_url:
                    external_storage_url = vid_vo.video_url
                elif vid_vo.retrieval_key:
                    external_storage_key = vid_vo.retrieval_key
                    external_storage_provider = "s3"

        # --- Create or get the content blob model ---
        blob_model, created = ContentBlobModel.objects.get_or_create(
            dedup_content_hash=content_hash,
            defaults={
                "dedup_content_hash": content_hash,
                "storage_src": content_src,
                "external_storage_url": external_storage_url,
                "external_storage_key": external_storage_key,
                "external_storage_provider": external_storage_provider,
                "mime_type": mime_type,
                "file_size_bytes": file_size,
                "blob": blob_data,
                "file_format": file_format,
            }
        )

        return ContentBlobReference(
            blob_id=blob_model.id,
            storage_location=blob_model.storage_src,
            external_url=blob_model.external_storage_url,
            external_key=blob_model.external_storage_key,
            external_provider=blob_model.external_storage_provider,
        )
    
    def store(self, content_vo: ContentToModerateVo, raw_bytes: Optional[bytes]) -> ContentBlobReference:
        # Determine storage location based on domain content_src
        storage_location = self._map_to_storage_location(content_vo.content_src)

        # Extract metadata
        mime_type, file_format, file_size = self._extract_metadata(content_vo, raw_bytes)
        storage_key = self._extract_storage_key(content_vo)

        # Calculate hash (from raw_bytes or fallback to storage_key)
        if raw_bytes is not None:
            content_hash = hashlib.sha256(raw_bytes).digest()
        else:
            content_hash = hashlib.sha256(storage_key.encode('utf-8')).digest()

        # Prepare external storage fields
        external_url = None
        external_key = None
        external_provider = None
        blob_data = None

        if storage_location == StorageLocationEnum.LOCAL_DB:
            blob_data = raw_bytes  # store in DB
        else:  # EXTERNAL_STORAGE
            # For external storage, we expect retrieval_key or URL from content_vo
            if content_vo.image_content:
                ext = content_vo.image_content
                if ext.image_url:
                    external_url = ext.image_url
                elif ext.retrieval_key:
                    external_key = ext.retrieval_key
                    external_provider = 's3'  # or detect from config
            elif content_vo.video_content:
                ext = content_vo.video_content
                if ext.video_url:
                    external_url = ext.video_url
                elif ext.retrieval_key:
                    external_key = ext.retrieval_key
                    external_provider = 's3'
            # No blob data for external storage
            blob_data = None

        # Get or create the blob model (deduplication)
        blob_model, created = ContentBlobModel.objects.get_or_create(
            dedup_content_hash=content_hash,
            defaults={
                'storage_location': storage_location,
                'external_storage_url': external_url,
                'external_storage_key': external_key,
                'external_storage_provider': external_provider,
                'mime_type': mime_type,
                'file_size_bytes': file_size,
                'blob': blob_data,
                'file_format': file_format,
            }
        )

        return ContentBlobReference(
            blob_id=blob_model.id,
            storage_location=blob_model.storage_location,
            external_url=blob_model.external_storage_url,
            external_key=blob_model.external_storage_key,
            external_provider=blob_model.external_storage_provider,
        )

    def find_by_hash(self, content_hash: bytes) -> Optional[ContentBlobReference]:
        try:
            blob = ContentBlobModel.objects.get(dedup_content_hash=content_hash)
            return ContentBlobReference(
                blob_id=blob.id,
                storage_location=blob.storage_src,
                external_url=blob.external_storage_url,
                external_key=blob.external_storage_key,
                external_provider=blob.external_storage_provider,
            )
        except ContentBlobModel.DoesNotExist:
            return None

    # ---------- Helper methods ----------
    def _map_to_storage_location(self, domain_src: MediaSourceEnum) -> StorageLocationEnum:
        """Transform domain MediaSourceEnum to infrastructure StorageLocationEnum."""
        if domain_src == MediaSourceEnum.REQUEST_BODY:
            return StorageLocationEnum.LOCAL_DB   # content from request goes to local DB
        elif domain_src == MediaSourceEnum.LOCAL_DB:
            return StorageLocationEnum.LOCAL_DB
        elif domain_src == MediaSourceEnum.EXTERNAL_STORAGE:
            return StorageLocationEnum.EXTERNAL_STORAGE
        else:
            raise ValueError(f"Unknown domain source: {domain_src}")

    def _extract_metadata(self, content_vo: ContentToModerateVo, raw_bytes: Optional[bytes]) -> tuple[str, str, int]:
        """Return (mime_type, file_format, file_size)."""
        content_type = content_vo.content_type
        if content_type == MediaTypeEnum.TEXT:
            return ("text/plain", "txt", len(raw_bytes) if raw_bytes else 0)
        elif content_type == MediaTypeEnum.IMG:
            fmt = content_vo.image_content.format or "jpeg"
            return (f"image/{fmt}", fmt, len(raw_bytes) if raw_bytes else 0)
        elif content_type == MediaTypeEnum.VIDEO:
            fmt = content_vo.video_content.format or "mp4"
            return (f"video/{fmt}", fmt, len(raw_bytes) if raw_bytes else 0)
        else:
            return ("application/octet-stream", None, 0)

    def _extract_storage_key(self, content_vo: ContentToModerateVo) -> str:
        """Extract retrieval key or URL for external storage references."""
        if content_vo.image_content:
            return content_vo.image_content.retrieval_key or content_vo.image_content.image_url or ""
        if content_vo.video_content:
            return content_vo.video_content.retrieval_key or content_vo.video_content.video_url or ""
        return ""