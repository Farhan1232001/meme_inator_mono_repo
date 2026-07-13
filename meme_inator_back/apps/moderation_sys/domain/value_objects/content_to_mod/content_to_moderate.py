# domain/value_objects/content_to_moderate.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union
from uuid import UUID
from apps.moderation_sys.domain.enums.media_type_enums import MediaTypeEnum
from apps.moderation_sys.domain.enums.media_src_enum import MediaSourceEnum
from apps.moderation_sys.domain.value_objects.content_to_mod.atomic_vos.img_to_mod import ImageToModerateVo
from apps.moderation_sys.domain.value_objects.content_to_mod.atomic_vos.txt_to_mod import TextToModerateVo
from apps.moderation_sys.domain.value_objects.content_to_mod.atomic_vos.video_to_mod import VideoToModerateVo

@dataclass(frozen=True)
class ContentToModerateVo:
    """
    Value object representing content to be moderated.

    moderation_sys does not care about the particular content (post, comment, profile bio); This vo can be used on any particular content. ModerationGateways consume ContentToModerateVo from posts, comments, etc apps and enter into the moderation_sys. 
    
    This is the unified entry point for all moderation requests.
    Uses composition over inheritance - only ONE content type should be present.
    The content_type attribute tracks which one is not None.
    TODO: assert on init that content specific attribute, only ONE of them is set, all others must be null. 
    """
    content_id: UUID
    author_id: UUID
    policy_routing_key: str  # tracks WHERE content is stored
    content_type: MediaTypeEnum
    content_src: MediaSourceEnum
    region: Optional[str] = None
    
    text_content: Optional['TextToModerateVo'] = None
    image_content: Optional['ImageToModerateVo'] = None
    video_content: Optional['VideoToModerateVo'] = None
    
    def __post_init__(self):
        """Validate that exactly one content type is set."""
        content_fields = [self.text_content, self.image_content, self.video_content]
        non_null_count = sum(1 for field in content_fields if field is not None)
        
        if non_null_count == 0:
            raise ValueError("Exactly one content type (text, image, or video) must be provided")
        if non_null_count > 1:
            raise ValueError(f"Cannot have multiple content types. Found {non_null_count}")
        
        # Validate consistency between content_type and actual content
        if self.content_type == MediaTypeEnum.TEXT and not self.text_content:
            raise ValueError("content_type is TEXT but text_content is None")
        if self.content_type == MediaTypeEnum.IMG and not self.image_content:
            raise ValueError("content_type is IMG but image_content is None")
        if self.content_type == MediaTypeEnum.VIDEO and not self.video_content:
            raise ValueError("content_type is VIDEO but video_content is None")
        
        # Validate content source consistency
        if self.has_content_in_request_body():
            if self.get_raw_content() is None:
                raise ValueError("content_src is REQUEST_BODY but no raw content provided")
        else:
            # For remote content, ensure retrieval_key or URL is present
            if self.image_content and not (self.image_content.retrieval_key or self.image_content.image_url):
                raise ValueError("Remote image content requires retrieval_key or image_url")
            if self.video_content and not (self.video_content.retrieval_key or self.video_content.video_url):
                raise ValueError("Remote video content requires retrieval_key or video_url")
    
    def get_content_type(self) -> MediaTypeEnum:
        """Returns the content type."""
        return self.content_type
    
    def has_content_in_request_body(self) -> bool:
        """Check if content is provided inline in the request."""
        return self.content_src == MediaSourceEnum.REQUEST_BODY
    
    def get_raw_content(self) -> Union[str, bytes, None]:
        """Returns the raw content data based on type."""
        if self.text_content:
            return self.text_content.text
        elif self.image_content:
            return self.image_content.image_data
        elif self.video_content:
            return self.video_content.video_data
        return None
    
    def get_remote_reference(self) -> Optional[Union[str, tuple[str, str]]]:
        """Returns remote reference (URL or (retrieval_key, URL))."""
        if self.image_content:
            if self.image_content.image_url:
                return self.image_content.image_url
            if self.image_content.retrieval_key:
                return (self.image_content.retrieval_key, None)
        elif self.video_content:
            if self.video_content.video_url:
                return self.video_content.video_url
            if self.video_content.retrieval_key:
                return (self.video_content.retrieval_key, None)
        return None

    def get_raw_bytes(self) -> Optional[bytes]:
        """Extract raw bytes from a ContentToModerateVo for hashing."""
        if self.content_type == MediaTypeEnum.TEXT and self.text_content:
            return self.text_content.text.encode('utf-8')
        elif self.content_type == MediaTypeEnum.IMG and self.image_content:
            return self.image_content.image_data
        elif self.content_type == MediaTypeEnum.VIDEO and self.video_content:
            return self.video_content.video_data
        return None

