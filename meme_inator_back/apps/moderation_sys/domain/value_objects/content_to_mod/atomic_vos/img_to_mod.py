from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ImageToModerateVo:
    """Image content, either stores raw bytes or a remote reference."""
    image_data: Optional[bytes] = None # endpoint request type can accept multipart and then client can sent image binary directly. 
    image_url: Optional[str] = None
    retrieval_key: Optional[str] = None
    format: Optional[str] = None  # e.g. jpeg, png

    def __post_init__(self):
        """Validate image content."""
        has_data = self.image_data is not None
        has_url = self.image_url is not None
        has_key = self.retrieval_key is not None
        
        if not (has_data or has_url or has_key):
            raise ValueError("Image must have either image_data, image_url, or retrieval_key")
        
        # if has_data and (has_url or has_key):
        #     raise ValueError("Cannot have both image_data and remote reference (image_url/retrieval_key)")
        
        if self.image_data and len(self.image_data) > 10 * 1024 * 1024:  # 10MB
            raise ValueError("Image data exceeds maximum size (10MB)")
        
        # Validate format if provided
        if self.format and self.format.lower() not in ['jpeg', 'jpg', 'png', 'gif', 'webp']:
            raise ValueError(f"Unsupported image format: {self.format}")


