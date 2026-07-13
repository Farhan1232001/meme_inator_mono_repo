
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class VideoToModerateVo:
    """Video content, either stores raw bytes or a remote reference."""
    video_data: Optional[bytes] = None
    video_url: Optional[str] = None
    retrieval_key: Optional[str] = None
    format: Optional[str] = None  # e.g. mp4

    def __post_init__(self):
        """Validate video content."""
        has_data = self.video_data is not None
        has_url = self.video_url is not None
        has_key = self.retrieval_key is not None
        
        if not (has_data or has_url or has_key):
            raise ValueError("Video must have either video_data, video_url, or retrieval_key")
        
        if has_data and (has_url or has_key):
            raise ValueError("Cannot have both video_data and remote reference (video_url/retrieval_key)")
        
        if self.video_data and len(self.video_data) > 100 * 1024 * 1024:  # 100MB
            raise ValueError("Video data exceeds maximum size (100MB)")