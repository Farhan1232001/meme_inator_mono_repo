# domain/value_objects/content_snapshot_vo.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid7

from apps.moderation_sys.domain.enums.media_type_enums import MediaTypeEnum


@dataclass()
class ContentSnapshotVo:
    """Immutable snapshot of content at submission time.
    TODO: assert on init that content specific attribute, only ONE of them is set, all others must be null. 
    """
    id: UUID # stores uuid7
    fingerprint: str
    type: MediaTypeEnum
    content_size_bytes: Optional[int] = None
    captured_at: Optional[datetime] = None
    
    # Content specific attributes (only one should be set based on content_type)
    text_snapshot: Optional['TextSnapshotVo'] = None
    image_snapshot: Optional['ImageSnapshotVo'] = None
    video_snapshot: Optional['VideoSnapshotVo'] = None
    
    def is_empty(self) -> bool:
        return not any([self.text_snapshot, self.image_snapshot, self.video_snapshot])
    
    def has_text(self) -> bool:
        return self.text_snapshot is not None
    
    def has_image(self) -> bool:
        return self.image_snapshot is not None
    
    def has_video(self) -> bool:
        return self.video_snapshot is not None


@dataclass(frozen=True)
class TextSnapshotVo:
    """Snapshot for text-based content."""
    text: str
    language: Optional[str] = None


@dataclass(frozen=True)
class ImageSnapshotVo:
    """Snapshot for image content."""
    image_data: Optional[bytes] = None
    image_url: Optional[str] = None
    retrieval_key: Optional[str] = None
    format: Optional[str] = None  # e.g. jpeg, png


@dataclass(frozen=True)
class VideoSnapshotVo:
    """Snapshot for video content."""
    video_data: Optional[bytes] = None
    video_url: Optional[str] = None
    retrieval_key: Optional[str] = None
    format: Optional[str] = None  # e.g. mp4