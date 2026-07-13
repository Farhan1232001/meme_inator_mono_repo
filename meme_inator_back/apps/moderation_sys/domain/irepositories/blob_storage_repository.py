from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from apps.moderation_sys.domain.value_objects.content_to_mod.content_to_moderate import ContentToModerateVo

class ContentBlobReference:
    """Domain value object representing a stored content blob."""
    def __init__(self, blob_id: UUID, storage_location: str, external_url: Optional[str] = None, 
                 external_key: Optional[str] = None, external_provider: Optional[str] = None):
        self.blob_id = blob_id
        self.storage_location = storage_location  # 'local_db' or 'external_storage'
        self.external_url = external_url
        self.external_key = external_key
        self.external_provider = external_provider

class IBlobStorageRepository(ABC):
    @abstractmethod
    def store(self, content_vo: ContentToModerateVo, raw_bytes: Optional[bytes]) -> ContentBlobReference:
        """
        Store the content blob (if raw_bytes provided) or create reference to existing blob.
        Returns a ContentBlobReference that can be used to retrieve the blob later.
        """
        pass

    # TODO: Should I find by hash? check when you impelement this. 
    @abstractmethod
    def find_by_hash(self, content_hash: bytes) -> Optional[ContentBlobReference]:
        """Find blob reference by its hash for deduplication."""
        pass