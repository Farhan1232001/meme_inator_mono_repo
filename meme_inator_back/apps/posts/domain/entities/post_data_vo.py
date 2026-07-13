# apps/posts/domain/value_objects/post_data_vo.py
from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID


@dataclass(frozen=True)
class PostDataVo:
    """Value object for post data - immutable and validates post creation data."""
    image_url: str
    author_id: UUID
    thumbnail_url: Optional[str] = None
    caption: Optional[str] = None
    post_type: Optional[str] = None
    file_format: Optional[str] = None
    tags: List[str] = None
    visibility: Optional[str] = None
    
    def __post_init__(self):
        """Validate the post data after initialization."""
        self._validate()
    
    def _validate(self):
        """Validate the post data."""
        if not self.image_url:
            raise ValueError("Image URL is required")
        
        if self.tags is None:
            object.__setattr__(self, 'tags', [])
        
        # Validate tags are strings
        for tag in self.tags:
            if not isinstance(tag, str):
                raise ValueError(f"Tag must be a string, got {type(tag)}")
        
        # Validate URL format (simplified)
        if self.image_url and not (self.image_url.startswith('http://') or self.image_url.startswith('https://')):
            raise ValueError("Image URL must be a valid URL")
        
        if self.thumbnail_url and not (self.thumbnail_url.startswith('http://') or self.thumbnail_url.startswith('https://')):
            raise ValueError("Thumbnail URL must be a valid URL")
    
    @classmethod
    def from_dict(cls, data: dict) -> "PostDataVo":
        """Create PostDataVo from dictionary."""
        return cls(
            image_url=data.get('image_url') or data.get('imageURL', ''),
            author_id=data['author_id'],
            thumbnail_url=data.get('thumbnail_url') or data.get('thumbnailURL'),
            caption=data.get('caption'),
            post_type=data.get('post_type'),
            file_format=data.get('file_format'),
            tags=data.get('tags', []),
            visibility=data.get('visibility')
        )